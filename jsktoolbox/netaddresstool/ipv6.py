# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 14.09.2023

  Purpose: Classes for IPv6
"""

import socket
import struct
from copy import deepcopy
from inspect import currentframe
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

    __listwords: Optional[List[Word16]] = None

    def __init__(
        self, addr: Union[str, int, List[Union[int, str, Word16]]]
    ) -> None:
        """Constructor."""
        self.words = addr

    def __eq__(self, arg: TAddress6) -> bool:
        """Equal."""
        return (
            self.words[0] == arg.words[0]
            and self.words[1] == arg.words[1]
            and self.words[2] == arg.words[2]
            and self.words[3] == arg.words[3]
            and self.words[4] == arg.words[4]
            and self.words[5] == arg.words[5]
            and self.words[6] == arg.words[6]
            and self.words[7] == arg.words[7]
        )

    def __ge__(self, arg: TAddress6) -> bool:
        """Greater or equal."""
        if self == arg:
            return True
        if self > arg:
            return True
        return False

    def __gt__(self, arg: TAddress6) -> bool:
        """Greater."""
        if self.words[0] > arg.words[0]:
            return True
        for i in range(1, 8):
            if self.words[i - 1] == arg.words[i - 1]:
                if self.words[i] > arg.words[i]:
                    return True
            else:
                return False
        return False

    def __le__(self, arg: TAddress6) -> bool:
        """Less or equal."""
        if self == arg:
            return True
        if self < arg:
            return True
        return False

    def __lt__(self, arg: TAddress6) -> bool:
        """Less."""
        if self.words[0] < arg.words[0]:
            return True
        for i in range(1, 8):
            if self.words[i - 1] == arg.words[i - 1]:
                if self.words[i] < arg.words[i]:
                    return True
            else:
                return False
        return False

    def __ne__(self, arg: TAddress6) -> bool:
        """Negative."""
        return (
            self.words[0] != arg.words[0]
            or self.words[1] != arg.words[1]
            or self.words[2] != arg.words[2]
            or self.words[3] != arg.words[3]
            or self.words[4] != arg.words[4]
            or self.words[5] != arg.words[5]
            or self.words[6] != arg.words[6]
            or self.words[7] != arg.words[7]
        )

    def __str__(self) -> str:
        """Return words as string."""
        return f"{self.words[0]}:{self.words[1]}:{self.words[2]}:{self.words[3]}:{self.words[4]}:{self.words[5]}:{self.words[6]}:{self.words[7]}"

    def __repr__(self) -> str:
        """Return class representation as string."""
        return (
            f"{self.__class__.__name}(["
            f"Word16({self.words[0]}), "
            f"Word16({self.words[1]}), "
            f"Word16({self.words[2]}), "
            f"Word16({self.words[3]}), "
            f"Word16({self.words[4]}), "
            f"Word16({self.words[5]}), "
            f"Word16({self.words[6]}), "
            f"Word16({self.words[7]})"
            "])"
        )

    @property
    def words(self) -> List[Word16]:
        """Return words list of eight Word16."""
        if self.__listwords is None:
            self.__listwords = [
                Word16(0),
                Word16(0),
                Word16(0),
                Word16(0),
                Word16(0),
                Word16(0),
                Word16(0),
                Word16(0),
            ]
        return self.__listwords

    @words.setter
    def words(
        self, value: Union[int, str, List[Union[int, str, Word16]]]
    ) -> None:
        if isinstance(value, List):
            self.__set_words_from_list(value)
        # TODO: analise sense of this argument method
        elif isinstance(value, int):
            pass
        elif isinstance(value, str):
            self.__set_words_from_string(value)
        else:
            raise Raise.error(
                f"", TypeError, self.__class__.__name__, currentframe()
            )

    def __set_words_from_list(self, value: Union[int, str, Word16]) -> None:
        """Set address from list."""
        if len(value) != 8:
            raise Raise.error(
                f"Expected list of eight elements.",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )
        for idx in range(0, 8):
            self.words[idx] = Word16(value[idx])

    def __set_words_from_string(self, value: str) -> None:
        """Set address from string."""


# #[EOF]#######################################################################