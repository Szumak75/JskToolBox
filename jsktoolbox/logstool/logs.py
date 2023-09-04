# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 04.09.2023

  Purpose: logs subsystem classes.
"""
import sys
from abc import ABC, abstractmethod

from typing import Optional, List, Dict
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.libs.base_data import BData


class ILoggerEngine(ABC):
    """Logger engine interface class."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Send message method."""


class LoggerEngineStdout(ILoggerEngine, BData, NoDynamicAttributes):
    """STDOUT Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to STDOUT."""
        sys.stdout.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stdout.write("\n")
        if not self.data["buffered"]:
            sys.stdout.flush()


class LoggerEngineStderr(ILoggerEngine, BData, NoDynamicAttributes):
    """STDERR Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to STDERR."""
        sys.stderr.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stderr.write("\n")
        if not self.data["buffered"]:
            sys.stderr.flush()


class LoggerEngineFile(ILoggerEngine, BData, NoDynamicAttributes):
    """FILE Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to file."""

    @property
    def logdir(self) -> Optional[str]:
        """Return log directory."""
        if "dir" not in self.data:
            self.data["dir"] = None
        return self.data["dir"]

    @logdir.setter
    def logdir(self, dirname: str) -> None:
        """Set log directory."""

    @property
    def logfile(self) -> Optional[str]:
        """Return log file name."""
        if "file" not in self.data:
            self.data["file"] = None
        return self.data["file"]

    @logfile.setter
    def logfile(self, filename: str) -> None:
        """Set log file name."""


class LoggerEngineSyslog(ILoggerEngine, BData, NoDynamicAttributes):
    """SYSLOG Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to SYSLOG."""


class LoggerClient(BData, NoDynamicAttributes):
    """Logger Client main class."""

    # TODO:
    # stworzyć obiekt konfiguracyjny z listą
    # silników do raportowania wszystkich typów
    # logów: message, error, warning, debug
    # przekazać konfigurator w konstruktorze

    # stworzyć obiekt z szablonami formatowania
    # informacji przekazywanych do każdego z typów silników

    def __init__(self, name: Optional[str] = None) -> None:
        """Constructor."""
        # store name
        self.data["name"] = name


# #[EOF]#######################################################################
