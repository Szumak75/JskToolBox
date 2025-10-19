# NetAddressTool.IPv4 Module

**Source:** `jsktoolbox/netaddresstool/ipv4.py`

**IPv4 Network Address Manipulation:**
The IPv4 submodule provides a complete toolkit for working with IPv4 addresses, network masks, network ranges, and subnet calculations. It supports multiple input formats, automatic validation, and memory-efficient iteration over large address spaces. All classes implement comparison operators and provide both human-readable string representations and efficient integer-based internal storage.

## Getting Started

Import the classes you need for IPv4 network operations. The package-level imports resolve symbols lazily, so the heavier submodules load only when you first touch a class. The module provides both low-level components (Octet) and high-level network manipulation (Network, SubNetwork).

```python
from jsktoolbox.netaddresstool import Address, Netmask, Network, SubNetwork
from jsktoolbox.netaddresstool import Octet
```

Lazy loading keeps CLI tools responsive while still exposing the full IPv4 toolkit through a single namespace.

---

## Public Classes

1. [Octet](#octet) - IPv4 octet representation (0-255)
1. [Address](#address) - Complete IPv4 address
1. [Netmask](#netmask) - Network mask with CIDR support
1. [Network](#network) - IPv4 network range
1. [SubNetwork](#subnetwork) - Subnet calculator

---

## `Octet` Class

**Building Block for IPv4 Addresses:**
The Octet class represents a single byte (0-255) of an IPv4 address with comprehensive validation and type conversion. It forms the foundation for the Address class but can also be used independently when you need validated byte-range values. The class ensures that all values remain within the valid octet range and provides automatic conversion between string, integer, and Octet representations.

### `Octet.__init__()`

**Initialize an IPv4 Octet:**
Creates an octet with automatic validation and type conversion. The constructor accepts multiple input formats and immediately validates that the value falls within the 0-255 range, raising ValueError for invalid inputs.

**Signature:**

```python
Octet(value: Union[str, int, Octet])
```

- **Arguments:**
  - `value: Union[str, int, Octet]` - Octet value as integer (0-255), string ("0"-"255"), or another Octet instance.
- **Returns:**
  - `Octet` - A validated octet instance.
- **Raises:**
  - `ValueError`: Value outside the 0-255 range.
  - `TypeError`: Invalid input type.

**Usage Example:**

```python
from jsktoolbox.netaddresstool import Octet

# Create octets from different input types
octet1 = Octet(192)           # From integer
octet2 = Octet("168")         # From string
octet3 = Octet(octet1)        # From another Octet

# Comparison operations
assert octet1 > octet2        # 192 > 168
assert octet2 == Octet(168)   # Value equality

# String and integer conversion
print(str(octet1))            # "192"
print(int(octet1))            # 192
```

---

### `Octet.value`

**Get Octet as Integer:**
Returns the octet's value as an integer in the 0-255 range. This property provides direct access to the validated internal value.

**Signature:**

```python
@property
def value(self) -> int
```

- **Returns:**
  - `int` - Octet value as integer (0-255).

**Usage Example:**

```python
octet = Octet(192)
value = octet.value  # 192
```

---

### `Octet.value` (setter)

**Set Octet Value with Validation:**
Assigns a new value to the octet with automatic validation. The setter accepts the same input formats as the constructor and immediately validates the range.

**Signature:**

```python
@value.setter
def value(self, args: Union[str, int, Octet]) -> None
```

- **Arguments:**
  - `args: Union[str, int, Octet]` - New octet value in any supported format.
- **Raises:**
  - `ValueError`: Value outside the 0-255 range.
  - `TypeError`: Invalid input type.

**Usage Example:**

```python
octet = Octet(0)
octet.value = 255      # Set to maximum
octet.value = "127"    # Set from string

# ValueError: out of range
try:
    octet.value = 256
except ValueError as e:
    print(f"Error: {e}")
```

---

## `Address` Class

**Complete IPv4 Address Representation:**
The Address class provides a comprehensive representation of IPv4 addresses with support for multiple input formats, automatic validation, and efficient storage. It internally stores addresses as 32-bit integers for fast comparisons and calculations while providing intuitive string representations. The class implements all comparison operators, allowing addresses to be naturally sorted or compared within network ranges.

### `Address.__init__()`

**Create an IPv4 Address:**
Initializes an IPv4 address from various input formats including dotted-decimal strings, 32-bit integers, or lists of octet components. The constructor automatically validates the address and converts it to the internal integer representation.

**Signature:**

```python
Address(addr: Union[str, int, Union[List[str], List[int], List[Octet]]])
```

- **Arguments:**
  - `addr: Union[str, int, List]` - IPv4 address as string ("192.168.0.1"), integer (3232235521), or list of four octet values.
- **Returns:**
  - `Address` - A validated IPv4 address instance.
- **Raises:**
  - `ValueError`: Invalid IPv4 address format or value.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
from jsktoolbox.netaddresstool import Address

# Multiple input formats
addr1 = Address("192.168.0.1")                    # String
addr2 = Address(3232235521)                       # Integer
addr3 = Address([192, 168, 0, 1])                 # List of integers
addr4 = Address(["192", "168", "0", "1"])         # List of strings

# All represent the same address
assert addr1 == addr2 == addr3 == addr4

# Comparison operations
assert Address("192.168.0.1") < Address("192.168.0.2")
assert Address("10.0.0.0") < Address("172.16.0.0")
```

---

### `Address.octets`

**Get Address as Octet List:**
Returns the IPv4 address as a list of four Octet objects. This provides a decomposed view of the address that's useful for octet-level inspection or manipulation. The returned list is a new object and doesn't affect the internal address storage.

**Signature:**

```python
@property
def octets(self) -> List[Octet]
```

- **Returns:**
  - `List[Octet]` - List of four Octet objects representing the address.

**Usage Example:**

```python
addr = Address("192.168.0.1")
octets = addr.octets

# Access individual octets
print(octets[0])  # Octet(192)
print(octets[3])  # Octet(1)

# Extract integer values
values = [int(o) for o in octets]  # [192, 168, 0, 1]
```

---

### `Address.octets` (setter)

**Set Address from Various Formats:**
Assigns a new IPv4 address from any supported input format with automatic validation. This setter accepts the same formats as the constructor and performs complete address validation.

**Signature:**

```python
@octets.setter
def octets(self, value: Union[str, int, Union[List[str], List[int], List[Octet]]]) -> None
```

- **Arguments:**
  - `value: Union[str, int, List]` - New address in any supported format.
- **Raises:**
  - `ValueError`: Invalid address format or out-of-range values.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
addr = Address("0.0.0.0")

# Update using different formats
addr.octets = "192.168.1.1"
addr.octets = [10, 0, 0, 1]
addr.octets = 2130706433  # 127.0.0.1

# String and integer conversion
ip_string = str(addr)     # "127.0.0.1"
ip_integer = int(addr)    # 2130706433
```

---

## `Netmask` Class

**IPv4 Network Mask Representation:**
The Netmask class represents IPv4 network masks in both CIDR notation (0-32) and dotted-decimal format (255.255.255.0). It automatically validates that mask values follow the contiguous 1-bits pattern required for valid netmasks and provides seamless conversion between CIDR and octet representations. This class is essential for network range calculations and subnet operations.

### `Netmask.__init__()`

**Create a Network Mask:**
Initializes a netmask from CIDR notation or dotted-decimal format with automatic validation. The constructor accepts integers (0-32), strings ("0"-"32" or "255.255.255.0"), or lists of octet values.

**Signature:**

```python
Netmask(addr: Union[str, int, Union[List[str], List[int], List[Octet]]])
```

- **Arguments:**
  - `addr: Union[str, int, List]` - Netmask as CIDR (16, "24") or dotted-decimal ("255.255.0.0") or list of octets.
- **Returns:**
  - `Netmask` - A validated netmask instance.
- **Raises:**
  - `ValueError`: Invalid netmask format, CIDR out of range (0-32), or invalid octet pattern.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
from jsktoolbox.netaddresstool import Netmask

# Create from CIDR notation
mask1 = Netmask(24)           # /24
mask2 = Netmask("16")         # /16

# Create from dotted-decimal
mask3 = Netmask("255.255.255.0")
mask4 = Netmask([255, 255, 0, 0])

# CIDR and string conversion
assert int(mask1) == 24
assert str(mask1) == "255.255.255.0"
```

---

### `Netmask.cidr`

**Get CIDR Notation:**
Returns the netmask in CIDR format as a string. CIDR represents the number of contiguous 1-bits in the mask (0-32), providing a compact representation of the mask size.

**Signature:**

```python
@property
def cidr(self) -> str
```

- **Returns:**
  - `str` - CIDR notation as string ("0" through "32").

**Usage Example:**

```python
mask = Netmask("255.255.255.0")
cidr = mask.cidr  # "24"
```

---

### `Netmask.cidr` (setter)

**Set Netmask from CIDR:**
Assigns a new netmask value using CIDR notation with validation. Accepts integers or digit strings in the 0-32 range.

**Signature:**

```python
@cidr.setter
def cidr(self, value: Union[str, int]) -> None
```

- **Arguments:**
  - `value: Union[str, int]` - CIDR value (0-32) as integer or string.
- **Raises:**
  - `ValueError`: CIDR value outside 0-32 range or non-digit string.

**Usage Example:**

```python
mask = Netmask(24)
mask.cidr = 16        # Change to /16
mask.cidr = "32"      # Change to /32 (host mask)
```

---

### `Netmask.octets`

**Get Netmask as Octet List:**
Returns the netmask in dotted-decimal format as a list of four Octet objects. This provides the traditional network mask representation.

**Signature:**

```python
@property
def octets(self) -> List[Octet]
```

- **Returns:**
  - `List[Octet]` - List of four Octet objects representing the mask.

**Usage Example:**

```python
mask = Netmask(24)
octets = mask.octets  # [Octet(255), Octet(255), Octet(255), Octet(0)]
```

---

### `Netmask.octets` (setter)

**Set Netmask from Octet Values:**
Assigns a netmask from dotted-decimal format with validation of the bit pattern. The mask must follow the valid pattern of contiguous 1-bits followed by contiguous 0-bits.

**Signature:**

```python
@octets.setter
def octets(self, addr: Union[str, int, Union[List[str], List[int], List[Octet]]]) -> None
```

- **Arguments:**
  - `addr: Union[str, int, List]` - Netmask in dotted-decimal format.
- **Raises:**
  - `ValueError`: Invalid netmask pattern (non-contiguous 1-bits).

**Usage Example:**

```python
mask = Netmask(0)
mask.octets = "255.255.255.0"
mask.octets = [255, 255, 0, 0]

# Invalid mask pattern
try:
    mask.octets = "255.0.255.0"  # Non-contiguous 1-bits
except ValueError as e:
    print(f"Invalid mask: {e}")
```

---

## `Network` Class

**IPv4 Network Range Representation:**
The Network class represents a complete IPv4 network defined by an address and netmask. It provides comprehensive network calculations including network and broadcast addresses, host ranges, and efficient host enumeration. The class uses lazy iteration for memory-safe processing of large networks while maintaining optional safety limits for backward compatibility with deprecated list-based methods.

### `Network.__init__()`

**Create an IPv4 Network:**
Initializes a network from CIDR notation or an address-mask pair. The network address is automatically calculated from the provided address and mask, regardless of whether the input address is the network address, a host address, or the broadcast address within the subnet.

**Signature:**

```python
Network(addr: Union[str, List])
```

- **Arguments:**
  - `addr: Union[str, List]` - Network as CIDR string ("192.168.1.0/24") or two-element list [Address/str/int, Netmask/str/int].
- **Returns:**
  - `Network` - A network instance with calculated addresses.
- **Raises:**
  - `ValueError`: Invalid network format or incompatible address/mask combination.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
from jsktoolbox.netaddresstool import Network, Address, Netmask

# Create from CIDR notation
net1 = Network("192.168.1.0/24")
net2 = Network("192.168.1.100/24")  # Any host address works

# Create from components
net3 = Network([Address("10.0.0.0"), Netmask(8)])
net4 = Network(["172.16.0.0", 16])

# All produce proper network addresses
print(net1.network)  # 192.168.1.0
print(net2.network)  # 192.168.1.0 (same network)
```

---

### `Network.address`

**Get Original Input Address:**
Returns the address that was provided to the constructor, before network address calculation. This allows you to preserve the original host or arbitrary address that defined the network.

**Signature:**

```python
@property
def address(self) -> Address
```

- **Returns:**
  - `Address` - The original address used to create the network.

**Usage Example:**

```python
net = Network("192.168.1.50/24")
print(net.address)   # 192.168.1.50 (input address)
print(net.network)   # 192.168.1.0 (calculated network)
```

---

### `Network.broadcast`

**Get Broadcast Address:**
Returns the broadcast address for this network. The broadcast address is the highest address in the network range and is used for sending packets to all hosts within the subnet.

**Signature:**

```python
@property
def broadcast(self) -> Address
```

- **Returns:**
  - `Address` - The network's broadcast address.

**Usage Example:**

```python
net = Network("192.168.1.0/24")
print(net.broadcast)  # 192.168.1.255

net = Network("10.0.0.0/30")
print(net.broadcast)  # 10.0.0.3
```

---

### `Network.count`

**Get Host Count:**
Returns the number of usable host addresses in the network range, excluding the network and broadcast addresses. For networks with only two addresses (/31) or one address (/32), returns 0 as there are no distinct host addresses.

**Signature:**

```python
@property
def count(self) -> int
```

- **Returns:**
  - `int` - Number of usable host addresses (0 for /31 and /32 networks).

**Usage Example:**

```python
net = Network("192.168.1.0/24")
print(net.count)  # 254 (256 - 2)

net = Network("10.0.0.0/30")
print(net.count)  # 2 (4 - 2)

net = Network("172.16.0.1/32")
print(net.count)  # 0 (single host)
```

---

### `Network.hosts()` _(deprecated)_

**Get Host List with Safety Limit:**
Returns a materialized list of all host addresses in the network range. This method is deprecated due to potential memory exhaustion on large networks. Use `iter_hosts()` for memory-safe lazy iteration.

**Signature:**

```python
def hosts(self, limit: Optional[int] = DEFAULT_IPV4_HOST_LIMIT) -> List[Address]
```

- **Arguments:**
  - `limit: Optional[int]` - Maximum hosts allowed to materialize. Defaults to `DEFAULT_IPV4_HOST_LIMIT` (65536). Pass `None` to disable.
- **Returns:**
  - `List[Address]` - List of host addresses.
- **Raises:**
  - `ValueError`: Host count exceeds the configured limit.

**Usage Example:**

```python
net = Network("192.168.1.0/29")

# Deprecated: materializes entire list
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    hosts = net.hosts()  # Returns list

# Large network would fail
try:
    big_net = Network("10.0.0.0/8")
    hosts = big_net.hosts()  # Exceeds default limit
except ValueError as e:
    print(f"Too many hosts: {e}")
```

---

### `Network.iter_hosts()`

**Iterate Hosts Lazily:**
Returns a generator that yields host addresses one at a time without materializing the entire list in memory. This is the recommended approach for processing network hosts, especially for large networks. The safety limit prevents accidental unbounded iteration.

**Signature:**

```python
def iter_hosts(self, limit: Optional[int] = DEFAULT_IPV4_HOST_LIMIT) -> Iterator[Address]
```

- **Arguments:**
  - `limit: Optional[int]` - Maximum hosts before raising. Defaults to `DEFAULT_IPV4_HOST_LIMIT`. Pass `None` for unlimited iteration.
- **Returns:**
  - `Iterator[Address]` - Generator yielding host addresses in ascending order.
- **Raises:**
  - `ValueError`: Host count exceeds limit (checked before iteration begins).

**Usage Example:**

```python
net = Network("192.168.1.0/24")

# Memory-efficient iteration
for host in net.iter_hosts():
    print(host)  # Process one at a time

# Convert to list if needed (small networks only)
hosts = list(net.iter_hosts(limit=254))

# Disable limit for known-safe large networks
big_net = Network("10.0.0.0/8")
for host in big_net.iter_hosts(limit=None):
    # Process 16 million hosts efficiently
    if some_condition(host):
        break
```

---

### `Network.mask`

**Get Network Mask:**
Returns the netmask that defines this network's size and range.

**Signature:**

```python
@property
def mask(self) -> Netmask
```

- **Returns:**
  - `Netmask` - The network's mask.

**Usage Example:**

```python
net = Network("192.168.0.0/16")
mask = net.mask
print(mask.cidr)  # "16"
print(str(mask))  # "255.255.0.0"
```

---

### `Network.max`

**Get Last Host Address:**
Returns the highest usable host address in the network range. For networks with usable hosts, this is one below the broadcast address. For /32 networks, returns the broadcast address.

**Signature:**

```python
@property
def max(self) -> Address
```

- **Returns:**
  - `Address` - Last usable host address.

**Usage Example:**

```python
net = Network("192.168.1.0/24")
print(net.max)  # 192.168.1.254

net = Network("10.0.0.0/30")
print(net.max)  # 10.0.0.2
```

---

### `Network.min`

**Get First Host Address:**
Returns the lowest usable host address in the network range. For networks with usable hosts, this is one above the network address. For /32 networks, returns the network address.

**Signature:**

```python
@property
def min(self) -> Address
```

- **Returns:**
  - `Address` - First usable host address.

**Usage Example:**

```python
net = Network("192.168.1.0/24")
print(net.min)  # 192.168.1.1

net = Network("10.0.0.0/30")
print(net.min)  # 10.0.0.1
```

---

### `Network.network`

**Get Network Address:**
Returns the network's base address with all host bits set to zero. This is the canonical network identifier used in routing tables and CIDR notation.

**Signature:**

```python
@property
def network(self) -> Address
```

- **Returns:**
  - `Address` - The network address.

**Usage Example:**

```python
net = Network("192.168.1.100/24")
print(net.network)  # 192.168.1.0

# String representation includes mask
print(str(net))  # "192.168.1.0/24"
```

---

## `SubNetwork` Class

**IPv4 Subnet Calculator:**
The SubNetwork class generates all subnets of a given size within a parent network. It efficiently subdivides networks into smaller subnets with lazy iteration to handle large subnet counts without memory exhaustion. This is essential for IP address planning, VLSM (Variable Length Subnet Masking), and network segmentation tasks.

### `SubNetwork.__init__()`

**Create a Subnet Calculator:**
Initializes a subnet calculator for dividing a parent network into smaller subnets. The subnet mask must be equal to or larger (more specific) than the parent network's mask.

**Signature:**

```python
SubNetwork(network: Network, mask: Netmask)
```

- **Arguments:**
  - `network: Network` - Parent network to subdivide.
  - `mask: Netmask` - Subnet mask for the desired subnets (must be >= parent mask).
- **Returns:**
  - `SubNetwork` - A subnet calculator instance.
- **Raises:**
  - `ValueError`: Subnet mask smaller than parent network mask.
  - `TypeError`: Invalid argument types.

**Usage Example:**

```python
from jsktoolbox.netaddresstool import SubNetwork

# Divide /24 into /26 subnets
parent = Network("192.168.1.0/24")
subnets = SubNetwork(parent, Netmask(26))

# Invalid: subnet mask smaller than parent
try:
    invalid = SubNetwork(Network("10.0.0.0/16"), Netmask(8))
except ValueError as e:
    print(f"Error: {e}")
```

---

### `SubNetwork.subnets()` _(deprecated)_

**Get Subnet List with Safety Limit:**
Returns a materialized list of all subnets. This method is deprecated due to potential memory exhaustion with large subnet counts. Use `iter_subnets()` for memory-safe lazy iteration.

**Signature:**

```python
def subnets(self, limit: Optional[int] = DEFAULT_IPV4_SUBNET_LIMIT) -> List[Network]
```

- **Arguments:**
  - `limit: Optional[int]` - Maximum subnets allowed. Defaults to `DEFAULT_IPV4_SUBNET_LIMIT` (4096). Pass `None` to disable.
- **Returns:**
  - `List[Network]` - List of subnet Network objects.
- **Raises:**
  - `ValueError`: Subnet count exceeds the configured limit.

**Usage Example:**

```python
parent = Network("192.168.0.0/22")
calc = SubNetwork(parent, Netmask(24))

# Deprecated: materializes entire list
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    subnet_list = calc.subnets()  # Returns list of 4 networks
```

---

### `SubNetwork.iter_subnets()`

**Iterate Subnets Lazily:**
Returns a generator that yields subnet Network objects one at a time without materializing the entire list in memory. This is the recommended approach for processing subnets, especially when dealing with large parent networks or small subnet masks.

**Signature:**

```python
def iter_subnets(self, limit: Optional[int] = DEFAULT_IPV4_SUBNET_LIMIT) -> Iterator[Network]
```

- **Arguments:**
  - `limit: Optional[int]` - Maximum subnets before raising. Defaults to `DEFAULT_IPV4_SUBNET_LIMIT`. Pass `None` for unlimited.
- **Returns:**
  - `Iterator[Network]` - Generator yielding Network objects in ascending address order.
- **Raises:**
  - `ValueError`: Subnet count exceeds limit (checked after each subnet).

**Usage Example:**

```python
# Divide /24 into /26 subnets (4 subnets)
parent = Network("192.168.1.0/24")
calc = SubNetwork(parent, Netmask(26))

# Memory-efficient iteration
for subnet in calc.iter_subnets():
    print(f"{subnet} has {subnet.count} hosts")
# Output:
# 192.168.1.0/26 has 62 hosts
# 192.168.1.64/26 has 62 hosts
# 192.168.1.128/26 has 62 hosts
# 192.168.1.192/26 has 62 hosts

# Convert to list if needed (small counts)
subnets = list(calc.iter_subnets())

# Disable limit for large operations
large_parent = Network("10.0.0.0/8")
large_calc = SubNetwork(large_parent, Netmask(16))
for subnet in large_calc.iter_subnets(limit=None):
    # Process 256 /16 subnets efficiently
    process_subnet(subnet)
```

---

## Complete Examples

### Example 1: Network Analysis

```python
from jsktoolbox.netaddresstool import Network

# Analyze a network
net = Network("192.168.1.64/26")

print(f"Network: {net.network}")
print(f"Mask: {net.mask} (/{net.mask.cidr})")
print(f"Broadcast: {net.broadcast}")
print(f"First host: {net.min}")
print(f"Last host: {net.max}")
print(f"Total hosts: {net.count}")

# Iterate hosts efficiently
print("\nHost addresses:")
for i, host in enumerate(net.iter_hosts(), 1):
    print(f"  {i}. {host}")
    if i >= 5:  # Show first 5
        print(f"  ... and {net.count - 5} more")
        break
```

### Example 2: Subnet Planning

```python
from jsktoolbox.netaddresstool import Network, SubNetwork, Netmask

# Plan subnets for a /22 network
parent = Network("10.10.0.0/22")
print(f"Parent: {parent}")
print(f"Total addresses: {parent.count + 2}")

# Divide into /24 subnets
calc = SubNetwork(parent, Netmask(24))
print("\nSubnets:")

for subnet in calc.iter_subnets():
    print(f"  {subnet}")
    print(f"    Range: {subnet.min} - {subnet.max}")
    print(f"    Hosts: {subnet.count}")
```

### Example 3: Address Validation

```python
from jsktoolbox.netaddresstool import Address, Network

def is_host_in_network(host_str, network_str):
    """Check if a host address belongs to a network."""
    try:
        host = Address(host_str)
        net = Network(network_str)
        return int(net.min) <= int(host) <= int(net.max)
    except ValueError:
        return False

# Test membership
print(is_host_in_network("192.168.1.50", "192.168.1.0/24"))  # True
print(is_host_in_network("192.168.2.1", "192.168.1.0/24"))   # False
print(is_host_in_network("10.0.0.0", "10.0.0.0/24"))         # False (network address)
```
