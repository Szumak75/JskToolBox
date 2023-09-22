# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 14.09.2023

  Purpose: Classes for IPv6

  https://www.ibm.com/docs/en/ts3500-tape-library?topic=formats-subnet-masks-ipv4-prefixes-ipv6
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

    __varint: int = 0

    def __init__(
        self, addr: Union[str, int, List[Union[int, str, Word16]]]
    ) -> None:
        """Constructor."""
        self.words = addr

    def __eq__(self, arg: TAddress6) -> bool:
        """Equal."""
        return int(self) == int(arg)

    def __ge__(self, arg: TAddress6) -> bool:
        """Greater or equal."""
        return int(self) >= int(arg)

    def __gt__(self, arg: TAddress6) -> bool:
        """Greater."""
        return int(self) > int(arg)

    def __le__(self, arg: TAddress6) -> bool:
        """Less or equal."""
        return int(self) <= int(arg)

    def __lt__(self, arg: TAddress6) -> bool:
        """Less."""
        return int(self) < int(arg)

    def __ne__(self, arg: TAddress6) -> bool:
        """Negative."""
        return int(self) != int(arg)

    @staticmethod
    def __check_groups(group_list: List[str]) -> List[str]:
        for i in range(0, len(group_list)):
            group_list[i] = group_list[i].zfill(4)
        return group_list

    @staticmethod
    def __expand_ipv6(ipv6_address: str) -> str:
        # Sprawdzenie czy adres jest już w pełnej reprezentacji
        if "::" not in ipv6_address:
            return ipv6_address

        # Podziel adres na dwie części, przed '::' i po '::'
        parts = ipv6_address.split("::", 1)
        head = Address6.__check_groups(parts[0].split(":"))
        tail = Address6.__check_groups(parts[1].split(":"))

        # Oblicz ile zer należy dodać, aby osiągnąć 8 części
        missing_zeros = 8 - (len(head) + len(tail))
        zero_part = "0000"

        # Połącz części przed '::' i po '::', wstawiając brakujące zera
        expanded_parts = ":".join(head + [zero_part] * missing_zeros + tail)

        return expanded_parts

    @staticmethod
    def __is_valid_ipv6(ipv6_addr: str) -> bool:
        """Check if ipv6_addr is valid."""
        try:
            # Używamy socket.inet_pton, aby sprawdzić poprawność adresu IPv6
            socket.inet_pton(socket.AF_INET6, ipv6_addr)
            return True
        except (socket.error, ValueError):
            return False

    @staticmethod
    def __int_to_ip(ipint: int) -> str:
        """Convert ip int representation to ipv6 str."""
        # W przypadku adresu IPv6 zawsze przekształcamy go na 16 bajtów (128 bitów)
        binary_ip = ipint.to_bytes(16, byteorder="big")
        ipv6_address = socket.inet_ntop(socket.AF_INET6, binary_ip)

        return ipv6_address

    @staticmethod
    def __ip_to_int(ipstr: str) -> int:
        """Convert ipv6 str representation to ip int."""
        # Używamy socket.inet_pton, aby przekształcić adres IPv6 w postać binarną
        packed_ip = socket.inet_pton(socket.AF_INET6, ipstr)
        # Następnie przekształcamy binarny adres IPv6 na liczbę całkowitą (integer)
        int_ip = int.from_bytes(packed_ip, byteorder="big")

        return int_ip

    def __set_words_from_list(self, value: Union[int, str, Word16]) -> None:
        """Set address from list."""
        if len(value) != 8:
            raise Raise.error(
                f"Expected list of eight elements.",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )
        tmp = (
            f"{str(Word16(value[0]))}:"
            f"{str(Word16(value[1]))}:"
            f"{str(Word16(value[2]))}:"
            f"{str(Word16(value[3]))}:"
            f"{str(Word16(value[4]))}:"
            f"{str(Word16(value[5]))}:"
            f"{str(Word16(value[6]))}:"
            f"{str(Word16(value[7]))}"
        )
        self.__set_words_from_str(tmp)

    def __set_words_from_int(self, value: int) -> None:
        if value >= 0 and value <= 340282366920938463463374607431768211455:
            self.__varint = value
        else:
            raise Raise.error(
                f"IP-int out of range (0-340282366920938463463374607431768211455), received: {value}",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )

    def __set_words_from_str(self, value: str) -> None:
        if Address6.__is_valid_ipv6(value):
            self.__varint = Address6.__ip_to_int(value)
        else:
            raise Raise.error(
                f"IPv6 address is invalid: {value}",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )

    def __int__(self) -> int:
        """Return ipv4 representation as integer."""
        return self.__varint

    def __str__(self) -> str:
        """Return string representation of address."""
        return Address6.__int_to_ip(self.__varint)

    def __repr__(self):
        """Return representation of object."""
        return f"{self.__class__.__name__}('{str(self)}')"

    @property
    def words(self) -> List[Word16]:
        """Return words list of eight Word16."""
        tmp = Address6.__expand_ipv6(str(self)).split(":")
        return [
            Word16(tmp[0]),
            Word16(tmp[1]),
            Word16(tmp[2]),
            Word16(tmp[3]),
            Word16(tmp[4]),
            Word16(tmp[5]),
            Word16(tmp[6]),
            Word16(tmp[7]),
        ]

    @words.setter
    def words(
        self, value: Union[str, int, List[Union[int, str, Word16]]]
    ) -> None:
        if isinstance(value, List):
            self.__set_words_from_list(value)
        elif isinstance(value, int):
            self.__set_words_from_int(value)
        elif isinstance(value, str):
            self.__set_words_from_str(value)
        else:
            raise Raise.error(
                f"String or Integer or List type expected, {type(value)} received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )


# prefix
# https://www.heficed.com/subnet-mask-cheat-sheet/

TPrefix6 = TypeVar("TPrefix6", bound="Prefix6")


class Prefix6(IComparators, NoDynamicAttributes):
    """Prefix6 class for IPv6 addresses.

    Constructor argument:
    prefix: Union[str, int] -- Set prefix from string or integer.

    Public property:
    prefix: str -- Return prefix as string.

    Public setter:
    prefix: Union[str, int] -- Set prefix from string or integer.
    """

    __prefix_int: int = 0

    def __init__(self, prefix: Union[str, int]) -> None:
        """Constructor."""
        self.prefix = prefix

    def __eq__(self, arg: TPrefix6) -> bool:
        """Equal."""
        return int(self) == int(arg)

    def __ge__(self, arg: TPrefix6) -> bool:
        """Greater or equal."""
        return int(self) >= int(arg)

    def __gt__(self, arg: TPrefix6) -> bool:
        """Greater."""
        return int(self) > int(arg)

    def __le__(self, arg: TPrefix6) -> bool:
        """Less or equal."""
        return int(self) <= int(arg)

    def __lt__(self, arg: TPrefix6) -> bool:
        """Less."""
        return int(self) < int(arg)

    def __ne__(self, arg: TPrefix6) -> bool:
        """Negative."""
        return int(self) != int(arg)

    def __str__(self) -> str:
        """Return prefix as string."""
        return str(self.__prefix_int)

    def __int__(self) -> int:
        """Return prefix as integer."""
        return self.__prefix_int

    def __repr__(self) -> str:
        """Return Prefix6 representation string."""
        return f"{self.__class__.__name__}({int(self)})"

    def __range_validator(self, value: int) -> bool:
        """Proper range validator."""
        if value not in range(8, 129):
            raise Raise.error(
                f"Prefix out of range (8-128), received: {value}",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )
        return True

    @staticmethod
    def __is_integer(value: str) -> bool:
        try:
            int(value)
            return True
        except:
            return False

    @property
    def prefix(self) -> str:
        """Return prefix as string."""
        return str(self)

    @prefix.setter
    def prefix(self, value: Union[str, int]) -> None:
        """Set prefix from string or integer."""
        if isinstance(value, int) and self.__range_validator(value):
            self.__prefix_int = value
        elif isinstance(value, str):
            if Prefix6.__is_integer(value) and self.__range_validator(
                int(value)
            ):
                self.__prefix_int = int(value)
            else:
                raise Raise.error(
                    f"Expected proper integer string, '{value}' received.",
                    ValueError,
                    self.__class__.__name__,
                    currentframe(),
                )
        else:
            raise Raise.error(
                f"String or integer expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )


# #[EOF]#######################################################################
