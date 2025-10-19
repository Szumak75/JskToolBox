# JskToolBox - Code Examples for AI Agents

This file contains practical examples of using JskToolBox library components.

## Table of Contents

1. [Configuration Management](#configuration-management)
2. [Logging System](#logging-system)
3. [Network Address Tools](#network-address-tools)
4. [Exception Handling](#exception-handling)
5. [Threading](#threading)
6. [Data Structures](#data-structures)
7. [Complete Application Example](#complete-application-example)

---

## Configuration Management

### Basic Configuration

```python
from jsktoolbox.configtool import Config

# Initialize configuration
config = Config(
    app_name="MyApplication",
    config_name="settings"
)

# Set values
config.set("Database", "host", "localhost")
config.set("Database", "port", 5432)
config.set("Database", "username", "admin")

# Get values
db_host = config.get("Database", "host")
db_port = config.get("Database", "port", var_type=int)

# Save configuration
config.save()

# Load configuration
config.load()
```

### Configuration with Default Values

```python
from jsktoolbox.configtool import Config
from typing import Optional

def setup_database_config() -> Config:
    """Setup database configuration with defaults."""
    config = Config(app_name="MyApp", config_name="database")
    
    # Try to load existing config
    if not config.load():
        # Set defaults if no config exists
        config.set("Database", "host", "localhost")
        config.set("Database", "port", 5432)
        config.set("Database", "name", "myapp_db")
        config.set("Database", "pool_size", 10)
        config.save()
    
    return config
```

---

## Logging System

### Queue-based Logging

```python
from jsktoolbox.logstool import LoggerQueue, LoggerClient, LoggerEngine
from jsktoolbox.logstool import LogFormatterTime
import logging

# Setup logging system
log_queue = LoggerQueue()
log_client = LoggerClient(log_queue)

# Configure formatter
formatter = LogFormatterTime(
    log_queue=log_queue,
    name="main_formatter"
)

# Setup engine
log_engine = LoggerEngine(
    log_queue=log_queue,
    formatter=formatter,
    log_level=logging.INFO
)

# Start engine
log_engine.start()

# Use logging
log_client.info("Application started")
log_client.debug("Debug information", extra={"user_id": 123})
log_client.warning("Warning message")
log_client.error("Error occurred", exc_info=True)

# Cleanup
log_engine.stop()
```

### File Logging

```python
from jsktoolbox.logstool import LoggerQueue, LoggerClient, LoggerEngine
from jsktoolbox.logstool import LogFormatterTime
import logging

def setup_file_logging(log_file: str):
    """Setup logging to file."""
    queue = LoggerQueue()
    client = LoggerClient(queue)
    
    # Configure handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    
    # Configure formatter
    formatter = LogFormatterTime(
        log_queue=queue,
        name="file_logger"
    )
    handler.setFormatter(formatter)
    
    # Setup engine
    engine = LoggerEngine(
        log_queue=queue,
        formatter=formatter,
        handlers=[handler]
    )
    engine.start()
    
    return client, engine
```

---

## Network Address Tools

### Understanding netaddresstool Classes

**Key distinction**:
- `Address` / `Address6`: Single IP address without mask/prefix
- `Network` / `Network6`: IP address WITH mask/prefix (network range)

### IPv4 Address Manipulation

```python
from jsktoolbox.netaddresstool import Address, Network, Netmask

# Single IPv4 address (no mask)
addr = Address("192.168.1.100")
print(f"Address: {addr}")  # 192.168.1.100
print(f"As integer: {int(addr)}")  # 3232235876
print(f"Octets: {addr.octets}")  # [Octet(192), Octet(168), Octet(1), Octet(100)]

# IPv4 network (with mask)
network = Network("192.168.1.0/24")
print(f"Network: {network}")  # 192.168.1.0/24
print(f"Network address: {network.network}")  # 192.168.1.0
print(f"Broadcast: {network.broadcast}")  # 192.168.1.255
print(f"Netmask: {network.mask}")  # 255.255.255.0
print(f"Host count: {network.count}")  # 254

# Alternative: create from list
network2 = Network([Address("192.168.1.100"), Netmask(24)])
print(f"Network: {network2}")

# Iterate over host addresses
for host_addr in network.iter_hosts(limit=10):
    print(f"Host: {host_addr}")

# Check if address is in network
if int(Address("192.168.1.50")) in range(int(network.min), int(network.max) + 1):
    print("Address is in network range")
```

### IPv6 Address Manipulation

**IMPORTANT**: Use `Address6` for single addresses without prefix, `Network6` for addresses with prefix.

```python
from jsktoolbox.netaddresstool import Address6, Network6, Prefix6

# Single IPv6 address (no prefix) - Address6
addr6 = Address6("2001:db8::1")
print(f"Address: {addr6}")  # 2001:db8::1
print(f"As integer: {int(addr6)}")

# IPv6 network (with prefix) - Network6
network6 = Network6("2001:db8::/64")
print(f"Network: {network6}")  # 2001:db8::/64
print(f"Network address: {network6.network}")  # 2001:db8::
print(f"Prefix: {network6.prefix}")  # 64

# Alternative: create from list
network6_alt = Network6([Address6("2001:db8::1"), Prefix6(64)])
print(f"Network: {network6_alt}")

# Iterate over hosts (limited)
for host in network6.iter_hosts(limit=5):
    print(f"Host: {host}")
```

### Working with Netmasks and Prefixes

```python
from jsktoolbox.netaddresstool import Netmask, Prefix6

# IPv4 Netmask
mask = Netmask(24)  # CIDR notation
print(f"Mask: {mask}")  # 255.255.255.0
print(f"CIDR: {int(mask)}")  # 24

mask2 = Netmask("255.255.255.0")  # Dotted notation
print(f"CIDR: {int(mask2)}")  # 24

# IPv6 Prefix
prefix = Prefix6(64)
print(f"Prefix: {prefix}")  # 64
print(f"As int: {int(prefix)}")  # 64
```

### Network Validation

```python
from jsktoolbox.netaddresstool import Address, Network, Address6, Network6

def validate_ipv4_address(ip_string: str) -> bool:
    """Validate IPv4 address format (single address without mask)."""
    try:
        addr = Address(ip_string)
        return True
    except Exception:
        return False

def validate_ipv4_network(network_string: str) -> bool:
    """Validate IPv4 network format (address with mask)."""
    try:
        net = Network(network_string)
        return True
    except Exception:
        return False

def validate_ipv6_address(ip_string: str) -> bool:
    """Validate IPv6 address format (single address without prefix)."""
    try:
        addr = Address6(ip_string)
        return True
    except Exception:
        return False

def validate_ipv6_network(network_string: str) -> bool:
    """Validate IPv6 network format (address with prefix)."""
    try:
        net = Network6(network_string)
        return True
    except Exception:
        return False

# Usage
print(validate_ipv4_address("192.168.1.1"))  # True
print(validate_ipv4_address("192.168.1.1/24"))  # False (needs Network)
print(validate_ipv4_network("192.168.1.0/24"))  # True
print(validate_ipv4_network("invalid"))  # False

print(validate_ipv6_address("2001:db8::1"))  # True
print(validate_ipv6_address("2001:db8::1/64"))  # False (needs Network6)
print(validate_ipv6_network("2001:db8::/64"))  # True
```

### Subnet Calculations

```python
from jsktoolbox.netaddresstool import Network, SubNetwork, Netmask

# Original network
original = Network("192.168.0.0/22")  # /22 network
print(f"Original: {original}")
print(f"Hosts: {original.count}")

# Calculate subnets
subnets = SubNetwork(original, Netmask(24))  # Split into /24 subnets

# Iterate over subnets
for subnet in subnets.iter_subnets(limit=10):
    print(f"Subnet: {subnet}")
    print(f"  Range: {subnet.min} - {subnet.max}")
    print(f"  Broadcast: {subnet.broadcast}")
```

---

## Exception Handling

### Using RaiseTool

**Important**: `Raise.error()` **creates** an exception object but does NOT raise it. You must use `raise` keyword.

```python
from jsktoolbox.raisetool import Raise
from inspect import currentframe
from typing import Optional

class DataProcessor:
    """Example class using standardized exception handling."""
    
    def process_file(self, filename: str) -> Optional[dict]:
        """Process file with proper exception handling."""
        if not filename:
            # CORRECT: Use 'raise' with Raise.error()
            raise Raise.error(
                "Filename cannot be empty",
                ValueError,
                self.__class__.__name__,
                currentframe()
            )
        
        try:
            with open(filename, 'r') as f:
                data = f.read()
            return {"status": "success", "data": data}
        except FileNotFoundError:
            # CORRECT: Use 'raise' to throw the exception
            raise Raise.error(
                f"File not found: {filename}",
                FileNotFoundError,
                self.__class__.__name__,
                currentframe()
            )
        except IOError as ex:
            # CORRECT: Re-raise with formatted message
            raise Raise.error(
                f"IO error reading file: {ex}",
                IOError,
                self.__class__.__name__,
                currentframe()
            )
```

### What Raise.error() Does

```python
from jsktoolbox.raisetool import Raise
from inspect import currentframe

# Raise.error() CREATES an exception object with formatted message
exception_obj = Raise.error(
    "Something went wrong",
    ValueError,
    "MyClass",
    currentframe()
)

print(type(exception_obj))  # <class 'ValueError'>
print(str(exception_obj))   # MyClass.function [line:123]: [ValueError]: Something went wrong

# To actually raise it, use 'raise'
raise exception_obj  # or: raise Raise.error(...)
```

### Message Formatting

```python
from jsktoolbox.raisetool import Raise
from inspect import currentframe

class MyClass:
    def my_method(self):
        # Formatted message includes:
        # - Class name: MyClass
        # - Method name: my_method
        # - Line number: where currentframe() is called
        # - Exception type: ValueError
        # - Your message
        raise Raise.error(
            "Invalid parameter value",
            ValueError,
            self.__class__.__name__,
            currentframe()
        )
        # Results in: "MyClass.my_method [line:XX]: [ValueError]: Invalid parameter value"
```

---

## Data Structures with BData

### Understanding Base Classes Hierarchy

**Inheritance chain**: `ThBaseObject` → `BData` → `BClasses` → `NoDynamicAttributes`

**BClasses** provides automatic properties:
- `_c_name`: Returns `self.__class__.__name__` automatically
- `_f_name`: Returns current method name from frame

**No need to declare** `_c_name` - it's auto-generated!

```python
from jsktoolbox.basetool import BData

class MyClass(BData):
    """Example class."""
    
    def my_method(self):
        # _c_name is automatic property
        print(f"Class: {self._c_name}")  # "MyClass"
        # _f_name is automatic property
        print(f"Method: {self._f_name}")  # "my_method"

obj = MyClass()
obj.my_method()
# Output:
#   Class: MyClass
#   Method: my_method
```

### BData Overview

`BData` is a powerful base class providing typed dictionary storage with automatic type checking. It's the foundation for data management in JskToolBox.

**Key Features**:
- Type-safe data storage
- Automatic type validation
- Deep copy support
- Memory management helpers
- No constructor - it's a mixin

**Best Practice - Immutable Keys**: Always use `ReadOnlyClass` metaclass for dictionary keys to prevent accidental modification:

```python
from jsktoolbox.attribtool import ReadOnlyClass

class MyClass(BData):
    # ✓ RECOMMENDED: Immutable keys
    class _Keys(object, metaclass=ReadOnlyClass):
        """Immutable data keys."""
        DATA: str = "data_key"
        COUNT: str = "count_key"
    
    # ✗ AVOID: Mutable class variables
    # _KEY_DATA = "data_key"  # Can be accidentally modified!
```

**Why ReadOnlyClass?**
- Prevents accidental modification: `MyClass._Keys.DATA = "wrong"` → `AttributeError`
- Self-documenting code
- Standard pattern used throughout JskToolBox
- IDE autocomplete support

### ReadOnlyClass Usage Patterns

There are **three common patterns** for organizing keys with `ReadOnlyClass`:

#### Pattern 1: Keys Inside Class (Class-Scoped)

**Use when**: Keys are specific to a single class.

```python
from jsktoolbox.basetool import BData
from jsktoolbox.attribtool import ReadOnlyClass

class MyClass(BData):
    """Keys scoped to this class only."""
    
    class _Keys(object, metaclass=ReadOnlyClass):
        """Private keys for MyClass."""
        DATA: str = "data"
        CONFIG: str = "config"
    
    def set_data(self, value: str):
        self._set_data(
            key=self._Keys.DATA,
            value=value,
            set_default_type=str
        )
```

#### Pattern 2: Keys at Module Level (Shared Between Classes)

**Use when**: Multiple classes in the same module share keys.

```python
# At module level (shared by multiple classes)
class _Keys(object, metaclass=ReadOnlyClass):
    """Shared keys for module classes.
    
    For internal purpose only.
    """
    CONFIG: str = "config"
    STATE: str = "state"
    LOGGER: str = "logger"

class ServiceA(BData):
    """Service A using shared keys."""
    
    def __init__(self):
        self._set_data(
            key=_Keys.CONFIG,
            value={},
            set_default_type=dict
        )

class ServiceB(BData):
    """Service B using same shared keys."""
    
    def __init__(self):
        self._set_data(
            key=_Keys.CONFIG,
            value={},
            set_default_type=dict
        )
```

**Real example from JskToolBox**:
```python
# jsktoolbox/configtool/main.py
class _Keys(object, metaclass=ReadOnlyClass):
    """Keys for Config module."""
    DP: str = "__data_processor__"
    FP: str = "__file_processor__"
    RE_SECTION: str = "__re_section__"
    # ... more keys

class Config(BData, NoDynamicAttributes):
    """Config class using module-level _Keys."""
    
    def __init__(self, filename: str):
        self._set_data(
            key=_Keys.FP,
            value=FileProcessor(),
            set_default_type=FileProcessor
        )
```

#### Pattern 3: Public Keys (Project-Wide)

**Use when**: Keys need to be shared across multiple modules/packages.

```python
# myproject/keys.py - Public keys module
from jsktoolbox.attribtool import ReadOnlyClass

class ProjectKeys(object, metaclass=ReadOnlyClass):
    """Public keys for entire project.
    
    Can be imported and used by any module.
    """
    VERSION: str = "app_version"
    APP_NAME: str = "app_name"
    CONFIG_PATH: str = "config_path"
    LOG_LEVEL: str = "log_level"

# myproject/component_a.py
from jsktoolbox.basetool import BData
from .keys import ProjectKeys

class ComponentA(BData):
    """Component using project-wide keys."""
    
    def __init__(self):
        self._set_data(
            key=ProjectKeys.APP_NAME,
            value="MyApp",
            set_default_type=str
        )

# myproject/component_b.py
from jsktoolbox.basetool import BData
from .keys import ProjectKeys

class ComponentB(BData):
    """Another component using same keys."""
    
    def get_app_name(self) -> str:
        return self._get_data(
            key=ProjectKeys.APP_NAME,
            set_default_type=str,
            default_value="Unknown"
        )
```

**Summary of Patterns**:

| Pattern | Scope | Naming | Use Case |
|---------|-------|--------|----------|
| Inside Class | Single class | `_Keys` (private) | Class-specific keys |
| Module Level | Multiple classes in module | `_Keys` (private) | Shared within module |
| Public Class | Entire project | `ProjectKeys` (public) | Cross-module sharing |

**Choose based on**:
- **Scope**: How widely are keys shared?
- **Maintenance**: Easier to change if centralized
- **Coupling**: Public keys increase coupling between modules

### Basic Usage

**Best Practice**: Use `ReadOnlyClass` metaclass for immutable keys to prevent accidental modification.

```python
from jsktoolbox.basetool import BData
from jsktoolbox.attribtool import ReadOnlyClass

class ApplicationConfig(BData):
    """Configuration storage using BData with immutable keys."""
    
    # Define immutable keys using ReadOnlyClass metaclass
    class _Keys(object, metaclass=ReadOnlyClass):
        """Immutable data keys - prevents accidental modification."""
        HOST: str = "host"
        PORT: str = "port"
        ENABLED: str = "enabled"
    
    def __init__(self):
        # BData has no constructor - it's a mixin
        # Just start using _get_data and _set_data
        pass
    
    @property
    def host(self) -> str:
        """Get host with type checking."""
        return self._get_data(
            key=self._Keys.HOST,
            set_default_type=str,
            default_value="localhost"
        )
    
    @host.setter
    def host(self, value: str) -> None:
        """Set host with type validation."""
        self._set_data(
            key=self._Keys.HOST,
            value=value,
            set_default_type=str
        )
    
    @property
    def port(self) -> int:
        """Get port with type checking."""
        return self._get_data(
            key=self._Keys.PORT,
            set_default_type=int,
            default_value=8080
        )
    
    @port.setter
    def port(self, value: int) -> None:
        """Set port with type validation."""
        self._set_data(
            key=self._Keys.PORT,
            value=value,
            set_default_type=int
        )
    
    @property
    def enabled(self) -> bool:
        """Get enabled status."""
        return self._get_data(
            key=self._Keys.ENABLED,
            set_default_type=bool,
            default_value=True
        )
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set enabled status."""
        self._set_data(
            key=self._Keys.ENABLED,
            value=value,
            set_default_type=bool
        )

# Usage
config = ApplicationConfig()
config.host = "api.example.com"
config.port = 443
config.enabled = True

print(f"Host: {config.host}")
print(f"Port: {config.port}")
print(f"Enabled: {config.enabled}")

# Type safety - this will raise TypeError:
try:
    config.port = "not a number"  # TypeError!
except TypeError as e:
    print(f"Type error caught: {e}")
```

### Advanced: Working with Collections

```python
from typing import List, Dict
from jsktoolbox.basetool import BData

class DataStore(BData):
    """Store collections with type safety."""
    
    _KEY_ITEMS = "items"
    _KEY_METADATA = "metadata"
    
    def add_item(self, item: str) -> None:
        """Add item to list."""
        items = self._get_data(
            key=self._KEY_ITEMS,
            set_default_type=List,
            default_value=[]
        )
        items.append(item)
        self._set_data(
            key=self._KEY_ITEMS,
            value=items,
            set_default_type=List
        )
    
    def get_items(self) -> List[str]:
        """Get items list."""
        return self._get_data(
            key=self._KEY_ITEMS,
            set_default_type=List,
            default_value=[]
        )
    
    def set_metadata(self, key: str, value: str) -> None:
        """Set metadata entry."""
        metadata = self._get_data(
            key=self._KEY_METADATA,
            set_default_type=Dict,
            default_value={}
        )
        metadata[key] = value
        self._set_data(
            key=self._KEY_METADATA,
            value=metadata,
            set_default_type=Dict
        )
    
    def get_metadata(self, key: str) -> str:
        """Get metadata entry."""
        metadata = self._get_data(
            key=self._KEY_METADATA,
            set_default_type=Dict,
            default_value={}
        )
        return metadata.get(key, "")
    
    def clear_items(self) -> None:
        """Clear items efficiently."""
        self._clear_data(self._KEY_ITEMS)
    
    def delete_metadata(self) -> None:
        """Delete metadata completely."""
        self._delete_data(self._KEY_METADATA)

# Usage
store = DataStore()
store.add_item("Item 1")
store.add_item("Item 2")
store.set_metadata("author", "John Doe")
store.set_metadata("version", "1.0")

print(f"Items: {store.get_items()}")
print(f"Author: {store.get_metadata('author')}")

# Clear items (efficient memory management)
store.clear_items()
print(f"After clear: {store.get_items()}")
```

### Deep Copy Support

```python
from jsktoolbox.basetool import BData

class SafeDataContainer(BData):
    """Container that provides safe copies."""
    
    _KEY_DATA = "data"
    
    def set_data(self, data: dict) -> None:
        """Store data."""
        self._set_data(
            key=self._KEY_DATA,
            value=data,
            set_default_type=Dict
        )
    
    def get_data_copy(self) -> dict:
        """Get deep copy of data (safe from external modifications)."""
        return self._copy_data(self._KEY_DATA) or {}
    
    def get_data_reference(self) -> dict:
        """Get direct reference (fast but not safe)."""
        return self._get_data(
            key=self._KEY_DATA,
            set_default_type=Dict,
            default_value={}
        )

# Usage
container = SafeDataContainer()
original = {"key": "value", "nested": {"data": 123}}
container.set_data(original)

# Safe copy - modifications don't affect stored data
copy = container.get_data_copy()
copy["key"] = "modified"
copy["nested"]["data"] = 999

print(f"Stored: {container.get_data_reference()}")  # Original unchanged!
print(f"Copy: {copy}")  # Modified
```

### BData Methods Reference

**Storage Methods:**
- `_get_data(key, set_default_type, default_value)` - Get data with type checking
- `_set_data(key, value, set_default_type)` - Set data with type validation
- `_copy_data(key)` - Get deep copy of data
- `_delete_data(key)` - Delete data and its type constraint
- `_clear_data(key)` - Clear data but keep type constraint

**Properties:**
- `_data` - Access internal dictionary (use with caution)

**Type Safety:**
- First `_set_data()` with `set_default_type` registers type constraint
- Subsequent operations validate against registered type
- TypeError raised on type mismatch
- Supports Optional types

### Best Practices

1. **Use ReadOnlyClass for keys** - Prevents accidental modification
   ```python
   class _Keys(object, metaclass=ReadOnlyClass):
       DATA: str = "data"
   ```
2. **Use properties** - Wrap _get_data/_set_data in properties
3. **Set types early** - Define set_default_type on first access
4. **Deep copy when needed** - Use _copy_data() for safe external access
5. **Clear vs Delete** - Use _clear_data() to preserve type, _delete_data() to remove completely

---

## Threading

### Important Note About Threading

The library enforces explicit attribute declaration through `NoDynamicAttributes`. Custom threads use:
1. **ThBaseObject** - Provides thread-related properties (_stop_event, sleep_period)
2. **BData** (inherited via ThBaseObject) - For storing thread data safely with ReadOnlyClass keys
3. **Properties from ThBaseObject** - Can be assigned directly (they have setters)

**Python Version Note**: Python 3.13 changed threading internals. Library designed for Python 3.10-3.12.

### Custom Thread with ThBaseObject and BData

Following the library's architecture pattern:

```python
import threading
from typing import List
from jsktoolbox.basetool import ThBaseObject
from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.logstool import LoggerClient
import time

class DataProcessorThread(threading.Thread, ThBaseObject, NoDynamicAttributes):
    """Custom thread following JskToolBox architecture.
    
    ThBaseObject provides:
    - Properties: _stop_event, sleep_period (can be assigned)
    - Methods: _sleep(), stop()
    - BData: _get_data(), _set_data() for safe data storage
    - _c_name: Auto-generated property returning class name
    
    No constructor call needed - ThBaseObject is a mixin.
    """
    
    # Immutable keys for BData storage
    class _Keys(object, metaclass=ReadOnlyClass):
        """Immutable data keys."""
        LOGGER: str = "logger"
        QUEUE: str = "data_queue"
    
    def __init__(self, logger: LoggerClient):
        """Initialize thread.
        
        Use BData methods to store instance data - this avoids
        NoDynamicAttributes restrictions.
        
        Note: _c_name is automatically "DataProcessorThread" via BClasses property.
        """
        # Use _c_name property for thread name (auto-generated)
        threading.Thread.__init__(self, name=self._c_name)
        
        # Properties from ThBaseObject (have setters):
        self._stop_event = threading.Event()
        self.sleep_period = 0.1
        self.daemon = True
        
        # Store data using BData methods with immutable keys:
        self._set_data(
            key=self._Keys.LOGGER,
            value=logger,
            set_default_type=LoggerClient
        )
        self._set_data(
            key=self._Keys.QUEUE,
            value=[],
            set_default_type=List
        )
    
    @property
    def logger(self) -> LoggerClient:
        """Get logger from BData storage."""
        return self._get_data(
            key=self._Keys.LOGGER,
            set_default_type=LoggerClient
        )
    
    @property
    def data_queue(self) -> List[str]:
        """Get queue from BData storage."""
        return self._get_data(
            key=self._Keys.QUEUE,
            set_default_type=List,
            default_value=[]
        )
    
    def add_data(self, data: str) -> None:
        """Add data to processing queue."""
        queue = self.data_queue
        queue.append(data)
        self._set_data(
            key=self._Keys.QUEUE,
            value=queue,
            set_default_type=List
        )
        self.logger.debug(f"Added to queue: {data}")
    
    def run(self) -> None:
        """Main thread loop."""
        self.logger.info(f"{self.name} thread started")
        
        while not self._stop_event.is_set():
            queue = self.data_queue
            if queue:
                data = queue.pop(0)
                self._set_data(
                    key=self._Keys.QUEUE,
                    value=queue,
                    set_default_type=List
                )
                self._process_item(data)
            else:
                self._sleep()  # Uses sleep_period from ThBaseObject
        
        self.logger.info(f"{self.name} thread stopped")
    
    def _process_item(self, data: str) -> None:
        """Process single item."""
        self.logger.debug(f"Processing: {data}")
        time.sleep(1)
        self.logger.info(f"Completed: {data}")

# Usage
from jsktoolbox.logstool import LoggerQueue, LoggerClient, LoggerEngine
from jsktoolbox.logstool import LogFormatterTime
import logging

# Setup logging
queue = LoggerQueue()
logger = LoggerClient(queue)
formatter = LogFormatterTime(log_queue=queue, name="fmt")
engine = LoggerEngine(log_queue=queue, formatter=formatter, log_level=logging.INFO)
engine.start()

# Create and start thread
processor = DataProcessorThread(logger)
processor.start()

# Add work
processor.add_data("Item 1")
processor.add_data("Item 2")

# Wait and stop
time.sleep(5)
processor.stop()  # Method from ThBaseObject
processor.join()

# Cleanup
engine.stop()
```

### Simplified Thread Example

For simpler cases without logging:

```python
import threading
from typing import Dict
from jsktoolbox.basetool import ThBaseObject
from jsktoolbox.attribtool import NoDynamicAttributes

class SimpleWorkerThread(threading.Thread, ThBaseObject, NoDynamicAttributes):
    """Simple worker using BData for state.
    
    Note: _c_name property auto-returns "SimpleWorkerThread" from BClasses.
    """
    
    # BData keys (class constants)
    _KEY_CONFIG = "config"
    _KEY_COUNTER = "counter"
    
    def __init__(self, config: dict):
        # _c_name is auto-generated property
        threading.Thread.__init__(self, name=self._c_name)
        self._stop_event = threading.Event()
        self.sleep_period = 1.0
        self.daemon = True
        
        # Store config using BData
        self._set_data(
            key=self._KEY_CONFIG,
            value=config,
            set_default_type=Dict
        )
        self._set_data(
            key=self._KEY_COUNTER,
            value=0,
            set_default_type=int
        )
    
    @property
    def counter(self) -> int:
        """Get counter value."""
        return self._get_data(
            key=self._KEY_COUNTER,
            set_default_type=int,
            default_value=0
        )
    
    def run(self) -> None:
        """Thread execution."""
        while not self._stop_event.is_set():
            # Increment counter
            count = self.counter + 1
            self._set_data(
                key=self._KEY_COUNTER,
                value=count,
                set_default_type=int
            )
            print(f"Counter: {count}")
            self._sleep()

# Usage
worker = SimpleWorkerThread({"mode": "production"})
worker.start()
time.sleep(3)
worker.stop()
worker.join()
print(f"Final counter: {worker.counter}")
```

---

## Complete Application Example

### Command-line Application with Full Features

This example demonstrates proper use of BData, threading, logging, and configuration:

```python
#!/usr/bin/env python3
"""
Complete example application using JskToolBox components.
"""

from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerQueue, LoggerClient, LoggerEngine
from jsktoolbox.logstool import LogFormatterTime
from jsktoolbox.raisetool import Raise
from jsktoolbox.systemtool import CommandLineParser
import threading
from typing import List
from jsktoolbox.basetool import ThBaseObject
from jsktoolbox.attribtool import NoDynamicAttributes
from queue import Queue
from inspect import currentframe
import logging
import time
import sys

class WorkerThread(threading.Thread, ThBaseObject, NoDynamicAttributes):
    """Worker thread using BData for storage.
    
    _c_name property will be "WorkerThread" automatically.
    """
    
    # BData keys (class constants)
    _KEY_LOGGER = "logger"
    _KEY_CONFIG = "config"
    _KEY_TASKS = "tasks"
    
    def __init__(self, logger: LoggerClient, config: Config):
        # Uses auto-generated _c_name property
        threading.Thread.__init__(self, name=self._c_name)
        self._stop_event = threading.Event()
        self.sleep_period = 0.1
        self.daemon = True
        
        # Store using BData methods:
        self._set_data(
            key=self._KEY_LOGGER,
            value=logger,
            set_default_type=LoggerClient
        )
        self._set_data(
            key=self._KEY_CONFIG,
            value=config,
            set_default_type=Config
        )
        self._set_data(
            key=self._KEY_TASKS,
            value=Queue(),
            set_default_type=Queue
        )
    
    @property
    def logger(self) -> LoggerClient:
        """Get logger."""
        return self._get_data(key=self._KEY_LOGGER, set_default_type=LoggerClient)
    
    @property
    def tasks(self) -> Queue:
        """Get tasks queue."""
        return self._get_data(key=self._KEY_TASKS, set_default_type=Queue)
    
    def add_task(self, task: str) -> None:
        """Add task to queue."""
        self.tasks.put(task)
        self.logger.info(f"Task added: {task}")
    
    def run(self) -> None:
        """Main processing loop."""
        self.logger.info("Worker thread started")
        
        while not self._stop_event.is_set():
            try:
                task = self.tasks.get(timeout=0.1)
                self._process_task(task)
            except:
                continue
        
        self.logger.info("Worker thread stopped")
    
    def _process_task(self, task: str) -> None:
        """Process single task."""
        self.logger.debug(f"Processing task: {task}")
        time.sleep(1)  # Simulate work
        self.logger.info(f"Task completed: {task}")


class Application:
    """Main application class."""
    
    def __init__(self):
        self.config = None
        self.logger = None
        self.log_engine = None
        self.worker = None
    
    def setup_logging(self) -> None:
        """Setup logging system."""
        try:
            log_queue = LoggerQueue()
            self.logger = LoggerClient(log_queue)
            
            formatter = LogFormatterTime(
                log_queue=log_queue,
                name="app_formatter"
            )
            
            self.log_engine = LoggerEngine(
                log_queue=log_queue,
                formatter=formatter,
                log_level=logging.INFO
            )
            
            self.log_engine.start()
            self.logger.info("Logging system initialized")
            
        except Exception as ex:
            raise Raise.error(
                f"Failed to setup logging: {ex}",
                RuntimeError,
                self.__class__.__name__,
                currentframe()
            )
    
    def setup_config(self) -> None:
        """Setup configuration."""
        try:
            self.config = Config(
                app_name="ExampleApp",
                config_name="settings"
            )
            
            if not self.config.load():
                # Set defaults
                self.config.set("App", "name", "ExampleApp")
                self.config.set("App", "version", "1.0.0")
                self.config.set("Worker", "thread_count", 1)
                self.config.save()
                self.logger.info("Default configuration created")
            else:
                self.logger.info("Configuration loaded")
                
        except Exception as ex:
            raise Raise.error(
                f"Failed to setup configuration: {ex}",
                RuntimeError,
                self.__class__.__name__,
                currentframe()
            )
    
    def start_worker(self) -> None:
        """Start worker thread."""
        self.worker = WorkerThread(self.logger, self.config)
        self.worker.start()
        self.logger.info("Worker thread started")
    
    def run(self) -> None:
        """Run application."""
        try:
            self.logger.info("Application starting...")
            
            # Add some tasks
            for i in range(5):
                self.worker.add_task(f"Task-{i+1}")
            
            # Wait for completion
            time.sleep(10)
            
            self.logger.info("Application stopping...")
            
        except KeyboardInterrupt:
            self.logger.warning("Application interrupted by user")
        except Exception as ex:
            self.logger.error(f"Application error: {ex}", exc_info=True)
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        if self.worker:
            self.worker.stop()
            self.worker.join()
            self.logger.info("Worker thread stopped")
        
        if self.log_engine:
            self.log_engine.stop()


def main():
    """Main entry point."""
    app = Application()
    
    try:
        # Initialize
        app.setup_logging()
        app.setup_config()
        app.start_worker()
        
        # Run
        app.run()
        
    finally:
        # Cleanup
        app.cleanup()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## Additional Resources

- **Full API Documentation**: `docs_api/build/html/index.html`
- **API Structure**: `api_structure.json`
- **Module Index**: `API_INDEX.md`
- **AI Agent Guide**: `AI_AGENT_GUIDE.md`

## Regenerate Documentation

```bash
# Using make
make docs

# Or directly
poetry run python generate_docs.py
```
