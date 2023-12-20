# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 06.12.2023

  Purpose: RB '/ip'
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

    ACCESS = "access"
    ACCOUNTING = "accounting"
    ACTIVE = "active"
    ACTIVE_PEERS = "active-peers"
    ADDRESS = "address"
    ADDRESS_LIST = "address-list"
    ADVANCED = "advanced"
    ALERT = "alert"
    ALL = "all"
    ARP = "arp"
    CACHE = "cache"
    CACHE_CONTENTS = "cache-contents"
    CALEA = "calea"
    CLOUD = "cloud"
    CONFIG = "config"
    CONNECTION = "connection"
    CONNECTIONS = "connections"
    COOKIE = "cookie"
    DEVICE = "device"
    DHCP_CLIENT = "dhcp-client"
    DHCP_RELAY = "dhcp-relay"
    DHCP_SERVER = "dhcp-server"
    DIRECT = "direct"
    DISCOVERY_SETTINGS = "discovery-settings"
    DNS = "dns"
    FILTER = "filter"
    FIREWALL = "firewall"
    GROUP = "group"
    HOST = "host"
    HOTSPOT = "hotspot"
    IDENTITY = "identity"
    INSERTS = "inserts"
    INSTALLED_SA = "installed-sa"
    INTERFACES = "interfaces"
    IP = "ip"
    IPFIX = "ipfix"
    IPSEC = "ipsec"
    IP_BINDING = "ip-binding"
    KEY = "key"
    KID_CONTROL = "kid-control"
    LAYER7_PROTOCOL = "layer7-protocol"
    LEASE = "lease"
    LOOKUPS = "lookups"
    MANGLE = "mangle"
    MATCHER = "matcher"
    MODE_CONFIG = "mode-config"
    NAT = "nat"
    NEIGHBOR = "neighbor"
    NETWORK = "network"
    NEXTHOP = "nexthop"
    OPTION = "option"
    PACKING = "packing"
    PEER = "peer"
    POLICY = "policy"
    POOL = "pool"
    PROFILE = "profile"
    PROPOSAL = "proposal"
    PROXY = "proxy"
    RAW = "raw"
    REFRESHES = "refreshes"
    ROOT = "ip"
    ROUTE = "route"
    RULE = "rule"
    SERVICE = "service"
    SERVICE_PORT = "service-port"
    SETS = "sets"
    SETTINGS = "settings"
    SHARES = "shares"
    SMB = "smb"
    SNAPSHOT = "snapshot"
    SOCKS = "socks"
    SSH = "ssh"
    STATIC = "static"
    STATISTICS = "statistics"
    TARGET = "target"
    TFTP = "tftp"
    TRACKING = "tracking"
    TRAFFIC_FLOW = "traffic-flow"
    UNCOUNTED = "uncounted"
    UPNP = "upnp"
    USED = "used"
    USER = "user"
    USERS = "users"
    VRF = "vrf"
    WALLED_GARDEN = "walled-garden"
    WEB_ACCESS = "web-access"


class RBIp(BRouterOS):
    """Ip class

    For command root: /ip/
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
            _Elements.ACCOUNTING: {
                _Elements.SNAPSHOT: {},
                _Elements.UNCOUNTED: {},
                _Elements.WEB_ACCESS: {},
            },
            _Elements.ADDRESS: {},
            _Elements.ARP: {},
            _Elements.CLOUD: {
                _Elements.ADVANCED: {},
            },
            _Elements.DHCP_CLIENT: {
                _Elements.OPTION: {},
            },
            _Elements.DHCP_RELAY: {},
            _Elements.DHCP_SERVER: {
                _Elements.ALERT: {},
                _Elements.CONFIG: {},
                _Elements.LEASE: {},
                _Elements.MATCHER: {},
                _Elements.NETWORK: {},
                _Elements.OPTION: {
                    _Elements.SETS: {},
                },
            },
            _Elements.DNS: {
                _Elements.CACHE: {
                    _Elements.ALL: {},
                },
                _Elements.STATIC: {},
            },
            _Elements.FIREWALL: {
                _Elements.ADDRESS_LIST: {},
                _Elements.CALEA: {},
                _Elements.CONNECTION: {
                    _Elements.TRACKING: {},
                },
                _Elements.FILTER: {},
                _Elements.LAYER7_PROTOCOL: {},
                _Elements.MANGLE: {},
                _Elements.NAT: {},
                _Elements.RAW: {},
                _Elements.SERVICE_PORT: {},
            },
            _Elements.HOTSPOT: {
                _Elements.ACTIVE: {},
                _Elements.COOKIE: {},
                _Elements.HOST: {},
                _Elements.IP_BINDING: {},
                _Elements.PROFILE: {},
                _Elements.SERVICE_PORT: {},
                _Elements.USER: {
                    _Elements.PROFILE: {},
                },
                _Elements.WALLED_GARDEN: {
                    _Elements.IP: {},
                },
            },
            _Elements.IPSEC: {
                _Elements.ACTIVE_PEERS: {},
                _Elements.IDENTITY: {},
                _Elements.INSTALLED_SA: {},
                _Elements.KEY: {},
                _Elements.MODE_CONFIG: {},
                _Elements.PEER: {},
                _Elements.POLICY: {
                    _Elements.GROUP: {},
                },
                _Elements.PROFILE: {},
                _Elements.PROPOSAL: {},
                _Elements.SETTINGS: {},
                _Elements.STATISTICS: {},
            },
            _Elements.KID_CONTROL: {
                _Elements.DEVICE: {},
            },
            _Elements.NEIGHBOR: {
                _Elements.DISCOVERY_SETTINGS: {},
            },
            _Elements.PACKING: {},
            _Elements.POOL: {
                _Elements.USED: {},
            },
            _Elements.PROXY: {
                _Elements.ACCESS: {},
                _Elements.CACHE: {},
                _Elements.CACHE_CONTENTS: {},
                _Elements.CONNECTIONS: {},
                _Elements.DIRECT: {},
                _Elements.INSERTS: {},
                _Elements.LOOKUPS: {},
                _Elements.REFRESHES: {},
            },
            _Elements.ROUTE: {
                _Elements.CACHE: {},
                _Elements.NEXTHOP: {},
                _Elements.RULE: {},
                _Elements.VRF: {},
            },
            _Elements.SERVICE: {},
            _Elements.SETTINGS: {},
            _Elements.SMB: {
                _Elements.SHARES: {},
                _Elements.USERS: {},
            },
            _Elements.SOCKS: {
                _Elements.ACCESS: {},
                _Elements.CONNECTIONS: {},
                _Elements.USERS: {},
            },
            _Elements.SSH: {},
            _Elements.TFTP: {
                _Elements.SETTINGS: {},
            },
            _Elements.TRAFFIC_FLOW: {
                _Elements.IPFIX: {},
                _Elements.TARGET: {},
            },
            _Elements.UPNP: {
                _Elements.INTERFACES: {},
            },
            _Elements.VRF: {},
        }
        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
