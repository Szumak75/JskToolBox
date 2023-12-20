# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.12.2023

  Purpose: RB '/radius/'
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

    INCOMING = "incoming"
    ROOT = "radius"


class RBRadius(BRouterOS):
    """Radius class

    For command root: /radius/
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
            _Elements.INCOMING: {},
        }
        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
