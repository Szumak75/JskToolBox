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

from jsktoolbox.devices.mikrotik.base import BRouterOS, BDev

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


class Interface(BRouterOS):
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
        self.elements[_Elements.BONDING] = Bonding(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.BRIDGE] = Bridge(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.EOIP] = Eoip(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.ETHERNET] = Ethernet(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.GRE] = Gre(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.IPIP] = Ipip(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.LTE] = Lte(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.VLAN] = Vlan(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.VPLS] = Vpls(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.VRRP] = Vrrp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.WIREGUARD] = Wireguard(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.WIRELESS] = Wireless(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        self.load(self.path)


class Bonding(BRouterOS):
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
        self.path = f"{_Elements.BONDING}/"

        # add elements

        # load data
        self.load(self.path)


class Bridge(BRouterOS):
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
        self.path = f"{_Elements.BRIDGE}/"

        # add elements

        # load data
        self.load(self.path)


class Eoip(BRouterOS):
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
        self.path = f"{_Elements.EOIP}/"

        # add elements

        # load data
        self.load(self.path)


class Ethernet(BRouterOS):
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
        self.path = f"{_Elements.ETHERNET}/"

        # add elements

        # load data
        self.load(self.path)


class Gre(BRouterOS):
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
        self.path = f"{_Elements.GRE}/"

        # add elements

        # load data
        self.load(self.path)


class Ipip(BRouterOS):
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
        self.path = f"{_Elements.IPIP}/"

        # add elements

        # load data
        self.load(self.path)


class Lte(BRouterOS):
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
        self.path = f"{_Elements.LTE}/"

        # add elements

        # load data
        self.load(self.path)


class Vlan(BRouterOS):
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
        self.path = f"{_Elements.VLAN}/"

        # add elements

        # load data
        self.load(self.path)


class Vpls(BRouterOS):
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
        self.path = f"{_Elements.VPLS}/"

        # add elements

        # load data
        self.load(self.path)


class Vrrp(BRouterOS):
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
        self.path = f"{_Elements.VRRP}/"

        # add elements

        # load data
        self.load(self.path)


class Wireguard(BRouterOS):
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
        self.path = f"{_Elements.WIREGUARD}/"

        # add elements

        # load data
        self.load(self.path)


class Wireless(BRouterOS):
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
        self.path = f"{_Elements.WIRELESS}/"

        # add elements

        # load data
        self.load(self.path)


# #[EOF]#######################################################################
