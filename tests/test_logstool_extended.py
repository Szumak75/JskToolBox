import io
import sys
import threading
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.basetool.data import BData
from jsktoolbox.basetool.logs import BLoggerEngine
from jsktoolbox.logstool.engines import (
    LogKeys,
    LoggerEngineFile,
    LoggerEngineStderr,
    LoggerEngineStdout,
    LoggerEngineSyslog,
)
from jsktoolbox.libs.interfaces.logger_engine import ILoggerEngine
from jsktoolbox.logstool.formatters import (
    LogFormatterDateTime,
    LogFormatterNull,
    LogFormatterTime,
    LogFormatterTimestamp,
)
from jsktoolbox.logstool.keys import LogsLevelKeys, SysLogKeys
from jsktoolbox.logstool.logs import LoggerClient, LoggerEngine, ThLoggerProcessor
from jsktoolbox.logstool.queue import LoggerQueue


class DummyEngine(ILoggerEngine, BLoggerEngine, BData):
    """Collect messages sent through the logging engine pipeline."""

    _KEY = "__messages__"

    def __init__(self) -> None:
        self._set_data(self._KEY, [], list)

    @property
    def messages(self) -> list[str]:
        messages = self._get_data(self._KEY, set_default_type=list)
        return messages if messages is not None else []

    def send(self, message: str) -> None:
        messages = self._get_data(self._KEY, set_default_type=list)
        if messages is None:
            messages = []
            self._set_data(self._KEY, messages, list)
        messages.append(message)


def test_logger_queue_invalid_level_raises() -> None:
    queue = LoggerQueue()
    with pytest.raises(KeyError):
        queue.put("message", log_level="UNKNOWN")


def test_logger_queue_roundtrip() -> None:
    queue = LoggerQueue()
    queue.put("message", LogsLevelKeys.INFO)
    assert queue.get() == (LogsLevelKeys.INFO, "message")
    assert queue.get() is None


@pytest.mark.parametrize(
    "formatter_cls, expected",
    [
        (LogFormatterNull, "payload"),
        (LogFormatterTime, "2024-01-01 12:34:56"),
    ],
)
def test_log_formatters(monkeypatch: pytest.MonkeyPatch, formatter_cls, expected) -> None:
    if formatter_cls is LogFormatterTime:
        class FakeDatetime:
            @staticmethod
            def now():
                class Fake:
                    def strftime(self, fmt: str) -> str:
                        return "12:34:56"

                return Fake()

        monkeypatch.setattr(
            "jsktoolbox.logstool.formatters.datetime", FakeDatetime
        )
        expected = "12:34:56"
    formatter = formatter_cls()
    assert expected in formatter.format("payload")


def test_log_formatter_datetime(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeDatetime:
        @staticmethod
        def now():
            class Fake:
                def strftime(self, fmt: str) -> str:
                    return "2024-01-02 03:04:05"

            return Fake()

    monkeypatch.setattr("jsktoolbox.logstool.formatters.datetime", FakeDatetime)
    formatter = LogFormatterDateTime()
    assert formatter.format("payload").startswith("2024-01-02 03:04:05")


def test_log_formatter_timestamp(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "jsktoolbox.logstool.formatters.Timestamp.now", lambda: "1700000000"
    )
    formatter = LogFormatterTimestamp()
    assert formatter.format("payload").startswith("1700000000")


def test_logger_engine_stdout_writes() -> None:
    engine = LoggerEngineStdout(name="app", buffered=False)
    buf = io.StringIO()
    with patch.object(sys, "stdout", buf):
        engine.send("hello")
    assert buf.getvalue() == "hello\n"


def test_logger_engine_stderr_writes() -> None:
    engine = LoggerEngineStderr(name="app", buffered=False)
    buf = io.StringIO()
    with patch.object(sys, "stderr", buf):
        engine.send("fail")
    assert buf.getvalue() == "fail\n"


def test_logger_engine_file_write(tmp_path: Path) -> None:
    engine = LoggerEngineFile(name="app", formatter=LogFormatterNull())
    engine.logdir = str(tmp_path)
    engine.logfile = "app.log"
    engine.send("message")
    assert (tmp_path / "app.log").read_text().strip() == "[app]: message"


def test_logger_engine_file_logfile_directory_conflict(tmp_path: Path) -> None:
    engine = LoggerEngineFile(name="app", formatter=LogFormatterNull())
    subdir = tmp_path / "existing"
    subdir.mkdir()
    with pytest.raises(FileExistsError):
        engine.logfile = str(subdir)


def test_logger_engine_syslog_send(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = LoggerEngineSyslog(name="app", formatter=LogFormatterNull())
    opened: list[int] = []
    messages: list[tuple[int, str]] = []

    monkeypatch.setattr(
        "jsktoolbox.logstool.engines.syslog.openlog",
        lambda *, facility: opened.append(facility),
    )
    monkeypatch.setattr(
        "jsktoolbox.logstool.engines.syslog.syslog",
        lambda priority, message: messages.append((priority, message)),
    )
    monkeypatch.setattr(
        "jsktoolbox.logstool.engines.syslog.closelog",
        lambda: None,
    )

    engine.level = "ERROR"
    engine.facility = "LOCAL0"
    engine.send("alert")

    assert opened == [SysLogKeys.facility.LOCAL0]
    assert messages == [(SysLogKeys.level.ERROR, "[app]: alert")]


def test_logger_engine_syslog_invalid_facility() -> None:
    engine = LoggerEngineSyslog()
    with pytest.raises(KeyError):
        engine.facility = "UNKNOWN"


def test_logger_engine_syslog_invalid_level() -> None:
    engine = LoggerEngineSyslog()
    with pytest.raises(KeyError):
        engine.level = "UNKNOWN"


def test_logger_engine_add_engine_invalid_inputs() -> None:
    engine = LoggerEngine()
    with pytest.raises(TypeError):
        engine.add_engine(123, LoggerEngineStdout())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        engine.add_engine(LogsLevelKeys.INFO, object())  # type: ignore[arg-type]


def test_logger_engine_send_custom_engine() -> None:
    engine = LoggerEngine()
    dummy = DummyEngine()
    engine.add_engine(LogsLevelKeys.INFO, dummy)
    assert engine.logs_queue is not None
    engine.logs_queue.put("hello", LogsLevelKeys.INFO)
    engine.send()
    assert dummy.messages == ["hello"]


def test_th_logger_processor_lifecycle() -> None:
    engine = LoggerEngine()
    dummy = DummyEngine()
    engine.add_engine(LogsLevelKeys.INFO, dummy)
    client = LoggerClient(engine.logs_queue, name="client")

    processor = ThLoggerProcessor(debug=False)
    processor.logger_engine = engine
    processor.logger_client = client
    processor.sleep_period = 0.05

    processor.start()
    try:
        client.message("ping")
        timeout = time.time() + 2
        while not dummy.messages and time.time() < timeout:
            time.sleep(0.05)
        assert dummy.messages
    finally:
        processor.stop()
        processor.join(timeout=2)


def test_th_logger_processor_missing_engine() -> None:
    processor = ThLoggerProcessor()
    processor.logger_client = LoggerClient()
    with pytest.raises(ValueError):
        processor.run()
