#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2025-10-16

Purpose: Showcase a queue-centric logging server built on JskToolBox base classes.

The example demonstrates how to:
* Extend `ThLoggerProcessor` to build a dedicated logging server thread.
* Share the server-managed queue with distributed components using a reusable mixin.
* Attach per-component `LoggerClient` instances with consistent naming.
* Coordinate worker threads that emit structured log messages.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Iterable, List, Optional
from venv import logger

from jsktoolbox.logstool import (
    LoggerClient,
    LoggerEngine,
    LoggerEngineFile,
    LoggerEngineStdout,
    LogFormatterDateTime,
    LogsLevelKeys,
    ThLoggerProcessor,
)
from jsktoolbox.basetool.logs import BLoggerQueue


class LoggingServer(ThLoggerProcessor):
    """Run the logging processor thread with predefined engine destinations.

    The server configures a `LoggerEngine`, registers file/stdout sinks, and exposes
    helpers to create additional `LoggerClient` instances that reuse the shared queue.
    """

    _engine: Optional[LoggerEngine] = None
    _log_path: Optional[Path] = None
    _server_client: Optional[LoggerClient] = None

    def __init__(self, log_path: Path, debug: bool = False) -> None:
        """Initialise the logging server with configured destinations.

        ### Arguments:
        * log_path: Path - Target file for persistent log storage.
        * debug: bool - Enables verbose lifecycle logging when True.

        ### Returns:
        None - Constructor.
        """
        super().__init__(debug=debug)
        self._log_path = log_path
        self._engine = LoggerEngine()
        self._configure_engine()
        self.logger_engine = self._engine
        self._server_client = LoggerClient(self._engine.logs_queue, name=self._c_name)
        self.logger_client = self._server_client

    def _configure_engine(self) -> None:
        """Configure file and console engines attached to the logger engine."""
        if self._engine is None or self._log_path is None:
            raise RuntimeError("LoggingServer initialisation incomplete.")

        formatter = LogFormatterDateTime()
        file_engine = LoggerEngineFile(
            name="FileSink", formatter=formatter, buffered=False
        )
        file_engine.logdir = str(self._log_path.parent)
        file_engine.logfile = self._log_path.name

        console_engine = LoggerEngineStdout(
            name="ConsoleSink", formatter=formatter, buffered=False
        )

        for level in LogsLevelKeys.keys:
            self._engine.add_engine(level, file_engine)

        for level in (
            LogsLevelKeys.INFO,
            LogsLevelKeys.NOTICE,
            LogsLevelKeys.WARNING,
            LogsLevelKeys.ERROR,
            LogsLevelKeys.CRITICAL,
        ):
            self._engine.add_engine(level, console_engine)

    @property
    def logs_queue(self) -> Optional["LoggerQueue"]:
        """Expose the server queue for external clients.

        ### Returns:
        Optional[LoggerQueue] - Shared logging queue instance or None.
        """
        if self._engine is None:
            return None
        return self._engine.logs_queue

    def create_client(self, name: Optional[str] = None) -> LoggerClient:
        """Create a logger client attached to the server queue.

        ### Arguments:
        * name: Optional[str] - Friendly component name used in log prefixes.

        ### Returns:
        LoggerClient - Configured client instance.

        ### Raises:
        * RuntimeError: When the server queue is not available.
        """
        queue = self.logs_queue
        if queue is None:
            raise RuntimeError("LoggingServer not initialised.")
        return LoggerClient(queue, name=name)

    def shutdown(self, timeout: float = 5.0) -> None:
        """Stop the processor thread and wait for graceful completion.

        ### Arguments:
        * timeout: float - Maximum seconds to wait for termination.

        ### Returns:
        None - The thread is joined.
        """
        self.stop()
        self.join(timeout=timeout)


class LoggingComponentMixin(BLoggerQueue):
    """Reusable mixin that binds components to the logging server."""

    _logger: Optional[LoggerClient] = None

    def attach_logger(self, server: LoggingServer, name: Optional[str] = None) -> None:
        """Bind the component to the server queue and create a dedicated client.

        ### Arguments:
        * server: LoggingServer - Active logging server instance.
        * name: Optional[str] - Optional override for the client name.

        ### Returns:
        None - Internal logger client configured.
        """
        queue = server.logs_queue
        if queue is None:
            raise RuntimeError("Logging server queue is not available.")
        self.logs_queue = queue
        resolved_name: str = name or self._c_name
        self._logger = LoggerClient(queue, name=resolved_name)

    @property
    def logger(self) -> LoggerClient:
        """Return the attached logger client.

        ### Returns:
        LoggerClient - Component-specific logger client.

        ### Raises:
        * RuntimeError: When the logger has not been attached.
        """
        if self._logger is None:
            raise RuntimeError("Logger client not attached.")
        return self._logger


