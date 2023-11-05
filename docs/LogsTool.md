# LogsTool

The project contains several classes that create a logging subsystem for the designed solutions.

## Public classes
1. [ThLoggerProcessor](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#thloggerprocessor)
1. [LoggerEngine](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#loggerengine)
1. [LoggerClient](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#loggerclient)

## Engine classes
1. [LoggerEngineStdout](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#loggerenginestdout)
1. [LoggerEngineStderr](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#loggerenginestderr)
1. [LoggerEngineFile](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#loggerenginefile)
1. [LoggerEngineSyslog](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#loggerenginesyslog)

## Formatter classes
1. [LogFormatterNull](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#logformatternull)
1. [LogFormatterDateTime](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#logformatterdatetime)
1. [LogFormatterTime](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#logformattertime)
1. [LogFormatterTimestamp](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#logformattertimestamp)

## Queue class
1. [LoggerQueue](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md#loggerqueue)

# Public classes
## ThLoggerProcessor

A class derived from `threading.Thread`, for processing in another thread messages from `LoggerClient` through `LoggerQueue` and formatted using the configured `LoggerEngine` class.

### Import
```
from jsktoolbox.logstool.logs import ThLoggerProcessor
```

### Constructor
```
ThLoggerProcessor()
```

### Public methods
```
.run() -> None
```

The method loops through the `.send()` procedure from the configured `LoggerEngine` class object and then suspends execution for the time specified by the `.sleep_period` property value.
The loop is interrupted by the execution of the `.stop()` method.

```
.stop() -> None
```
Terminates the execution of the `.run()` method.

### Public properties
```
.logger_engine -> Optional[LoggerEngine]
```

Returns the configured object of class `LoggerEngine` or `None` otherwise.

```
.logger_client -> Optional[LoggerClient]
```

Returns the configured object of class `LoggerClient` or `None` otherwise.

```
.sleep_period -> float
```

Returns the length of time to pause the execution of the main loop in the `.run()` method.

```
.started -> bool
```

Returns information whether a start event has been set using the `.run()` method.

```
.stopped -> bool
```

Returns information whether a stop event has been set using the `.stop()` method.

```
.is_stopped -> bool
```

When the thread terminates, the flag returns to `True`.

### Public setters
```
.logger_engine = LoggerEngine()
```

Sets the configured `LoggerEngine` class object.
Throws a `TypeError` exception when trying to assign an object to an invalid class.

```
.logger_client = LoggerClient()
```

Sets the configured `LoggerClient` class object.
Throws a `TypeError` exception when trying to assign an object to an invalid class.

```
.sleep_period = float
```

Sets the sleep period value for the main loop of the `run()` method. Value given in seconds.
Throws a `TypeError` exception when trying to assign an invalid type.

## LoggerEngine

A container class that allows you to assign different engines for selected logging levels.

### Import
```
from jsktoolbox.logstool.logs import LoggerEngine
```

## LoggerClient

A class that defines a client API that allows sending messages with different logging levels.

### Import
```
from jsktoolbox.logstool.logs import LoggerClient
```

# Engine classes
## LoggerEngineStdout

A class that formats the message using the `LogFormatter` class and sends the result to STDOUT.

### Import
```
from jsktoolbox.logstool.engines import LoggerEngineStdout
```

## LoggerEngineStderr

A class that formats the message using the `LogFormatter` class and sends the result to STDERR.

### Import
```
from jsktoolbox.logstool.engines import LoggerEngineStderr
```

## LoggerEngineFile

A class that formats the message using the `LogFormatter` class and writes the result to a file.

### Import
```
from jsktoolbox.logstool.engines import LoggerEngineFile
```

## LoggerEngineSyslog

A class that formats the message using the `LogFormatter` class and sends the result to the system syslog.

### Import
```
from jsktoolbox.logstool.engines import LoggerEngineSyslog
```

# Formatter classes
## LogFormatterNull

A class that formats the transmitted message.
If the `name` variable has been defined for the `LoggerEngine` class, the message will be preceded by the `[name]` prefix, otherwise it will be processed unchanged.

### Import
```
from jsktoolbox.logstool.formatters import LogFormatterNull
```

## LogFormatterDateTime

A class that formats the transmitted message.
If the `name` variable has been defined for the `LoggerEngine` class, the message will be prefixed with `[name]`.
The processed message will be preceded by information about the current date and time in the format: `%Y-%m-%d %H:%M:%S`.

### Import
```
from jsktoolbox.logstool.formatters import LogFormatterDateTime
```

## LogFormatterTime

A class that formats the transmitted message.
If the `name` variable has been defined for the `LoggerEngine` class, the message will be prefixed with `[name]`.
The processed message will be preceded by information about the current time in the format: `%H:%M:%S`.

### Import
```
from jsktoolbox.logstool.formatters import LogFormatterTime
```

## LogFormatterTimestamp

A class that formats the transmitted message.
If the `name` variable has been defined for the `LoggerEngine` class, the message will be prefixed with `[name]`.
The processed message will be prefixed with the current timestamp rounded to an integer value.

### Import
```
from jsktoolbox.logstool.formatters import LogFormatterTimestamp
```

# Queue class
## LoggerQueue

A simple class that defines a queue of messages sent between the `LoggerClient` and `LoggerEngine` classes.

### Import
```
from jsktoolbox.logstool.libs.base_logs import LoggerQueue
```
