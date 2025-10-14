# NetTool Module

**Source:** `jsktoolbox/nettool.py`

**High-Level Introduction:**
A lightweight toolkit for reachability checks, route tracing, and hostname validation built on top of common system networking utilities.

## Getting Started

```python
from jsktoolbox.nettool import Pinger, Tracert, HostResolvableChecker
```

---

## `Pinger` Class

**Class Introduction:**
Wraps platform ping commands (`fping`, `ping`) to provide a uniform, timeout-aware reachability check for IPv4 hosts.

### `Pinger.__init__(timeout: int = 1)`

**Detailed Description:**
Initialises the ping command registry and selects the first available executable, applying the provided timeout multiplier.

**Signature:**
```python
Pinger(timeout: int = 1)
```

- **Arguments:**
  - `timeout: int` - Timeout in seconds; defaults to 1.
- **Returns:**
  - `None` - Constructor.
- **Raises:**
  - `ValueError`: Propagated when an invalid timeout is passed to the internal data store.

**Usage Example:**
```python
pinger = Pinger(timeout=2)
if pinger.is_alive("8.8.8.8"):
    print("Google DNS is reachable")
```

### `Pinger.is_alive(ip: str)`

**Detailed Description:**
Executes the previously selected ping command and reports whether ICMP echo succeeds for the given IPv4 address.

**Signature:**
```python
is_alive(ip: str) -> bool
```

- **Arguments:**
  - `ip: str` - IPv4 address to test.
- **Returns:**
  - `bool` - True if the host responds.
- **Raises:**
  - `ChildProcessError`: Raised when no ping command is available on the system.

**Usage Example:**
```python
if not pinger.is_alive("203.0.113.10"):
    raise RuntimeError("Host down")
```

---

## `Tracert` Class

**Class Introduction:**
Provides traceroute execution with multiple command templates, selecting whichever tool (`traceroute`) is installed.

### `Tracert.__init__()`

**Detailed Description:**
Populates traceroute command candidates, probing the environment for a usable executable.

**Signature:**
```python
Tracert()
```

- **Arguments:**
  - _None_
- **Returns:**
  - `None`

### `Tracert.execute(ip: str)`

**Detailed Description:**
Runs traceroute against an IPv4 destination and captures the command output as a list of strings.

**Signature:**
```python
execute(ip: str) -> List[str]
```

- **Arguments:**
  - `ip: str` - Target IPv4 address.
- **Returns:**
  - `List[str]` - Raw stdout lines from traceroute.
- **Raises:**
  - `ChildProcessError`: When traceroute is unavailable.

**Usage Example:**
```python
tracer = Tracert()
for hop in tracer.execute("8.8.8.8"):
    print(hop.strip())
```

---

## `HostResolvableChecker` Class

**Class Introduction:**
Static helper methods for validating host strings and retrieving resolved IP addresses.

### `HostResolvableChecker.is_resolvable(host: str)`

**Detailed Description:**
Leverages `socket.getaddrinfo` to determine if the host resolves on the current system.

**Signature:**
```python
is_resolvable(host: str) -> bool
```

- **Arguments:**
  - `host: str` - Hostname or IP literal.
- **Returns:**
  - `bool` - True if resolution succeeds.

### `HostResolvableChecker.validate_host(host: str)`

**Detailed Description:**
Checks whether the string is a valid IP address or resolvable hostname, returning an explanatory error when invalid.

**Signature:**
```python
validate_host(host: str) -> Optional[str]
```

- **Arguments:**
  - `host: str`
- **Returns:**
  - `Optional[str]` - None when valid; error message otherwise.

### `HostResolvableChecker.ip4_from_hostname(hostname: str)`

**Detailed Description:**
Resolves the first IPv4 address for the provided hostname and wraps it in an `Address` object.

**Signature:**
```python
ip4_from_hostname(hostname: str) -> Optional[Address]
```

- **Arguments:**
  - `hostname: str`
- **Returns:**
  - `Optional[Address]`

### Additional Helpers

- `is_ip_address(host: str) -> bool`
- `is_hostname(host: str) -> bool`
- `ip_from_hostname(hostname: str) -> Optional[str>`
- `validate_hosts(hosts: List[str]) -> Dict[str, Optional[str]]`
- `filter_valid_hosts(hosts: List[str]) -> List[str]`
- `filter_invalid_hosts(hosts: List[str]) -> Dict[str, str]`
- `ip6_from_hostname(hostname: str) -> Optional[Address6]`

These methods provide convenience wrappers for bulk operations and IPv6 resolution.

---

## Dependencies

- System binaries: `fping`, `ping`, `traceroute`
- Core modules: `socket`, `subprocess`, `re`
- Internal dependencies: `jsktoolbox.attribtool`, `jsktoolbox.netaddresstool`, `jsktoolbox.raisetool`

---

## Example Workflow

```python
from jsktoolbox.nettool import Pinger, Tracert, HostResolvableChecker

hosts = ["1.1.1.1", "example.com", "invalid_host"]

# Validate host list
invalid = HostResolvableChecker.filter_invalid_hosts(hosts)
if invalid:
    print("Invalid hosts:", invalid)

# Ping only valid entries
pinger = Pinger()
for host in HostResolvableChecker.filter_valid_hosts(hosts):
    if pinger.is_alive(host):
        print(f"{host} is reachable")

# Trace route for a single host
Tracert().execute("1.1.1.1")
```

---

**JskToolBox Project**
