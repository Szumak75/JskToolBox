# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 04.12.2023

  Purpose: Base classes.
"""

from typing import Optional, TypeVar
from inspect import currentframe


from ...attribtool import ReadOnlyClass
from ...raisetool import Raise
from ...logstool.logs import LoggerClient
from ...basetool.data import BData


from ..network.connectors import IConnector

TDev = TypeVar("TDev", bound="BDev")


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    CH: str = "__connector_handler__"
    DEBUG: str = "__debug__"
    LC: str = "__logs_client__"
    PARENT: str = "__parent__"
    ROOT: str = "__root__"
    VERBOSE: str = "__verbose__"


class BDebug(BData):
    """Base class for debug flags."""

    @property
    def debug(self) -> bool:
        """Return debug flag."""
        return self._get_data(
            key=_Keys.DEBUG, set_default_type=bool, default_value=False
        )  # type: ignore

    @debug.setter
    def debug(self, debug: bool) -> None:
        """Set debug flag."""
        self._set_data(key=_Keys.DEBUG, set_default_type=bool, value=debug)

    @property
    def verbose(self) -> bool:
        """Return verbose flag."""
        return self._get_data(
            key=_Keys.VERBOSE, set_default_type=bool, default_value=False
        )  # type: ignore

    @verbose.setter
    def verbose(self, verbose: bool) -> None:
        """Set verbose flag."""
        self._set_data(key=_Keys.VERBOSE, set_default_type=bool, value=verbose)


class BDev(BDebug):
    """Base devices class."""

    @property
    def _ch(self) -> Optional[IConnector]:
        """Returns optional Connector object."""
        return self._get_data(key=_Keys.CH, set_default_type=Optional[IConnector])

    @_ch.setter
    def _ch(self, value: IConnector) -> None:
        """Sets Connector object."""
        self._set_data(key=_Keys.CH, value=value, set_default_type=Optional[IConnector])

    @property
    def logs(self) -> Optional[LoggerClient]:
        """Returns optional LoggerClient object."""
        return self._get_data(key=_Keys.LC, set_default_type=Optional[LoggerClient])

    @logs.setter
    def logs(self, value: LoggerClient) -> None:
        """Sets Connector object."""
        self._set_data(
            key=_Keys.LC, value=value, set_default_type=Optional[LoggerClient]
        )

    @property
    def root(self) -> str:
        """Gets RouterOS command root."""
        tmp: str = self._get_data(
            key=_Keys.ROOT, set_default_type=str, default_value=""
        )  # type: ignore
        if self.parent is not None:
            item: BDev = self.parent
            tmp = f"{item.root}{tmp}"
        return tmp

    @root.setter
    def root(self, value: str) -> None:
        """Sets RouterOS command root."""
        self._set_data(key=_Keys.ROOT, set_default_type=str, value=value)

    @property
    def parent(self) -> Optional[TDev]:
        """Returns parent for current object."""
        return self._get_data(
            key=_Keys.PARENT, set_default_type=Optional[BDev], default_value=None
        )

    @parent.setter
    def parent(self, value: Optional[TDev]) -> None:
        """Sets parent for current object."""
        self._set_data(key=_Keys.PARENT, set_default_type=Optional[BDev], value=value)


# #[EOF]#######################################################################
