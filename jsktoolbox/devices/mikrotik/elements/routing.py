# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.12.2023

  Purpose: RB '/routing/'
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

    ADVERTISEMENTS: str = "advertisements"
    AGGREGATE: str = "aggregate"
    AREA: str = "area"
    AREA_BORDER_ROUTER: str = "area-border-router"
    AS_BORDER_ROUTER: str = "as-border-router"
    BFD: str = "bfd"
    BGP: str = "bgp"
    BSR: str = "bsr"
    CANDIDATE: str = "candidate"
    CHAIN: str = "chain"
    COMMUNITY_EXT_LIST: str = "community-ext-list"
    COMMUNITY_LARGE_LIST: str = "community-large-list"
    COMMUNITY_LIST: str = "community-list"
    CONFIGURATION: str = "configuration"
    CONNECTION: str = "connection"
    FANTASY: str = "fantasy"
    FILTER: str = "filter"
    GMP: str = "gmp"
    ID: str = "id"
    IGMP_INTERFACE_TEMPLATE: str = "igmp-interface-template"
    IGMP_PROXY: str = "igmp-proxy"
    INSTANCE: str = "instance"
    INTERFACE: str = "interface"
    INTERFACE_TEMPLATE: str = "interface-template"
    KEYS: str = "keys"
    LSA: str = "lsa"
    MEMORY: str = "memory"
    MFC: str = "mfc"
    MME: str = "mme"
    NBMA_NEIGHBOR: str = "nbma-neighbor"
    NEIGHBOR: str = "neighbor"
    NETWORK: str = "network"
    NEXTHOP: str = "nexthop"
    NUM_LIST: str = "num-list"
    ORIGIN: str = "origin"
    ORIGINATORS: str = "originators"
    OSPF: str = "ospf"
    PCAP: str = "pcap"
    PEER: str = "peer"
    PIMSM: str = "pimsm"
    PREFIX_LIST: str = "prefix-lists"
    PROCESS: str = "process"
    RANGE: str = "range"
    RIP: str = "rip"
    ROOT: str = "routing"
    ROUTE: str = "route"
    RPKI: str = "rpki"
    RP_CANDIDATE: str = "rp-candidate"
    RP_SET: str = "rp-set"
    RULE: str = "rule"
    SELECT_RULE: str = "select-rule"
    SESSION: str = "session"
    SHAM_LINK: str = "sham-link"
    STATIC_NEIGHBOR: str = "static-neighbor"
    STATIC_RP: str = "static-rp"
    STATS: str = "stats"
    STEP: str = "step"
    TABLE: str = "table"
    TEMPLATE: str = "template"
    UIB_G: str = "uib-g"
    UIB_SG: str = "uib-sg"
    VIRTUAL_LINK: str = "virtual-link"
    VPLS: str = "vpls"
    VPN: str = "vpn"
    VPNV4_ROUTE: str = "vpnv4-route"
    VRF: str = "vrf"


class RBRouting(BRouterOS):
    """Routing class

    For command root: /routing/
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
            _Elements.BFD: {
                _Elements.INTERFACE: {},
                _Elements.NEIGHBOR: {},
                _Elements.CONFIGURATION: {},
                _Elements.SESSION: {},
            },
            _Elements.BGP: {
                _Elements.ADVERTISEMENTS: {},
                _Elements.AGGREGATE: {},
                _Elements.CONNECTION: {},
                _Elements.INSTANCE: {
                    _Elements.VRF: {},
                },
                _Elements.NETWORK: {},
                _Elements.PEER: {},
                _Elements.SESSION: {},
                _Elements.TEMPLATE: {},
                _Elements.VPLS: {},
                _Elements.VPN: {},
                _Elements.VPNV4_ROUTE: {},
            },
            _Elements.FANTASY: {},
            _Elements.FILTER: {
                _Elements.CHAIN: {},
                _Elements.COMMUNITY_EXT_LIST: {},
                _Elements.COMMUNITY_LARGE_LIST: {},
                _Elements.COMMUNITY_LIST: {},
                _Elements.NUM_LIST: {},
                _Elements.RULE: {},
                _Elements.SELECT_RULE: {},
            },
            _Elements.GMP: {},
            _Elements.ID: {},
            _Elements.IGMP_PROXY: {
                _Elements.INTERFACE: {},
                _Elements.MFC: {},
            },
            _Elements.NEXTHOP: {},
            _Elements.MME: {
                _Elements.INTERFACE: {},
                _Elements.NETWORK: {},
                _Elements.ORIGINATORS: {},
            },
            _Elements.OSPF: {
                _Elements.AREA: {
                    _Elements.RANGE: {},
                },
                _Elements.AREA_BORDER_ROUTER: {},
                _Elements.AS_BORDER_ROUTER: {},
                _Elements.INSTANCE: {},
                _Elements.INTERFACE: {},
                _Elements.INTERFACE_TEMPLATE: {},
                _Elements.LSA: {},
                _Elements.NBMA_NEIGHBOR: {},
                _Elements.NEIGHBOR: {},
                _Elements.NETWORK: {},
                _Elements.ROUTE: {},
                _Elements.SHAM_LINK: {},
                _Elements.STATIC_NEIGHBOR: {},
                _Elements.VIRTUAL_LINK: {},
            },
            _Elements.PIMSM: {
                _Elements.BSR: {
                    _Elements.CANDIDATE: {},
                    _Elements.RP_CANDIDATE: {},
                    _Elements.RP_SET: {},
                },
                _Elements.IGMP_INTERFACE_TEMPLATE: {},
                _Elements.INSTANCE: {},
                _Elements.INTERFACE: {},
                _Elements.INTERFACE_TEMPLATE: {},
                _Elements.NEIGHBOR: {},
                _Elements.STATIC_RP: {},
                _Elements.UIB_G: {},
                _Elements.UIB_SG: {},
            },
            _Elements.PREFIX_LIST: {},
            _Elements.RIP: {
                _Elements.INSTANCE: {},
                _Elements.INTERFACE: {},
                _Elements.INTERFACE_TEMPLATE: {},
                _Elements.KEYS: {},
                _Elements.NEIGHBOR: {},
                _Elements.NETWORK: {},
                _Elements.ROUTE: {},
                _Elements.STATIC_NEIGHBOR: {},
            },
            _Elements.ROUTE: {
                _Elements.RULE: {},
            },
            _Elements.RPKI: {
                _Elements.SESSION: {},
            },
            _Elements.RULE: {},
            _Elements.STATS: {
                _Elements.MEMORY: {},
                _Elements.ORIGIN: {},
                _Elements.PCAP: {},
                _Elements.PROCESS: {},
                _Elements.STEP: {},
            },
            _Elements.TABLE: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
