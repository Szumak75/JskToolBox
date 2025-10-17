# NetAddressTool.IPv6 Module

**Source:** `jsktoolbox/netaddresstool/ipv6.py`

**IPv6 Network Address Manipulation:**
The IPv6 submodule provides comprehensive support for working with 128-bit IPv6 addresses, network prefixes, and subnet calculations. It handles both expanded and compressed IPv6 notation automatically, validates address formats, and provides memory-efficient iteration over potentially massive address spaces. The module mirrors the IPv4 API design while accounting for IPv6-specific concepts like prefix length instead of netmasks and the absence of broadcast addresses.

## Getting Started

Import the classes needed for IPv6 network operations. Package-level imports resolve symbols lazily, so each submodule activates only when the requested class is accessed. The module provides components ranging from low-level word representation to high-level network calculations.

```python
from jsktoolbox.netaddresstool import Address6, Prefix6, Network6, SubNetwork6
from jsktoolbox.netaddresstool import Word16
```

This lazy loading keeps startup time predictable even when the IPv6 helpers bring in heavier dependencies.

---

## Public Classes

1. [Word16](#word16) - IPv6 16-bit word representation (0x0000-0xFFFF)
1. [Address6](#address6) - Complete IPv6 address
1. [Prefix6](#prefix6) - Network prefix length (0-128)
1. [Network6](#network6) - IPv6 network range
1. [SubNetwork6](#subnetwork6) - IPv6 subnet calculator

---

## `Word16` Class

**Building Block for IPv6 Addresses:**
The Word16 class represents a single 16-bit word (hextet) of an IPv6 address with comprehensive validation and type conversion. It accepts both decimal and hexadecimal input formats and provides hexadecimal string output without the '0x' prefix. This class forms the foundation for the Address6 class but can also be used independently for validated 16-bit value operations.

### `Word16.__init__()`

**Initialize an IPv6 Word:**
Creates a 16-bit word with automatic validation and type conversion. The constructor accepts decimal integers, decimal strings, hexadecimal strings (with or without '0x' prefix), or other Word16 instances.

**Signature:**

```python
Word16(value: Union[str, int, Word16])
```

- **Arguments:**
  - `value: Union[str, int, Word16]` - Word value as integer (0-65535), decimal/hex string ("255", "0xFF"), or another Word16 instance.
- **Returns:**
  - `Word16` - A validated 16-bit word instance.
- **Raises:**
  - `ValueError`: Value outside 0-65535 range or invalid string format.
  - `TypeError`: Invalid input type.

**Usage Example:**

```python
from jsktoolbox.netaddresstool.libs.words import Word16

# Create words from different formats
word1 = Word16(255)           # Decimal integer
word2 = Word16("255")         # Decimal string
word3 = Word16("0xFF")        # Hexadecimal string
word4 = Word16("FF")          # Hex without prefix
word5 = Word16(word1)         # From another Word16

# All represent the same value
assert word1 == word2 == word3 == word4 == word5

# Comparison operations
assert Word16(0x1000) > Word16(0x0FFF)
assert Word16("FFFF") == Word16(65535)

# String output is hexadecimal
print(str(word1))  # "ff"
print(int(word1))  # 255
```

---

### `Word16.value`

**Get Word as Integer:**
Returns the word's value as an integer in the 0-65535 range. This property provides direct access to the validated internal value.

**Signature:**

```python
@property
def value(self) -> int
```

- **Returns:**
  - `int` - Word value as integer (0-65535).

**Usage Example:**

```python
word = Word16("0x1234")
value = word.value  # 4660
```

---

### `Word16.value` (setter)

**Set Word Value with Validation:**
Assigns a new value to the word with automatic validation. The setter accepts the same input formats as the constructor and immediately validates the range.

**Signature:**

```python
@value.setter
def value(self, args: Union[str, int, Word16]) -> None
```

- **Arguments:**
  - `args: Union[str, int, Word16]` - New word value in any supported format.
- **Raises:**
  - `ValueError`: Value outside 0-65535 range or invalid string.
  - `TypeError`: Invalid input type.

**Usage Example:**

```python
word = Word16(0)
word.value = 0xFFFF    # Set to maximum
word.value = "8080"    # Set from decimal string
word.value = "0x2000"  # Set from hex string

# ValueError: out of range
try:
    word.value = 65536
except ValueError as e:
    print(f"Error: {e}")
```

---

## `Address6` Class

**Complete IPv6 Address Representation:**
The Address6 class provides comprehensive representation of 128-bit IPv6 addresses with support for multiple input formats including compressed notation (::), expanded notation, integers, and word component lists. It automatically handles format conversion and validation, internally storing addresses as 128-bit integers for efficient comparisons while providing both compressed and expanded string representations.

### `Address6.__init__()`

**Create an IPv6 Address:**
Initializes an IPv6 address from various input formats including standard notation with compression, 128-bit integers, or lists of eight 16-bit word components. The constructor automatically validates addresses and converts them to the internal integer representation.

**Signature:**

```python
Address6(addr: Union[str, int, Union[List[int], List[str], List[Word16]]])
```

- **Arguments:**
  - `addr: Union[str, int, List]` - IPv6 address as string ("2001:db8::1"), integer, or list of eight word values.
- **Returns:**
  - `Address6` - A validated IPv6 address instance.
- **Raises:**
  - `ValueError`: Invalid IPv6 address format or value.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
from jsktoolbox.netaddresstool.ipv6 import Address6

# Multiple input formats
addr1 = Address6("2001:db8::1")                           # Compressed
addr2 = Address6("2001:0db8:0000:0000:0000:0000:0000:0001")  # Expanded
addr3 = Address6("::1")                                   # Loopback
addr4 = Address6(1)                                       # As integer
addr5 = Address6([0, 0, 0, 0, 0, 0, 0, 1])              # From words

# Comparison operations
assert Address6("::1") < Address6("::2")
assert Address6("2001:db8::1") == Address6("2001:0db8::1")

# String representation uses compression
print(str(Address6("2001:0db8:0000:0000:0000:0000:0000:0001")))  # "2001:db8::1"
```

---

### `Address6.words`

**Get Address as Word List:**
Returns the IPv6 address as a list of eight Word16 objects representing the expanded address. This provides a decomposed view useful for word-level inspection. The returned list represents the fully expanded address format.

**Signature:**

```python
@property
def words(self) -> List[Word16]
```

- **Returns:**
  - `List[Word16]` - List of eight Word16 objects representing the address.

**Usage Example:**

```python
addr = Address6("2001:db8::1")
words = addr.words

# Access individual words
print(words[0])  # Word16(8193) -> "2001"
print(words[1])  # Word16(3512) -> "0db8"
print(words[7])  # Word16(1)    -> "0001"

# Extract integer values
values = [int(w) for w in words]  # [8193, 3512, 0, 0, 0, 0, 0, 1]
```

---

### `Address6.words` (setter)

**Set Address from Various Formats:**
Assigns a new IPv6 address from any supported input format with automatic validation. This setter accepts the same formats as the constructor.

**Signature:**

```python
@words.setter
def words(self, value: Union[str, int, Union[List[int], List[str], List[Word16]]]) -> None
```

- **Arguments:**
  - `value: Union[str, int, List]` - New address in any supported format.
- **Raises:**
  - `ValueError`: Invalid address format or out-of-range values.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
addr = Address6("::")

# Update using different formats
addr.words = "2001:db8::1"
addr.words = [0x2001, 0xdb8, 0, 0, 0, 0, 0, 1]
addr.words = 42540766411282592856903984951653826561  # As 128-bit int

# String and integer conversion
ip_string = str(addr)     # Compressed notation
ip_integer = int(addr)    # 128-bit integer
```

---

## `Prefix6` Class

**IPv6 Network Prefix Representation:**
The Prefix6 class represents IPv6 network prefix lengths (0-128), which are equivalent to CIDR notation in IPv4 but specific to IPv6's 128-bit address space. The prefix defines how many bits of the address represent the network portion versus the host portion. It provides validation and comparison operations for prefix values.

### `Prefix6.__init__()`

**Create a Network Prefix:**
Initializes a prefix with validation. IPv6 prefixes range from 0 (the entire Internet) to 128 (a single host).

**Signature:**

```python
Prefix6(prefix: Union[str, int])
```

- **Arguments:**
  - `prefix: Union[str, int]` - Prefix length as integer (0-128) or string ("0"-"128").
- **Returns:**
  - `Prefix6` - A validated prefix instance.
- **Raises:**
  - `ValueError`: Prefix outside 0-128 range or non-integer string.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
from jsktoolbox.netaddresstool.ipv6 import Prefix6

# Create prefixes
prefix1 = Prefix6(64)      # Standard /64 subnet
prefix2 = Prefix6("48")    # /48 allocation
prefix3 = Prefix6(128)     # Single host

# Comparison operations
assert Prefix6(64) > Prefix6(48)   # More specific
assert Prefix6(0) < Prefix6(128)   # Less specific

# Conversions
print(str(prefix1))  # "64"
print(int(prefix1))  # 64
```

---

### `Prefix6.prefix`

**Get Prefix as String:**
Returns the prefix length as a string representation of the integer value.

**Signature:**

```python
@property
def prefix(self) -> str
```

- **Returns:**
  - `str` - Prefix length as string ("0" through "128").

**Usage Example:**

```python
prefix = Prefix6(64)
length = prefix.prefix  # "64"
```

---

### `Prefix6.prefix` (setter)

**Set Prefix with Validation:**
Assigns a new prefix value with range validation. Accepts integers or digit strings in the 0-128 range.

**Signature:**

```python
@prefix.setter
def prefix(self, value: Union[str, int]) -> None
```

- **Arguments:**
  - `value: Union[str, int]` - Prefix value (0-128) as integer or string.
- **Raises:**
  - `ValueError`: Prefix outside 0-128 range or non-digit string.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
prefix = Prefix6(64)
prefix.prefix = 48        # Change to /48
prefix.prefix = "128"     # Change to /128 (host)

# ValueError: out of range
try:
    prefix.prefix = 129
except ValueError as e:
    print(f"Error: {e}")
```

---

## `Network6` Class

**IPv6 Network Range Representation:**
The Network6 class represents a complete IPv6 network defined by an address and prefix length. Unlike IPv4, IPv6 networks don't have broadcast addresses but still provide network and host address ranges. The class handles potentially massive address spaces (a /64 subnet contains 2^64 addresses) through lazy iteration with configurable safety limits to prevent memory exhaustion.

### `Network6.__init__()`

**Create an IPv6 Network:**
Initializes a network from CIDR notation or an address-prefix pair. The network address is automatically calculated from the provided address and prefix, regardless of whether the input address is the network address or any host address within the subnet.

**Signature:**

```python
Network6(addr: Union[str, List])
```

- **Arguments:**
  - `addr: Union[str, List]` - Network as CIDR string ("2001:db8::/32") or two-element list [Address6/str/int, Prefix6/str/int].
- **Returns:**
  - `Network6` - A network instance with calculated addresses.
- **Raises:**
  - `ValueError`: Invalid network format or incompatible address/prefix combination.
  - `TypeError`: Unsupported input type.

**Usage Example:**

```python
from jsktoolbox.netaddresstool.ipv6 import Network6, Address6, Prefix6

# Create from CIDR notation
net1 = Network6("2001:db8::/32")
net2 = Network6("2001:db8::1234/32")  # Any address works

# Create from components
net3 = Network6([Address6("fe80::"), Prefix6(64)])
net4 = Network6(["::1", 128])

# All produce proper network addresses
print(net1.network)  # 2001:db8::
print(net2.network)  # 2001:db8:: (same network)
```

---

### `Network6.address`

**Get Original Input Address:**
Returns the address that was provided to the constructor, before network address calculation. This preserves the original host or arbitrary address that defined the network.

**Signature:**

```python
@property
def address(self) -> Address6
```

- **Returns:**
  - `Address6` - The original address used to create the network.

**Usage Example:**

```python
net = Network6("2001:db8::50/64")
print(net.address)   # 2001:db8::50 (input address)
print(net.network)   # 2001:db8:: (calculated network)
```

---

### `Network6.count`

**Get Address Count:**
Returns the total number of addresses in the network range. For IPv6, this can be astronomically large (a /64 contains 2^64 = 18,446,744,073,709,551,616 addresses). Use this property carefully as it returns the mathematical count, not a materialized list.

**Signature:**

```python
@property
def count(self) -> int
```

- **Returns:**
  - `int` - Number of addresses in the network (including network address).

**Usage Example:**

```python
net = Network6("2001:db8::/64")
print(net.count)  # 18446744073709551616 (2^64)

net = Network6("fe80::/10")
print(net.count)  # 332306998946228968225951765070086144 (2^118)

net = Network6("::1/128")
print(net.count)  # 1 (single host)
```

---

### `Network6.hosts()` _(deprecated)_

**Get Host List with Safety Limit:**
Returns a materialized list of all addresses in the network range. This method is deprecated because IPv6 networks can contain truly massive address spaces that would exhaust all available memory. Use `iter_hosts()` for memory-safe lazy iteration.

**Signature:**

```python
def hosts(self, limit: Optional[int] = DEFAULT_IPV6_HOST_LIMIT) -> List[Address6]
```

- **Arguments:**
  - `limit: Optional[int]` - Maximum addresses allowed to materialize. Defaults to `DEFAULT_IPV6_HOST_LIMIT` (65536). Pass `None` to disable (dangerous).
- **Returns:**
  - `List[Address6]` - List of addresses.
- **Raises:**
  - `ValueError`: Address count exceeds the configured limit.

**Usage Example:**

```python
net = Network6("2001:db8::/120")  # 256 addresses

# Deprecated: materializes entire list
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    hosts = net.hosts()  # Returns list

# Large network would fail
try:
    big_net = Network6("2001:db8::/64")
    hosts = big_net.hosts()  # Exceeds default limit
except ValueError as e:
    print(f"Too many addresses: {e}")
```

---

### `Network6.iter_hosts()`

**Iterate Addresses Lazily:**
Returns a generator that yields addresses one at a time without materializing the entire list in memory. This is the only safe way to process large IPv6 networks. The safety limit prevents accidental unbounded iteration that could run for geological time periods on very large subnets.

**Signature:**

```python
def iter_hosts(self, limit: Optional[int] = DEFAULT_IPV6_HOST_LIMIT) -> Iterator[Address6]
```

- **Arguments:**
  - `limit: Optional[int]` - Maximum addresses before raising. Defaults to `DEFAULT_IPV6_HOST_LIMIT`. Pass `None` for unlimited (use with caution).
- **Returns:**
  - `Iterator[Address6]` - Generator yielding addresses in ascending order.
- **Raises:**
  - `ValueError`: Address count exceeds limit (checked before iteration begins).

**Usage Example:**

```python
net = Network6("2001:db8::/120")

# Memory-efficient iteration
for addr in net.iter_hosts():
    print(addr)  # Process one at a time

# Convert to list if needed (small networks only)
addresses = list(net.iter_hosts(limit=256))

# Disable limit for controlled processing
large_net = Network6("2001:db8::/64")
for i, addr in enumerate(large_net.iter_hosts(limit=None)):
    # Process with explicit control
    process(addr)
    if i >= 1000:  # Process first 1000 only
        break
```

---

### `Network6.max`

**Get Last Address:**
Returns the highest address in the network range. This is the last address that can be assigned within the subnet.

**Signature:**

```python
@property
def max(self) -> Address6
```

- **Returns:**
  - `Address6` - Last address in the network.

**Usage Example:**

```python
net = Network6("2001:db8::/120")
print(net.max)  # 2001:db8::ff

net = Network6("fe80::/10")
print(net.max)  # febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff
```

---

### `Network6.min`

**Get First Address:**
Returns the lowest address in the network range. This is the network address itself and can be used for host assignment in IPv6 (unlike IPv4 where the network address is reserved).

**Signature:**

```python
@property
def min(self) -> Address6
```

- **Returns:**
  - `Address6` - First address in the network.

**Usage Example:**

```python
net = Network6("2001:db8::/64")
print(net.min)  # 2001:db8::

# In IPv6, the network address can be assigned to hosts
print(net.min == net.network)  # True
```

---

### `Network6.network`

**Get Network Address:**
Returns the network's base address with all host bits set to zero. This is the canonical network identifier used in routing and CIDR notation.

**Signature:**

```python
@property
def network(self) -> Address6
```

- **Returns:**
  - `Address6` - The network address.

**Usage Example:**

```python
net = Network6("2001:db8::1234/32")
print(net.network)  # 2001:db8::

# String representation includes prefix
print(str(net))  # "2001:db8::/32"
```

---

### `Network6.prefix`

**Get Network Prefix:**
Returns the prefix length that defines this network's size and range.

**Signature:**

```python
@property
def prefix(self) -> Prefix6
```

- **Returns:**
  - `Prefix6` - The network's prefix.

**Usage Example:**

```python
net = Network6("2001:db8::/48")
prefix = net.prefix
print(prefix.prefix)  # "48"
print(int(prefix))    # 48
```

---

## `SubNetwork6` Class

**IPv6 Subnet Calculator:**
The SubNetwork6 class generates all subnets of a given prefix length within a parent network. Due to IPv6's vast address space, even relatively small prefix differences can generate enormous numbers of subnets (dividing a /48 into /64s creates 65,536 subnets). The class uses lazy iteration with safety limits to handle these calculations efficiently.

### `SubNetwork6.__init__()`

**Create a Subnet Calculator:**
Initializes a subnet calculator for dividing a parent network into smaller subnets. The subnet prefix must be equal to or larger (more specific, numerically higher) than the parent network's prefix.

**Signature:**

```python
SubNetwork6(network: Network6, prefix: Prefix6)
```

- **Arguments:**
  - `network: Network6` - Parent network to subdivide.
  - `prefix: Prefix6` - Subnet prefix for the desired subnets (must be >= parent prefix).
- **Returns:**
  - `SubNetwork6` - A subnet calculator instance.
- **Raises:**
  - `ValueError`: Subnet prefix smaller than parent network prefix.
  - `TypeError`: Invalid argument types.

**Usage Example:**

```python
from jsktoolbox.netaddresstool.ipv6 import SubNetwork6

# Divide /48 into /64 subnets (65,536 subnets)
parent = Network6("2001:db8::/48")
subnets = SubNetwork6(parent, Prefix6(64))

# Invalid: subnet prefix smaller than parent
try:
    invalid = SubNetwork6(Network6("2001:db8::/48"), Prefix6(32))
except ValueError as e:
    print(f"Error: {e}")
```

---

### `SubNetwork6.subnets()` _(deprecated)_

**Get Subnet List with Safety Limit:**
Returns a materialized list of all subnets. This method is deprecated because IPv6 subnet counts can be extremely large and exhaust memory. Use `iter_subnets()` for memory-safe lazy iteration.

**Signature:**

```python
def subnets(self, limit: Optional[int] = DEFAULT_IPV6_SUBNET_LIMIT) -> List[Network6]
```

- **Arguments:**
  - `limit: Optional[int]` - Maximum subnets allowed. Defaults to `DEFAULT_IPV6_SUBNET_LIMIT` (4096). Pass `None` to disable (risky).
- **Returns:**
  - `List[Network6]` - List of subnet Network6 objects.
- **Raises:**
  - `ValueError`: Subnet count exceeds the configured limit.

**Usage Example:**

```python
parent = Network6("2001:db8::/125")
calc = SubNetwork6(parent, Prefix6(127))

# Deprecated: materializes entire list
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    subnet_list = calc.subnets()  # Returns list of 4 networks
```

---

### `SubNetwork6.iter_subnets()`

**Iterate Subnets Lazily:**
Returns a generator that yields subnet Network6 objects one at a time without materializing the entire list in memory. This is the recommended approach for processing subnets, especially when dealing with large parent networks where even reasonable prefix differences can create thousands or millions of subnets.

**Signature:**

```python
def iter_subnets(self, limit: Optional[int] = DEFAULT_IPV6_SUBNET_LIMIT) -> Iterator[Network6]
```

- **Arguments:**
  - `limit: Optional[int]` - Maximum subnets before raising. Defaults to `DEFAULT_IPV6_SUBNET_LIMIT`. Pass `None` for unlimited.
- **Returns:**
  - `Iterator[Network6]` - Generator yielding Network6 objects in ascending address order.
- **Raises:**
  - `ValueError`: Subnet count exceeds limit (checked after each subnet).

**Usage Example:**

```python
# Divide /125 into /127 subnets (4 subnets)
parent = Network6("2001:db8::/ 125")
calc = SubNetwork6(parent, Prefix6(127))

# Memory-efficient iteration
for subnet in calc.iter_subnets():
    print(f"{subnet} contains {subnet.count} addresses")
# Output:
# 2001:db8::/127 contains 2 addresses
# 2001:db8::2/127 contains 2 addresses
# 2001:db8::4/127 contains 2 addresses
# 2001:db8::6/127 contains 2 addresses

# Convert to list if needed (small counts only)
subnets = list(calc.iter_subnets())

# Disable limit for large operations (use with caution)
large_parent = Network6("2001:db8::/48")
large_calc = SubNetwork6(large_parent, Prefix6(64))
for i, subnet in enumerate(large_calc.iter_subnets(limit=None)):
    # Process 65,536 /64 subnets
    process_subnet(subnet)
    if i >= 100:  # Process first 100 only
        break
```

---

## Complete Examples

### Example 1: IPv6 Network Analysis

```python
from jsktoolbox.netaddresstool.ipv6 import Network6

# Analyze a network
net = Network6("2001:db8::/48")

print(f"Network: {net.network}")
print(f"Prefix: /{net.prefix.prefix}")
print(f"First address: {net.min}")
print(f"Last address: {net.max}")
print(f"Total addresses: {net.count:,}")

# Process a manageable subnet
small_net = Network6("2001:db8::/120")
print(f"\nProcessing {small_net}:")
for i, addr in enumerate(small_net.iter_hosts(), 1):
    print(f"  {i}. {addr}")
    if i >= 5:
        remaining = small_net.count - 5
        print(f"  ... and {remaining:,} more")
        break
```

### Example 2: IPv6 Subnet Planning

```python
from jsktoolbox.netaddresstool.ipv6 import Network6, SubNetwork6, Prefix6

# Plan /64 subnets within a /48 allocation
parent = Network6("2001:db8::/48")
print(f"Parent: {parent}")
print(f"Total addresses: {parent.count:,}")

# Divide into /64 subnets (standard size)
calc = SubNetwork6(parent, Prefix6(64))
print("\nFirst 10 /64 subnets:")

for i, subnet in enumerate(calc.iter_subnets(limit=None), 1):
    print(f"  {subnet}")
    if i >= 10:
        total = 2 ** (64 - 48)  # 65,536 total subnets
        print(f"  ... and {total - 10:,} more /64 subnets")
        break
```

### Example 3: IPv6 Address Validation and Comparison

```python
from jsktoolbox.netaddresstool.ipv6 import Address6, Network6

def is_address_in_network(addr_str, network_str):
    """Check if an IPv6 address belongs to a network."""
    try:
        addr = Address6(addr_str)
        net = Network6(network_str)
        return int(net.min) <= int(addr) <= int(net.max)
    except ValueError:
        return False

# Test membership
print(is_address_in_network("2001:db8::1", "2001:db8::/32"))    # True
print(is_address_in_network("2001:db9::1", "2001:db8::/32"))    # False
print(is_address_in_network("::1", "::1/128"))                  # True

# Address comparison
addrs = [
    Address6("2001:db8::1"),
    Address6("::1"),
    Address6("fe80::1"),
    Address6("2001:db8::ffff"),
]

# Sort addresses
for addr in sorted(addrs):
    print(f"{addr} = {int(addr)}")
```

### Example 4: Working with Link-Local Addresses

```python
from jsktoolbox.netaddresstool.ipv6 import Network6

# IPv6 link-local prefix
link_local = Network6("fe80::/10")

print(f"Link-local range: {link_local}")
print(f"First: {link_local.min}")
print(f"Last: {link_local.max}")
print(f"Total addresses: {link_local.count:,}")

# Typical link-local /64 subnet
typical_ll = Network6("fe80::/64")
print(f"\nTypical link-local subnet: {typical_ll}")
print(f"EUI-64 example: fe80::1234:5678:90ab:cdef/{typical_ll.prefix.prefix}")
```
