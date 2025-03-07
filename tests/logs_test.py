#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 03.11.2023

Purpose: test logs engine
"""

import time
import sys

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.logstool.keys import LogsLevelKeys
from jsktoolbox.logstool.logs import (
    LoggerEngine,
    LoggerClient,
    LoggerEngineFile,
    LoggerEngineStderr,
    LoggerEngineStdout,
    LoggerEngineSyslog,
    ThLoggerProcessor,
)
from jsktoolbox.basetool.logs import BLoggerQueue
from jsktoolbox.logstool.formatters import (
    LogFormatterDateTime,
    LogFormatterNull,
    LogFormatterTime,
    LogFormatterTimestamp,
)
from jsktoolbox.logstool.queue import LoggerQueue


class A(BLoggerQueue, NoDynamicAttributes):
    """"""

    __le = None  # type: ignore

    def __init__(self) -> None:
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
        self.__le: LoggerEngine = le

    def send(self) -> None:
        """"""
        self.__le.send()


class B(BLoggerQueue, NoDynamicAttributes):
    """"""

    msg = None  # type: ignore

    def __init__(self, logger: LoggerClient) -> None:
        """Constructor."""
        self.msg: LoggerClient = logger
        self.msg.message_debug = "coś się stało"

    def send(self, msg: str) -> None:
        """Test"""
        # self.msg.logs_queue.put(msg)
        # self.msg.logs_queue.put(msg, LogsLevelKeys.DEBUG)
        self.msg.message_info = msg
        self.msg.message_debug = msg


if __name__ == "__main__":
    print(f"sys.argv: {sys.argv}")
    obj_a = ThLoggerProcessor()

    le = LoggerEngine()
    le.add_engine(
        LogsLevelKeys.INFO,
        LoggerEngineStdout("name", LogFormatterDateTime()),
    )
    le.add_engine(
        LogsLevelKeys.DEBUG,
        LoggerEngineStderr("name", LogFormatterTimestamp()),
    )
    lff = LoggerEngineFile("name", LogFormatterTime())
    lff.logdir = "/tmp"
    lff.logfile = "A.debug.log"
    le.add_engine(LogsLevelKeys.DEBUG, lff)

    obj_a.logger_engine = le

    obj_a.logger_client = LoggerClient(le.logs_queue, "ThLoggerProcessor")

    # make connection to logs_queue from A object
    obj_b = B(LoggerClient(le.logs_queue, "B"))

    obj_a.start()
    count = 0
    while True:
        count += 1
        time.sleep(0.7)
        obj_b.send(f"Count: {count}")
        if count == 10:
            obj_a.stop()
            break
    time.sleep(1.0)
    obj_a.join()
    print(obj_a._data)

# #[EOF]#######################################################################
