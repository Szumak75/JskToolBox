# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 04.09.2023

  Purpose: base class for log subsystem.
"""

import syslog

from inspect import currentframe
from typing import Optional, Tuple, List, Dict, Any

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData


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
    def CONF(cls) -> str:
        """Return CONF Key."""
        return "__conf__"

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
    def NO_CONF(cls) -> str:
        """Return NO_CONF Key."""
        return "__noconf__"

    @classmethod
    @property
    def QUEUE(cls) -> str:
        """Return QUEUE Key."""
        return "__queue__"

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


class LogsLevelKeys(NoDynamicAttributes):
    """LogsLevelKeys container class."""

    @classmethod
    @property
    def keys(cls) -> Tuple[str]:
        """Return tuple of avaiable keys."""
        return tuple(
            [
                LogsLevelKeys.ALERT,
                LogsLevelKeys.CRITICAL,
                LogsLevelKeys.DEBUG,
                LogsLevelKeys.EMERGENCY,
                LogsLevelKeys.ERROR,
                LogsLevelKeys.INFO,
                LogsLevelKeys.NOTICE,
                LogsLevelKeys.WARNING,
            ]
        )

    @classmethod
    @property
    def ALERT(cls) -> str:
        """Return ALERT Key."""
        return "ALERT"

    @classmethod
    @property
    def CRITICAL(cls) -> str:
        """Return CRITICAL Key."""
        return "CRITICAL"

    @classmethod
    @property
    def DEBUG(cls) -> str:
        """Return DEBUG Key."""
        return "DEBUG"

    @classmethod
    @property
    def EMERGENCY(cls) -> str:
        """Return EMERGENCY Key."""
        return "EMERGENCY"

    @classmethod
    @property
    def ERROR(cls) -> str:
        """Return ERROR Key."""
        return "ERROR"

    @classmethod
    @property
    def INFO(cls) -> str:
        """Return INFO Key."""
        return "INFO"

    @classmethod
    @property
    def NOTICE(cls) -> str:
        """Return NOTICE Key."""
        return "NOTICE"

    @classmethod
    @property
    def WARNING(cls) -> str:
        """Return WARNING Key."""
        return "WARNING"


class LoggerQueue(NoDynamicAttributes):
    """LoggerQueue simple class."""

    __queue: List[str] = None

    def __init__(self):
        """Constructor."""
        self.__queue = []

    def get(self) -> Optional[Tuple[str, str]]:
        """Get item from queue.

        Returs queue tuple[logs_level:str, message:str] or None if empty.
        """
        try:
            return tuple(self.__queue.pop(0))
        except IndexError:
            return None
        except Exception as ex:
            raise Raise.error(
                f"Unexpected exception was thrown: {ex}",
                self.__class__.__name__,
                currentframe(),
            )

    def put(
        self, message: str, logs_level: str = LogsLevelKeys.INFO
    ) -> None:
        """Put item to queue."""
        if logs_level not in LogsLevelKeys.keys:
            raise Raise.error(
                f"logs_level key not found, '{logs_level}' received.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )
        self.__queue.append(
            [
                logs_level,
                message,
            ]
        )


class BLoggerQueue(BData, NoDynamicAttributes):
    """Logger Queue base metaclass."""

    @property
    def logs_queue(self) -> Optional[LoggerQueue]:
        """Get LoggerQueue object."""
        if Keys.QUEUE not in self._data:
            return None
        return self._data[Keys.QUEUE]

    @logs_queue.setter
    def logs_queue(self, obj: LoggerQueue) -> None:
        """Set LoggerQueue object."""
        if not isinstance(obj, LoggerQueue):
            raise Raise.error(
                f"LoggerQueue type object expected, '{type(obj)}' received.",
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.QUEUE] = obj


class BLoggerEngine(BData, NoDynamicAttributes):
    """Base class for LoggerEngine classes."""

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


class BLogFormatter(NoDynamicAttributes):
    """Log formatter base class."""

    __template: Optional[str] = None
    __forms: Optional[List] = None

    def __init__(self) -> None:
        """Constructor."""
        self.__forms = []

    def format(self, message: str, name: str = None) -> str:
        """Method for format message string.

        Arguments:
        message [str]: log string to send
        name [str]: optional name of apps,
        """
        out = ""
        for item in self._forms_:
            if callable(item):
                out += f"{item()} "
            elif isinstance(item, str):
                if name is None:
                    if item.find("name") == -1:
                        out += item.format(message=f"{message}")
                else:
                    if item.find("name") > 0:
                        out += item.format(
                            name=f"{name}",
                            message=f"{message}",
                        )
        return out

    @property
    def _forms_(self) -> List:
        """Get forms list."""
        return self.__forms

    @_forms_.setter
    def _forms_(self, item: Any) -> None:
        """Set forms list."""
        # assigning function to a variable
        # def a(): print('test')
        # var=a
        # var()
        ####
        # >>> x._forms_[2].__class__
        # <class 'builtin_function_or_method'>
        # >>> x._forms_[1].__class__
        # <class 'float'>
        # >>> x._forms_[0].__class__
        # <class 'str'>

        self.__forms.append(item)


# #[EOF]#######################################################################
