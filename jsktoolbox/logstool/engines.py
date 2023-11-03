# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2023

  Purpose: logger engine classes.
"""

import os
import sys
import syslog
from abc import ABC, abstractmethod
from inspect import currentframe

from typing import Optional, Union, List, Dict
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.libs.system import Env, PathChecker
from jsktoolbox.logstool.formatters import BLogFormatter

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

    @classmethod
    @property
    def FORMATTER(cls) -> str:
        """Return FORMATTER Key."""
        return "__formatter__"

    @classmethod
    @property
    def FACILITY(cls) -> str:
        """Return FACILITY Key."""
        return "__facility__"

    @classmethod
    @property
    def LEVEL(cls) -> str:
        """Return LEVEL Key."""
        return "__level__"

    @classmethod
    @property
    def NAME(cls) -> str:
        """Return NAME Key."""
        return "__name__"

    @classmethod
    @property
    def SYSLOG(cls) -> str:
        """Return SYSLOG Key."""
        return "__syslog__"


class SysLogKeys(NoDynamicAttributes):
    """SysLog keys definition container class."""

    class __Levels(NoDynamicAttributes):
        @classmethod
        @property
        def NOTICE(cls) -> int:
            return syslog.LOG_NOTICE

        @classmethod
        @property
        def EMERGENCY(cls) -> int:
            return syslog.LOG_EMERG

        @classmethod
        @property
        def ALERT(cls) -> int:
            return syslog.LOG_ALERT

        @classmethod
        @property
        def CRITICAL(cls) -> int:
            return syslog.LOG_CRIT

        @classmethod
        @property
        def INFO(cls) -> int:
            return syslog.LOG_INFO

        @classmethod
        @property
        def DEBUG(cls) -> int:
            return syslog.LOG_DEBUG

        @classmethod
        @property
        def WARNING(cls) -> int:
            return syslog.LOG_WARNING

        @classmethod
        @property
        def ERROR(cls) -> int:
            return syslog.LOG_ERR

    class __Facilities(NoDynamicAttributes):
        @classmethod
        @property
        def DAEMON(cls) -> int:
            return syslog.LOG_DAEMON

        @classmethod
        @property
        def USER(cls) -> int:
            return syslog.LOG_USER

        @classmethod
        @property
        def LOCAL0(cls) -> int:
            return syslog.LOG_LOCAL0

        @classmethod
        @property
        def LOCAL1(cls) -> int:
            return syslog.LOG_LOCAL1

        @classmethod
        @property
        def LOCAL2(cls) -> int:
            return syslog.LOG_LOCAL2

        @classmethod
        @property
        def LOCAL3(cls) -> int:
            return syslog.LOG_LOCAL3

        @classmethod
        @property
        def LOCAL4(cls) -> int:
            return syslog.LOG_LOCAL4

        @classmethod
        @property
        def LOCAL5(cls) -> int:
            return syslog.LOG_LOCAL5

        @classmethod
        @property
        def LOCAL6(cls) -> int:
            return syslog.LOG_LOCAL6

        @classmethod
        @property
        def LOCAL7(cls) -> int:
            return syslog.LOG_LOCAL7

        @classmethod
        @property
        def MAIL(cls) -> int:
            return syslog.LOG_MAIL

        @classmethod
        @property
        def SYSLOG(cls) -> int:
            return syslog.LOG_SYSLOG

    @classmethod
    @property
    def level(cls):
        """Returns Levels keys property."""
        return cls.__Levels

    @classmethod
    @property
    def facility(cls):
        """Returns Facility keys property."""
        return cls.__Facilities

    @classmethod
    @property
    def level_keys(cls) -> Dict:
        """Returns level keys property."""
        return {
            "NOTICE": SysLogKeys.level.NOTICE,
            "INFO": SysLogKeys.level.INFO,
            "DEBUG": SysLogKeys.level.DEBUG,
            "WARNING": SysLogKeys.level.WARNING,
            "ERROR": SysLogKeys.level.ERROR,
            "EMERGENCY": SysLogKeys.level.EMERGENCY,
            "ALERT": SysLogKeys.level.ALERT,
            "CRITICAL": SysLogKeys.level.CRITICAL,
        }

    @classmethod
    @property
    def facility_keys(cls) -> Dict:
        """Returns Facility keys property."""
        return {
            "DAEMON": SysLogKeys.facility.DAEMON,
            "USER": SysLogKeys.facility.USER,
            "LOCAL0": SysLogKeys.facility.LOCAL0,
            "LOCAL1": SysLogKeys.facility.LOCAL1,
            "LOCAL2": SysLogKeys.facility.LOCAL2,
            "LOCAL3": SysLogKeys.facility.LOCAL3,
            "LOCAL4": SysLogKeys.facility.LOCAL4,
            "LOCAL5": SysLogKeys.facility.LOCAL5,
            "LOCAL6": SysLogKeys.facility.LOCAL6,
            "LOCAL7": SysLogKeys.facility.LOCAL7,
            "MAIL": SysLogKeys.facility.MAIL,
            "SYSLOG": SysLogKeys.facility.SYSLOG,
        }


class ILoggerEngine(ABC):
    """Logger engine interface class."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Send message method."""


class BLoggerEngine(BData, NoDynamicAttributes):
    """"""

    @property
    def name(self) -> Optional[str]:
        """Return app name string."""
        if Keys.NAME not in self._data:
            self._data[Keys.NAME] = None
        return self._data[Keys.NAME]

    @name.setter
    def name(self, value: str) -> None:
        """Set app name string."""
        self._data[Keys.NAME] = value


