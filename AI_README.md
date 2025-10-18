# JskToolBox - Quick Reference for AI Agents

**Version**: 1.2.dev  
**Python**: 3.10, 3.11, 3.12 (3.13+ support pending)  
**Repository**: https://github.com/Szumak75/JskToolBox

## Installation

```bash
pip install jsktoolbox
```

## Essential Documentation Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `api_structure.json` | Machine-readable API structure | Programmatic API discovery |
| `API_INDEX.md` | Quick module index with imports | Finding modules and import syntax |
| `AI_AGENT_GUIDE.md` | Detailed integration guide | Understanding library architecture |
| `EXAMPLES_FOR_AI.md` | Complete code examples | Learning usage patterns |
| `docs_api/build/html/` | Full HTML API reference | Detailed method documentation |

## Quick Start

### 1. Generate Documentation

```bash
poetry run python generate_docs.py
```

This creates all documentation files needed for AI agent integration.

### 2. Preferred Import Patterns

The library uses **lazy imports** for performance. Always use the shorter, preferred patterns:

```python
# ✓ PREFERRED - Lazy loading
from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerClient, LoggerEngine
from jsktoolbox.basetool import BData

# ✗ AVOID - Works but longer and bypasses lazy loading benefits
from jsktoolbox.configtool.main import Config
from jsktoolbox.logstool.logs import LoggerClient
from jsktoolbox.basetool.data import BData
```

See `PREFERRED_IMPORTS.md` for complete list of all lazy imports.

### 3. Key Module Categories

```python
# Configuration Management
from jsktoolbox.configtool import Config

# Logging System
from jsktoolbox.logstool import LoggerClient, LoggerQueue

# Network Tools
from jsktoolbox.netaddresstool import Address

# Exception Handling
from jsktoolbox.raisetool import Raise

# Threading Utilities
from jsktoolbox.basetool import ThBaseObject
import threading
```

### 3. Most Common Patterns

#### Preferred Imports (Lazy Loading)

```python
# Configuration Management
from jsktoolbox.configtool import Config

# Logging System
from jsktoolbox.logstool import LoggerClient, LoggerQueue, LoggerEngine
from jsktoolbox.logstool import LogFormatterTime

# Network Tools
from jsktoolbox.netaddresstool import Address

# Exception Handling
from jsktoolbox.raisetool import Raise

# Data Storage
from jsktoolbox.basetool import BData

# Threading
from jsktoolbox.basetool import ThBaseObject
import threading
```

```python
config = Config(app_name="MyApp", config_name="settings")
config.set("section", "key", "value")
config.save()
```

#### Logging

```python
from jsktoolbox.logstool import LoggerQueue, LoggerClient

queue = LoggerQueue()

```python
queue = LoggerQueue()
logger = LoggerClient(queue)
logger.info("Message")
```

#### IP Addresses

```python
from jsktoolbox.netaddresstool import Network

# Network with CIDR
net = Network("192.168.1.0/24")
print(net.network)  # 192.168.1.0
print(net.broadcast)  # 192.168.1.255
```

#### Exception Handling

**Important**: `Raise.error()` creates an exception - use `raise` to throw it.

```python
from jsktoolbox.raisetool import Raise
from inspect import currentframe

# CORRECT usage - with 'raise'
raise Raise.error(
    "Error message",
    ExceptionType,
    self.__class__.__name__,
    currentframe()
)
```

#### Immutable Keys Pattern

**Always use ReadOnlyClass** for dictionary keys to prevent accidental modification:

```python
from jsktoolbox.basetool import BData
from jsktoolbox.attribtool import ReadOnlyClass

class MyClass(BData):
    # Three patterns:
    
    # 1. Inside class (class-specific)
    class _Keys(object, metaclass=ReadOnlyClass):
        DATA: str = "data"
    
    def method(self):
        self._set_data(key=self._Keys.DATA, value="test", set_default_type=str)

# 2. Module level (shared in module)
class _Keys(object, metaclass=ReadOnlyClass):
    CONFIG: str = "config"

# 3. Public (project-wide in separate module)
class ProjectKeys(object, metaclass=ReadOnlyClass):
    APP_NAME: str = "app_name"
```

## Module Structure

```
jsktoolbox/
├── attribtool      # Attribute restriction and management
├── basetool/       # Base classes, data structures, threading
├── configtool/     # Configuration file management
├── datetool        # Date/time utilities
├── devices/        # Device management (MikroTik, network)
├── edmctool/       # Elite Dangerous Market Connector tools
├── logstool/       # Logging system components
├── netaddresstool/ # IPv4/IPv6 address manipulation
├── nettool         # Network utilities
├── raisetool       # Exception handling
├── stringtool/     # String and crypto utilities
├── systemtool      # System interaction utilities
└── tktool/         # Tkinter GUI utilities
```

## Type Hints

All public APIs use type hints. Enable IDE autocomplete for best experience.

```python
from typing import Optional, Dict, Any
from jsktoolbox.configtool import Config

def setup(name: str) -> Optional[Config]:
    config = Config(app_name=name)
    return config if config.load() else None
```

## Best Practices

1. **Import Specifically**: Always import from exact module
2. **Use RaiseTool**: Standardize exception handling
3. **Type Hints**: Add type hints when using the library
4. **Threading**: Inherit from ThBaseObject + NoDynamicAttributes
5. **No super() for mixins**: Don't call __init__() on base tool classes
6. **Configuration**: Use Config class for settings management
7. **Logging**: Use LoggerClient for thread-safe logging
8. **Python Version**: Target Python 3.10-3.12 (3.13+ may need updates)

## Documentation Access Priority

For AI agents, consult in this order:

1. **Quick lookup**: `API_INDEX.md` - Find module and import
2. **Understanding**: `AI_AGENT_GUIDE.md` - Learn architecture
3. **Examples**: `EXAMPLES_FOR_AI.md` - See usage patterns
4. **Details**: `docs_api/build/html/` - Full API reference
5. **Programmatic**: `api_structure.json` - Parse API structure

## Common Tasks

### Task: Setup logging
**Reference**: `EXAMPLES_FOR_AI.md` → Logging System section

### Task: Parse IP addresses
**Reference**: `EXAMPLES_FOR_AI.md` → Network Address Tools section

### Task: Manage configuration
**Reference**: `EXAMPLES_FOR_AI.md` → Configuration Management section

### Task: Create background thread
**Reference**: `EXAMPLES_FOR_AI.md` → Threading section

### Task: Handle exceptions
**Reference**: `EXAMPLES_FOR_AI.md` → Exception Handling section

## Testing

```python
import unittest
from jsktoolbox.configtool import Config

class TestMyCode(unittest.TestCase):
    def test_config(self):
        config = Config(app_name="Test")
        self.assertIsNotNone(config)
```

## Dependency Management

This library requires:
- Python 3.10+
- requests
- urllib3

Development dependencies (for documentation):
- sphinx
- sphinx-rtd-theme
- sphinx-autodoc-typehints

## Regenerate Documentation

After library updates:

```bash
# Full regeneration
make docs

# Or individually
cd docs_api && poetry run make html
poetry run python generate_docs.py
```

## Support

- **GitHub**: https://github.com/Szumak75/JskToolBox
- **Issues**: Report via GitHub Issues
- **Documentation**: See generated HTML docs

## License

MIT License - See LICENSE file

---

**Note for AI Agents**: This library is actively maintained. Always generate fresh documentation before working with it to ensure you have the latest API information.
