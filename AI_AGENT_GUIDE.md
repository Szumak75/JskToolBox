# JskToolBox - AI Agent Integration Guide

## Overview

JskToolBox is a Python library providing utility classes for various operations including configuration management, logging, network tools, system utilities, and more.

## Installation

```bash
pip install jsktoolbox
```

Or if using Poetry:

```bash
poetry add jsktoolbox
```

**Python Requirements**: 3.10, 3.11, or 3.12 (Python 3.13+ support pending - threading changes)

## Quick Start for AI Agents

### 1. Available Resources

When working with JskToolBox, you have access to:

- **HTML Documentation**: Complete API reference in `docs_api/build/html/index.html`
- **API Structure JSON**: Machine-readable API structure in `api_structure.json`
- **Module Index**: Quick reference in `API_INDEX.md`
- **Preferred Imports**: Lazy import patterns in `PREFERRED_IMPORTS.md`
- **Example Code**: Usage examples in `docs/` and `examples/` directories

### 2. Preferred Import Patterns (IMPORTANT)

The library uses **lazy imports** for better performance. Always use the shorter patterns:

```python
# ✓ PREFERRED - Uses lazy loading
from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerClient, LoggerEngine, LogFormatterTime
from jsktoolbox.netaddresstool import Address
from jsktoolbox.basetool import BData, ThBaseObject

# ✗ AVOID - Works but bypasses lazy loading
from jsktoolbox.configtool.main import Config
from jsktoolbox.logstool.logs import LoggerClient
from jsktoolbox.netaddresstool.ipv4 import Address
from jsktoolbox.basetool.data import BData
```

**Why it matters**:
- Lazy imports defer module loading until first use
- Faster startup for applications
- Lower memory footprint
- TYPE_CHECKING provides full IDE support

See `PREFERRED_IMPORTS.md` for the complete mapping.

### 3. Core Modules

#### Configuration Management

```python
from jsktoolbox.configtool import Config

# Create and use configuration
config = Config(app_name="MyApp", config_name="settings")
config.set("section", "key", "value")
value = config.get("section", "key")
config.save()
```

#### Logging

```python
from jsktoolbox.logstool import LoggerClient, LoggerQueue

# Setup logging
log_queue = LoggerQueue()
logger = LoggerClient(log_queue)
logger.info("Application started")
```

#### Network Address Tools

```python
from jsktoolbox.netaddresstool import Address, Network

# Single IPv4 address
addr = Address("192.168.1.100")
print(addr)  # 192.168.1.100

# IPv4 network with mask
net = Network("192.168.1.0/24")
print(net.network)  # 192.168.1.0
print(net.broadcast)  # 192.168.1.255
```

#### Raise Tool (Exception Handling)

**Important**: Always use `raise` with `Raise.error()` - it creates but doesn't throw the exception.

```python
from jsktoolbox.raisetool import Raise
from inspect import currentframe

# CORRECT: Use 'raise' keyword
raise Raise.error(
    "Configuration file not found",
    FileNotFoundError,
    self.__class__.__name__,
    currentframe()
)
```

#### System Tools

```python
from jsktoolbox.systemtool import CommandLineParser

# Parse command line arguments
parser = CommandLineParser()
parser.parse()
```

### 3. Module Categories

#### Base Tools (`jsktoolbox.basetool`)
- **classes**: Base classes (BClasses with NoDynamicAttributes)
- **data**: Data structure utilities (BData)
- **logs**: Logging base classes
- **threads**: Threading mixins (ThBaseObject - provides thread properties)

#### Configuration (`jsktoolbox.configtool`)
- Configuration file management
- INI/JSON format support
- Automatic config directory creation

#### Device Management (`jsktoolbox.devices`)
- Network device interfaces
- MikroTik router support
- Device converters and utilities

#### Network Tools
- **nettool**: Network utilities
- **netaddresstool**: IPv4/IPv6 address manipulation

#### String Tools (`jsktoolbox.stringtool`)
- Cryptographic operations
- String manipulation utilities

#### Tkinter Tools (`jsktoolbox.tktool`)
- GUI base classes
- Layout management
- Custom widgets

### 4. Best Practices for AI Agents

#### Importing Modules

Always import from the specific module:

```python
# ✓ Good
from jsktoolbox.configtool import Config

# ✗ Avoid
from jsktoolbox import *
```

#### Error Handling

Use the standardized RaiseTool with `raise` keyword:

```python
from jsktoolbox.raisetool import Raise
from inspect import currentframe

try:
    # Your code
    pass
except Exception as ex:
    # IMPORTANT: Use 'raise' - Raise.error() only creates the exception
    raise Raise.error(
        f"Error description: {ex}",
        type(ex),
        self.__class__.__name__,
        currentframe()
    )
```

#### Type Hints

The library uses type hints extensively. When using in your code:

```python
from typing import Optional, Dict, Any
from jsktoolbox.configtool import Config

def setup_config(app_name: str) -> Optional[Config]:
    """Setup configuration with type hints."""
    config = Config(app_name=app_name)
    return config if config.load() else None
```

#### Thread Safety

Custom threads use `ThBaseObject` + `BData` for data storage:

