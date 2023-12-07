# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 06.12.2023

  Purpose: RB '/ip'
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

    IP = "ip"
    ADDRESS = "address"
    ARP = "arp"
    CLOUD = "cloud"
    DHCP_CLIENT = "dhcp-client"
    DHCP_RELAY = "dhcp-relay"
    DHCP_SERVER = "dhcp-server"
    DNS = "dns"
    FIREWALL = "firewall"
    HOTSPOT = "hotspot"
    IPSEC = "ipsec"
    KID_CONTROL = "kid-control"
    NEIGHBOR = "neighbor"
    PACKING = "packing"
    POOL = "pool"
    PROXY = "proxy"
    ROUTE = "route"
    SERVICE = "service"
    SETTINGS = "settings"
    SMB = "smb"
    SOCKS = "socks"
    SSH = "ssh"
    TFTP = "tftp"
    TRAFFIC_FLOW = "traffic-flow"
    UPNP = "upnp"
    VRF = "vrf"
    # cloud
    ADVANCED = "advanced"
    # dhcp-client
    OPTION = "option"
    # dhcp-server
    ALERT = "alert"
    CONFIG = "config"
    LEASE = "lease"
    MATCHER = "matcher"
    NETWORK = "network"
    # OPTION
    SETS = "sets"
    # dns
    CACHE = "cache"
    ALL = "all"
    STATIC = "static"
    # firewall
    ADDRESS_LIST = "address-list"
    CALEA = "calea"
    CONNECTION = "connection"
    TRACKING = "tracking"
    FILTER = "filter"
    LAYER7_PROTOCOL = "layer7-protocol"
    MANGLE = "mangle"
    NAT = "nat"
    RAW = "raw"
    SERVICE_PORT = "service-port"
    # hotspot
    ACTIVE = "active"
    COOKIE = "cookie"
    HOST = "host"
    IP_BINDING = "ip-binding"
    PROFILE = "profile"
    # SERVICE_PORT
    USER = "user"
    # PROFILE
    WALLED_GARDEN = "walled-garden"
    # IP
    # ipsec
    ACTIVE_PEERS = "active-peers"
    IDENTITY = "identity"
    INSTALLED_SA = "installed-sa"
    KEY = "key"
    MODE_CONFIG = "mode-config"
    PEER = "peer"
    POLICY = "policy"
    # policy
    GROUP = "group"
    # >'profile'
    PROPOSAL = "proposal"
    # >'settings'
    STATISTICS = "statistics"
    # kid-control
    DEVICE = "device"
    # NEIGHBOR
    DISCOVERY_SETTINGS = "discovery-settings"
    # POOL
    USED = "used"
    # PROXY
    ACCESS = "access"
    # > CACHE
    CACHE_CONTENTS = "cache-contents"
    CONNECTIONS = "connections"
    DIRECT = "direct"
    INSERTS = "inserts"
    LOOKUPS = "lookups"
    REFRESHES = "refreshes"
    # SMB
    SHARES = "shares"
    USERS = "users"
    # TRAFFIC_FLOW
    IPFIX = "ipfix"
    TARGET = "target"
    # UPNP
    INTERFACES = "interfaces"


