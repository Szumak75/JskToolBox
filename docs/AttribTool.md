# Attrib Tool Module

**Source:** `jsktoolbox/attribtool.py`

**High-Level Introduction:**
The Attrib Tool module aggregates mixins and metaclasses that guard against accidental attribute creation. By wrapping `__setattr__`, it ensures only predefined attributes can be written, protecting objects that require strict schemas.

## Getting Started

Import the helper that fits your target class. Use `NoDynamicAttributes` for instances, `NoNewAttributes` when you also need metaclass-level protection, and `ReadOnlyClass` for immutable class attributes.

```python
from jsktoolbox.attribtool import NoDynamicAttributes, NoNewAttributes, ReadOnlyClass
```

---

## `NoNewAttributes` Class

**Class Introduction:**
Combines instance and metaclass interceptors to forbid adding new attributes after class definition. Existing attributes remain writable.

### `NoNewAttributes.__setattr__()`

**Detailed Description:**
Delegates to Python’s default `object.__setattr__` while checking attribute existence. Intended for internal wiring; you typically inherit from the mixin instead of overriding this method.

**Signature:**

```python
def __setattr__(self, name: str, value: Any) -> None
```

- **Arguments:**
  - `name: str` - Name of the attribute to set.
  - `value: Any` - Value to assign.
- **Raises:**
  - `AttributeError`: Attribute does not exist on the instance yet.

**Usage Example:**

```python
class Locked(NoNewAttributes):
    existing = 1

obj = Locked()
obj.existing = 2          # OK
obj.new_field = "fail"    # AttributeError
```

---

## `NoDynamicAttributes` Class

**Class Introduction:**
Lightweight mixin that prevents instance-level attribute creation while leaving class attributes untouched. Use it when metaclass protection is unnecessary.

### `NoDynamicAttributes.__setattr__()`

**Detailed Description:**
Checks whether the attribute already exists on the instance before delegating to `super().__setattr__`. Raising early helps catch misspellings and schema drift.

**Signature:**

```python
def __setattr__(self, name: str, value: Any) -> None
```

- **Arguments:**
  - `name: str` - Attribute name.
  - `value: Any` - Value to assign.
- **Raises:**
  - `AttributeError`: New attribute is rejected.

**Usage Example:**

```python
class Model(NoDynamicAttributes):
    id: int = 0

m = Model()
m.id = 42          # OK
m.created_at = 0   # AttributeError
```

---

## `ReadOnlyClass` Metaclass

**Class Introduction:**
Metaclass that blocks reassignment of class attributes. The restriction safeguards constants and configuration baked into the class definition.

### `ReadOnlyClass.__setattr__()`

**Detailed Description:**
Overrides metaclass `__setattr__` so attempts to adjust class attributes raise `AttributeError`.

**Signature:**

```python
def __setattr__(self, name: str, value: Any) -> None
```

- **Arguments:**
  - `name: str` - Attribute to override.
  - `value: Any` - New value supplied by the caller.
- **Raises:**
  - `AttributeError`: Always raised to prevent modification.

**Usage Example:**

```python
class Constants(metaclass=ReadOnlyClass):
    FOO = "immutable"

Constants.FOO = "mutated"  # AttributeError
```

---

## Best Practices for Key Storage

**ReadOnlyClass for Safe Key Storage:**

When working with dictionary keys throughout a project, it's recommended to use `ReadOnlyClass` metaclass to create immutable key containers. This prevents accidental modification of key names which could lead to hard-to-debug errors. Keys can be organized at different scopes:

### Module-level Keys (Private)

For multi-class modules where multiple classes share the same keys:

```python
from jsktoolbox.attribtool import ReadOnlyClass

class _Keys(object, metaclass=ReadOnlyClass):
    """Shared keys for module classes."""
    KEY_DATA: str = 'my_data'
    KEY_STATUS: str = 'status'

class DataProcessor:
    def process(self):
        value = self._get_data(_Keys.KEY_DATA)
```

### Class-level Keys (Nested)

For keys used within a single class:

```python
class MyThread(BData, ThBaseObject):
    """Thread with typed data storage."""

    class _Keys(object, metaclass=ReadOnlyClass):
        """Private keys for this class only."""
        KEY_DATA: str = 'my_data'
        KEY_COUNT: str = 'count'

    def run(self):
        data = self._get_data(self._Keys.KEY_DATA)
```

### Project-level Keys (Public)

For large projects with shared keys across multiple modules:

```python
# In keys.py or constants.py
class Keys(object, metaclass=ReadOnlyClass):
    """Global project keys."""
    KEY_CONFIG: str = 'config'
    KEY_LOGGER: str = 'logger'

# In other modules
from myproject.keys import Keys

class Service:
    def setup(self):
        config = self._get_data(Keys.KEY_CONFIG)
```

This pattern ensures type safety and prevents runtime errors from typos or accidental key modification.
