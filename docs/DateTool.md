# DateTool Module

**Source:** `jsktoolbox/datetool.py`

The `datetool` module provides two utility classes for common date and time operations: `DateTime` and `Timestamp`. These classes offer a set of static methods for generating and converting various date/time structures.

## Getting Started

To use the classes from this module, import them as follows:

```python
from jsktoolbox.datetool import DateTime, Timestamp
from datetime import timezone
```

---

## `DateTime` Class

The `DateTime` class provides tools for generating `datetime` and `timedelta` objects.

### `DateTime.now()`

Returns the current local time as a `datetime` object, with an optional timezone.

**Signature:**
```python
@classmethod
def now(cls, tz: Optional[timezone] = None) -> datetime:
```

- **Arguments:**
  - `tz` (Optional[timezone]): The timezone for the `datetime` object. Defaults to `None` (local timezone).
- **Returns:**
  - A `datetime` object representing the current time.

**Example:**
```python
# Get current local time
local_time = DateTime.now()
print(f"Local time: {local_time}")

# Get current UTC time
utc_time = DateTime.now(tz=timezone.utc)
print(f"UTC time: {utc_time}")
```

### `DateTime.datetime_from_timestamp()`

Creates a `datetime` object from a Unix timestamp.

**Signature:**
```python
@classmethod
def datetime_from_timestamp(cls, timestamp_seconds: Union[int, float], tz: Optional[timezone] = None) -> datetime:
```

- **Arguments:**
  - `timestamp_seconds` (Union[int, float]): The Unix timestamp in seconds.
  - `tz` (Optional[timezone]): The timezone for the resulting `datetime` object. Defaults to `None`.
- **Returns:**
  - The `datetime` object corresponding to the timestamp.
- **Raises:**
  - `TypeError`: If `timestamp_seconds` is not an `int` or `float`.

**Example:**
```python
# Timestamp for 2023-01-01 12:00:00 UTC
ts = 1672574400
dt_object = DateTime.datetime_from_timestamp(ts, tz=timezone.utc)
print(f"Datetime from timestamp: {dt_object}")
```

### `DateTime.elapsed_time_from_seconds()`

Converts a duration in seconds into a `timedelta` object.

**Signature:**
```python
@classmethod
def elapsed_time_from_seconds(cls, seconds: Union[int, float]) -> timedelta:
```

- **Arguments:**
  - `seconds` (Union[int, float]): The duration in seconds.
- **Returns:**
  - A `timedelta` object representing the duration.
- **Raises:**
  - `TypeError`: If `seconds` is not an `int` or `float`.

**Example:**
```python
duration_seconds = 86400  # 1 day
timedelta_obj = DateTime.elapsed_time_from_seconds(duration_seconds)
print(f"Timedelta: {timedelta_obj}")
```

### `DateTime.elapsed_time_from_timestamp()`

Calculates the elapsed time from a given Unix timestamp to the present time.

**Signature:**
```python
@classmethod
def elapsed_time_from_timestamp(cls, seconds: Union[int, float], tz: Optional[timezone] = None) -> timedelta:
```

- **Arguments:**
  - `seconds` (Union[int, float]): The starting Unix timestamp in seconds.
  - `tz` (Optional[timezone]): The timezone for the calculation. Defaults to `None`.
- **Returns:**
  - A `timedelta` object representing the elapsed time, accurate to the second.
- **Raises:**
  - `TypeError`: If `seconds` is not an `int` or `float`.

**Example:**
```python
# Timestamp from one hour ago
past_timestamp = Timestamp.now() - 3600
elapsed = DateTime.elapsed_time_from_timestamp(past_timestamp)
print(f"Time elapsed: {elapsed}")
```

---

## `Timestamp` Class

The `Timestamp` class provides tools for generating Unix timestamps.

### `Timestamp.now()`

Gets the current Unix timestamp.

**Signature:**
```python
@classmethod
def now(cls, returned_type: Union[type[int], type[float]] = int) -> Union[int, float]:
```

- **Arguments:**
  - `returned_type` (Union[type[int], type[float]]): The desired return type, either `int` (default) or `float`.
- **Returns:**
  - The current Unix timestamp.
- **Raises:**
  - `TypeError`: If `returned_type` is not `int` or `float`.

**Example:**
```python
# Get timestamp as integer
ts_int = Timestamp.now()
print(f"Integer timestamp: {ts_int}")

# Get timestamp as float
ts_float = Timestamp.now(returned_type=float)
print(f"Float timestamp: {ts_float}")
```

### `Timestamp.from_string()`

Creates a Unix timestamp from a date/time string.

**Signature:**
```python
@classmethod
def from_string(cls, date_string: str, format: str, returned_type: Union[type[int], type[float]] = int) -> Union[int, float]:
```

- **Arguments:**
  - `date_string` (str): The string containing the date/time.
  - `format` (str): The `strptime` format code to parse the string (e.g., `'%Y-%m-%d'`).
  - `returned_type` (Union[type[int], type[float]]): The desired return type, `int` (default) or `float`.
- **Returns:**
  - The Unix timestamp derived from the string.
- **Raises:**
  - `TypeError`: If `returned_type` is not `int` or `float`.
  - `ValueError`: If the `date_string` cannot be parsed with the given `format`.

**Example:**
```python
date_str = "2023-10-27 10:00:00"
fmt = "%Y-%m-%d %H:%M:%S"
ts = Timestamp.from_string(date_str, fmt)
print(f"Timestamp from string: {ts}")
```

### `Timestamp.month_timestamp_tuple()`

Returns the start and end Unix timestamps for a given month.

**Signature:**
```python
@classmethod
def month_timestamp_tuple(cls, query_date: Optional[Union[float, int, datetime]] = None, tz: Optional[timezone] = timezone.utc) -> Tuple[float, float]:
```

- **Arguments:**
  - `query_date` (Optional[Union[float, int, datetime]]): The date to determine the month. It can be a timestamp or a `datetime` object. If `None`, the current month is used.
  - `tz` (Optional[timezone]): The timezone for the calculation. Defaults to `timezone.utc`.
- **Returns:**
  - A tuple containing the start and end timestamps of the month `(start_timestamp, end_timestamp)`.
- **Raises:**
  - `TypeError`: If `query_date` or `tz` has an unsupported type.

**Example:**
```python
# Get timestamps for the current month
start_of_month, end_of_month = Timestamp.month_timestamp_tuple()
print(f"Current month start: {start_of_month}, end: {end_of_month}")

# Get timestamps for a month from a datetime object
import datetime
specific_date = datetime.datetime(2022, 2, 15)
start, end = Timestamp.month_timestamp_tuple(query_date=specific_date)
print(f"February 2022 start: {start}, end: {end}")
```