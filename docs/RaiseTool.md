# RaiseTool Module

**Source:** `jsktoolbox/raisetool.py`

**High-Level Introduction:**

The `raisetool` module provides a simple but powerful interface for standardizing exception handling across a project. Its primary goal is to make debugging easier by enriching error messages with valuable context, such as the class, method, and line number where an error occurred. Instead of raising generic exceptions, you can use the `Raise.error()` factory to generate consistent, informative, and easy-to-trace exception objects.

## Getting Started

To use the `Raise` class, import it from the module. It is highly recommended to also import the `inspect` module, which is needed to capture the execution frame and provide detailed context.

```python
import inspect
from jsktoolbox.raisetool import Raise
```

---

## `Raise` Class

**Class Introduction:**

The `Raise` class is a static utility and is not meant to be instantiated. It provides two class methods: `message()` for formatting strings with context, and `error()` for creating fully-formed exception objects. Think of it as a centralized factory for all your project's exceptions.

### `Raise.message()`

**Detailed Description:**

This method is a string formatting utility. It takes a basic message and enhances it with contextual details like the class name, method name, and line number. While you can use it for general-purpose logging or messaging, its primary role is as a helper for the `Raise.error()` method.

**Signature:**
```python
@classmethod
def message(cls, message: str, class_name: str = "", currentframe: Optional[FrameType] = None) -> str:
```

- **Arguments:**
  - `message: str` - The core message to be formatted.
  - `class_name: str` - The name of the class from which the call is made. Defaults to `""`.
  - `currentframe: Optional[FrameType]` - A frame object from `inspect.currentframe()` to automatically extract method and line number.
- **Returns:**
  - `str` - A formatted message string with contextual details.

**Usage Example:**
```python
class DataProcessor:
    def process(self):
        # This example shows how to format a status message with full context.
        status_update = Raise.message(
            "Starting data processing...",
            class_name=self.__class__.__name__,
            currentframe=inspect.currentframe()
        )
        print(status_update)

processor = DataProcessor()
processor.process()
```

**Example Output:**
```
DataProcessor.process [line:10]: Starting data processing...
```

### `Raise.error()`

**Detailed Description:**

This is the core method of the module. It is a factory that creates and returns an exception instance with a rich, contextual error message. You provide a message and an exception type (like `ValueError` or `TypeError`), and it constructs an exception object that is ready to be `raise`d. This ensures all exceptions thrown by your application have a consistent and debug-friendly format.

**Signature:**
```python
@classmethod
def error(cls, message: str, exception: type[Exception] = Exception, class_name: str = "", currentframe: Optional[FrameType] = None) -> Exception:
```

- **Arguments:**
  - `message: str` - The core error message.
  - `exception: type[Exception]` - The exception class (not an instance) to be instantiated. Defaults to the base `Exception`.
  - `class_name: str` - The name of the class where the error occurred. Defaults to `""`.
  - `currentframe: Optional[FrameType]` - A frame object from `inspect.currentframe()` for detailed error location.
- **Returns:**
  - `Exception` - An instance of the specified exception class, with a formatted message.
- **Raises:**
  - `TypeError`: If the `exception` argument is not a class that inherits from `Exception`.

**Usage Example:**
```python
# A function that validates user input
def set_user_age(age):
    if not isinstance(age, int) or age < 0:
        # Raise a specific, contextual error if validation fails.
        raise Raise.error(
            f"Invalid age provided: '{age}'. Age must be a positive integer.",
            TypeError,
            class_name="UserValidator",
            currentframe=inspect.currentframe()
        )
    print(f"Age set to {age}")

try:
    set_user_age("-25")
except TypeError as e:
    print(f"Caught an error: {e}")
```

**Example Output:**
```
Caught an error: UserValidator.set_user_age [line:10]: [TypeError]: Invalid age provided: '-25'. Age must be a positive integer.
```