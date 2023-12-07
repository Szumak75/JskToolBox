# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 06.12.2023

  Purpose:
"""


from typing import Dict, List, Optional, Union, Tuple, Any
from inspect import currentframe

from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue


# from jsktoolbox.netaddresstool.ipv4 import (
# Address,
# Netmask,
# Network,
# SubNetwork,
# )
# from jsktoolbox.netaddresstool.ipv6 import (
# Address6,
# Network6,
# Prefix6,
# SubNetwork6,
# )

from jsktoolbox.devices.mikrotik.base import BRouterOS, BDev, Element

from jsktoolbox.devices.network.connectors import IConnector, API, SSH


class _Keys(object, metaclass=ReadOnlyClass):
    """"""


class _Elements(object, metaclass=ReadOnlyClass):
    """"""

    INTERFACE = "interface"
    BONDING = "bonding"
    BRIDGE = "bridge"
    EOIP = "eoip"
    ETHERNET = "ethernet"
    GRE = "gre"
    IPIP = "ipip"
    LTE = "lte"
    VLAN = "vlan"
    VPLS = "vpls"
    VRRP = "vrrp"
    WIREGUARD = "wireguard"
    WIRELESS = "wireless"


class RBInterface(BRouterOS):
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
        self.path = f"{_Elements.INTERFACE}/"

        # add elements
        elements = [
            _Elements.BONDING,
            _Elements.BRIDGE,
            _Elements.EOIP,
            _Elements.ETHERNET,
            _Elements.GRE,
            _Elements.IPIP,
            _Elements.LTE,
            _Elements.VLAN,
            _Elements.VPLS,
            _Elements.WIREGUARD,
            _Elements.WIRELESS,
        ]
        for element in elements:
            self._add_element(
                key=element,
                btype=Element,
                parent=self,
                connector=self._ch,
                qlog=self.logs.logs_queue,
                debug=self.debug,
                verbose=self.verbose,
            )


# #[EOF]#######################################################################
