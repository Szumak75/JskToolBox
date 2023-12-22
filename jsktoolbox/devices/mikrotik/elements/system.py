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

    ACTION = "action"
    BACKUP = "backup"
    CLIENT = "client"
    CLOCK = "clock"
    CLOUD = "cloud"
    CONSOLE = "console"
    CPU = "cpu"
    DEVICE_MODE = "device-mode"
    ENVIRONMENT = "environment"
    GAUGES = "gauges"
    HEALTH = "health"
    HISTORY = "history"
    IDENTITY = "identity"
    IRQ = "irq"
    JOB = "job"
    KEY = "key"
    LEDS = "leds"
    LICENSE = "license"
    LOGGING = "logging"
    MANUAL = "manual"
    NOTE = "note"
    NTP = "ntp"
    PACKAGE = "package"
    PCI = "pci"
    RESOURCE = "resource"
    ROOT = "system"
    ROUTERBOARD = "routerboard"
    SCHEDULER = "scheduler"
    SCRIPT = "script"
    SERVER = "server"
    SERVERS = "servers"
    SETTINGS = "settings"
    UPDATE = "update"
    UPGRADE = "upgrade"
    USB = "usb"
    WATCHDOG = "watchdog"


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
            _Elements.BACKUP: {
                _Elements.CLOUD: {},
            },
            _Elements.CLOCK: {
                _Elements.MANUAL: {},
            },
            _Elements.CONSOLE: {},
            _Elements.DEVICE_MODE: {},
            _Elements.HEALTH: {
                _Elements.SETTINGS: {},
                _Elements.GAUGES: {},
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
