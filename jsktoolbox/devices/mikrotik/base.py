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

from jsktoolbox.devices.mikrotik.elements.libs.interfaces import IElement
from jsktoolbox.devices.mikrotik.elements.libs.base import BElement
from jsktoolbox.devices.libs.base import BDev
from jsktoolbox.devices.network.connectors import IConnector, API, SSH

TRouterOs = TypeVar("TRouterOs", bound="BRouterOs")
TElement = TypeVar("TElement", bound="Element")


class _Keys(object, metaclass=ReadOnlyClass):
    """"""

    ELEMENTS = "__elements__"
    LOADED = "__loaded__"


class BRouterOS(BDev, BElement):
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
        self._data[_Keys.LOADED] = False

    def __str__(self) -> str:
        """"""
        return f"{self._c_name}(path='{self.path}', elements='{self.elements}', attrib='{self.attrib}')"

    def _add_element(
        self,
        key: str,
        btype: TElement,
        parent: TRouterOs,
        connector: IConnector,
        qlog: LoggerQueue,
        debug: bool,
        verbose: bool,
    ) -> None:
        """Add child class to elemets dict."""
        self.elements[key] = btype(
            key=key,
            parent=parent,
            connector=connector,
            qlog=qlog,
            debug=debug,
            verbose=verbose,
        )

    def dump(self):
        """Dump all dataset."""
        print(self.path)
        self.load(self.path)
        if self.attrib:
            print(f"attrib: {self.attrib}")
        if self.list:
            # print(f"list: {self.list}")
            for item in self.list:
                print(f"list: {item}")
        for item in self.elements.values():
            item.dump()

    def element(
        self, path: str, auto_load: bool = False
    ) -> Optional[TElement]:
        """Returns Element object for coresponding path."""
        # check if first and last char in path is '/'
        if path:
            if path[0] != "/":
                path = f"/{path}"
            if path[-1:] != "/":
                path = f"{path}/"
        for key in self.elements.keys():
            element: Element = self.elements[key]
            if element.path == path:
                if auto_load:
                    element.load(path)
                return element
            element2: Element = element.element(path, auto_load)
            if element2 is not None:
                return element2
        return None

    @property
    def elements(self) -> Dict:
        """Return elements dict."""
        if _Keys.ELEMENTS not in self._data:
            self._data[_Keys.ELEMENTS] = {}
        return self._data[_Keys.ELEMENTS]

    def get(self) -> bool:
        """Gets config for current element."""
        return self.load(self.path)

    @property
    def is_loaded(self) -> bool:
        """Returns True if loaded."""
        return self._data[_Keys.LOADED]

    def load(self, path: str) -> bool:
        """Gets element config from RB."""
        if path is not None and not self._data[_Keys.LOADED]:
            # print(f"Path: {path}")
            ret = self._ch.execute(f"{path}print")
            # print(ret)
            if ret:
                out, err = self._ch.outputs()
                if (
                    out[0]
                    and isinstance(out[0], List)
                    and len(out[0]) == 1
                    and isinstance(out[0][0], Dict)
                ):
                    self.attrib.update(out[0][0])
                    self._data[_Keys.LOADED] = True
                elif (
                    out[0]
                    and isinstance(out[0], List)
                    and len(out[0]) > 1
                    and isinstance(out[0][0], Dict)
                ):
                    for item in out[0]:
                        self.list.append(item)
                    self._data[_Keys.LOADED] = True
                else:
                    if out[0]:
                        print(f"DEBUG_: {out}")
                if err[0]:
                    self.logs.message_warning = f"{out[0][0]}"
                    return False
                return True
        return False


class Element(BRouterOS):
    """MiktoTik Element class."""

    def __init__(
        self,
        key: str,
        parent: BDev,
        connector: IConnector,
        qlog: LoggerQueue = None,
        debug: bool = False,
        verbose: bool = False,
    ):
        """Constructor."""
        super().__init__(
            parent,
            connector,
            LoggerClient(queue=qlog, name=key),
            debug,
            verbose,
        )
        self.path = f"{key}/"


# #[EOF]#######################################################################
