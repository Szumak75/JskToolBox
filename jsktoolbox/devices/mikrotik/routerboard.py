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

from jsktoolbox.devices.mikrotik import elements


class _Elements(object, metaclass=ReadOnlyClass):
    """Internal keys class."""

    CERTIFICATE: str = "certificate"
    DISK: str = "disk"
    FILE: str = "file"
    INTERFACE: str = "interface"
    IP: str = "ip"
    IPV6: str = "ipv6"
    LCD: str = "lcd"
    LOG: str = "log"
    MPLS: str = "mpls"
    PARTITIONS: str = "partitions"
    PORT: str = "port"
    PPP: str = "ppp"
    QUEUE: str = "queue"
    RADIUS: str = "radius"
    ROUTING: str = "routing"
    SNMP: str = "snmp"
    SYSTEM: str = "system"
    TOOL: str = "tool"
    USER: str = "user"


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
        self.elements[_Elements.CERTIFICATE] = elements.RBCertificate(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.DISK] = elements.RBDisk(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.FILE] = elements.RBFile(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.INTERFACE] = elements.RBInterface(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.IP] = elements.RBIp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.IPV6] = elements.RBIpv6(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.LCD] = elements.RBLcd(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.LOG] = elements.RBLog(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.MPLS] = elements.RBMpls(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.PARTITIONS] = elements.RBPartitions(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.PORT] = elements.RBPort(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.PPP] = elements.RBPpp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.QUEUE] = elements.RBQueue(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.RADIUS] = elements.RBRadius(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.ROUTING] = elements.RBRouting(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SNMP] = elements.RBSnmp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SYSTEM] = elements.RBSystem(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.TOOL] = elements.RBTool(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.USER] = elements.RBUser(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )


# #[EOF]#######################################################################
