# NetAddressTool Module

**Source:** `jsktoolbox/netaddresstool/`

**Network Address Manipulation for IPv4 and IPv6:**
The NetAddressTool module provides comprehensive, type-safe utilities for working with IPv4 and IPv6 network addresses, masks, prefixes, subnets, and host enumeration. It enables precise network calculations, validation, and iteration with built-in safety limits to prevent accidental memory exhaustion when dealing with large address spaces.

## Getting Started

The module exposes two parallel sets of classes for IPv4 and IPv6 operations, along with configurable safety limits for legacy list-based helpers. Package-level imports now resolve lazily, so each submodule activates only when the exported symbol is accessed.

```python
from jsktoolbox.netaddresstool import (
    Address,
    Address6,
    DEFAULT_IPV4_HOST_LIMIT,
    DEFAULT_IPV4_SUBNET_LIMIT,
    DEFAULT_IPV6_HOST_LIMIT,
    DEFAULT_IPV6_SUBNET_LIMIT,
    Netmask,
    Network,
    Network6,
    Prefix6,
    SubNetwork,
    SubNetwork6,
)
```

Importing through the package keeps startup time low while maintaining IDE visibility into IPv4 and IPv6 utilities.

---

## NetAddressTool.IPv4

**Comprehensive IPv4 Address Manipulation:**
This submodule provides classes for representing and manipulating IPv4 addresses, network masks, network ranges, and subnet calculations. It supports multiple input formats including strings, integers, and lists, with automatic validation and conversion between representations.

[Detailed NetAddressTool.IPv4 Documentation](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool4.md)

### Global Configuration for IPv4

You can adjust safety limits that guard against materializing excessively large host or subnet lists in memory. These limits apply to deprecated list-based helper methods.

```python
from jsktoolbox.netaddresstool import (
    DEFAULT_IPV4_HOST_LIMIT,
    DEFAULT_IPV4_SUBNET_LIMIT,
)

# Override before calling deprecated APIs
DEFAULT_IPV4_HOST_LIMIT = 10_000
DEFAULT_IPV4_SUBNET_LIMIT = 8192
```

Both constants define the maximum number of hosts or subnetworks materialized by deprecated list-based helpers (`Network.hosts`, `SubNetwork.subnets`). For memory-safe processing, prefer the iterative APIs (`iter_hosts()`, `iter_subnets()`) that yield addresses lazily.

**Key Classes:**

- `Octet` - IPv4 octet representation (0-255)
- `Address` - Complete IPv4 address with multiple input format support
- `Netmask` - Network mask with CIDR and dotted-decimal notation
- `Network` - IPv4 network range with host enumeration
- `SubNetwork` - Subnet calculator for network subdivision

---

## NetAddressTool.IPv6

**Modern IPv6 Address Support:**
This submodule mirrors the IPv4 functionality for IPv6 addresses, using 128-bit addressing with prefix notation. It handles expanded and compressed IPv6 formats automatically, providing the same validation and iteration capabilities as its IPv4 counterpart.

[Detailed NetAddressTool.IPv6 Documentation](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool6.md)

### Global Configuration for IPv6

IPv6 networks can contain astronomically large address spaces. The module provides configurable safety limits for deprecated helpers that materialize addresses in memory.

```python
from jsktoolbox.netaddresstool import (
    DEFAULT_IPV6_HOST_LIMIT,
    DEFAULT_IPV6_SUBNET_LIMIT,
)

# Adjust limits before invoking deprecated helpers
DEFAULT_IPV6_HOST_LIMIT = 100_000
DEFAULT_IPV6_SUBNET_LIMIT = 1_024
```

Set these values before invoking deprecated list helpers (`Network6.hosts`, `SubNetwork6.subnets`) if your application requires different thresholds. Always prefer `iter_hosts()` and `iter_subnets()` for production code working with large address spaces.

**Key Classes:**

- `Word16` - IPv6 16-bit word representation (0x0000-0xFFFF)
- `Address6` - Complete IPv6 address with format auto-detection
- `Prefix6` - IPv6 network prefix (0-128)
- `Network6` - IPv6 network range with host enumeration
- `SubNetwork6` - IPv6 subnet calculator

---

## Usage Philosophy

The module follows a consistent design pattern across IPv4 and IPv6:

**Type Safety:** All classes validate input data and raise descriptive exceptions for invalid values, preventing silent failures.

**Multiple Input Formats:** Addresses and masks accept strings, integers, or component lists, automatically converting between representations.

**Comparison Support:** All address-like classes implement full comparison operators (==, !=, <, <=, >, >=) for natural sorting and range checks.

**Memory Safety:** Iterator-based methods (`iter_hosts()`, `iter_subnets()`) generate addresses lazily, allowing safe processing of large address spaces without memory exhaustion.

**Backward Compatibility:** Deprecated list-based methods remain available with configurable safety limits, issuing deprecation warnings to encourage migration to iterators.

---

## Examples

**IPv4 Network Operations:**

```python
from jsktoolbox.netaddresstool import Network

# Create network from CIDR notation
net = Network("192.168.1.0/24")

# Access network properties
print(f"Network: {net.network}")        # 192.168.1.0
print(f"Broadcast: {net.broadcast}")    # 192.168.1.255
print(f"Hosts: {net.count}")            # 254

# Iterate hosts safely
for host in net.iter_hosts():
    print(host)  # 192.168.1.1, 192.168.1.2, ..., 192.168.1.254
```

**IPv6 Network Operations:**

```python
from jsktoolbox.netaddresstool import Network6

# Create IPv6 network
net = Network6("2001:db8::/32")

# Access properties
print(f"Network: {net.network}")
print(f"First: {net.min}")
print(f"Last: {net.max}")

# Safe iteration with limit
for host in net.iter_hosts(limit=1000):
    print(host)
```

---

## Migration Guide

If you're using deprecated list-based methods, migration to iterators is straightforward:

**Before (deprecated):**

```python
hosts = network.hosts()
for host in hosts:
    process(host)
```

**After (recommended):**

```python
for host in network.iter_hosts():
    process(host)
```

The iterator version uses negligible memory regardless of network size and provides the same safety limit mechanism through the `limit` parameter. Pass `limit=None` to explicitly disable guards when processing known-safe networks.