```python
import threading
from jsktoolbox.basetool import ThBaseObject
from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass

class MyThread(threading.Thread, ThBaseObject, NoDynamicAttributes):
    """Custom thread with type-safe data storage.
    
    Architecture:
    1. ThBaseObject provides threading properties (_stop_event, sleep_period)
    2. BData (inherited) provides type-safe data storage
    3. BClasses (inherited) provides _c_name property (auto-generated)
    4. NoDynamicAttributes enforces explicit declarations
    5. Use _get_data/_set_data for instance data
    6. ReadOnlyClass ensures immutable keys
    
    Note: _c_name automatically returns "MyThread" - no need to declare it.
    """
    
    # Immutable keys using ReadOnlyClass metaclass
    class _Keys(object, metaclass=ReadOnlyClass):
        """Immutable data keys."""
        DATA: str = "my_data"
    
    def __init__(self, data: str):
        # _c_name is auto-property from BClasses
        threading.Thread.__init__(self, name=self._c_name)
        self._stop_event = threading.Event()
        self.sleep_period = 1.0
        self.daemon = True
        
        # Store data using BData methods with immutable key:
        self._set_data(
            key=self._Keys.DATA,
            value=data,
            set_default_type=str
        )
    
    @property
    def data(self) -> str:
        """Get data from BData storage."""
        return self._get_data(
            key=self._Keys.DATA,
            set_default_type=str,
            default_value=""
        )
    
    def run(self) -> None:
        """Thread execution."""
        while not self._stop_event.is_set():
            print(f"Data: {self.data}")
            self._sleep()
```

**Python Version Note**: Requires Python 3.10-3.12. Python 3.13+ may need threading updates.

**Key Points**:
- Don't call ThBaseObject.__init__() - it's a mixin
- Properties from ThBaseObject can be assigned (have setters)
- Use _get_data/_set_data for custom data storage
- This avoids NoDynamicAttributes restrictions

### 5. Common Patterns

#### Using BData for Type-Safe Storage

All data storage should use BData methods with immutable keys via `ReadOnlyClass`.

**Three organizational patterns**:

1. **Inside class** (class-specific keys):
```python
class MyClass(BData):
    class _Keys(object, metaclass=ReadOnlyClass):
        VALUE: str = "value"
```

2. **Module level** (shared by classes in module):
```python
# At module level
class _Keys(object, metaclass=ReadOnlyClass):
    """Shared keys for module."""
    CONFIG: str = "config"

class ClassA(BData):
    # Uses _Keys.CONFIG
    pass
```

3. **Public class** (project-wide):
```python
# myproject/keys.py
class ProjectKeys(object, metaclass=ReadOnlyClass):
    """Public keys for entire project."""
    APP_NAME: str = "app_name"

# Other modules import and use ProjectKeys
```

**Complete example**:

```python
from jsktoolbox.basetool import BData
from jsktoolbox.attribtool import ReadOnlyClass

class MyClass(BData):
    """Class using type-safe data storage with immutable keys."""
    
    # Define immutable keys using ReadOnlyClass
    class _Keys(object, metaclass=ReadOnlyClass):
        """Immutable data keys."""
        VALUE: str = "value"
    
    def __init__(self):
        # BData has no constructor - just use it
        pass
    
    @property
    def value(self) -> str:
        """Get value with type checking."""
        return self._get_data(
            key=self._Keys.VALUE,
            set_default_type=str,
            default_value=""
        )
    
    @value.setter
    def value(self, val: str) -> None:
        """Set value with type validation."""
        self._set_data(
            key=self._Keys.VALUE,
            value=val,
            set_default_type=str
        )
```

#### Singleton Pattern

```python
from jsktoolbox.basetool import BData

class MyConfig(BData):
    """Configuration with singleton behavior."""
    pass
```

#### Queue-based Logging

```python
from jsktoolbox.logstool import LoggerQueue, LoggerClient, LoggerEngine

# Setup
queue = LoggerQueue()
client = LoggerClient(queue)
engine = LoggerEngine(queue)

# Use
client.info("Processing started")
client.error("Error occurred", exc_info=True)

# Cleanup
engine.stop()
```

### 6. Documentation Access

#### View Module Documentation

To see detailed API documentation for any module:

1. Generate docs: `poetry run python generate_docs.py`
2. Open: `docs_api/build/html/index.html` in browser
3. Navigate to the module of interest

#### Check API Structure Programmatically

```python
import json

with open('api_structure.json', 'r') as f:
    api = json.load(f)
    
# List all modules
for module_name in api['modules']:
    print(f"Module: {module_name}")
```

### 7. Version Compatibility

- **Python**: 3.10, 3.11, 3.12 recommended
- **Python 3.13+**: Threading may require library updates due to changes in threading.Thread internals
- **Dependencies**: See `pyproject.toml`
- **API Stability**: Check module docstrings for stability notes

### 8. Testing

When implementing features using JskToolBox:

```python
import unittest
from jsktoolbox.configtool import Config

class TestConfig(unittest.TestCase):
    def test_config_creation(self):
        config = Config(app_name="TestApp")
        self.assertIsNotNone(config)
```

### 9. Getting Help

- **API Reference**: `docs_api/build/html/index.html`
- **Examples**: Check `examples/` directory
- **Module Documentation**: Each module has inline documentation
- **Type Hints**: Use IDE autocomplete for available methods

### 10. Advanced Usage

#### Custom Logging Formatters

```python
from jsktoolbox.logstool import LogFormatterNull, LogFormatterTime

# Custom log formatting
formatter = LogFormatterTime(
    log_queue=queue,
    name="custom_formatter"
)
```

#### Device Communication

```python
from jsktoolbox.devices.network import NetworkDevice

# Network device interaction
device = NetworkDevice(host="192.168.1.1")
device.connect()
```

## Regenerating Documentation

To regenerate documentation after library updates:

```bash
poetry run python generate_docs.py
```

This will update:
- HTML API documentation
- JSON API structure
- Markdown module index

## Support

For issues or questions:
- Repository: https://github.com/Szumak75/JskToolBox
- Documentation: See generated HTML docs