class RBIp(BRouterOS):
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
        self.path = f"{_Elements.IP}/"

        # add elements
        if parent.path == "/":
            elements = [
                _Elements.ADDRESS,
                _Elements.ARP,
                _Elements.CLOUD,
                _Elements.DHCP_CLIENT,
                _Elements.DHCP_RELAY,
                _Elements.DHCP_SERVER,
                _Elements.DNS,
                _Elements.FIREWALL,
                _Elements.HOTSPOT,
                _Elements.IPSEC,
                _Elements.KID_CONTROL,
                _Elements.NEIGHBOR,
                _Elements.PACKING,
                _Elements.POOL,
                _Elements.PROXY,
                _Elements.ROUTE,
                _Elements.SERVICE,
                _Elements.SETTINGS,
                _Elements.SMB,
                _Elements.SOCKS,
                _Elements.SSH,
                _Elements.TFTP,
                _Elements.TRAFFIC_FLOW,
                _Elements.UPNP,
                _Elements.VRF,
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
        # subelements
        elements = {
            _Elements.CLOUD: [_Elements.ADVANCED],
            _Elements.DHCP_CLIENT: [_Elements.OPTION],
            _Elements.DHCP_SERVER: [
                _Elements.ALERT,
                _Elements.CONFIG,
                _Elements.LEASE,
                _Elements.MATCHER,
                _Elements.NETWORK,
                _Elements.OPTION,
            ],
            f"{_Elements.DHCP_SERVER}/{_Elements.OPTION}": [_Elements.SETS],
            _Elements.DNS: [_Elements.CACHE, _Elements.STATIC],
            f"{_Elements.DNS}/{_Elements.CACHE}": [_Elements.ALL],
            _Elements.FIREWALL: [
                _Elements.ADDRESS_LIST,
                _Elements.CALEA,
                _Elements.CONNECTION,
                _Elements.FILTER,
                _Elements.LAYER7_PROTOCOL,
                _Elements.MANGLE,
                _Elements.NAT,
                _Elements.RAW,
                _Elements.SERVICE_PORT,
            ],
            f"{_Elements.FIREWALL}/{_Elements.CONNECTION}": [
                _Elements.TRACKING
            ],
            _Elements.HOTSPOT: [
                _Elements.ACTIVE,
                _Elements.COOKIE,
                _Elements.HOST,
                _Elements.IP_BINDING,
                _Elements.PROFILE,
                _Elements.SERVICE_PORT,
                _Elements.USER,
                _Elements.WALLED_GARDEN,
            ],
            f"{_Elements.HOTSPOT}/{_Elements.USER}": [_Elements.PROFILE],
            f"{_Elements.HOTSPOT}/{_Elements.WALLED_GARDEN}": [_Elements.IP],
            _Elements.IPSEC: [
                _Elements.ACTIVE_PEERS,
                _Elements.IDENTITY,
                _Elements.INSTALLED_SA,
                _Elements.KEY,
                _Elements.MODE_CONFIG,
                _Elements.PEER,
                _Elements.POLICY,
                _Elements.PROFILE,
                _Elements.PROPOSAL,
                _Elements.SETTINGS,
                _Elements.STATISTICS,
            ],
            f"{_Elements.IPSEC}/{_Elements.POLICY}": [_Elements.GROUP],
            _Elements.KID_CONTROL: [_Elements.DEVICE],
            _Elements.NEIGHBOR: [_Elements.DISCOVERY_SETTINGS],
            _Elements.POOL: [_Elements.USED],
            _Elements.PROXY: [
                _Elements.ACCESS,
                _Elements.CACHE,
                _Elements.CACHE_CONTENTS,
                _Elements.CONNECTIONS,
                _Elements.DIRECT,
                _Elements.INSERTS,
                _Elements.LOOKUPS,
                _Elements.REFRESHES,
            ],
            _Elements.SMB: [_Elements.SHARES, _Elements.USERS],
            _Elements.SOCKS: [
                _Elements.ACCESS,
                _Elements.CONNECTIONS,
                _Elements.USERS,
            ],
            _Elements.TFTP: [_Elements.SETTINGS],
            _Elements.TRAFFIC_FLOW: [_Elements.IPFIX, _Elements.TARGET],
            _Elements.UPNP: [_Elements.INTERFACES],
        }
        for key in sorted(elements.keys()):
            # print(key)
            obj: Element = self.element(f"{self.path}{key}")
            if obj:
                for key2 in elements[key]:
                    obj._add_element(
                        key=key2,
                        btype=Element,
                        parent=obj,
                        connector=self._ch,
                        qlog=self.logs.logs_queue,
                        debug=self.debug,
                        verbose=self.verbose,
                    )


# #[EOF]#######################################################################
