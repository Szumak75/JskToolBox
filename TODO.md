# datetool

## Timestamp

Create timestamp from formatted date/time string.

```
import time
import date

time.mktime(datetime.datetime.strptime('22-02-2024','%d-%m-%Y').timetuple())
```
