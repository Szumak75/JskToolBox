# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 06.12.2023

  Purpose:
"""


from typing import Dict, Optional, Any

from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue

from jsktoolbox.devices.mikrotik.base import BRouterOS, BDev

from jsktoolbox.devices.network.connectors import IConnector


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """


class _Elements(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ACCESS_LIST: str = "access-list"
    ALIGN: str = "align"
    APN: str = "apn"
    BGP_VPLS: str = "bgp-vpls"
    BONDING: str = "bonding"
    BRIDGE: str = "bridge"
    CALEA: str = "calea"
    CAP: str = "cap"
    CHANNELS: str = "channels"
    CISCO_BGP_VPLS: str = "cisco-bgp-vpls"
    CONNECT_LIST: str = "connect-list"
    DEVICE: str = "device"
    EOIP: str = "eoip"
    ESIM: str = "esim"
    ETHERNET: str = "ethernet"
    FILTER: str = "filter"
    GRE: str = "gre"
    HOST: str = "host"
    INFO: str = "info"
    INTERWORKING_PROFILES: str = "interworking-profiles"
    IPIP: str = "ipip"
    LTE: str = "lte"
    MANUAL_TX_POWER_TABLE: str = "manual-tx-power-table"
    MDB: str = "mdb"
    MSTI: str = "msti"
    MST_OVERRIDE: str = "mst-override"
    NAT: str = "nat"
    NSTREME: str = "nstreme"
    NSTREME_DUAL: str = "nstreme-dual"
    PACKET: str = "packet"
    PEERS: str = "peers"
    POE: str = "poe"
    PORT: str = "port"
    PORT_CONTROLLER: str = "port-controller"
    PORT_EXTENDER: str = "port-extender"
    PORT_ISOLATION: str = "port-isolation"
    REGISTRATION_TABLE: str = "registration-table"
    ROOT: str = "interface"
    RULE: str = "rule"
    SECURITY_PROFILES: str = "security-profiles"
    SETTINGS: str = "settings"
    SNIFFER: str = "sniffer"
    SNOOPER: str = "snooper"
    STATION: str = "station"
    SWITCH: str = "switch"
    VLAN: str = "vlan"
    VPLS: str = "vpls"
    VRRP: str = "vrrp"
    W60G: str = "w60g"
    WDS: str = "wds"
    WIREGUARD: str = "wireguard"
    WIRELESS: str = "wireless"


class RBInterface(BRouterOS):
    """Interface class

    For command root: /interface/
    """

    def __init__(
        self,
        parent: BDev,
        connector: IConnector,
        qlog: Optional[LoggerQueue] = None,
        debug: bool = False,
        verbose: bool = False,
    ) -> None:
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
        elements: Dict[str, Any] = {
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