class BackgroundWorker(LoggingComponentMixin):
    """Perform periodic work while emitting detailed log messages."""

    _worker_id: int = 0
    _interval: float = 0.0
    _stop_event: Optional[threading.Event] = None
    _thread: Optional[threading.Thread] = None

    def __init__(
        self, server: LoggingServer, worker_id: int, interval: float = 0.5
    ) -> None:
        """Initialise the background worker and bind logging.

        ### Arguments:
        * server: LoggingServer - Active logging server.
        * worker_id: int - Unique identifier for this worker.
        * interval: float - Sleep duration between iterations in seconds.

        ### Returns:
        None - Constructor.
        """
        self._worker_id = worker_id
        self._interval = interval
        self._stop_event = threading.Event()
        self._thread = None
        self.attach_logger(server, name=f"Worker-{worker_id}")

    def start(self) -> None:
        """Start the worker loop in a dedicated thread."""
        if self._thread and self._thread.is_alive():
            return

        self.logger.message_info = f"Starting background worker {self._worker_id}"
        self._thread = threading.Thread(
            target=self._run_loop, name=f"WorkerThread-{self._worker_id}", daemon=False
        )
        self._thread.start()

    def stop(self) -> None:
        """Signal the worker loop to stop and wait for completion."""
        if self._stop_event:
            self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5.0)
            self.logger.message_info = f"Worker {self._worker_id} stopped"

    def _run_loop(self) -> None:
        """Execute the worker loop until the stop event is triggered."""
        iteration = 0
        while self._stop_event and not self._stop_event.is_set():
            iteration += 1
            self.logger.message_debug = (
                f"Worker {self._worker_id} iteration {iteration}"
            )
            if iteration % 7 == 0:
                self.logger.message_notice = (
                    f"Worker {self._worker_id} produced checkpoint {iteration}"
                )
            if iteration % 11 == 0:
                self.logger.message_warning = (
                    f"Worker {self._worker_id} approaching load limit"
                )
            time.sleep(self._interval)


class DiagnosticsController(LoggingComponentMixin):
    """Aggregate signals from multiple workers and emit summary logs."""

    _workers: List[BackgroundWorker] = []

    def __init__(
        self, server: LoggingServer, workers: Iterable[BackgroundWorker]
    ) -> None:
        """Initialise the controller and attach logging.

        ### Arguments:
        * server: LoggingServer - Active logging server.
        * workers: Iterable[BackgroundWorker] - Workers managed by this controller.

        ### Returns:
        None - Constructor.
        """
        self._workers = list(workers)
        self.attach_logger(server, name=f"{self.__class__.__name__}")

    def emit_status(self) -> None:
        """Log aggregated state derived from managed workers."""
        active_workers = sum(
            1
            for worker in self._workers
            if worker._thread and worker._thread.is_alive()
        )
        self.logger.message_info = f"Active workers: {active_workers}"

    def request_shutdown(self) -> None:
        """Coordinate worker shutdown signals."""
        self.logger.message_notice = "Initiating cooperative worker shutdown"
        for worker in self._workers:
            worker.stop()


def main() -> None:
    """Bootstrap the logging server and coordinated worker components."""
    log_path = Path("/tmp/jsktoolbox_log_example.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    server = LoggingServer(log_path=log_path, debug=True)
    server.start()
    time.sleep(0.2)

    logger: Optional[LoggerClient] = server.logger_client
    if logger is None:
        raise RuntimeError("Logging server client not available.")

    logger.message_notice = "Logging server started"

    worker_fast = BackgroundWorker(server, worker_id=1, interval=0.3)
    worker_slow = BackgroundWorker(server, worker_id=2, interval=0.6)
    worker_fast.start()
    worker_slow.start()

    controller = DiagnosticsController(server, workers=[worker_fast, worker_slow])

    try:
        for _ in range(3):
            time.sleep(2.0)
            controller.emit_status()
    finally:
        controller.request_shutdown()
        logger.message_info = "Waiting for workers to stop"
        time.sleep(1.0)
        server.shutdown(timeout=3.0)
        logger.message_notice = "Logging server stopped"


if __name__ == "__main__":
    main()


# #[EOF]#######################################################################
