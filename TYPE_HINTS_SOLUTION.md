# Type Hints Solution for Lazy Loading Modules

## Problem

The `jsktoolbox.logstool` module uses lazy loading via `__getattr__()` to avoid circular imports. While this works functionally, it causes IDE issues:

* Type checkers see exported names as `Any`
* No autocomplete for methods and attributes
* No docstring tooltips on hover
* No parameter hints during function calls
* No type validation in IDE

## Solution

Use `TYPE_CHECKING` constant from the `typing` module to provide type stubs that are only evaluated by static type checkers, not at runtime.

### Implementation

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # These imports are ONLY evaluated by type checkers (mypy, pyright, IDE)
    # They are NOT executed at runtime, so no circular imports occur
    from .logs import LoggerClient as LoggerClient
    from .engines import LoggerEngineFile as LoggerEngineFile
    # ... other imports
```

### How It Works

1. **Runtime behavior**: `TYPE_CHECKING` is `False` at runtime, so the imports inside the block are never executed. Lazy loading via `__getattr__()` continues to work as before.

2. **Type checker behavior**: Type checkers set `TYPE_CHECKING` to `True` during static analysis, so they see the imports and can resolve types correctly.

3. **Re-export syntax**: Using `from .module import Name as Name` explicitly marks the name as re-exported, which is required by PEP 484 for proper type stub behavior.

## Benefits

✅ **Full IDE support**: Autocomplete, parameter hints, docstrings all work  
✅ **Type safety**: Static type checkers can validate code  
✅ **No runtime cost**: Zero performance impact, lazy loading preserved  
✅ **No circular imports**: Type stubs don't execute at runtime  
✅ **Standard practice**: Uses official Python typing conventions (PEP 484)

## Testing

### Verify lazy loading still works:
```python
import sys
import jsktoolbox.logstool

# Module not loaded yet
assert 'jsktoolbox.logstool.logs' not in sys.modules

# Access triggers lazy load
from jsktoolbox.logstool import LoggerClient

# Now it's loaded
assert 'jsktoolbox.logstool.logs' in sys.modules
```

### Verify type hints work:
```python
from jsktoolbox.logstool import LoggerClient, LoggerQueue

# IDE now shows autocomplete for LoggerClient methods
client = LoggerClient(queue=LoggerQueue(), name="test")

# Hovering over 'message_info' shows property signature and docstring
client.message_info = "Hello"

# Parameter hints work
client.message("text", log_level="INFO")
```

## Alternative Approaches Considered

### 1. `.pyi` stub files
**Pros**: Official typing mechanism  
**Cons**: Requires maintaining separate files, duplication of signatures

### 2. Direct imports
**Pros**: Simplest approach  
**Cons**: Breaks lazy loading, causes circular import issues

### 3. String annotations
**Pros**: Defers evaluation  
**Cons**: Only helps within module, not for external users

### 4. `__init__.pyi` stub
**Pros**: Separate from implementation  
**Cons**: Still requires duplication, adds complexity

## Conclusion

The `TYPE_CHECKING` approach provides the best balance:
* Preserves lazy loading behavior
* Adds full IDE/type checker support  
* No code duplication
* Single source of truth
* Standard Python practice

This pattern can be applied to any module using `__getattr__()` for lazy loading.
