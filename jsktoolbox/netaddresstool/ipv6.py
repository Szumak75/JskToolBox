# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 14.09.2023

  Purpose: Classes for IPv6
"""

import inspect
import socket
import struct
from copy import deepcopy

from typing import TypeVar, Union, List, Optional

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from .libs.words import Word16
from jsktoolbox.libs.interfaces.comparators import IComparators

TAddress6 = TypeVar("TAddress6", bound="Address6")


class Address6(IComparators, NoDynamicAttributes):
    """Address6 class for representing IPv6 adresses.

    Constructor arguments:
    addr: Union[str, int, List[Word16]] -- IPv6 address representation as string, integer or list of eight Word16

    Public property:
    words: List[Word16] -- Return list of eight Word16

    Public setter:
    words: Union[str, int, List] -- Set IPv6 address from string, integer or list of Word16.
    """

    __listint: Optional[List[Word16]] = None

    def __init__(
        self, addr: Union[str, int, List[Union[int, str, Word16]]]
    ) -> None:
        """Constructor."""
        self.words = addr

    def __eq__(self, arg: TAddress6) -> bool:
        """Equal."""
        return False

    def __ge__(self, arg: TAddress6) -> bool:
        """Greater or equal."""
        return False

    def __gt__(self, arg: TAddress6) -> bool:
        """Greater."""
        return False

    def __le__(self, arg: TAddress6) -> bool:
        """Less or equal."""
        return False

    def __lt__(self, arg: TAddress6) -> bool:
        """Less."""
        return False

    def __ne__(self, arg: TAddress6) -> bool:
        """Negative."""
        return False


# #[EOF]#######################################################################
