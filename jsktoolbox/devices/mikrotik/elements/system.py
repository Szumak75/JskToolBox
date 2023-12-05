# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 04.12.2023

  Purpose: RB '/system'
"""

from typing import Dict, List, Optional, Union, Tuple, Any
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

from jsktoolbox.devices.mikrotik.base import BRouterOS, BDev
from jsktoolbox.devices.mikrotik.elements.interfaces import IElement
from jsktoolbox.devices.mikrotik.elements.base import BElement

from jsktoolbox.devices.network.connectors import IConnector, API, SSH


class _Keys(object, metaclass=ReadOnlyClass):
    """"""


class _Elements(object, metaclass=ReadOnlyClass):
    """"""

    IDENTITY = "identity"
    RESOURCE = "resource"
    ROUTERBOARD = "routerboard"
    CLOCK = "clock"
    HEALTH = "health"
    LICENSE = "license"
    LOGGING = "logging"
    NTP = "ntp"
    SCHEDULER = "scheduler"
    SCRIPT = "script"
    SYSTEM = "system"
    UPGRADE = "upgrade"
    WATCHDOG = "watchdog"


class System(BRouterOS, BElement, IElement):
    """"""

    def __init__(
        self,
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
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.path = f"{_Elements.SYSTEM}/"

        # add elements
        self.elements[_Elements.IDENTITY] = Identity(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.ROUTERBOARD] = RouterBoard(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.RESOURCE] = Resource(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        # print(f"P: {self.path}")
        # self.load(self.path)


class Identity(BRouterOS, BElement, IElement):
    """"""

    def __init__(
        self,
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
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.path = f"{_Elements.IDENTITY}/"

        # add elements

        # load data
        self.load(self.path)


class RouterBoard(BRouterOS, BElement, IElement):
    """"""

    def __init__(
        self,
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
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.path = f"{_Elements.ROUTERBOARD}/"

        # add elements

        # load data
        self.load(self.path)


class Resource(BRouterOS, BElement, IElement):
    """"""

    def __init__(
        self,
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
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.path = f"{_Elements.RESOURCE}/"

        # add elements

        # load data
        self.load(self.path)

    # def load(self) -> bool:
    # """"""
    # ret = self._ch.execute(f"{self.path}print")
    # print(ret)

    # for key, item in self.elements.items():
    # element: IElement = item
    # element.load()


# #[EOF]#######################################################################
