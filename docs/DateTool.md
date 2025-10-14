# DateTool Module

**Source:** `jsktoolbox/datetool.py`

**High-Level Introduction:**

The `datetool` module is a collection of essential utilities designed to simplify common date and time manipulations in Python. It abstracts away some of the boilerplate code involved in converting between timestamps and `datetime` objects, calculating elapsed time, and handling timezones. Whether you need the current time, a timestamp from a string, or the boundaries of a specific month, this module provides a clean, static interface to get the job done efficiently.

## Getting Started

To begin, import the `DateTime` and `Timestamp` classes from the module. It's also helpful to import `timezone` from the standard `datetime` library when working with timezone-aware objects.

```python
from jsktoolbox.datetool import DateTime, Timestamp
from datetime import timezone
```

---

## `DateTime` Class

**Class Introduction:**

The `DateTime` class is a static utility focused on creating `datetime` and `timedelta` objects. It acts as a factory for generating date-related objects from various sources like timestamps or raw seconds, and provides a consistent way to handle timezone information.

### `DateTime.now()`

**Detailed Description:**

This method is a straightforward wrapper around `datetime.now()`. Its main advantage is providing a consistent, centralized point in your code for getting the current time, and it simplifies the process of creating a timezone-aware `datetime` object for the present moment.

**Signature:**
```python
@classmethod
def now(cls, tz: Optional[timezone] = None) -> datetime:
```

- **Arguments:**
  - `tz: Optional[timezone]` - The timezone for the object. Defaults to `None`, which returns a naive `datetime` object representing the local time.
- **Returns:**
  - `datetime` - The current `datetime` object.

**Usage Example:**
```python
# Get the current naive local time
local_time = DateTime.now()
print(f"Current Local Time: {local_time}")

# Get the current time in the UTC timezone
utc_time = DateTime.now(tz=timezone.utc)
print(f"Current UTC Time: {utc_time}")
```

### `DateTime.datetime_from_timestamp()`

**Detailed Description:**

This method provides a reliable way to convert a standard Unix timestamp (seconds since the epoch) into a human-readable `datetime` object. It is particularly useful when processing data from systems or APIs that communicate time information as timestamps. It also supports creating timezone-aware objects directly.

**Signature:**
```python
@classmethod
def datetime_from_timestamp(cls, timestamp_seconds: Union[int, float], tz: Optional[timezone] = None) -> datetime:
```

- **Arguments:**
  - `timestamp_seconds: Union[int, float]` - The Unix timestamp in seconds.
  - `tz: Optional[timezone]` - The timezone for the resulting `datetime` object. Defaults to `None`.
- **Returns:**
  - `datetime` - The `datetime` object corresponding to the given timestamp.
- **Raises:**
  - `TypeError`: If `timestamp_seconds` is not an `int` or `float`.

**Usage Example:**
```python
# The Unix timestamp for January 1, 2023, 12:00:00 PM UTC
timestamp = 1672574400

# Convert to a timezone-aware datetime object
dt_utc = DateTime.datetime_from_timestamp(timestamp, tz=timezone.utc)
print(f"Datetime in UTC: {dt_utc}")
```

### `DateTime.elapsed_time_from_seconds()`

**Detailed Description:**

This is a simple converter method that turns a numerical value representing seconds into a `timedelta` object. `timedelta` is Python's standard way of representing a duration of time. This method is useful when you have a duration in a simple format (like seconds) and need to perform date arithmetic with it.

**Signature:**
```python
@classmethod
def elapsed_time_from_seconds(cls, seconds: Union[int, float]) -> timedelta:
```

- **Arguments:**
  - `seconds: Union[int, float]` - The duration in seconds.
- **Returns:**
  - `timedelta` - The `timedelta` object representing the duration.
- **Raises:**
  - `TypeError`: If `seconds` is not an `int` or `float`.

**Usage Example:**
```python
# Represent a duration of 2 days in seconds
duration_in_seconds = 2 * 24 * 60 * 60  # 172800

# Convert to a timedelta object
time_delta = DateTime.elapsed_time_from_seconds(duration_in_seconds)

print(f"'{duration_in_seconds} seconds' is equal to '{time_delta}'")
```

### `DateTime.elapsed_time_from_timestamp()`

**Detailed Description:**

This method calculates the duration between a specific point in the past (given as a Unix timestamp) and the current moment. It is useful for determining how long ago an event occurred, for example, to display messages like "posted 2 hours ago". The result is truncated to the nearest second for cleaner output.

**Signature:**
```python
@classmethod
def elapsed_time_from_timestamp(cls, seconds: Union[int, float], tz: Optional[timezone] = None) -> timedelta:
```

- **Arguments:**
  - `seconds: Union[int, float]` - The starting Unix timestamp in seconds.
  - `tz: Optional[timezone]` - The timezone for the calculation. Defaults to `None`.
