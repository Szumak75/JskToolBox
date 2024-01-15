# DateTool

The project contains several classes that return common date/time structures.

## Public classes
1. [DateTime](https://github.com/Szumak75/JskToolBox/blob/1.0.15/docs/DateTool.md#datetime)
1. [Timestamp](https://github.com/Szumak75/JskToolBox/blob/1.0.15/docs/DateTool.md#timestamp)

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

### Public classmethod property
```
.now
```
The property returns the current timestamp in seconds as an integer.
