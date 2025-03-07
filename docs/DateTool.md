# DateTool

The project contains several classes that return common date/time structures.

## Public classes

1. [DateTime](https://github.com/Szumak75/JskToolBox/blob/releases/docs/DateTool.md#datetime)
1. [Timestamp](https://github.com/Szumak75/JskToolBox/blob/releases/docs/DateTool.md#timestamp)

## DateTime

### Import

```
from jsktoolbox.datetool import DateTool
```

### Public classmethod

```
.now(tz: Optional[timezone] = None) -> datetime.datetime
```

The method returns a datetime.datetime.now() object with an optional time zone specified.

```
.datetime_from_timestamp(
    timestamp_seconds: Union[int, float],
    tz: Optional[timezone] = None
) -> datetime.datetime
```

The method returns a datetime.datetime object based on the provided timestamp value as an integer or floating point with an optional time zone.

```
.elapsed_time_from_seconds(seconds: Union[int, float]) -> datetime.timedelta
```

The method converts the given seconds value as an integer or float with an optional time zone to a timedelta structure.

```
.elapsed_time_from_timestamp(
    seconds: Union[int, float],
    tz: Optional[timezone] = None
) -> datetime.timedelta:
```

The method returns a datetime.timedelta object as the difference between the current time and the seconds value specified as an integer or floating point number with an optional time zone.
Timedelta is returned accurate to the second.

## Timestamp

### Import

```
from datetool import Timestamp
```


### Public classmethod

```
.now(return_type: Union[type[int], type[float]] = int) -> Union[int, float]
```

The methods returns the current timestamp in seconds as an integer or float depending on `return_type`.

#### Arguments

- **return_type** [type[int] or type[float]] - the method returns the data in the type specified by this variable, by default `int`.


```
.from_string(date_string: str, format: str, return_type: Union[type[int], type[float]] = int) -> Union[int, float]
```

The method returns timestamp as int from date/time string in strptime format.

#### Arguments

- **date_string** [str] - a string containing a date/time representation, for example: `"2000-01-28"`
- **format** [str] - strptime date/time format, for the above example: `"%Y-%m-%d"`
- **return_type** [type[int] or type[float]] - the method returns the data in the type specified by this variable, by default `int`.
