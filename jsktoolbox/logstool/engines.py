# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2023

  Purpose: logger engine classes.
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

# https://www.geeksforgeeks.org/python-testing-output-to-stdout/


class Keys(NoDynamicAttributes):
    """Keys definition class.

    For internal purpose only.
    """

    @classmethod
    @property
    def BUFFERED(cls) -> str:
        """Return BUFFERED Key."""
        return "__buffered__"

    @classmethod
    @property
    def DIR(cls) -> str:
        """Return DIR Key."""
        return "__dir__"

    @classmethod
    @property
    def FILE(cls) -> str:
        """Return FILE Key."""
        return "__file__"


class ILoggerEngine(ABC):
    """Logger engine interface class."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Send message method."""


class LoggerEngineStdout(ILoggerEngine, BData, NoDynamicAttributes):
    """STDOUT Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self._data[Keys.BUFFERED] = buffered

    def send(self, message: str) -> None:
        """Send message to STDOUT."""
        sys.stdout.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stdout.write("\n")
        if not self._data[Keys.BUFFERED]:
            sys.stdout.flush()


class LoggerEngineStderr(ILoggerEngine, BData, NoDynamicAttributes):
    """STDERR Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self._data[Keys.BUFFERED] = buffered

    def send(self, message: str) -> None:
        """Send message to STDERR."""
        sys.stderr.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stderr.write("\n")
        if not self._data[Keys.BUFFERED]:
            sys.stderr.flush()


class LoggerEngineFile(ILoggerEngine, BData, NoDynamicAttributes):
    """FILE Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self._data[Keys.BUFFERED] = buffered

    def send(self, message: str) -> None:
        """Send message to file."""

    @property
    def logdir(self) -> Optional[str]:
        """Return log directory."""
        if Keys.DIR not in self._data:
            self._data[Keys.DIR] = None
        return self._data[Keys.DIR]

    @logdir.setter
    def logdir(self, dirname: str) -> None:
        """Set log directory."""
        if dirname[-1] != os.sep:
            dirname = f"{dirname}/"
        ld = PathChecker(dirname)
        if not ld.exists:
            ld.create()
        if ld.exists and ld.is_dir:
            self._data[Keys.DIR] = ld.path

    @property
    def logfile(self) -> Optional[str]:
        """Return log file name."""
        if Keys.FILE not in self._data:
            self._data[Keys.FILE] = None
        return self._data[Keys.FILE]

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
        self._data[Keys.FILE] = ld.filename


class LoggerEngineSyslog(ILoggerEngine, BData, NoDynamicAttributes):
    """SYSLOG Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self._data[Keys.BUFFERED] = buffered

    def send(self, message: str) -> None:
        """Send message to SYSLOG."""


# #[EOF]#######################################################################
