# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 04.09.2023

  Purpose: logs subsystem classes.
"""

import os
import sys
from abc import abstractmethod
from inspect import currentframe

from typing import Optional, List, Dict, Tuple

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.libs.system import Env, PathChecker
from jsktoolbox.logstool.engines import *


class Keys(NoDynamicAttributes):
    """Keys definition class.

    For internal purpose only.
    """

    @classmethod
    @property
    def CONF(cls) -> str:
        """Return CONF Key."""
        return "__conf__"

    @classmethod
    @property
    def NO_CONF(cls) -> str:
        """Return NO_CONF Key."""
        return "__noconf__"

    @classmethod
    @property
    def NAME(cls) -> str:
        """Return NAME Key."""
        return "__name__"

    @classmethod
    @property
    def QUEUE(cls) -> str:
        """Return QUEUE Key."""
        return "__queue__"


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


class LoggerProcessor:
    """LoggerProcessor thread engine."""

    def __init__(self):
        """Constructor."""


class MLoggerQueue(BData, NoDynamicAttributes):
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


class LoggerEngine(MLoggerQueue, NoDynamicAttributes):
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


class LoggerClient(MLoggerQueue, NoDynamicAttributes):
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
        if not isinstance(name, str):
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


# #[EOF]#######################################################################
