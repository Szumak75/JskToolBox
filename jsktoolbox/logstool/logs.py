# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 04.09.2023

  Purpose: logs subsystem classes.
"""

import time
import threading
from inspect import currentframe

from typing import Optional, List, Tuple, Any

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_logs import (
    BLoggerQueue,
    LoggerQueue,
    LogsLevelKeys,
    Keys,
)
from jsktoolbox.libs.base_th import ThBaseObject
from jsktoolbox.logstool.engines import *


class LoggerEngine(BLoggerQueue, NoDynamicAttributes):
    """LoggerEngine container class."""

    def __init__(self) -> None:
        """Constructor."""
        # make logs queue object
        self._data[Keys.QUEUE] = LoggerQueue()
        # default logs level configuration
        self._data[Keys.NO_CONF] = {}
        self._data[Keys.NO_CONF][LogsLevelKeys.INFO] = [LoggerEngineStdout()]
        self._data[Keys.NO_CONF][LogsLevelKeys.DEBUG] = [
            LoggerEngineStderr()
        ]

    def add_engine(self, log_level: str, engine: ILoggerEngine) -> None:
        """Add LoggerEngine to specific log level."""
        if not isinstance(log_level, str):
            raise Raise.error(
                f"Key as string expected, '{type(log_level)}' received.'",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        if not isinstance(engine, ILoggerEngine):
            raise Raise.error(
                f"ILoggerEngine type expected, '{type(engine)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        if Keys.CONF not in self._data:
            self._data[Keys.CONF] = {}
            self._data[Keys.CONF][log_level] = [engine]
        else:
            if log_level not in self._data[Keys.CONF].keys():
                self._data[Keys.CONF][log_level] = [engine]
            else:
                test = False
                for i in range(0, len(self._data[Keys.CONF][log_level])):
                    if (
                        self._data[Keys.CONF][log_level][i].__class__
                        == engine.__class__
                    ):
                        self._data[Keys.CONF][log_level][i] = engine
                        test = True
                if not test:
                    self._data[Keys.CONF][log_level].append(engine)

    def send(self) -> None:
        """The LoggerEngine method.

        For sending messages to the configured logging subsystem.
        """
        while True:
            item = self.logs_queue.get()
            if item is None:
                return
            # get tuple(log_level, message)
            log_level, message = item
            # check if has have configured logging subsystem
            if Keys.CONF in self._data and len(self._data[Keys.CONF]) > 0:
                if log_level in self._data[Keys.CONF]:
                    for item in self._data[Keys.CONF][log_level]:
                        engine: ILoggerEngine = item
                        engine.send(message)
            else:
                if log_level in self._data[Keys.NO_CONF]:
                    for item in self._data[Keys.NO_CONF][log_level]:
                        engine: ILoggerEngine = item
                        engine.send(message)


class LoggerClient(BLoggerQueue, NoDynamicAttributes):
    """Logger Client main class."""

    # TODO:
    # stworzyć obiekt konfiguracyjny z listą
    # silników do raportowania wszystkich typów
    # logów: message, error, warning, debug
    # przekazać konfigurator w konstruktorze

    # stworzyć obiekt z szablonami formatowania
    # informacji przekazywanych do każdego z typów silników

    def __init__(
        self, queue: LoggerQueue, name: Optional[str] = None
    ) -> None:
        """Constructor.

        Arguments:
        queue [LoggerQueue] - LoggerQeueu class object from LoggerEngine,
        name [str] - optional app name for logs decorator
        """
        # store name
        self.name = name
        # logger queue
        if not isinstance(queue, LoggerQueue):
            raise Raise.error(
                f"LoggerQueue type expected, '{type(queue)}' received."
            )
        self.logs_queue = queue

    @property
    def name(self) -> Optional[str]:
        """Get LoggerClient name string."""
        if Keys.NAME not in self._data:
            self._data[Keys.NAME] = None
        return self._data[Keys.NAME]

    @name.setter
    def name(self, name: str) -> None:
        """Set LoggerClient name string."""
        if name and not isinstance(name, str):
            raise Raise.error(
                f"name as string expected, '{type(name)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.NAME] = name

    def message(
        self, message: str, log_level: str = LogsLevelKeys.INFO
    ) -> None:
        """Send message to logging subsystem."""
        if self.name is not None:
            message = f"[{self.name}] {message}"
        self.logs_queue.put(message, log_level)

    @property
    def message_alert(self) -> None:
        """Do nothing, for defining setter only."""

    @message_alert.setter
    def message_alert(self, message: str) -> None:
        """Send message property."""
        self.message(message, LogsLevelKeys.ALERT)

    @property
    def message_critical(self) -> None:
        """Do nothing, for defining setter only."""

    @message_alert.setter
    def message_critical(self, message: str) -> None:
        """Send message property."""
        self.message(message, LogsLevelKeys.CRITICAL)

    @property
    def message_debug(self) -> None:
        """Do nothing, for defining setter only."""

    @message_debug.setter
    def message_debug(self, message: str) -> None:
        """Send message property."""
        self.message(message, LogsLevelKeys.DEBUG)

    @property
    def message_emergency(self) -> None:
        """Do nothing, for defining setter only."""

    @message_emergency.setter
    def message_emergency(self, message: str) -> None:
        """Send message property."""
        self.message(message, LogsLevelKeys.EMERGENCY)

    @property
    def message_error(self) -> None:
        """Do nothing, for defining setter only."""

    @message_error.setter
    def message_error(self, message: str) -> None:
        """Send message property."""
        self.message(message, LogsLevelKeys.ERROR)

    @property
    def message_info(self) -> None:
        """Do nothing, for defining setter only."""

    @message_info.setter
    def message_info(self, message: str) -> None:
        """Send message property."""
        self.message(message, LogsLevelKeys.INFO)

    @property
    def message_notice(self) -> None:
        """Do nothing, for defining setter only."""

    @message_notice.setter
    def message_notice(self, message: str) -> None:
        """Send message property."""
        self.message(message, LogsLevelKeys.NOTICE)

    @property
    def message_warning(self) -> None:
        """Do nothing, for defining setter only."""

    @message_warning.setter
    def message_warning(self, message: str) -> None:
        """Send message property."""
        self.message(message, LogsLevelKeys.WARNING)


class ThLoggerProcessor(threading.Thread, ThBaseObject, NoDynamicAttributes):
    """LoggerProcessor thread engine."""

    def __init__(self):
        """Constructor."""
        threading.Thread.__init__(self, name=self.__class__.__name__)
        self._stop_event = threading.Event()
        self.daemon = True
        self._sleep_period = 0.2

    @property
    def logger_engine(self) -> Optional[LoggerEngine]:
        """Return LoggerEngine object if any."""
        if "__LEO__" not in self._data:
            self._data["__LEO__"] = None
        return self._data["__LEO__"]

    @logger_engine.setter
    def logger_engine(self, obj: LoggerEngine) -> None:
        """Set LoggerEngine object."""
        if not isinstance(obj, LoggerEngine):
            raise Raise.error(
                f"LoggerEngine type object expected, '{type(obj)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data["__LEO__"] = obj
        if self.logger_client is not None:
            self.logger_client.logs_queue = self.logger_engine.logs_queue

    @property
    def logger_client(self) -> Optional[LoggerClient]:
        """Return LoggerClient object if any."""
        if "__LCO__" not in self._data:
            self._data["__LCO__"] = None
        return self._data["__LCO__"]

    @logger_client.setter
    def logger_client(self, obj: LoggerClient) -> None:
        """Set LoggerEngine object."""
        if not isinstance(obj, LoggerClient):
            raise Raise.error(
                f"LoggerClient type object expected, '{type(obj)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data["__LCO__"] = obj
        if self.logger_engine is not None and obj.logs_queue is None:
            self.logger_client.logs_queue = self.logger_engine.logs_queue

    def run(self) -> None:
        """Start the procedure."""
        # check list
        if self.logger_engine is None:
            raise Raise.error(
                "LoggerEngine not set.",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )
        if self.logger_client is None:
            raise Raise.error(
                "LoggerClient not set.",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )

        self.logger_client.message_debug = f"Start {self.__class__.__name__}"
        # run
        while not self.stopped:
            self.logger_engine.send()
            time.sleep(self._sleep_period)
        self.logger_client.message_debug = f"Stop {self.__class__.__name__}"

    def stop(self) -> None:
        """Set stop event."""
        self.logger_client.message_debug = "stopping..."
        print(self._data)
        self._stop_event.set()
        print(self._data)

    @property
    def stopped(self) -> bool:
        """Return stop flag."""
        return self._stop_event.is_set()


# #[EOF]#######################################################################
