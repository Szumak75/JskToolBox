# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 04.12.2023

  Purpose: Base classes.
"""

from typing import Dict, List, Optional, Union, Tuple, Any, TypeVar
from inspect import currentframe

from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue
from jsktoolbox.libs.base_data import BData

from jsktoolbox.netaddresstool.ipv4 import (
    Address,
    Netmask,
    Network,
    SubNetwork,
)
from jsktoolbox.netaddresstool.ipv6 import (
    Address6,
    Network6,
    Prefix6,
    SubNetwork6,
)

from jsktoolbox.devices.network.connectors import IConnector

TDev = TypeVar("TDev", bound="BDev")


class _Keys(object, metaclass=ReadOnlyClass):
    """"""

    CH = "__connector_handler__"
    LC = "__logs_client__"
    DEBUG = "__debug__"
    VERBOSE = "__verbose__"
    PARENT = "__parent__"
    PATH = "__path__"


class BDebug(BData):
    """Base class for debug flags."""

    @property
    def debug(self) -> bool:
        """Return debug flag."""
        if _Keys.DEBUG not in self._data:
            self._data[_Keys.DEBUG] = False
        return self._data[_Keys.DEBUG]

    @debug.setter
    def debug(self, debug: bool) -> None:
        """Set debug flag."""
        self._data[_Keys.DEBUG] = debug

    @property
    def verbose(self) -> bool:
        """Return verbose flag."""
        if _Keys.VERBOSE not in self._data:
            self._data[_Keys.VERBOSE] = False
        return self._data[_Keys.VERBOSE]

    @verbose.setter
    def verbose(self, verbose: bool) -> None:
        """Set verbose flag."""
        self._data[_Keys.VERBOSE] = verbose


class BDev(BDebug):
    """Base devices class."""

    @property
    def _ch(self) -> Optional[IConnector]:
        """Returns optional Connector object."""
        if _Keys.CH not in self._data:
            self._data[_Keys.CH] = None
        return self._data[_Keys.CH]

    @_ch.setter
    def _ch(self, value: IConnector) -> None:
        """Sets Connector object."""
        if not isinstance(value, IConnector):
            raise Raise.error(
                f"Expected IConnector derived type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.CH] = value

    @property
    def logs(self) -> Optional[LoggerClient]:
        """Returns optional LoggerClient object."""
        if _Keys.LC not in self._data:
            self._data[_Keys.LC] = None
        return self._data[_Keys.LC]

    @logs.setter
    def logs(self, value: LoggerClient) -> None:
        """Sets Connector object."""
        if not isinstance(value, LoggerClient):
            raise Raise.error(
                f"Expected LoggerClient type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.LC] = value

    @property
    def path(self) -> str:
        """"""
        if _Keys.PATH not in self._data:
            self._data[_Keys.PATH] = ""
        tmp = self._data[_Keys.PATH]
        item: BDev = self.parent
        if item:
            tmp = f"{item.path}{tmp}"
        return tmp

    @path.setter
    def path(self, value: str) -> None:
        """"""
        if not isinstance(value, str):
            raise Raise.error(
                f"Expected string type, received: '{type(value)}'",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.PATH] = value

    @property
    def parent(self) -> TDev:
        """"""
        if _Keys.PARENT not in self._data:
            self._data[_Keys.PARENT] = None
        return self._data[_Keys.PARENT]

    @parent.setter
    def parent(self, value: Optional[TDev]) -> None:
        """"""
        if value is not None and not isinstance(value, BDev):
            raise Raise.error(
                f"Expected BDev type, received: '{type(value)}'",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.PARENT] = value


# #[EOF]#######################################################################
