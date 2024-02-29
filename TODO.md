# datetool

## Timestamp

Create timestamp from formatted date/time string.

```
import time
import datetime

time.mktime(datetime.datetime.strptime('22-02-2024','%d-%m-%Y').timetuple())
```

```
import datetime

string = "20/01/2020"

element = datetime.datetime.strptime(string,"%d/%m/%Y")
timestamp = datetime.datetime.timestamp(element)
```