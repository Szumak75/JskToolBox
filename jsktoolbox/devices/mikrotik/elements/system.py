# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 04.12.2023

  Purpose: RB '/system'
"""

from typing import Dict, List, Optional, Union, Tuple, Any
from inspect import currentframe

from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue


from jsktoolbox.netaddresstool.ipv4 import (
    Address,
    Netmask,
    Network,
    SubNetwork,
)
from jsktoolbox.netaddresstool.ipv6 import (
    Address6,
    Network6,
    Prefix6,
    SubNetwork6,
)

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

    ROOT = "system"
    IDENTITY = "identity"
    RESOURCE = "resource"
    ROUTERBOARD = "routerboard"
    CLOCK = "clock"
    DEVICE_MODE = "device-mode"
    HEALTH = "health"
    HISTORY = "history"
    LEDS = "leds"
    LICENSE = "license"
    LOGGING = "logging"
    NOTE = "note"
    NTP = "ntp"
    PACKAGE = "package"
    UPDATE = "update"
    SCHEDULER = "scheduler"
    SCRIPT = "script"
    UPGRADE = "upgrade"
    WATCHDOG = "watchdog"
    # resource
    CPU = "cpu"
    IRQ = "irq"
    PCI = "pci"
    USB = "usb"
    # routerboard
    SETTINGS = "settings"
    # clock
    MANUAL = "manual"
    # logging
    ACTION = "action"
    # ntp
    CLIENT = "client"
    KEY = "key"
    SERVER = "server"
    SERVERS = "servers"
    # script
    ENVIRONMENT = "environment"
    JOB = "job"


class RBSystem(BRouterOS):
    """System class

    For command root: /system/
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
            _Elements.CLOCK: {
                _Elements.MANUAL: {},
            },
            _Elements.DEVICE_MODE: {},
            _Elements.HEALTH: {
                _Elements.SETTINGS: {},
            },
            _Elements.HISTORY: {},
            _Elements.IDENTITY: {},
            _Elements.LEDS: {
                _Elements.SETTINGS: {},
            },
            _Elements.LICENSE: {},
            _Elements.LOGGING: {
                _Elements.ACTION: {},
            },
            _Elements.NOTE: {},
            _Elements.NTP: {
                _Elements.CLIENT: {
                    _Elements.SERVERS: {},
                },
                _Elements.KEY: {},
                _Elements.SERVER: {},
            },
            _Elements.PACKAGE: {
                _Elements.UPDATE: {},
            },
            _Elements.RESOURCE: {
                _Elements.CPU: {},
                _Elements.IRQ: {},
                _Elements.PCI: {},
                _Elements.USB: {
                    _Elements.SETTINGS: {},
                },
            },
            _Elements.ROUTERBOARD: {
                _Elements.SETTINGS: {},
            },
            _Elements.SCHEDULER: {},
            _Elements.SCRIPT: {
                _Elements.ENVIRONMENT: {},
                _Elements.JOB: {},
            },
            _Elements.UPGRADE: {},
            _Elements.WATCHDOG: {},
        }
        self._add_elements(self, elements)


# #[EOF]#######################################################################
