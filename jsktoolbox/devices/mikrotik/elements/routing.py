# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.12.2023

  Purpose: RB '/routing/'
"""


from typing import Dict, List, Optional, Union, Tuple, Any
from inspect import currentframe

from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue


from jsktoolbox.devices.mikrotik.base import BRouterOS, BDev, Element
from jsktoolbox.devices.network.connectors import IConnector


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """


class _Elements(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ADVERTISEMENTS = "advertisements"
    AGGREGATE = "aggregate"
    AREA = "area"
    AREA_BORDER_ROUTER = "area-border-router"
    AS_BORDER_ROUTER = "as-border-router"
    BFD = "bfd"
    BGP = "bgp"
    BSR = "bsr"
    CANDIDATE = "candidate"
    CHAIN = "chain"
    COMMUNITY_EXT_LIST = "community-ext-list"
    COMMUNITY_LARGE_LIST = "community-large-list"
    COMMUNITY_LIST = "community-list"
    CONFIGURATION = "configuration"
    CONNECTION = "connection"
    FANTASY = "fantasy"
    FILTER = "filter"
    GMP = "gmp"
    ID = "id"
    IGMP_INTERFACE_TEMPLATE = "igmp-interface-template"
    IGMP_PROXY = "igmp-proxy"
    INSTANCE = "instance"
    INTERFACE = "interface"
    INTERFACE_TEMPLATE = "interface-template"
    KEYS = "keys"
    LSA = "lsa"
    MEMORY = "memory"
    MFC = "mfc"
    MME = "mme"
    NBMA_NEIGHBOR = "nbma-neighbor"
    NEIGHBOR = "neighbor"
    NETWORK = "network"
    NEXTHOP = "nexthop"
    NUM_LIST = "num-list"
    ORIGIN = "origin"
    ORIGINATORS = "originators"
    OSPF = "ospf"
    PCAP = "pcap"
    PEER = "peer"
    PIMSM = "pimsm"
    PREFIX_LIST = "prefix-lists"
    PROCESS = "process"
    RANGE = "range"
    RIP = "rip"
    ROOT = "routing"
    ROUTE = "route"
    RPKI = "rpki"
    RP_CANDIDATE = "rp-candidate"
    RP_SET = "rp-set"
    RULE = "rule"
    SELECT_RULE = "select-rule"
    SESSION = "session"
    SHAM_LINK = "sham-link"
    STATIC_NEIGHBOR = "static-neighbor"
    STATIC_RP = "static-rp"
    STATS = "stats"
    STEP = "step"
    TABLE = "table"
    TEMPLATE = "template"
    UIB_G = "uib-g"
    UIB_SG = "uib-sg"
    VIRTUAL_LINK = "virtual-link"
    VPLS = "vpls"
    VPN = "vpn"
    VPNV4_ROUTE = "vpnv4-route"
    VRF = "vrf"


class RBRouting(BRouterOS):
    """Routing class

    For command root: /routing/
    """

    def __init__(
        self,
        parent: BDev,
        connector: IConnector,
        qlog: LoggerQueue = None,
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
        elements = {
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