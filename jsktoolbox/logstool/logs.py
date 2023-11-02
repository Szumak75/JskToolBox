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

from typing import Optional, List, Dict

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


class LoggerEngine(BData, NoDynamicAttributes):
    """LoggerEngine container class."""

    def __init__(self) -> None:
        """Constructor."""
        self._data[Keys.NO_CONF] = {}
        self._data[Keys.NO_CONF][LogsLevelKeys.info] = [LoggerEngineStdout()]
        self._data[Keys.NO_CONF][LogsLevelKeys.debug] = [
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
        self._data[Keys.NAME] = name


# #[EOF]#######################################################################
