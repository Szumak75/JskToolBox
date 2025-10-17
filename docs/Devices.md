# Devices Module

**Source:** `jsktoolbox/devices`

**High-Level Introduction:**
The devices package aggregates reusable helpers for network-enabled equipment. It centralises debugging flags, connector plumbing, MikroTik RouterOS abstractions, and binary converters behind a single namespace. Each export is delivered through a lazy loader, so heavy dependencies load only after the symbol is accessed.

## Getting Started

Import the components required for your workflow. The package-level imports resolve lazily, keeping startup time low for scripts that touch only a subset of device helpers.

```python
from jsktoolbox.devices import (
    API,
    BDebug,
    BDev,
    BRouterOS,
    B64Converter,
    Element,
    IConnector,
    RouterBoard,
)
```

Lazy loading means you can import the entire surface while only instantiating the connectors or RouterOS wrappers you need.

---

## `BDebug` Class

**Class Introduction:**
`BDebug` exposes boolean flags that toggle verbose output for device-oriented classes. It stores the values inside a protected dictionary managed by the base data mixin, so any subclass inherits consistent debug handling.

### `BDebug.debug`

**Detailed Description:**
Property accessor that returns or updates the debug flag. When set to `True`, downstream classes can opt in to extra diagnostics.

**Signature:**

```python
@property
def debug(self) -> bool

@debug.setter
def debug(self, debug: bool) -> None
```

- **Returns:**
  - `bool` - Current debug flag.
- **Raises:**
  - `TypeError`: If a non-boolean value is assigned.

**Usage Example:**

```python
helper = BDebug()
helper.debug = True
assert helper.debug
```

### `BDebug.verbose`

**Detailed Description:**
Mirrors the behaviour of the `debug` property but tracks verbose output separately, giving callers granular control over logging verbosity.

**Signature:**

```python
@property
def verbose(self) -> bool

@verbose.setter
def verbose(self, verbose: bool) -> None
```

- **Returns:**
  - `bool` - Current verbose flag.

---

## `BDev` Class

**Class Introduction:**
`BDev` combines connector wiring, logging clients, and hierarchical root handling for device trees. It inherits `BDebug`, so subclasses gain both logging flags and stateful helpers managed by the typed data container.

### `BDev._ch`

**Detailed Description:**
Protected property that stores the active connector implementing `IConnector`. It enables device nodes to communicate with their backend transport.

**Signature:**

```python
@property
def _ch(self) -> Optional[IConnector]

@_ch.setter
def _ch(self, value: IConnector) -> None
```

- **Returns:**
  - `Optional[IConnector]` - Currently bound connector.

### `BDev.logs`

**Detailed Description:**
Manages the `LoggerClient` instance used for messaging. Subclasses rely on this to emit warnings or debug statements related to remote operations.

**Signature:**

```python
@property
def logs(self) -> Optional[LoggerClient]

@logs.setter
def logs(self, value: LoggerClient) -> None
```

- **Returns:**
  - `Optional[LoggerClient]` - The logger bound to the device.

### `BDev.root`

**Detailed Description:**
Constructs a RouterOS-style path prefix that honours the entire parent chain. This keeps nested devices in sync with their top-level command path.

**Signature:**

```python
@property
def root(self) -> str

@root.setter
def root(self, value: str) -> None
```

- **Returns:**
  - `str` - Aggregated command prefix.

---

## `B64Converter` Class

**Class Introduction:**
Utility class that converts text to and from Base64, ensuring byte-safe interchange with RouterOS APIs or device files.

### `B64Converter.string_to_base64()`

**Detailed Description:**
Encodes a UTF-8 string to Base64 bytes. Useful when RouterOS commands expect encoded payloads.

**Signature:**

```python
@staticmethod
def string_to_base64(value: str) -> bytes
```

- **Arguments:**
  - `value: str` - Plain text to encode.
- **Returns:**
  - `bytes` - Base64-encoded payload.

### `B64Converter.base64_to_string()`

**Detailed Description:**
Decodes Base64 bytes back to a UTF-8 string. Raises a `ValueError` through `Raise` when the payload cannot be decoded.

**Signature:**

```python
@staticmethod
def base64_to_string(data: bytes) -> str
```

- **Arguments:**
  - `data: bytes` - Base64-encoded payload.
- **Returns:**
  - `str` - Decoded text.

---

## `IConnector` Interface

**Class Introduction:**
Abstract base class defining the contract implemented by device connectors. It standardises connection lifecycle, credential management, and command execution across transports such as API and SSH.

### Required Methods

- `connect() -> bool` / `disconnect() -> bool` — manage session lifecycle.
- `execute(commands: Union[str, List[str]]) -> bool` — send commands to the remote endpoint.
- `outputs() -> Tuple[List[List[Dict[str, Any]]], List[List[Dict[str, Any]]]]` — retrieve buffered stdout and stderr.

