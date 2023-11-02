# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2023

  Purpose:
"""

import os
import sys
import time
from datetime import datetime

from abc import ABC, abstractmethod
from inspect import currentframe
from typing import Optional, List, Dict, Any
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise

#  https://www.programiz.com/python-programming/datetime/strftime
# timestamp: int(time.time())
# now: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


class BLogFormatter(NoDynamicAttributes):
    """Log formatter base class."""

    __template: Optional[str] = None
    __forms: Optional[List] = None

    def __init__(self) -> None:
        """Constructor."""
        self.__forms = []

    def format(self, message: str, name: str = None) -> str:
        """Method for format message string.

        Arguments:
        message [str]: log string to send
        name [str]: optional name of apps,
        """
        out = ""
        for item in self._forms_:
            if callable(item):
                out += f"{item()} "
            elif isinstance(item, str):
                if name is None:
                    if item.find("name") == -1:
                        out += item.format(message=f"{message}")
                else:
                    if item.find("name") > 0:
                        out += item.format(
                            name=f"{name}",
                            message=f"{message}",
                        )
        return out

    @property
    def _forms_(self) -> List:
        """Get forms list."""
        return self.__forms

    @_forms_.setter
    def _forms_(self, item: Any) -> None:
        """Set forms list."""
        # assigning function to a variable
        # def a(): print('test')
        # var=a
        # var()
        ####
        # >>> x._forms_[2].__class__
        # <class 'builtin_function_or_method'>
        # >>> x._forms_[1].__class__
        # <class 'float'>
        # >>> x._forms_[0].__class__
        # <class 'str'>

        self.__forms.append(item)


class LogFormatterNull(BLogFormatter):
    """Log Formatter Null class."""

    def __init__(self):
        """Constructor."""
        BLogFormatter.__init__(self)
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")


class LogFormatterDateTime(BLogFormatter):
    """Log Formatter DateTime class."""

    def __init__(self):
        """Constructor."""
        BLogFormatter.__init__(self)
        self._forms_.append(self.__get_formated_date__)
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")

    def __get_formated_date__(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class LogFormatterTime(BLogFormatter):
    """Log Formatter Time class."""

    def __init__(self):
        """Constructor."""
        BLogFormatter.__init__(self)
        self._forms_.append(self.__get_formated_time__)
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")

    def __get_formated_time__(self):
        return datetime.now().strftime("%H:%M:%S")


class LogFormatterTimestamp(BLogFormatter):
    """Log Formatter Timestamp class."""

    def __init__(self):
        """Constructor."""
        BLogFormatter.__init__(self)
        self._forms_.append(self.__get_timestamp__)
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")

    def __get_timestamp__(self):
        return int(time.time())


# #[EOF]#######################################################################
