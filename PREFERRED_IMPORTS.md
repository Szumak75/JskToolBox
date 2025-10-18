# JskToolBox - Preferred Import Patterns

The library uses lazy imports for performance. This document lists the preferred (shorter) import patterns for all exported classes.

## General Pattern

**Preferred**: `from jsktoolbox.module import ClassName`  
**Also works**: `from jsktoolbox.module.submodule import ClassName`

The preferred pattern uses lazy loading and is more concise.

---

## configtool

```python
# Preferred imports
from jsktoolbox.configtool import Config
from jsktoolbox.configtool import DataProcessor
from jsktoolbox.configtool import FileProcessor
from jsktoolbox.configtool import SectionModel
from jsktoolbox.configtool import VariableModel

# Also works (but longer)
from jsktoolbox.configtool.main import Config
from jsktoolbox.configtool.libs.data import DataProcessor
from jsktoolbox.configtool.libs.file import FileProcessor
```

---

## logstool

```python
# Preferred imports - Keys
from jsktoolbox.logstool import LogKeys
from jsktoolbox.logstool import LogsLevelKeys
from jsktoolbox.logstool import SysLogKeys

# Preferred imports - Queue
from jsktoolbox.logstool import LoggerQueue

# Preferred imports - Formatters
from jsktoolbox.logstool import LogFormatterNull
from jsktoolbox.logstool import LogFormatterDateTime
from jsktoolbox.logstool import LogFormatterTime
from jsktoolbox.logstool import LogFormatterTimestamp

# Preferred imports - Engines
from jsktoolbox.logstool import LoggerEngineStdout
from jsktoolbox.logstool import LoggerEngineStderr
from jsktoolbox.logstool import LoggerEngineFile
from jsktoolbox.logstool import LoggerEngineSyslog

# Preferred imports - Main classes
from jsktoolbox.logstool import LoggerClient
from jsktoolbox.logstool import LoggerEngine
from jsktoolbox.logstool import ThLoggerProcessor

# Also works (but longer)
from jsktoolbox.logstool.keys import LogKeys
from jsktoolbox.logstool.queue import LoggerQueue
from jsktoolbox.logstool.formatters import LogFormatterTime
from jsktoolbox.logstool.engines import LoggerEngineFile
from jsktoolbox.logstool.logs import LoggerClient
```

---

## netaddresstool

```python
# Preferred imports - IPv4
from jsktoolbox.netaddresstool import Address
from jsktoolbox.netaddresstool import Netmask
from jsktoolbox.netaddresstool import Network
from jsktoolbox.netaddresstool import SubNetwork
from jsktoolbox.netaddresstool import DEFAULT_IPV4_HOST_LIMIT
from jsktoolbox.netaddresstool import DEFAULT_IPV4_SUBNET_LIMIT

# Preferred imports - IPv6
from jsktoolbox.netaddresstool import Address6
from jsktoolbox.netaddresstool import Prefix6
from jsktoolbox.netaddresstool import Network6
from jsktoolbox.netaddresstool import SubNetwork6
from jsktoolbox.netaddresstool import DEFAULT_IPV6_HOST_LIMIT
from jsktoolbox.netaddresstool import DEFAULT_IPV6_SUBNET_LIMIT

# Preferred imports - Utilities
from jsktoolbox.netaddresstool import Octet
from jsktoolbox.netaddresstool import Word16

# Also works (but longer)
from jsktoolbox.netaddresstool.ipv4 import Address
from jsktoolbox.netaddresstool.ipv6 import Address6
from jsktoolbox.netaddresstool.libs.octets import Octet
```

---

## basetool

```python
# Preferred imports
from jsktoolbox.basetool import BClasses
from jsktoolbox.basetool import BData
from jsktoolbox.basetool import BLogFormatter
from jsktoolbox.basetool import BLoggerEngine
from jsktoolbox.basetool import BLoggerQueue
from jsktoolbox.basetool import ThBaseObject

# Also works (but longer)
from jsktoolbox.basetool.classes import BClasses
from jsktoolbox.basetool.data import BData
from jsktoolbox.basetool.logs import BLogFormatter
from jsktoolbox.basetool.threads import ThBaseObject
```