**Usage Example:**

```python
def ensure_connected(connector: IConnector) -> None:
    if not connector.connect():
        raise RuntimeError("Unable to connect")
```

---

## `API` Class

**Class Introduction:**
Concrete `IConnector` implementation for MikroTik RouterOS API transport. It handles authentication, request framing, and response parsing via the MikroTik binary protocol.

### `API.__init__()`

**Detailed Description:**
Configures connection parameters including host, port, credentials, timeout, and SSL usage. Values are stored via the base data container to support runtime updates.

**Signature:**

```python
API(
    ip_address: Optional[Union[Address, Address6]] = None,
    port: int = 8728,
    login: Optional[str] = None,
    password: Optional[str] = None,
    timeout: float = 60.0,
    use_ssl: bool = False,
    debug: bool = False,
    verbose: bool = False,
)
```

- **Arguments:**
  - `ip_address: Optional[Union[Address, Address6]]` - Target device address.
  - `port: int` - API port, default `8728`.
  - `login: Optional[str]` - Username for RouterOS API.
  - `password: Optional[str]` - Password for RouterOS API.
  - `timeout: float` - Socket timeout in seconds.
  - `use_ssl: bool` - Toggle TLS-wrapped API connections.
  - `debug: bool`, `verbose: bool` - Logging flags inherited from `BDebug`.

**Usage Example:**

```python
from jsktoolbox.netaddresstool import Address

connector = API(ip_address=Address("10.0.0.1"), login="admin", password="secret")
with connector:
    connector.execute("/system/identity/print")
```

---

## `BRouterOS` Class

**Class Introduction:**
Provides the common infrastructure for RouterOS resource trees, combining `BDev` with element handling logic. It manages child element registration, lazy data loading, and recursive traversal.

### `BRouterOS.load()`

**Detailed Description:**
Fetches RouterOS data for the specified path via the attached connector. Populates attribute dictionaries or lists depending on the response payload.

**Signature:**

```python
def load(self, root: str) -> bool
```

- **Arguments:**
  - `root: str` - RouterOS command path to fetch.
- **Returns:**
  - `bool` - `True` when the load succeeds and data is cached.

### `BRouterOS.element()`

**Detailed Description:**
Searches the registered element tree for a path and optionally loads it on access, enabling intuitive navigation of hierarchical RouterOS resources.

**Signature:**

```python
def element(self, root: str, auto_load: bool = False) -> Optional["Element"]
```

- **Arguments:**
  - `root: str` - Path of the desired element (e.g., `/system/routerboard/`).
  - `auto_load: bool` - Fetch data immediately when `True`.

---

## `Element` Class

**Class Introduction:**
Represents an individual RouterOS configuration node. Elements inherit the connector, logging, and debug facilities from `BRouterOS`, and can recursively host child elements for complex menu structures.

### `Element.dump()`

**Detailed Description:**
Convenience method to print the element contents, recursing through the tree for debugging or exploration.

**Signature:**

```python
def dump(self) -> None
```

- **Usage Example:**

```python
element = routerboard.element("/system/routerboard/", auto_load=True)
if element:
    element.dump()
```

---

## `RouterBoard` Class

**Class Introduction:**
Concrete entry point for interacting with MikroTik RouterOS devices. Instantiating `RouterBoard` seeds the entire element tree (system, interfaces, routing, logs, and more) using the provided connector and logging queue.

### `RouterBoard.__init__()`

**Detailed Description:**
Attaches the supplied connector, builds a logger client, then registers all known RouterOS element categories as children. The class exposes `root`, `elements`, and `logs` inherited from `BRouterOS`.

**Signature:**

```python
RouterBoard(
    connector: IConnector,
    qlog: Optional[LoggerQueue] = None,
    debug: bool = False,
    verbose: bool = False,
)
```

- **Arguments:**
  - `connector: IConnector` - Active connector (API or SSH).
  - `qlog: Optional[LoggerQueue]` - Shared logging queue.
  - `debug: bool`, `verbose: bool` - Logging flags cascaded to elements.

**Usage Example:**

```python
connector = API(ip_address=Address("10.0.0.1"), login="admin", password="secret")
routerboard = RouterBoard(connector=connector, debug=True)
system = routerboard.element("/system/", auto_load=True)
```

---

## Suggested Workflow

1. Instantiate a connector `API` and supply credentials.
2. Create a `RouterBoard` passing the connector and optional logging queue.
3. Navigate the element tree using `element()` or iterate through `routerboard.elements` to inspect or modify configuration blocks.
4. Enable `debug` or `verbose` on the root or specific elements to trace interactions during development.
