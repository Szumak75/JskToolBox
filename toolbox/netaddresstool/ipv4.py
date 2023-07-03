# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 23.06.2023

  Purpose: Classes for IPv4
"""

import inspect
import socket
import struct
from copy import deepcopy

from typing import TypeVar, Union, List

from toolbox.attribtool import NoDynamicAttributes
from toolbox.raisetool import Raise
from .libs.octets import Octet
from .libs.interfaces import IComparators

TAddress = TypeVar("TAddress", bound="Address")


class Address(IComparators, NoDynamicAttributes):
    """Address class for representing IPv4 adresses.

    Constructor arguments:
    addr: Union[str, int, List[Octets]] -- IPv4 address representation as string, integer or list of four Octets

    Public property:
    octets: List[Octet] -- Return list of four Octets

    Public setter:
    octets: Union[str, int, List] -- Set IPv4 address from string, integer or list of octets.
    """

    __varint: int = 0

    def __init__(
        self, addr: Union[str, int, List[Union[int, str, Octet]]]
    ) -> None:
        """Constructor."""
        self.octets = addr

    def __eq__(self, arg: TAddress) -> bool:
        """Equal."""
        return self.__varint == int(arg)

    def __ge__(self, arg: TAddress) -> bool:
        """Greater or equal."""
        return self.__varint >= int(arg)

    def __gt__(self, arg: TAddress) -> bool:
        """Greater."""
        return self.__varint > int(arg)

    def __le__(self, arg: TAddress) -> bool:
        """Less or equal."""
        return self.__varint <= int(arg)

    def __lt__(self, arg: TAddress) -> bool:
        """Less."""
        return self.__varint < int(arg)

    def __ne__(self, arg: TAddress) -> bool:
        """Negative."""
        return self.__varint != int(arg)

    @staticmethod
    def __int_to_ip(ipint: int) -> str:
        """Convert ip int representation to ipv4 str."""
        return socket.inet_ntoa(struct.pack("!L", ipint))

    @staticmethod
    def __ip_to_int(ipstr: str) -> int:
        """Convert ipv4 str representation to ip int."""
        return struct.unpack("!L", socket.inet_aton(ipstr))[0]

    def __set_octets_from_list(
        self, value: List[Union[int, str, Octet]]
    ) -> None:
        if not value:
            raise Raise.value_error(
                "Empty list received.",
                self.__class__.__name__,
                inspect.currentframe(),
            )
        if len(value) != 4:
            raise Raise.value_error(
                f"Expected list with four elements, len({len(value)}) received.",
                self.__class__.__name__,
                inspect.currentframe(),
            )

        self.__varint = Address.__ip_to_int(
            f"{Octet(value[0])}.{Octet(value[1])}.{Octet(value[2])}.{Octet(value[3])}"
        )

    def __set_octets_from_int(self, value: int) -> None:
        if value >= 0 and value <= 4294967295:
            self.__varint = value
        else:
            raise Raise.value_error(
                f"IP-int out of range (0-4294967295), received: {value}"
            )

    def __set_octets_from_str(self, value: str) -> None:
        self.__set_octets_from_list(value.split("."))

    def __int__(self) -> int:
        """Return ipv4 representation as integer."""
        return self.__varint

    def __str__(self) -> str:
        """Return string representation of address."""
        return Address.__int_to_ip(self.__varint)

    def __repr__(self):
        """Return representation of object."""
        return f"Address('{str(self)}')"

    @property
    def octets(self) -> List[Octet]:
        """Return octets list of four Octets."""
        tmp = str(self).split(".")
        return [Octet(tmp[0]), Octet(tmp[1]), Octet(tmp[2]), Octet(tmp[3])]

    @octets.setter
    def octets(
        self, value: Union[str, int, List[Union[int, str, Octet]]]
    ) -> None:
        if isinstance(value, List):
            self.__set_octets_from_list(value)
        elif isinstance(value, int):
            self.__set_octets_from_int(value)
        elif isinstance(value, str):
            self.__set_octets_from_str(value)
        else:
            raise Raise.type_error(
                f"String or Integer or List type expected, {type(value)} received.",
                self.__class__.__name__,
                inspect.currentframe(),
            )


# netmask
class Netmask(NoDynamicAttributes):
    """Netmask class for IPv4 addresses.

    Constructor argument:
    addr: Union[str, int, List] -- Set netmask from string, integer or list of proper format of netmask octets.

    Public property:
    octets: List[Octet] -- Return netmask as list of four octets.
    cidr: str -- Return netmask in CIDR string format.

    Public setter:
    octets: List[Octet] -- Set netmask from list of 4 values [int||str||Octets].
    cidr: Union[str, int] -- Set netmask from CIDR format of string or integer.
    """

    # CIDR format
    __cidr: int = 0

    def __init__(
        self, addr: Union[str, int, List[Union[int, str, Octet]]]
    ) -> None:
        """Constructor."""
        if isinstance(addr, int):
            self.cidr = addr
        elif isinstance(addr, str):
            if len(addr) < 3:
                self.cidr = addr
            else:
                self.octets = addr
        elif isinstance(addr, List):
            self.octets = str(Address(addr))
        else:
            raise Raise.value_error(
                f"String, integer or list expected, '{type(addr)}' received.",
                self.__class__.__name__,
                inspect.currentframe(),
            )

    def __int__(self) -> int:
        return self.__cidr

    def __str__(self) -> str:
        # convert CIDR to netmask
        return socket.inet_ntoa(
            struct.pack("!I", (1 << 32) - (1 << (32 - self.__cidr)))
        )

    def __repr__(self) -> str:
        return f"Netmask({self.cidr})"

    def __cidr_validator(self, cidr: int) -> None:
        """Check and set cidr."""
        if cidr >= 0 and cidr <= 32:
            self.__cidr = cidr
        else:
            raise Raise.value_error(
                f"CIDR is out of range (0-32), received: {cidr}",
                self.__class__.__name__,
                inspect.currentframe(),
            )

    @staticmethod
    def __octets_validator(octets: str) -> bool:
        """Check if given octets list is valid."""
        test = [
            "0.0.0.0",
            "128.0.0.0",
            "192.0.0.0",
            "224.0.0.0",
            "240.0.0.0",
            "248.0.0.0",
            "252.0.0.0",
            "254.0.0.0",
            "255.0.0.0",
            "255.128.0.0",
            "255.192.0.0",
            "255.224.0.0",
            "255.240.0.0",
            "255.248.0.0",
            "255.252.0.0",
            "255.254.0.0",
            "255.255.0.0",
            "255.255.128.0",
            "255.255.192.0",
            "255.255.224.0",
            "255.255.240.0",
            "255.255.248.0",
            "255.255.252.0",
            "255.255.254.0",
            "255.255.255.0",
            "255.255.255.128",
            "255.255.255.192",
            "255.255.255.224",
            "255.255.255.240",
            "255.255.255.248",
            "255.255.255.252",
            "255.255.255.254",
            "255.255.255.255",
        ]
        if octets in test:
            return True
        return False

    @staticmethod
    def __octets_validator2(octets: List[Octet]) -> bool:
        """Check if given octets list is valid."""
        # tu binary string
        tmp = str().join([bin(octet.value)[2:] for octet in octets])
        test = octets[0].value == 0
        for bit in tmp[1:]:
            if bit == "1" and test:
                return False
            if bit == "0":
                test = True
        return True

    @property
    def octets(self) -> List[Octet]:
        """Return octets list of four Octets."""
        tmp = str(self).split(".")
        return [Octet(tmp[0]), Octet(tmp[1]), Octet(tmp[2]), Octet(tmp[3])]

    # @octets.setter
    # def octets(self, addr: List[Union[int, str, Octet]]) -> None:
    # """Set netmask from list of 4 values [int||str||Octets]."""
    # tmp = str(Address(addr))
    # if not Netmask.__octets_validator(tmp):
    # raise Raise.value_error(f"Invalid mask, received: {tmp}")
    # self.cidr = sum(
    # [bin(x.value).count("1") for x in Address(addr).octets]
    # )

    @octets.setter
    def octets(self, addr: List[Union[int, str, Octet]]) -> None:
        """Set netmask from list of 4 values [int||str||Octets]."""
        if not Netmask.__octets_validator2(Address(addr).octets):
            raise Raise.value_error(
                f"Invalid mask, received: {Address(addr)}"
            )
        self.cidr = sum(
            [bin(x.value).count("1") for x in Address(addr).octets]
        )

    @property
    def cidr(self) -> str:
        """Return CIDR netmask as string type."""
        return str(self.__cidr)

    @cidr.setter
    def cidr(self, value: Union[str, int]) -> None:
        if isinstance(value, str) and value.isdigit():
            self.__cidr_validator(int(value))
        elif isinstance(value, int):
            self.__cidr_validator(value)
        else:
            raise Raise.value_error(
                f"Digit string or int expected. Received: {value}"
            )


# Network
class Network(NoDynamicAttributes):
    """Network IPv4 class.

    Constructor argument:
    addr: Union[str, List] -- Set IPv4 network address from string or two element list of address [Address,str,int,list] and netmask [Netmask, str, int, list].

    Public property:
    address: Address -- Return IPv4 address set in the constructor.
    broadcast: Address -- Return broadcast address.
    count: int -- Return count hosts adresses in network range.
    hosts: List[Address] -- Return hosts address list.
    network: Address -- Return network address.
    mask: Netmask -- Return netmask.
    max: Address -- Return max address of host in network range.
    min: Address -- Return min address of host in network range.
    """

    __address: Address = None
    __mask: Netmask = None

    def __init__(self, addr: Union[str, List]) -> None:
        """Constructor."""
        if isinstance(addr, str):
            self.__network_from_str(addr)
        elif isinstance(addr, List):
            self.__network_from_list(addr)
        else:
            raise Raise.value_error(
                f"IP network string or list expected, '{type(addr)}' received.",
                self.__class__.__name__,
                inspect.currentframe(),
            )

    def __str__(self) -> str:
        """Return string representation of network address."""
        return f"{self.network}/{int(self.mask)}"

    def __repr__(self) -> str:
        """Return  string representation of class object."""
        return f"Network({str(self)})"

    def __network_from_str(self, addr: str) -> None:
        """Build configuration from string."""
        if addr.find("/") > 0:
            tmp = addr.split("/")
            self.__address = Address(tmp[0])
            self.__mask = Netmask(tmp[1])
        else:
            raise Raise.value_error(
                f"Expected network address in 'ip/mask' format string, received '{addr}'",
                self.__class__.__name__,
                inspect.currentframe(),
            )

    def __network_from_list(self, addr: List) -> None:
        """Build configuration from list."""
        if len(addr) != 2:
            raise Raise.value_error(
                "Two element list expected ['ip','netmask']",
                self.__class__.__name__,
                inspect.currentframe(),
            )
        if isinstance(addr[0], Address):
            self.__address = deepcopy(addr[0])
        else:
            self.__address = Address(addr[0])
        if isinstance(addr[1], Netmask):
            self.__mask = deepcopy(addr[1])
        else:
            self.__mask = Netmask(addr[1])

    @staticmethod
    def __ip_int_to_address(ipint: int) -> Address:
        """Converting IPv4 binary to Address."""
        return Address(socket.inet_ntoa(struct.pack("!L", ipint)))

    @property
    def address(self) -> Address:
        """Return IPv4 address."""
        return self.__address

    @property
    def broadcast(self) -> Address:
        """Return broadcast address."""
        ip = int(self.address)
        mask = int(Address(self.mask.octets))
        broadcast = ip | (mask ^ (1 << 32) - 1)
        return Network.__ip_int_to_address(broadcast)

    @property
    def count(self) -> int:
        """Return count hosts adresses in network range."""
        net = int(self.network)
        broadcast = int(self.broadcast)
        return broadcast - net - 1 if broadcast - net > 2 else 0

    @property
    def hosts(self) -> List[Address]:
        """Return list of hosts in network range."""
        tmp: List[Address] = []
        net = int(self.network)
        broadcast = int(self.broadcast)
        for i in range(1, broadcast - net):
            tmp.append(Address(net + i))
        return tmp

    @property
    def mask(self) -> Netmask:
        """Return IPv4 network mask."""
        return self.__mask

    @property
    def max(self) -> Address:
        """Return last address of host in network range."""
        net = int(self.network)
        broadcast = int(self.broadcast)
        ip = broadcast - 1
        return Address(ip) if ip > net else self.broadcast

    @property
    def min(self) -> Address:
        """Return first host address in network range."""
        net = int(self.network)
        broadcast = int(self.broadcast)
        ip = net + 1
        return Address(ip) if ip < broadcast else self.network

    @property
    def network(self) -> Address:
        """Return network address."""
        ip = int(self.address)
        mask = int(Address(self.mask.octets))
        net = ip & mask
        return Network.__ip_int_to_address(net)


# SubNetwork
class SubNetwork(NoDynamicAttributes):
    """SubNetwork calculator class.

    Constructor argument:
    network: Network -- The address of the network where the subnet is being searched for.
    mask: Netmask -- Subnet mask.

    Public property:
    subnets: List[Network] -- Subnet list.
    """

    __network: Network = None
    __mask: Netmask = None

    def __init__(self, network: Network, mask: Netmask) -> None:
        """Constructor."""
        if isinstance(network, Network) and isinstance(mask, Netmask):
            if int(network.mask) <= int(mask):
                self.__network = network
                self.__mask = mask
            else:
                raise Raise.value_error(
                    (
                        "The network mask must be greater then or equal to the subnet mask you are looking for."
                        f"Received: {int(network.mask)} and {int(mask)}"
                    ),
                    self.__class__.__name__,
                    inspect.currentframe(),
                )
        else:
            raise Raise.type_error(
                f"Argument of (Network, Netmask) expected, ({type(network)},{type(mask)}) received.",
                self.__class__.__name__,
                inspect.currentframe(),
            )

    @property
    def subnets(self) -> List[Network]:
        """Return subnets list."""
        tmp: List[Network] = []
        nstart = int(self.__network.network)
        nend = int(self.__network.broadcast)
        start = nstart
        while True:
            subnet = Network([Address(start), self.__mask])
            tmp.append(subnet)
            if int(subnet.broadcast) >= nend:
                break
            start = int(subnet.broadcast) + 1
        return tmp


# #[EOF]#######################################################################
