# NetAddressTool.IPv4

The project contains sets of base classes for operations on IPv4 addresses.

## Public Classes

1. [Octet](https://github.com/Szumak75/JskToolBox/blob/1.1.5/docs/NetAddressTool4.md#octet)
1. [Address](https://github.com/Szumak75/JskToolBox/blob/1.1.5/docs/NetAddressTool4.md#address)
1. [Netmask](https://github.com/Szumak75/JskToolBox/blob/1.1.5/docs/NetAddressTool4.md#netmask)
1. [Network](https://github.com/Szumak75/JskToolBox/blob/1.1.5/docs/NetAddressTool4.md#network)
1. [SubNetwork](https://github.com/Szumak75/JskToolBox/blob/1.1.5/docs/NetAddressTool4.md#subnetwork)

## Octet

The class for IPv4 octet representation.

### Import

```
from jsktoolbox.netaddresstool.libs.octets import Octet
```

### Constructor

```
Octet(value: Union[str, int, Octet])
```

### Public properties

```
.value: int
```

Return octet as integer.

### Public setters

```
.value: Union[str, int, Octet]
```

Set octet from integer, string or other octet object.

### Functional properties

The class has been equipped with comparators that allow comparing objects with each other.

Validation of the assigned value is also carried out, in the event of exceeding the allowable range, the ValueError exception is thrown.

## Address

The class for IPv4 address representation.

### Import

```
from jsktoolbox.netaddresstool.ipv4 import Address
```

### Constructor

```
Address(addr: Union[str, int, Union[List[str], List[int], List[Octet]]])
```

The addr argument takes values such as the `.octets` property described in the head **Public setters**.

### Public properties

```
.octets: List[Octet]
```

Returns a list of four Octet objects representing the stored address. The list is a copy of the stored value and does not allow modification of the class object.

### Public setters

```
.octets: Union[str, int, Union[List[str], List[int], List[Octet]]]
```

Allows you to configure the network address by accepting input data in one of the selected formats:

- **"192.168.0.1"** -- *as a string*
- **3232235521** -- *as an integer*
- **[192, 168, 0, 1]** -- *as a list of integers*
- **["192", "168", "0", "1"]** -- *as a list of strings*
- **[Octet(192), Octet(168), Octet(0), Octet(1)]** -- *as a list of Octet objects.*

### Functional properties

1. The class has been equipped with comparators that allow comparing objects with each other.
1. `int(Address("192.168.0.1"))` will return the numeric representation of the address as integer: `3232235521`.
1. `str(Address(3232235521))` will return the text representation of the address as string: `"192.168.0.1"`.
1. Attempting to create an object with an invalid IPv4 address `Address("192.256.0.1")` will throw a `ValueError` exception.

## Netmask

The class for IPv4 network mask representation.

### Import

```
from jsktoolbox.netaddresstool.ipv4 import Netmask
```

### Constructor

```
Netmask(addr: Union[str, int, Union[List[str], List[int], List[Octet]]])
```

The addr argument takes values in several formats:

- **16** -- *as an integer in range at 0 to 32 (CIDR format)*
- **"32"** -- *as a string in range at "0" to "32" (CIDR format)*
- **[255, 255, 0, 0]** -- *as a list of integers containing valid octet values for the netmask*
- **["255", "255", "0", "0"]** -- *as a list of strings containing valid octet values for the netmask*
- **[Octet(255), Octet(255), Octet(0), Octet(0)]** -- *as a list of Octet objects containing valid octet values for the netmask.*

### Public properties

```
.octets: List[Octet]
```

Returns the netmask as a list of four Octet objects.

```
.cidr: str
```

Returns the netmask in CIDR format.

### Public setters

```
.octets: Union[List[str], List[int], List[Octet]]
```

Takes values as list:

- **[255, 255, 0, 0]** -- *as a list of integers containing valid octet values for the netmask*
- **["255", "255", "0", "0"]** -- *as a list of strings containing valid octet values for the netmask*
- **[Octet(255), Octet(255), Octet(0), Octet(0)]** -- *as a list of Octet objects containing valid octet values for the netmask.*

```
.cidr: Union[str, int]
```

Takes values in CIDR format:

- **16** -- *as an integer in range at 0 to 32*
- **"32"** -- *as a string in range at "0" to "32"*

### Functional properties

1. `int(Netmask(16))` will return the netmask value as an integer as CIDR format: `16`
1. `str(Netmask(16))` will return the netmask value in text form: `"255.255.0.0"`
1. Attempting to create an object with an invalid IPv4 netmask `Netmask(33)` will throw a `ValueError` exception.

## Network

The class for IPv4 network address representation.

### Import

```
from jsktoolbox.netaddresstool.ipv4 import Network
```

### Constructor

```
Network(addr: Union[str, List])
```

The addr argument takes the value as a string written in the form of the network
address `"192.168.1.22/30"` (the IPv4 address can be any address within the subnet
indicated by the netmask) or in the form of a two-element list: `[ipv4 address, netmask]`.

### Public properties

```
.address: Address
```

Returns the address passed when creating the object.

```
.broadcast: Address
```

Returns the broadcast address.

```
.count: int
```

Returns the number of host addresses in the network range.

```
.hosts: List[Address]
```

Returns a list of host addresses in the network range.

```
.mask: Netmask
```

Returns the network mask.

```
.max: Address
```

Returns the last host address in the network range.

```
.min: Address
```

Returns the first host address in the network range.

```
.network: Address
```

Returns the network address.

### Functional properties

1. `str(Network("192.168.1.22/30"))` will return the network address: `"192.168.1.20/30"`
1. `str(Network("192.168.1.22/30").address)` will return the ipv4 address: `"192.168.1.22"`
1. `str(Network("192.168.1.22/30").broadcast)` will return the ipv4 broadcast address: `"192.168.1.23"`
1. `str(Network("192.168.1.22/30").count)` will return the number of hosts in the network range: `"2"`
1. `str(Network("192.168.1.22/30").hosts)` will return the list of hosts in the network range: `"[Address('192.168.1.21'), Address('192.168.1.22')]"`
1. `str(Network("192.168.1.22/30").mask)` will return the network mask: `"255.255.255.252"`
1. `str(Network("192.168.1.22/30").max)` will return the ipv4 last host address: `"192.168.1.22"`
1. `str(Network("192.168.1.22/30").min)` will return the ipv4 first host address: `"192.168.1.21"`
1. `str(Network("192.168.1.22/30").network)` will return the ipv4 network address: `"192.168.1.20"`

## SubNetwork

A calculator that generates subnet addresses in the given network address and with the assumed network mask.

### Import

```
from jsktoolbox.netaddresstool.ipv4 import SubNetwork
```

### Constructor

```
SubNetwork(network: Network, mask: Netmask)
```

It takes Network and Netmask objects as arguments.
The Network object is the address of the network where we are looking for a subnet.
The Netmask object is the netmask value for the subnets you are looking for.

### Public properties

```
.subnets: List[Network]
```

Returns a list of subnets found in the given network address with the given netmask.

### Functional properties

1. `SubNetwork(Network('192.168.1.20/29'), Netmask(30)).subnets` will return the list of subnets: `[Network(192.168.1.16/30), Network(192.168.1.20/30)]`
