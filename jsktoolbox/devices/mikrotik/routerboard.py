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

from jsktoolbox.devices.mikrotik.base import BRouterOS, Element

from jsktoolbox.devices.network.connectors import IConnector

from jsktoolbox.devices.mikrotik.elements.libs.interfaces import IElement

from jsktoolbox.devices.mikrotik.elements.system import RBSystem
from jsktoolbox.devices.mikrotik.elements.ip import RBIp
from jsktoolbox.devices.mikrotik.elements.interface import RBInterface
from jsktoolbox.devices.mikrotik.elements.mpls import RBMpls
from jsktoolbox.devices.mikrotik.elements.radius import RBRadius
from jsktoolbox.devices.mikrotik.elements.routing import RBRouting


class _Elements(object, metaclass=ReadOnlyClass):
    """"""

    INTERFACE = "interface"
    IP = "ip"
    MPLS = "mpls"
    RADIUS = "radius"
    ROUTING = "routing"
    SYSTEM = "system"


class RouterBoard(BRouterOS):
    """MikroTik RouterBoard class."""

    system = None

    def __init__(
        self,
        connector: IConnector,
        qlog: Optional[LoggerQueue] = None,
        debug: bool = False,
        verbose: bool = False,
    ) -> None:
        """Constructor."""
        super().__init__(
            None,
            connector,
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.root = "/"

        # add elements
        if self._ch is None:
            return None
        self.elements[_Elements.IP] = RBIp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SYSTEM] = RBSystem(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.INTERFACE] = RBInterface(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.MPLS] = RBMpls(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.RADIUS] = RBRadius(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.ROUTING] = RBRouting(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )


# #[EOF]#######################################################################