class LoggerEngineStdout(
    ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes
):
    """STDOUT Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Constructor."""
        if name is not None:
            self.name = name
        self._data[Keys.BUFFERED] = buffered
        self._data[Keys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[Keys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"LogFormatter type expected, '{type(formatter)}' received.",
                    TypeError,
                    self.__class__.__name__,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Send message to STDOUT."""
        if self._data[Keys.FORMATTER]:
            message = self._data[Keys.FORMATTER].format(message, self.name)
        sys.stdout.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stdout.write("\n")
        if not self._data[Keys.BUFFERED]:
            sys.stdout.flush()


class LoggerEngineStderr(
    ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes
):
    """STDERR Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Constructor."""
        if name is not None:
            self.name = name
        self._data[Keys.BUFFERED] = buffered
        self._data[Keys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[Keys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"LogFormatter type expected, '{type(formatter)}' received.",
                    TypeError,
                    self.__class__.__name__,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Send message to STDERR."""
        if self._data[Keys.FORMATTER]:
            message = self._data[Keys.FORMATTER].format(message, self.name)
        sys.stderr.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stderr.write("\n")
        if not self._data[Keys.BUFFERED]:
            sys.stderr.flush()


class LoggerEngineFile(
    ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes
):
    """FILE Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Constructor."""
        if name is not None:
            self.name = name
        self._data[Keys.BUFFERED] = buffered
        self._data[Keys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[Keys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"LogFormatter type expected, '{type(formatter)}' received.",
                    TypeError,
                    self.__class__.__name__,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Send message to file."""
        if self._data[Keys.FORMATTER]:
            message = self._data[Keys.FORMATTER].format(message, self.name)
            if self.logfile is None:
                raise Raise.error(
                    f"The {self.__class__.__name__} is not configured correctly.",
                    ValueError,
                    self.__class__.__name__,
                    currentframe(),
                )
            with open(os.path.join(self.logdir, self.logfile), "a") as file:
                if file.writable:
                    file.write(message)
                    file.write("\n")

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


class LoggerEngineSyslog(
    ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes
):
    """SYSLOG Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Constructor."""
        if name is not None:
            self.name = name
        self._data[Keys.BUFFERED] = buffered
        self._data[Keys.FORMATTER] = None
        self._data[Keys.LEVEL] = SysLogKeys.level.INFO
        self._data[Keys.FACILITY] = SysLogKeys.facility.USER
        self._data[Keys.SYSLOG] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[Keys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"LogFormatter type expected, '{type(formatter)}' received.",
                    TypeError,
                    self.__class__.__name__,
                    currentframe(),
                )

    def __del__(self):
        try:
            self._data[Keys.SYSLOG].closelog()
        except:
            pass
        self._data[Keys.SYSLOG] = None

    @property
    def facility(self) -> int:
        """Return syslog facility."""
        return self._data[Keys.FACILITY]

    @facility.setter
    def facility(self, value: Union[int, str]) -> None:
        """Set syslog facility."""
        if isinstance(value, int):
            if value in tuple(SysLogKeys.facility_keys.values()):
                self._data[Keys.FACILITY] = value
            else:
                raise Raise.error(
                    f"Syslog facility: '{value}' not found.",
                    ValueError,
                    self.__class__.__name__,
                    currentframe(),
                )
        if isinstance(value, str):
            if value in SysLogKeys.facility_keys:
                self._data[Keys.FACILITY] = SysLogKeys.facility_keys[value]
            else:
                raise Raise.error(
                    f"Syslog facility name not found: '{value}'",
                    KeyError,
                    self.__class__.__name__,
                    currentframe(),
                )
        try:
            self._data[Keys.SYSLOG].closelog()
        except:
            pass
        self._data[Keys.SYSLOG] = None

    @property
    def level(self) -> int:
        """Return syslog level."""
        return self._data[Keys.LEVEL]

    @level.setter
    def level(self, value: Union[int, str]) -> None:
        """Set syslog level."""
        if isinstance(value, int):
            if value in tuple(SysLogKeys.level_keys.values()):
                self._data[Keys.LEVEL] = value
            else:
                raise Raise.error(
                    f"Syslog level: '{value}' not found.",
                    ValueError,
                    self.__class__.__name__,
                    currentframe(),
                )
        if isinstance(value, str):
            if value in SysLogKeys.level_keys:
                self._data[Keys.LEVEL] = SysLogKeys.level_keys[value]
            else:
                raise Raise.error(
                    f"Syslog level name not found: '{value}'",
                    KeyError,
                    self.__class__.__name__,
                    currentframe(),
                )
        try:
            self._data[Keys.SYSLOG].closelog()
        except:
            pass
        self._data[Keys.SYSLOG] = None

    def send(self, message: str) -> None:
        """Send message to SYSLOG."""
        if self._data[Keys.FORMATTER]:
            message = self._data[Keys.FORMATTER].format(message, self.name)
        if self._data[Keys.SYSLOG] is None:
            self._data[Keys.SYSLOG] = syslog
            self._data[Keys.SYSLOG].openlog(
                facility=self._data[Keys.FACILITY]
            )
        self._data[Keys.SYSLOG].syslog(
            priority=self._data[Keys.LEVEL], message=message
        )


# #[EOF]#######################################################################
