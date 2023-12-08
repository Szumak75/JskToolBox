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
    """Keys definition class.

    For internal purpose only.
    """


class _Elements(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ROOT = "interface"
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
    PEERS = "peers"
    WIRELESS = "wireless"
    POE = "poe"
    SWITCH = "switch"
    PORT = "port"
    HOST = "host"
    PORT_ISOLATION = "port-isolation"
    RULE = "rule"
    CALEA = "calea"
    FILTER = "filter"
    MDB = "mdb"
    MSTI = "msti"
    NAT = "nat"
    PORT_CONTROLLER = "port-controller"
    PORT_EXTENDER = "port-extender"
    SETTINGS = "settings"
    MST_OVERRIDE = "mst-override"
    DEVICE = "device"
    APN = "apn"
    ESIM = "esim"
    ACCESS_LIST = "access-list"
    ALIGN = "align"
    CAP = "cap"
    CHANNELS = "channels"
    CONNECT_LIST = "connect-list"
    INFO = "info"
    INTERWORKING_PROFILES = "interworking-profiles"
    MANUAL_TX_POWER_TABLE = "manual-tx-power-table"
    NSTREME = "nstreme"
    NSTREME_DUAL = "nstreme-dual"
    REGISTRATION_TABLE = "registration-table"
    SECURITY_PROFILES = "security-profiles"
    SNIFFER = "sniffer"
    SNOOPER = "snooper"
    WDS = "wds"
    PACKET = "packet"
    W60G = "w60g"
    STATION = "station"
    BGP_VPLS = "bgp-vpls"
    CISCO_BGP_VPLS = "cisco-bgp-vpls"


class RBInterface(BRouterOS):
    """Interface class

    For command root: /interface/
    """

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
        self.root = f"{_Elements.ROOT}/"

        # add elements
        elements = {
            _Elements.BONDING: {},
            _Elements.BRIDGE: {
                _Elements.CALEA: {},
                _Elements.FILTER: {},
                _Elements.HOST: {},
                _Elements.MDB: {},
                _Elements.MSTI: {},
                _Elements.NAT: {},
                _Elements.PORT: {
                    _Elements.MST_OVERRIDE: {},
                },
                _Elements.PORT_CONTROLLER: {
                    _Elements.DEVICE: {},
                    _Elements.PORT: {
                        _Elements.POE: {},
                    },
                },
                _Elements.PORT_EXTENDER: {},
                _Elements.SETTINGS: {},
                _Elements.VLAN: {},
            },
            _Elements.EOIP: {},
            _Elements.ETHERNET: {
                _Elements.SWITCH: {
                    _Elements.HOST: {},
                    _Elements.PORT: {},
                    _Elements.PORT_ISOLATION: {},
                    _Elements.RULE: {},
                    _Elements.VLAN: {},
                },
                _Elements.POE: {},
            },
            _Elements.GRE: {},
            _Elements.IPIP: {},
            _Elements.LTE: {
                _Elements.APN: {},
                _Elements.ESIM: {},
                _Elements.SETTINGS: {},
            },
            _Elements.VLAN: {},
            _Elements.VPLS: {
                _Elements.BGP_VPLS: {},
                _Elements.CISCO_BGP_VPLS: {},
            },
            _Elements.WIREGUARD: {
                _Elements.PEERS: {},
            },
            _Elements.WIRELESS: {
                _Elements.ACCESS_LIST: {},
                _Elements.ALIGN: {},
                _Elements.CAP: {},
                _Elements.CHANNELS: {},
                _Elements.CONNECT_LIST: {},
                _Elements.INFO: {},
                _Elements.INTERWORKING_PROFILES: {},
                _Elements.MANUAL_TX_POWER_TABLE: {},
                _Elements.NSTREME: {},
                _Elements.NSTREME_DUAL: {},
                _Elements.REGISTRATION_TABLE: {},
                _Elements.SECURITY_PROFILES: {},
                _Elements.SNIFFER: {
                    _Elements.PACKET: {},
                },
                _Elements.SNOOPER: {},
                _Elements.WDS: {},
            },
            _Elements.W60G: {
                _Elements.STATION: {},
            },
        }
        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
