# NetAddressTool

The project contains sets of base classes for operations on IPv4 addresses.

## Public Classes

```
Octet(self, value: Union[str, int, Octet])
Address(self, addr: Union[str, int, List[Union[int, str, Octet]]])
Netmask(self, addr: Union[str, int, List[Union[int, str, Octet]]])
Network(self, addr: Union[str, List])
SubNetwork(self, network: Network, mask: Netmask)
```

## Octet

The class for IPv4 octet representation.

### Import
```
from toolbox.netaddresstool.libs.octets import Octet
```

### Constructor
```
Octet(self, value: Union[str, int, Octet])
```

### Public properties

```
value: int
```
Return ostet as integer.

### Public setters

```
value: Union[str, int, Octet]
```
Set octet from integer, string or other octet object.

### Functional properties

The class has been equipped with comparators that allow comparing objects with each other.

Validation of the assigned value is also carried out, in the event of exceeding the allowable range, the ValueError exception is thrown.

## Address

The class for IPv4 address representation.

### Import
```
from toolbox.netaddresstool.ipv4 import Address
```

### Constructor
```
Address(self, addr: Union[str, int, List[Union[int, str, Octet]]])
```

### Public properties
```
octets: List[Octet]
```
Returns a list of four Octet objects representing the stored address. The list is a copy of the stored value and does not allow modification of the class object.

### Public setters
```
octets: Union[str, int, List[Union[int, str, Octet]]]
```
Allows you to configure the network address by accepting input data in one of the selected formats:
- "192.168.0.1" # as string
- 3232235521 # as an integer
- [192, 168, 0, 1] # as a list of integers
- ["192", "168", "0", "1"] # as a list of strings
- [Octet(192), Octet(168), Octet(0), Octet(1)] # as a list of Octet objects.

### Functional properties

## Netmask

The class for IPv4 network mask representation.

### Import
```
from toolbox.netaddresstool.ipv4 import Netmask
```

### Constructor
```
Netmask(self, addr: Union[str, int, List[Union[int, str, Octet]]])
```

### Public properties
```
octets: List[Octet]
```
Returns the netmask as a list of four Octet objects.

```
cidr: str
```
Returns the netmask in CIDR format.

### Public setters

```
octets: List[Union[int, str, Octet]]
```
```
cidr: Union[str, int]
```

### Functional properties

## Network

The class for IPv4 network address representation.

### Import
```
from toolbox.netaddresstool.ipv4 import Network
```

### Constructor
```
Network(self, addr: Union[str, List])
```

### Public properties
```
address: Address
```
Returns the address passed when creating the object.

```
broadcast: Address
```
Returns the broadcast address.

```
count: int
```
Returns the number of host addresses in the network range.

```
hosts: List[Address]
```
Returns a list of host addresses in the network range.

```
mask: Netmask
```
Returns the network mask.

```
max: Address
```
Returns the last host address in the network range.

```
min: Address
```
Returns the first host address in the network range.

```
network: Address
```
Returns the network address.

### Public setters
### Functional properties

## SubNetwork

A calculator that generates subnet addresses in the given network address and with the assumed network mask.

### Import
```
from toolbox.netaddresstool.ipv4 import SubNetwork
```

### Constructor
```
SubNetwork(self, network: Network, mask: Netmask)
```

### Public properties
```
subnets: List[Network]
```
Returns a list of subnets found in the given network address with the given netmask.

### Public setters
### Functional properties
