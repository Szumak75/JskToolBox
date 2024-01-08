# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.12.2023

  Purpose: RB '/mpls/'
"""

from typing import Dict, List, Optional, Union, Tuple, Any
from inspect import currentframe

from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
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

    ACCEPT_FILTER = "accept-filter"
    ADVERTISE_FILTER = "advertise-filter"
    FLOW = "flow"
    FORWARDING_TABLE = "forwarding-table"
    INTERFACE = "interface"
    LDP = "ldp"
    LOCAL_MAPPING = "local-mapping"
    NEIGHBOR = "neighbor"
    PATH = "path"
    REMOTE_MAPPING = "remote-mapping"
    ROOT = "mpls"
    SETTINGS = "settings"
    TRAFFIC_ENG = "traffic-eng"
    TUNNEL = "tunnel"


class RBMpls(BRouterOS):
    """MPLS class

    For command root: /mpls/
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
        elements = {
            _Elements.FORWARDING_TABLE: {},
            _Elements.INTERFACE: {},
            _Elements.LDP: {
                _Elements.ACCEPT_FILTER: {},
                _Elements.ADVERTISE_FILTER: {},
                _Elements.INTERFACE: {},
                _Elements.LOCAL_MAPPING: {},
                _Elements.NEIGHBOR: {},
                _Elements.REMOTE_MAPPING: {},
            },
            _Elements.SETTINGS: {},
            _Elements.TRAFFIC_ENG: {
                _Elements.FLOW: {},
                _Elements.INTERFACE: {},
                _Elements.PATH: {},
                _Elements.TUNNEL: {},
            },
        }
        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
