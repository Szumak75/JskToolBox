# Module Documentation: nettool.py

## Overview

The nettool.py module provides classes for basic network operations, such as ICMP echo (ping) testing and IPv4 route tracing (traceroute).  
Author: Jacek 'Szumak' Kotlarski  
Created: 29.08.2025

---

## Contents

### Classes

#### `Pinger`

Class for testing host availability using ICMP echo (ping).

- **Constructor:**  
  `Pinger(timeout: int = 1)`
  - `timeout`: Timeout in seconds for the ping operation.

- **Methods:**
  - `is_alive(ip: str) -> bool`  
    Checks if the given IP address responds to an ICMP echo request.

- **Properties:**
  - `__is_tool`  
    Checks for available system ping tools and returns the appropriate command and multiplier.

#### `Tracert`

Class for tracing the route to an IPv4 address (traceroute).

- **Constructor:**  
  `Tracert()`

- **Methods:**
  - `execute(ip: str) -> List[str]`  
    Performs a traceroute to the specified IPv4 address and returns the output as a list of strings.

- **Properties:**
  - `__is_tool`  
    Checks for available system traceroute tools and returns the appropriate command configuration.

---

## Requirements

- Linux/Unix system with access to: `fping`, `ping`, `traceroute`
- Dependencies:
  - `attribtool.ReadOnlyClass`
  - `raisetool.Raise`
  - `netaddresstool.ipv4.Address`
  - `basetool.data.BData`

---

## Usage Example

```python
from jsktoolbox.nettool import Pinger, Tracert

# Check host availability
pinger = Pinger(timeout=2)
if pinger.is_alive("8.8.8.8"):
    print("Host is reachable.")
else:
    print("Host is not responding.")

# Trace route to host
tracert = Tracert()
route = tracert.execute("8.8.8.8")
for line in route:
    print(line.strip())
```

---

## License

Copyright by the author.  
All rights reserved.

---

**[JskToolBox](https://github.com/jkotlarski/JskToolBox)**
