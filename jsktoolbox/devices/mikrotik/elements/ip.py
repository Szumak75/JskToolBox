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

from jsktoolbox.devices.mikrotik.base import BRouterOS, BDev

from jsktoolbox.devices.network.connectors import IConnector, API, SSH


class _Keys(object, metaclass=ReadOnlyClass):
    """"""


class _Elements(object, metaclass=ReadOnlyClass):
    """"""

    IP = "ip"
    ADDRESS = "address"


class Ip(BRouterOS):
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
        self.elements[_Elements.ADDRESS] = Address(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )


class Address(BRouterOS):
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
        self.path = f"{_Elements.ADDRESS}/"

        # add elements

        # load data
        self.load(self.path)


# #[EOF]#######################################################################
