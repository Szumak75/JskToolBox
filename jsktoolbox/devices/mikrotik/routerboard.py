# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 04.12.2023

  Purpose: MikroTik RouterOS main class.
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

from jsktoolbox.devices.mikrotik.base import BRouterOS
from jsktoolbox.devices.network.connectors import IConnector, API, SSH

from jsktoolbox.devices.mikrotik.elements.interfaces import IElement

from jsktoolbox.devices.mikrotik.elements.system import System
from jsktoolbox.devices.mikrotik.elements.ip import Ip


class _Elements(object, metaclass=ReadOnlyClass):
    """"""

    SYSTEM = "system"
    IP = "ip"
    INTERFACE = "interface"


class RouterBoard(BRouterOS):
    """MikroTik RouterBoard class."""

    system = None

    def __init__(
        self,
        connector: IConnector,
        qlog: LoggerQueue = None,
        debug: bool = False,
        verbose: bool = False,
    ):
        """Constructor."""
        super().__init__(
            None,
            connector,
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.path = "/"

        # add elements
        self.elements[_Elements.IP] = Ip(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SYSTEM] = System(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )


# #[EOF]#######################################################################