---

## stringtool

```python
# Preferred import
from jsktoolbox.stringtool import SimpleCrypto

# Also works (but longer)
from jsktoolbox.stringtool.crypto import SimpleCrypto
```

---

## tktool

```python
# Preferred imports - Base
from jsktoolbox.tktool import TkBase

# Preferred imports - Layout
from jsktoolbox.tktool import Pack
from jsktoolbox.tktool import Grid
from jsktoolbox.tktool import Place

# Preferred imports - Tools
from jsktoolbox.tktool import ClipBoard

# Preferred imports - Widgets
from jsktoolbox.tktool import StatusBarTkFrame
from jsktoolbox.tktool import StatusBarTtkFrame
from jsktoolbox.tktool import CreateToolTip
from jsktoolbox.tktool import VerticalScrolledTkFrame
from jsktoolbox.tktool import VerticalScrolledTtkFrame

# Also works (but longer)
from jsktoolbox.tktool.base import TkBase
from jsktoolbox.tktool.layout import Grid
from jsktoolbox.tktool.tools import ClipBoard
from jsktoolbox.tktool.widgets import StatusBarTkFrame
```

---

## devices

```python
# Preferred imports - Base classes
from jsktoolbox.devices import BDebug
from jsktoolbox.devices import BDev
from jsktoolbox.devices import B64Converter

# Preferred imports - Network connectors
from jsktoolbox.devices import IConnector
from jsktoolbox.devices import API

# Preferred imports - MikroTik
from jsktoolbox.devices import BRouterOS
from jsktoolbox.devices import Element
from jsktoolbox.devices import RouterBoard

# Also works (but longer)
from jsktoolbox.devices.libs.base import BDebug
from jsktoolbox.devices.libs.converters import B64Converter
from jsktoolbox.devices.network.connectors import API
from jsktoolbox.devices.mikrotik.base import Element
from jsktoolbox.devices.mikrotik.routerboard import RouterBoard
```

---

## Modules Without Lazy Imports

These modules export directly - only one import style available:

### attribtool
```python
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.attribtool import ReadOnlyClass
```

### raisetool
```python
from jsktoolbox.raisetool import Raise
```

### systemtool
```python
from jsktoolbox.systemtool import CommandLineParser
```

### datetool
```python
from jsktoolbox.datetool import Timestamp
from jsktoolbox.datetool import DateTime
```

### nettool
```python
from jsktoolbox.nettool import NetworkAddress
```

### edmctool
Exports directly - no lazy loading in __init__.py

---

## Benefits of Preferred Imports

1. **Shorter**: Less typing, cleaner code
2. **Lazy loading**: Only loads what you use
3. **IDE support**: Full type hints via TYPE_CHECKING
4. **Performance**: Deferred initialization
5. **Future-proof**: Internal module reorganization won't break your imports

## Example: Converting Imports

### Before (longer)
```python
from jsktoolbox.configtool.main import Config
from jsktoolbox.logstool.logs import LoggerClient, LoggerEngine
from jsktoolbox.logstool.formatters import LogFormatterTime
from jsktoolbox.netaddresstool.ipv4 import Address
from jsktoolbox.basetool.data import BData
```

### After (preferred)
```python
from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerClient, LoggerEngine, LogFormatterTime
from jsktoolbox.netaddresstool import Address
from jsktoolbox.basetool import BData
```

---

## Testing Lazy Imports

You can verify lazy loading works:

```python
import sys

# Import the module
from jsktoolbox import configtool

# Check what's loaded (should be minimal)
print("Loaded before access:", [m for m in sys.modules if 'configtool' in m])

# Access a class (triggers lazy loading)
from jsktoolbox.configtool import Config

# Check what's loaded now
print("Loaded after access:", [m for m in sys.modules if 'configtool' in m])
```

---

**Note**: Always use the preferred pattern for new code. The longer patterns are maintained for backwards compatibility.
