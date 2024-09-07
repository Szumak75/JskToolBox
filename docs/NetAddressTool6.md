# NetAddressTool.IPv6

The project contains sets of base classes for operations on IPv6 addresses.

## Public Classes

1. [Word16](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool6.md#word16)
1. [Address6](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool6.md#address6)
1. [Prefix6](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool6.md#prefix6)
1. [Network6](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool6.md#network6)
1. [SubNetwork6](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool6.md#subnetwork6)

## Word16

The class for IPv6 Word16 representation.

### Import

```from jsktoolbox.netaddresstool.libs.words import Word16
```

### Constructor

```Word16(value: Union[str, int, Word16])
```

### Public properties

```.value: int
```

Return Word16 as integer.

### Public setters

```.value: Union[str, int, Word16]
```

Set Word16 from integer, string or other Word16 object.

### Functional properties

The class has been equipped with comparators that allow comparing objects with each other.

Validation of the assigned value is also carried out, in the event of exceeding the allowable range, the ValueError exception is thrown.

## Address6

The class for IPv6 address representation.

### Import

```from jsktoolbox.netaddresstool.ipv6 import Address6
```

### Constructor

```Address6(addr: Union[str, int, Union[List[int], List[str], List[Word16]]])
```

The addr argument takes values such as the `.words` property described in the head **Public setters**.

### Public properties

```.words: List[Word16]
```

Returns a list of eight Word16 objects representing the stored address. The list is a copy of the stored value and does not allow modification of the class object.

### Public setters

```.words: Union[str, int, Union[List[int], List[str], List[Word16]]]
```

Allows you to configure the network address by accepting input data in one of the selected formats:

- **"2000::FF"** -- *as a string*
- **42535295865117307932921825928971026687** -- *as an integer*
- **[1, 2, 3, 4, 5, 6, 7, 8]** -- *as a list of integers*
- **["1", "2", "3", "4", "5", "6", "7", "8"]** -- *as a list of strings*
- **[Word16("0xFF"),Word16("0"),Word16("0x0"),Word16("0"),Word16("0x0"),Word16("0"),Word16("0x0"),Word16("0xFFFF")]** -- *as a list of Word16 objects.*

### Functional properties

1. The class has been equipped with comparators that allow comparing objects with each other.
1. `int(Address("::1"))` will return the numeric representation of the address as integer: `1`.
1. `str(Address(1))` will return the text representation of the address as string: `"::1"`.
1. Attempting to create an object with an invalid IPv6 address `Address("FFFFF::")` will throw a `ValueError` exception.

## Prefix6

The class for IPv6 address prefix representation.

### Import

```from jsktoolbox.netaddresstool.ipv6 import Prefix6
```

### Constructor

```Prefix6(addr: Union[str, int])
```

The addr argument takes values in several formats:

- **125** -- *as an integer in range at 0 to 128*
- **"127"** -- *as a string in range at "0" to "128"*

### Public properties

```.prefix: str
```

Returns the prefix as a string objects.

### Public setters

```.prefix: Union[int, str]
```

Takes values as integer or string:

- **125** -- *as an integer in range at 0 to 128*
- **"127"** -- *as a string in range at "0" to "128"*

### Functional properties

1. The class has been equipped with comparators that allow comparing objects with each other.
1. `int(Prefix6(16))` will return the prefix value as an integer: `16`
1. `str(Netmask(16))` will return the prefix value in text: `"16"`
1. Attempting to create an object with an invalid IPv6 netmask `Prefix6(200)` will throw a `ValueError` exception.

## Network6

The class for IPv6 network address representation.

### Import

```from jsktoolbox.netaddresstool.ipv6 import Network6
```

### Constructor

```Network6(addr: Union[str, List])
```

The addr argument takes the value as a string written in the form of the network
address `"2000::7/125"` (the IPv6 address can be any address within the subnet
indicated by the prefix) or in the form of a two-element list: `[ipv6 address, prefix]`.

### Public properties

```.address: Address6
```

Returns the address passed when creating the object.

```.count: int
```

Returns the number of host addresses in the network range.

```.hosts: List[Address6]
```

Returns a list of host addresses in the network range.

```.network: Address6
```

Returns the network address.

```.prefix: Prefix6
```

Returns the network mask.

```.max: Address6
```

Returns the last host address in the network range.

```.min: Address6
```

Returns the first host address in the network range.

### Functional properties

1. `str(Network6("FF::1/30"))` will return the network address: `"ff::1/30"`
1. `str(Network6("FF::1/30").address)` will return the ipv6 address: `"ff::1"`
1. `str(Network6("FF::1/125").count)` will return the number of hosts in the network range: `"8"`
1. `str(Network6("FF::1/127").hosts)` will return the list of hosts in the network range: `"[Address6('ff::'), Address6('ff::1')]"`
1. `str(Network6("FF::1/127").prefix)` will return the network prefix: `"127"`
1. `str(Network6("FF::1/125").max)` will return the ipv6 last host address: `"ff::7"`
1. `str(Network6("FF::1/127").min)` will return the ipv4 first host address: `"ff::"`
1. `str(Network6("FF::1/127").network)` will return the ipv6 first address: `"ff::"`

## SubNetwork6

A calculator that generates subnet addresses in the given network address and with the assumed network mask.

### Import

```
from jsktoolbox.netaddresstool.ipv6 import SubNetwork6
```

### Constructor

```
SubNetwork6(network: Network6, prefix: Prefix6)
```

It takes Network6 and Prefix6 objects as arguments.
The Network6 object is the address of the network where we are looking for a subnet.
The Prefix6 object is the prefix value for the subnets you are looking for.

### Public properties

```
.subnets: List[Network6]
```

Returns a list of subnets found in the given network address with the given netmask.

### Functional properties

1. `SubNetwork6(Network6('2000::123/125'), Prefix6(127)).subnets` will return the list of subnets: `[Network6(2000::120/127), Network6(2000::122/127), Network6(2000::124/127), Network6(2000::126/127)]`
