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

from jsktoolbox.devices.mikrotik.base import BRouterOS, BDev

from jsktoolbox.devices.network.connectors import IConnector, API, SSH


class _Keys(object, metaclass=ReadOnlyClass):
    """"""


class _Elements(object, metaclass=ReadOnlyClass):
    """"""

    IDENTITY = "identity"
    RESOURCE = "resource"
    ROUTERBOARD = "routerboard"
    CLOCK = "clock"
    HEALTH = "health"
    LICENSE = "license"
    LOGGING = "logging"
    NTP = "ntp"
    SCHEDULER = "scheduler"
    SCRIPT = "script"
    SYSTEM = "system"
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
    # script
    ENVIRONMENT = "environment"
    JOB = "job"


class System(BRouterOS):
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
        self.path = f"{_Elements.SYSTEM}/"

        # add elements
        self.elements[_Elements.IDENTITY] = Identity(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.RESOURCE] = Resource(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.ROUTERBOARD] = RouterBoard(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.CLOCK] = Clock(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.HEALTH] = Health(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.LICENSE] = License(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.LOGGING] = Logging(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.NTP] = Ntp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SCHEDULER] = Scheduler(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SCRIPT] = Script(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.UPGRADE] = Upgrade(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.WATCHDOG] = Watchdog(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )


class Identity(BRouterOS):
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
        self.path = f"{_Elements.IDENTITY}/"

        # add elements

        # load data
        self.load(self.path)


class Resource(BRouterOS):
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
        self.path = f"{_Elements.RESOURCE}/"

        # add elements
        self.elements[_Elements.CPU] = Cpu(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.IRQ] = Irq(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.PCI] = Pci(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.USB] = Usb(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        self.load(self.path)


class RouterBoard(BRouterOS):
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
        self.path = f"{_Elements.ROUTERBOARD}/"

        # add elements
        self.elements[_Elements.SETTINGS] = Settings(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        self.load(self.path)


class Clock(BRouterOS):
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
        self.path = f"{_Elements.CLOCK}/"

        # add elements
        self.elements[_Elements.MANUAL] = Manual(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        self.load(self.path)


class Health(BRouterOS):
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
        self.path = f"{_Elements.HEALTH}/"

        # add elements
        self.elements[_Elements.SETTINGS] = Settings(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        self.load(self.path)


class License(BRouterOS):
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
        self.path = f"{_Elements.LICENSE}/"

        # add elements

        # load data
        self.load(self.path)


class Logging(BRouterOS):
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
        self.path = f"{_Elements.LOGGING}/"

        # add elements
        self.elements[_Elements.ACTION] = Action(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        self.load(self.path)


class Ntp(BRouterOS):
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
        self.path = f"{_Elements.NTP}/"

        # add elements
        self.elements[_Elements.CLIENT] = Client(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.KEY] = Key(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SERVER] = Server(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        self.load(self.path)


class Scheduler(BRouterOS):
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
        self.path = f"{_Elements.SCHEDULER}/"

        # add elements

        # load data
        self.load(self.path)


class Script(BRouterOS):
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
        self.path = f"{_Elements.SCRIPT}/"

        # add elements
        self.elements[_Elements.ENVIRONMENT] = Environment(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.JOB] = Job(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue,
            debug=self.debug,
            verbose=self.verbose,
        )

        # load data
        self.load(self.path)


class Upgrade(BRouterOS):
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
        self.path = f"{_Elements.UPGRADE}/"

        # add elements

        # load data
        self.load(self.path)


class Watchdog(BRouterOS):
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
        self.path = f"{_Elements.WATCHDOG}/"

        # add elements

        # load data
        self.load(self.path)


class Cpu(BRouterOS):
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
        self.path = f"{_Elements.CPU}/"

        # add elements

        # load data
        self.load(self.path)


class Irq(BRouterOS):
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
        self.path = f"{_Elements.IRQ}/"

        # add elements

        # load data
        self.load(self.path)


class Pci(BRouterOS):
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
        self.path = f"{_Elements.PCI}/"

        # add elements

        # load data
        self.load(self.path)


class Usb(BRouterOS):
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
        self.path = f"{_Elements.USB}/"

        # add elements

        # load data
        self.load(self.path)


class Settings(BRouterOS):
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
        self.path = f"{_Elements.SETTINGS}/"

        # add elements

        # load data
        self.load(self.path)


class Manual(BRouterOS):
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
        self.path = f"{_Elements.MANUAL}/"

        # add elements

        # load data
        self.load(self.path)


class Action(BRouterOS):
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
        self.path = f"{_Elements.ACTION}/"

        # add elements

        # load data
        self.load(self.path)


class Client(BRouterOS):
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
        self.path = f"{_Elements.CLIENT}/"

        # add elements

        # load data
        self.load(self.path)


class Key(BRouterOS):
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
        self.path = f"{_Elements.KEY}/"

        # add elements

        # load data
        self.load(self.path)


class Server(BRouterOS):
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
        self.path = f"{_Elements.SERVER}/"

        # add elements

        # load data
        self.load(self.path)


class Environment(BRouterOS):
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
        self.path = f"{_Elements.ENVIRONMENT}/"

        # add elements

        # load data
        self.load(self.path)


class Job(BRouterOS):
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
        self.path = f"{_Elements.JOB}/"

        # add elements

        # load data
        self.load(self.path)


# #[EOF]#######################################################################
