#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 03.11.2023

  Purpose: test logs engine
"""

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.logstool.logs import (
    LoggerEngine,
    LoggerClient,
    LogsLevelKeys,
    LoggerEngineFile,
    LoggerEngineStderr,
    LoggerEngineStdout,
    LoggerEngineSyslog,
    LoggerQueue,
    MLoggerQueue,
)
from jsktoolbox.logstool.formatters import (
    LogFormatterDateTime,
    LogFormatterNull,
    LogFormatterTime,
    LogFormatterTimestamp,
)


class A(MLoggerQueue, NoDynamicAttributes):
    """"""

    __le = None

    def __init__(self):
        """Constructor."""
        name = self.__class__.__name__
        le = LoggerEngine()
        # make connection to LoggerEngine queue
        self.logs_queue = le.logs_queue
        le.add_engine(
            LogsLevelKeys.INFO,
            LoggerEngineStdout(name, LogFormatterDateTime()),
        )
        le.add_engine(
            LogsLevelKeys.DEBUG,
            LoggerEngineStderr(name, LogFormatterTimestamp()),
        )
        lff = LoggerEngineFile(name, LogFormatterTime())
        lff.logdir = "/tmp"
        lff.logfile = "A.debug.log"
        le.add_engine(LogsLevelKeys.DEBUG, lff)
        self.__le = le

    def send(self):
        """"""
        self.__le.send()


class B(MLoggerQueue, NoDynamicAttributes):
    """"""

    msg = None

    def __init__(self, logger: LoggerClient):
        """Constructor."""
        self.msg = logger
        self.msg.logs_queue.put("test")
        self.msg.logs_queue.put("test 2", LogsLevelKeys.DEBUG)
        self.msg.message_debug = "coś się stało"


if __name__ == "__main__":
    obj_a = A()

    # make connection to logs_queue from A object
    obj_b = B(LoggerClient(obj_a.logs_queue, "B"))

    print(obj_a._data)
    print(obj_b._data)
    obj_a.send()


# #[EOF]#######################################################################