- **Returns:**
  - `timedelta` - The `timedelta` object representing the elapsed time.
- **Raises:**
  - `TypeError`: If `seconds` is not an `int` or `float`.

**Usage Example:**
```python
# Get a timestamp from 30 minutes ago
past_event_timestamp = Timestamp.now() - (30 * 60)

# Calculate how much time has passed
elapsed = DateTime.elapsed_time_from_timestamp(past_event_timestamp)

print(f"Time since event: {elapsed}")
```

---

## `Timestamp` Class

**Class Introduction:**

The `Timestamp` class is a static utility for creating and converting Unix timestamps. Timestamps are a common, language-agnostic way to represent a point in time, and this class provides helpers to get the current timestamp or convert one from a string.

### `Timestamp.now()`

**Detailed Description:**

This method returns the current time as a Unix timestamp, which is the number of seconds that have elapsed since the Unix epoch (January 1, 1970). It allows you to specify whether you need a precise floating-point number or a truncated integer, which is often sufficient.

**Signature:**
```python
@classmethod
def now(cls, returned_type: Union[type[int], type[float]] = int) -> Union[int, float]:
```

- **Arguments:**
  - `returned_type: Union[type[int], type[float]]` - The desired return type, either `int` (default) or `float`.
- **Returns:**
  - `Union[int, float]` - The current Unix timestamp.
- **Raises:**
  - `TypeError`: If `returned_type` is not `int` or `float`.

**Usage Example:**
```python
# Get the current timestamp as a simple integer
int_timestamp = Timestamp.now()
print(f"Integer timestamp: {int_timestamp}")

# Get a more precise timestamp as a float
float_timestamp = Timestamp.now(returned_type=float)
print(f"Float timestamp: {float_timestamp}")
```

### `Timestamp.from_string()`

**Detailed Description:**

This method is a powerful tool for parsing a date and time from a string, provided you know the format. It converts a human-readable date string (like "2023-12-25") into a machine-readable Unix timestamp. This is essential when you need to process dates from log files, user input, or text-based data sources.

**Signature:**
```python
@classmethod
def from_string(cls, date_string: str, format: str, returned_type: Union[type[int], type[float]] = int) -> Union[int, float]:
```

- **Arguments:**
  - `date_string: str` - The string containing the date and/or time.
  - `format: str` - The `strptime` format code used to parse the string (e.g., `'%Y-%m-%d %H:%M:%S'`)
  - `returned_type: Union[type[int], type[float]]` - The desired return type, `int` (default) or `float`.
- **Returns:**
  - `Union[int, float]` - The Unix timestamp derived from the string.
- **Raises:**
  - `TypeError`: If `returned_type` is not `int` or `float`.
  - `ValueError`: If the `date_string` cannot be parsed with the given `format`.

**Usage Example:**
```python
date_as_string = "2023-01-01 12:00:00"
format_code = "%Y-%m-%d %H:%M:%S"

# Convert the string to a timestamp
timestamp = Timestamp.from_string(date_as_string, format_code)
print(f"The timestamp for '{date_as_string}' is: {timestamp}")
```

### `Timestamp.month_timestamp_tuple()`

**Detailed Description:**

This utility method calculates the exact start and end timestamps for a given month. This is extremely useful for database queries, report generation, or any scenario where you need to filter data within a specific month's boundaries. It correctly handles months of different lengths and can operate on the current month or any month specified by a `datetime` object or timestamp.

**Signature:**
```python
@classmethod
def month_timestamp_tuple(cls, query_date: Optional[Union[float, int, datetime]] = None, tz: Optional[timezone] = timezone.utc) -> Tuple[float, float]:
```

- **Arguments:**
  - `query_date: Optional[Union[float, int, datetime]]` - The date to determine the month. Can be a timestamp or a `datetime` object. If `None`, the current month is used.
  - `tz: Optional[timezone]` - The timezone for the calculation. Defaults to `timezone.utc`.
- **Returns:**
  - `Tuple[float, float]` - A tuple containing the start and end timestamps of the month `(start_timestamp, end_timestamp)`.
- **Raises:**
  - `TypeError`: If `query_date` or `tz` has an unsupported type.

**Usage Example:**
```python
import datetime

# Get the start and end timestamps for the current month
start_current, end_current = Timestamp.month_timestamp_tuple()
print(f"Current month runs from {start_current} to {end_current}")

# Get the boundaries for February 2024 (a leap year)
date_in_feb = datetime.datetime(2024, 2, 10)
start_feb, end_feb = Timestamp.month_timestamp_tuple(query_date=date_in_feb)

# Verify the start and end by converting back to datetime
print(f"Feb 2024 starts at: {DateTime.datetime_from_timestamp(start_feb, tz=timezone.utc)}")
print(f"Feb 2024 ends at:   {DateTime.datetime_from_timestamp(end_feb, tz=timezone.utc)}")
```