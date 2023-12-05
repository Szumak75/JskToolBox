# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 04.12.2023

  Purpose: Base classes for RouterOS
"""

from typing import Dict, List, Optional, Union, Tuple, Any, TypeVar
from inspect import currentframe

from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue


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

from jsktoolbox.devices.libs.base import BDev
from jsktoolbox.devices.network.connectors import IConnector, API, SSH

TRouterOs = TypeVar("TRouterOs", bound="BRouterOs")


class _Keys(object, metaclass=ReadOnlyClass):
    """"""

    ELEMENTS = "__elements__"


class BRouterOS(BDev):
    """"""

    def __init__(
        self,
        parent: BDev,
        connector: IConnector,
        logs: LoggerClient,
        debug: bool,
        verbose: bool,
    ) -> None:
        """Constructor."""
        self.parent = parent
        self._ch = connector
        self.logs = logs
        self.debug = debug
        self.verbose = verbose

    @property
    def elements(self) -> Dict:
        """"""
        if _Keys.ELEMENTS not in self._data:
            self._data[_Keys.ELEMENTS] = {}
        return self._data[_Keys.ELEMENTS]

    def load(self, path: str) -> bool:
        """"""
        if path is not None:
            print(f"Path: {path}")
            ret = self._ch.execute(f"{path}print")
            print(ret)

        # for key, item in self.elements.items():
        # print(f"Key: {key}")
        # element: TRouterOs = item
        # element.load()


# #[EOF]#######################################################################
