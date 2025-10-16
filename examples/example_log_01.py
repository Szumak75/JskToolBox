#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2025-10-15

Purpose: Demonstrate best practices for logstool with threaded server and clients.

This example showcases:
* Centralized logging server running in a dedicated thread
* Multiple client components sharing the same logging queue
* File-based logging with timestamp formatting
* Proper lifecycle management and graceful shutdown
* Thread-safe logging operations
"""

import time
import threading
from typing import Optional

from jsktoolbox.logstool import (
    LoggerClient,
    LoggerEngine,
    ThLoggerProcessor,
    LoggerEngineFile,
    LoggerEngineStdout,
    LogFormatterDateTime,
    LogsLevelKeys,
)


class LoggingServer:
    """Centralized logging server managing the engine and processor thread.
    
    This class encapsulates the logging infrastructure, providing a clean
    interface for initialization, starting, and stopping the logging subsystem.
    """

    def __init__(self, log_file: str = "/tmp/application.log", debug: bool = False):
        """Initialize the logging server.
        
        ### Arguments:
        * log_file: str - Path to the log file. Defaults to /tmp/application.log.
        * debug: bool - Enable debug mode for processor lifecycle messages.
        
        ### Returns:
        None - Constructor.
        """
        self._log_file = log_file
        self._debug = debug
        self._engine: Optional[LoggerEngine] = None
        self._processor: Optional[ThLoggerProcessor] = None
        self._running = False

    def initialize(self) -> None:
        """Set up the logging engine with file and stdout outputs.
        
        Configures two logging destinations:
        * File with datetime formatter for persistent logging
        * Stdout for real-time console feedback
        
        ### Returns:
        None - Internal state initialized.
        """
        # Create the main logging engine
        self._engine = LoggerEngine()

        # Configure file engine with datetime formatter
        file_engine = LoggerEngineFile(
            name="APP",
            formatter=LogFormatterDateTime(),
            buffered=False,
        )
        file_engine.logfile = self._log_file

        # Configure stdout engine for console output
        stdout_engine = LoggerEngineStdout(
            name="APP",
            formatter=LogFormatterDateTime(),
            buffered=False,
        )

        # Route different log levels to appropriate engines
        self._engine.add_engine(LogsLevelKeys.DEBUG, file_engine)
        self._engine.add_engine(LogsLevelKeys.INFO, file_engine)
        self._engine.add_engine(LogsLevelKeys.INFO, stdout_engine)
        self._engine.add_engine(LogsLevelKeys.NOTICE, file_engine)
        self._engine.add_engine(LogsLevelKeys.NOTICE, stdout_engine)
        self._engine.add_engine(LogsLevelKeys.WARNING, file_engine)
        self._engine.add_engine(LogsLevelKeys.WARNING, stdout_engine)
        self._engine.add_engine(LogsLevelKeys.ERROR, file_engine)
        self._engine.add_engine(LogsLevelKeys.ERROR, stdout_engine)
        self._engine.add_engine(LogsLevelKeys.CRITICAL, file_engine)
        self._engine.add_engine(LogsLevelKeys.CRITICAL, stdout_engine)
        self._engine.add_engine(LogsLevelKeys.ALERT, file_engine)
        self._engine.add_engine(LogsLevelKeys.ALERT, stdout_engine)
        self._engine.add_engine(LogsLevelKeys.EMERGENCY, file_engine)
        self._engine.add_engine(LogsLevelKeys.EMERGENCY, stdout_engine)

    def start(self) -> None:
        """Start the background logging processor thread.
        
        ### Returns:
        None - Processor thread started.
        
        ### Raises:
        * RuntimeError: When engine is not initialized or server is already running.
        """
        if self._engine is None:
            raise RuntimeError("LoggingServer not initialized. Call initialize() first.")
        
        if self._running:
            raise RuntimeError("LoggingServer is already running.")

        # Create internal client for server messages
        server_client = LoggerClient(self._engine.logs_queue, name="LogServer")

        # Create and configure the processor thread
        self._processor = ThLoggerProcessor(debug=self._debug)
        self._processor.logger_engine = self._engine
        self._processor.logger_client = server_client
        self._processor.sleep_period = 0.1  # Process queue every 100ms

        # Start the processor thread
        self._processor.start()
        self._running = True

        # Log server startup
        server_client.message_info = "Logging server started"

    def stop(self, timeout: float = 5.0) -> None:
        """Stop the logging processor and flush remaining messages.
        
        ### Arguments:
        * timeout: float - Maximum seconds to wait for thread termination.
        
        ### Returns:
        None - Processor stopped and joined.
        """
        if not self._running or self._processor is None:
            return

        # Request processor to stop
        self._processor.stop()
        
        # Wait for the thread to finish
        self._processor.join(timeout=timeout)
        self._running = False

    def create_client(self, name: Optional[str] = None) -> LoggerClient:
        """Create a new logging client connected to this server.
        
        ### Arguments:
        * name: Optional[str] - Client identifier for message prefixing.
        
        ### Returns:
        LoggerClient - New client instance sharing the server's queue.
        
        ### Raises:
        * RuntimeError: When engine is not initialized.
        """
        if self._engine is None:
            raise RuntimeError("LoggingServer not initialized. Call initialize() first.")
        
        return LoggerClient(self._engine.logs_queue, name=name)

    @property
    def is_running(self) -> bool:
        """Check if the logging server is currently running.
        
        ### Returns:
        bool - True when processor thread is active.
        """
        return self._running


class WorkerComponent:
    """Example component that performs work and logs its activity.
    
    Demonstrates how application components should interact with the logging
    system through a dedicated client instance.
    """

    def __init__(self, logger: LoggerClient, worker_id: int):
        """Initialize the worker component.
        
        ### Arguments:
        * logger: LoggerClient - Logging client for this component.
        * worker_id: int - Unique identifier for this worker.
        
        ### Returns:
        None - Constructor.
        """
        self._logger = logger
        self._worker_id = worker_id
        self._stop_event = threading.Event()

    def run(self) -> None:
        """Execute the worker's main task loop.
        
        Simulates periodic work with logging at various levels.
        
        ### Returns:
        None - Method blocks until stop() is called.
        """
        self._logger.message_info = f"Worker {self._worker_id} started"

        iteration = 0
        while not self._stop_event.is_set():
            iteration += 1
            
            # Log periodic status
            if iteration % 5 == 0:
                self._logger.message_debug = f"Worker {self._worker_id} iteration {iteration}"
            
            # Simulate work
            time.sleep(0.5)
            
            # Simulate occasional warnings
            if iteration == 10:
                self._logger.message_warning = (
                    f"Worker {self._worker_id} approaching threshold"
                )
            
            # Simulate error condition
            if iteration == 15:
                self._logger.message_error = (
                    f"Worker {self._worker_id} encountered an error condition"
                )
                break

        self._logger.message_info = f"Worker {self._worker_id} stopped"

    def stop(self) -> None:
        """Signal the worker to stop processing.
        
        ### Returns:
        None - Stop event set.
        """
        self._stop_event.set()


class ApplicationController:
    """Main application controller coordinating logging and worker components.
    
    Demonstrates the recommended pattern for structuring applications that use
    centralized logging with multiple components.
    """

    def __init__(self, log_file: str = "/tmp/application.log"):
        """Initialize the application controller.
        
        ### Arguments:
        * log_file: str - Path to the application log file.
        
        ### Returns:
        None - Constructor.
        """
        self._log_file = log_file
        self._log_server: Optional[LoggingServer] = None
        self._main_logger: Optional[LoggerClient] = None
        self._workers: list[WorkerComponent] = []
        self._worker_threads: list[threading.Thread] = []

    def initialize(self) -> None:
        """Initialize the logging infrastructure and main logger.
        
        ### Returns:
        None - Application initialized and ready to run.
        """
        # Initialize and start the logging server
        self._log_server = LoggingServer(log_file=self._log_file, debug=False)
        self._log_server.initialize()
        self._log_server.start()

        # Create the main application logger
        self._main_logger = self._log_server.create_client(name="MainApp")
        self._main_logger.message_info = "Application initialized"

    def start_workers(self, num_workers: int = 3) -> None:
        """Create and start worker components.
        
        ### Arguments:
        * num_workers: int - Number of worker threads to create.
        
        ### Returns:
        None - Workers started in separate threads.
        """
        if self._main_logger is None or self._log_server is None:
            raise RuntimeError("Application not initialized.")

        self._main_logger.message_info = f"Starting {num_workers} worker(s)"

        for i in range(num_workers):
            # Create a dedicated logger for this worker
            worker_logger = self._log_server.create_client(name=f"Worker-{i+1}")
            
            
            # Create the worker component
            worker = WorkerComponent(worker_logger, i + 1)
            self._workers.append(worker)
            
            # Start worker in a separate thread
            thread = threading.Thread(
                target=worker.run,
                name=f"WorkerThread-{i+1}",
                daemon=False,
            )
            thread.start()
            self._worker_threads.append(thread)

    def wait_for_workers(self, timeout: Optional[float] = None) -> None:
        """Wait for all worker threads to complete.
        
        ### Arguments:
        * timeout: Optional[float] - Maximum seconds to wait per thread.
        
        ### Returns:
        None - All worker threads joined.
        """
        if self._main_logger is None:
            return

        self._main_logger.message_info = "Waiting for workers to complete"
        
        for thread in self._worker_threads:
            thread.join(timeout=timeout)

        self._main_logger.message_info = "All workers completed"

    def shutdown(self) -> None:
        """Gracefully shut down the application and logging system.
        
        ### Returns:
        None - All components stopped and cleaned up.
        """
        if self._main_logger is not None:
            self._main_logger.message_info = "Application shutting down"

        # Stop all workers
        for worker in self._workers:
            worker.stop()

        # Wait for worker threads to finish
        for thread in self._worker_threads:
            if thread.is_alive():
                thread.join(timeout=2.0)

        # Give logging system time to flush
        time.sleep(0.5)

        if self._main_logger is not None:
            self._main_logger.message_info = "Application shutdown complete"

        # Stop the logging server
        if self._log_server is not None:
            self._log_server.stop(timeout=3.0)


def main() -> None:
    """Main entry point demonstrating the complete logging workflow.
    
    ### Returns:
    None - Example execution complete.
    """
    print("=" * 70)
    print("JskToolBox LogsTool Example - Threaded Logging Server")
    print("=" * 70)
    print()
    print("This example demonstrates:")
    print("  * Centralized logging server in a dedicated thread")
    print("  * Multiple client components with independent loggers")
    print("  * File and console output with datetime formatting")
    print("  * Graceful shutdown with message flushing")
    print()
    print(f"Log file: /tmp/application.log")
    print()
    print("=" * 70)
    print()

    # Create and initialize the application
    app = ApplicationController(log_file="/tmp/application.log")
    
    try:
        # Initialize logging infrastructure
        app.initialize()
        
        # Start worker components
        app.start_workers(num_workers=3)
        
        # Wait for workers to complete their tasks
        app.wait_for_workers(timeout=30.0)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as ex:
        print(f"\n\nError: {ex}")
    finally:
        # Always clean up properly
        app.shutdown()
        
    print()
    print("=" * 70)
    print("Example completed. Check /tmp/application.log for full log output.")
    print("=" * 70)


if __name__ == "__main__":
    main()


# #[EOF]#######################################################################
