# NetAddressTool

## NetAddressTool.IPv4

The project contains sets of base classes for operations on IPv4 addresses.

[NetAddressTool.IPv4 Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool4.md)

### Global Configuration

You can adjust legacy helper safeguards at runtime:

```python
from jsktoolbox.netaddresstool import (
    DEFAULT_IPV4_HOST_LIMIT,
    DEFAULT_IPV4_SUBNET_LIMIT,
)

DEFAULT_IPV4_HOST_LIMIT = 10_000  # override before calling deprecated APIs
```

Both constants define the maximum number of hosts or subnetworks materialised by
deprecated list-based helpers (`Network.hosts`, `SubNetwork.subnets`). Use the
iterative APIs for memory-safe processing whenever possible.

## NetAddressTool.IPv6

The project contains sets of base classes for operations on IPv6 addresses.

[NetAddressTool.IPv6 Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool6.md)

### Global Configuration

IPv6 counterparts expose similar guard rails:

```python
from jsktoolbox.netaddresstool import (
    DEFAULT_IPV6_HOST_LIMIT,
    DEFAULT_IPV6_SUBNET_LIMIT,
)

DEFAULT_IPV6_SUBNET_LIMIT = 1_024
```

Set these values before invoking deprecated list helpers (`Network6.hosts`,
`SubNetwork6.subnets`) if you need custom thresholds.
