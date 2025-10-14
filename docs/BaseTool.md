# Base Tool Module

**Source:** `jsktoolbox/basetool`

**High-Level Introduction:**
The Base Tool package gathers reusable mixins that standardise metadata access, typed data storage, logging integration, and thread orchestration across the project. These helpers keep higher-level modules focused on domain logic instead of repeating boilerplate for state handling and diagnostics.

## Getting Started

Import the component that matches your use case. Mix and match the classes to augment existing implementations with the desired capabilities.

```python
from jsktoolbox.basetool.classes import BClasses
from jsktoolbox.basetool.data import BData
from jsktoolbox.basetool.logs import BLoggerQueue, BLoggerEngine, BLogFormatter
from jsktoolbox.basetool.threads import ThBaseObject
```

---

## `BClasses` Class

**Class Introduction:**
Provides convenient properties that expose the current class and calling method name. Ideal for logging contexts where human-readable identifiers are required.

### `BClasses._c_name`

**Detailed Description:**
Returns the class name of the current instance without module qualifications. Commonly used to tag log messages or error reports with the originating class.

**Signature:**

```python
@property
def _c_name(self) -> str
```

- **Returns:**
  - `str` - Name of the subclass using the mixin.

**Usage Example:**

```python
class Service(BClasses):
    def debug(self) -> None:
        print(self._c_name)

Service().debug()  # prints "Service"
```

### `BClasses._f_name`

**Detailed Description:**
Inspects the current frame stack to report the caller method name. Helpful for instrumentation or verbose logging without hard-coded strings.

**Signature:**

```python
@property
def _f_name(self) -> str
```

- **Returns:**
  - `str` - Name of the method that accessed the property.

**Usage Example:**

```python
class Service(BClasses):
    def debug(self) -> None:
        print(self._f_name)

Service().debug()  # prints "debug"
```

---

## `BData` Class

**Class Introduction:**
Acts as a typed dictionary container with convenience accessors for managing state. It lets subclasses establish type constraints, copy values safely, and purge entries.

### `BData._get_data()`

**Detailed Description:**
Retrieves a value from the internal dictionary. Callers can register expected types on demand and supply default fallbacks when missing.

**Signature:**

```python
def _get_data(self, key: str,
              set_default_type: Optional[Any] = None,
              default_value: Optional[Any] = None) -> Optional[Any]
```

- **Arguments:**
  - `key: str` - Dictionary key.
  - `set_default_type: Optional[Any]` - Optional type constraint to register.
  - `default_value: Optional[Any]` - Fallback when the key is absent.
- **Returns:**
  - `Optional[Any]` - Stored value or supplied default.
- **Raises:**
  - `TypeError`: Default value conflicts with the registered type.

**Usage Example:**

```python
state = self._get_data("port", set_default_type=int, default_value=22)
```

### `BData._set_data()`

**Detailed Description:**
Stores a value in the managed dictionary. When a type constraint exists, the method validates new assignments and raises informative errors on mismatch.

**Signature:**

```python
def _set_data(self, key: str, value: Optional[Any],
              set_default_type: Optional[Any] = None) -> None
```

- **Arguments:**
  - `key: str` - Dictionary key.
  - `value: Optional[Any]` - Value to assign.
  - `set_default_type: Optional[Any]` - Optional type constraint to register.
- **Raises:**
  - `TypeError`: Value violates the registered type constraint.

**Usage Example:**

```python
self._set_data("hosts", ["srv1", "srv2"], set_default_type=list)
```

### `BData._copy_data()`

**Detailed Description:**
Returns a deep copy of the stored value so callers can mutate the result without affecting internal state.

**Signature:**

```python
def _copy_data(self, key: str) -> Optional[Any]
```

- **Arguments:**
  - `key: str` - Dictionary key to copy.
- **Returns:**
  - `Optional[Any]` - Deep copy or `None` when the key is absent.

**Usage Example:**

```python
payload = self._copy_data("config") or {}
payload["debug"] = True
```

### `BData._delete_data()` and `_clear_data()`

**Detailed Description:**
`_delete_data` removes both the stored value and its type constraint. `_clear_data` drops only the value, keeping the type restriction intact for subsequent assignments.

**Signature:**

```python
def _delete_data(self, key: str) -> None
def _clear_data(self, key: str) -> None
```

- **Arguments:**
  - `key: str` - Dictionary key to remove.

**Usage Example:**

```python
self._delete_data("session")  # drop value and type
self._clear_data("cache")     # drop value but enforce future type checks
```

---

## `BLoggerQueue` and `BLoggerEngine` Classes

**Class Introduction:**
These containers wrap logging-specific state. `BLoggerQueue` exposes a `LoggerQueue` reference while `BLoggerEngine` tracks the application name, both with type-safe getters and setters.

### `BLoggerQueue.logs_queue`

**Detailed Description:**
Manages access to the shared `LoggerQueue` instance required by logging engines.

**Signature:**

```python
@property
def logs_queue(self) -> Optional[LoggerQueue]
@logs_queue.setter
def logs_queue(self, obj: Optional[LoggerQueue]) -> None
```

- **Usage Example:**

```python
queue_holder.logs_queue = LoggerQueue()
```

### `BLoggerEngine.name`

**Detailed Description:**
Stores the human-friendly name for the logger engine.

**Signature:**

```python
@property
def name(self) -> Optional[str]
@name.setter
def name(self, value: str) -> None
```

- **Usage Example:**

```python
engine.name = "AuditWorker"
```

---

## `BLogFormatter` Class

**Class Introduction:**
Provides a minimal templating system driven by a list of callable or string components. It is designed to be extended for bespoke formatting strategies.

### `BLogFormatter.format()`

**Detailed Description:**
Iterates over the forms list and builds the final string. Callables are evaluated and concatenated with a space, while string templates use Python's `format` with message and optional name placeholders.

**Signature:**

```python
def format(self, message: str, name: Optional[str] = None) -> str
```

- **Arguments:**
  - `message: str` - Log message payload.
  - `name: Optional[str]` - Optional application or logger name.
- **Returns:**
  - `str` - Formatted log entry.

**Usage Example:**

```python
formatter = BLogFormatter()
formatter._forms_ = lambda: "[ts]"
formatter._forms_ = "[{name}] {message}"
entry = formatter.format("started", name="scheduler")
```

---

## `ThBaseObject` Class

**Class Introduction:**
Mirrors the attributes exposed by `threading.Thread` so custom thread implementations can rely on the same property names and type constraints.

### `ThBaseObject.sleep_period` and `_sleep()`

**Detailed Description:**
`sleep_period` stores the default delay used when the helper method `_sleep` is invoked without parameters.

**Signature:**

```python
@property
def sleep_period(self) -> float
@sleep_period.setter
def sleep_period(self, value: float) -> None
def _sleep(self, sleep_period: Optional[float] = None) -> None
```

- **Usage Example:**

```python
class Worker(ThBaseObject, Thread):
    def run(self) -> None:
        while not self.stopped:
            self._sleep()
```

### `ThBaseObject.stop()`

**Detailed Description:**
Triggers the stored stop event, allowing cooperative loop termination in derived threads.

**Signature:**

```python
def stop(self) -> None
```

- **Usage Example:**

```python
worker.stop()
worker.join()
```
