# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 04.09.2023

  Purpose: logs subsystem classes.
"""

import os
import sys
from abc import ABC, abstractmethod
from inspect import currentframe

from typing import Optional, List, Dict
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.libs.system import Env, PathChecker


class LogsLevelKeys(NoDynamicAttributes):
    """LogsLevelKeys container class."""

    @classmethod
    @property
    def emergency(cls) -> str:
        """Return EMERGENCY Key."""
        return "EMERGENCY"

    @classmethod
    @property
    def alert(cls) -> str:
        """Return ALERT Key."""
        return "ALERT"

    @classmethod
    @property
    def critical(cls) -> str:
        """Return CRITICAL Key."""
        return "CRITICAL"

    @classmethod
    @property
    def error(cls) -> str:
        """Return ERROR Key."""
        return "ERROR"

    @classmethod
    @property
    def warning(cls) -> str:
        """Return WARNING Key."""
        return "WARNING"

    @classmethod
    @property
    def notice(cls) -> str:
        """Return NOTICE Key."""
        return "NOTICE"

    @classmethod
    @property
    def info(cls) -> str:
        """Return INFO Key."""
        return "INFO"

    @classmethod
    @property
    def debug(cls) -> str:
        """Return DEBUG Key."""
        return "DEBUG"


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
        if dirname[-1] != os.sep:
            dirname = f"{dirname}/"
        ld = PathChecker(dirname)
        if not ld.exists:
            ld.create()
        if ld.exists and ld.is_dir:
            self.data["dir"] = ld.path

    @property
    def logfile(self) -> Optional[str]:
        """Return log file name."""
        if "file" not in self.data:
            self.data["file"] = None
        return self.data["file"]

    @logfile.setter
    def logfile(self, filename: str) -> None:
        """Set log file name."""
        # TODO: check procedure
        fn = None
        if self.logdir is None:
            fn = filename
        else:
            fn = os.path.join(self.logdir, filename)
        ld = PathChecker(fn)
        if ld.exists:
            if not ld.is_file:
                raise Raise.error(
                    f"The filename passed: '{filename}' is a directory.",
                    FileExistsError,
                    self.__class__.__name__,
                    currentframe(),
                )
        else:
            if not ld.create():
                raise Raise.error(
                    f"I cannot create a file: {ld.path}",
                    PermissionError,
                    self.__class__.__name__,
                    currentframe(),
                )
        self.logdir = ld.dirname
        self.data["file"] = ld.filename


class LoggerEngineSyslog(ILoggerEngine, BData, NoDynamicAttributes):
    """SYSLOG Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to SYSLOG."""


class LoggerEngine(BData, NoDynamicAttributes):
    """LoggerEngine container class."""

    __ckey = "conf"
    __nkey = "noconf"

    def __init__(self) -> None:
        """Constructor."""
        self.data[self.__nkey] = {}
        self.data[self.__nkey][LogsLevelKeys.info] = [LoggerEngineStdout()]
        self.data[self.__nkey][LogsLevelKeys.debug] = [LoggerEngineStderr()]

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
        if self.__ckey not in self.data:
            self.data[self.__ckey] = {}
            self.data[self.__ckey][log_level] = [engine]
        else:
            if log_level not in self.data[self.__ckey].keys():
                self.data[self.__ckey][log_level] = [engine]
            else:
                test = False
                for i in range(0, len(self.data[self.__ckey][log_level])):
                    if (
                        self.data[self.__ckey][log_level][i].__class__
                        == engine.__class__
                    ):
                        self.data[self.__ckey][log_level][i] = engine
                        test = True
                if not test:
                    self.data[self.__ckey][log_level].append(engine)


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
