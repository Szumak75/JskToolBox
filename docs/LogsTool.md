# LogsTool

The project contains several classes that create a logging subsystem for the designed solutions.

## Public classes

1. [ThLoggerProcessor](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#thloggerprocessor)
1. [LoggerEngine](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#loggerengine)
1. [LoggerClient](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#loggerclient)

## Engine classes

1. [LoggerEngineStdout](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#loggerenginestdout)
1. [LoggerEngineStderr](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#loggerenginestderr)
1. [LoggerEngineFile](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#loggerenginefile)
1. [LoggerEngineSyslog](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#loggerenginesyslog)

## Formatter classes

1. [LogFormatterNull](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#logformatternull)
1. [LogFormatterDateTime](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#logformatterdatetime)
1. [LogFormatterTime](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#logformattertime)
1. [LogFormatterTimestamp](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#logformattertimestamp)

## Queue class

1. [LoggerQueue](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/LogsTool.md#loggerqueue)

# Public classes

## ThLoggerProcessor

A class derived from `threading.Thread`, for processing in another thread messages from `LoggerClient` through `LoggerQueue` and formatted using the configured `LoggerEngine` class.

### Import

```
from jsktoolbox.logstool.logs import ThLoggerProcessor
```

### Constructor

```
ThLoggerProcessor(debug: bool = False)
```

Arguments:

- **debug** [bool] - _debug flag for additional logging messages_

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
Throws a `TypeError` exception when attempting to assign an object of an invalid type.

```
.logger_client = LoggerClient()
```

Sets the configured `LoggerClient` class object.
Throws a `TypeError` exception when attempting to assign an object of an invalid type.

```
.sleep_period = float
```

Sets the sleep period value for the main loop of the `run()` method. Value given in seconds.
Throws a `TypeError` exception when trying to assign an invalid type.

## LoggerEngine

The container class that allows you to assign different engines for selected logging levels.

### Import

```
from jsktoolbox.logstool.logs import LoggerEngine
```

### Constructor

```
LoggerEngine()
```

The constructor returns a class object with an initialized instance of the `LoggerQueue` class and pre-configured logging levels for the `LoggerEngineStdout` engine: [**INFO**, **NOTICE**, **WARNING**, **ERROR**, **CRITICAL**] and for the `LoggerEngineStderr` engine: [**ERROR**, **CRITICAL**, **DEBUG**].
The default engine configuration is only used if there is no user configuration. When you add any engine to any login level, the default configuration is bypassed.

### Public methods

```
.add_engine(log_level: str, engine: LoggerEngine) -> None
```

Arguments:

- **log_level** [str] - _the key as a string from the `base_log.LogsLevelKeys.keys` list._
- **engine** [LoggerEngine] - _an object created from any Engine classes._

The method that adds an engine object of any engine class to the list of engines used to process messages for the specified logging level.

```
.send() -> None
```

The method that sends messages to engines assigned to the appropriate logging levels.

### Public properties

```
.logs_queue -> Optional[LoggerQueue]
```

The property that returns an object of the `LoggerQueue` class created in the constructor.
It is used to pass references of the communication queue for objects of the `LoggerClient` class.

### Public setters

```
.logs_queue = LoggerQueue()
```

The setter that allows you to assign an object of the `LoggerQueue` class.
Throws a `TypeError` exception when attempting to assign an object of an invalid type.

## LoggerClient

A class that defines a client API that allows sending messages with different logging levels.

### Import

```
from jsktoolbox.logstool.logs import LoggerClient
```

### Constructor

```
LoggerClient(queue: Optional[LoggerQueue] = None, name: Optional[str] = None)
```

Arguments:

- **queue** [LoggerQueue] - _optional `LoggerQeueu` class object from `LoggerEngine`, required, but can be set after the object is created,_
- **name** [str] - _optional client name string, will be added to the sent message if its value is other than `None`._

### Public methods

```
.message(message: str, log_level: str = .libs.base_log.LogsLevelKeys.INFO) -> None
```

Arguments:

- **message** [str] - _message string_.
- **log_level** [str] - _logging level string from `.libs.base_log.LogsLevelKeys.keys` tuple_.

Method that adds a message with the given logging level to the `LoggerQueue` queue.

### Public properties

```
.logs_queue -> Optional[LoggerQueue]
```

The property that returns a reference to an object of class `LoggerQueue` if assigned, `None` otherwise.

```
.name -> Optional[str]
```

The property that returns a name string if assigned, otherwise `None`.

### Public setters

```
.logs_queue = LoggerQueue()
```

The setter that allows you to assign an object of the `LoggerQueue` class.
Throws a `TypeError` exception when attempting to assign an object of an invalid type.

```
.name = Optional[str]
```

The setter thet allows you to assign an name string or `None`.

```
.message_alert = str
```

The setter sending a message with logging level `ALERT`.

```
.message_critical = str
```

The setter sending a message with logging level `CRITICAL`.

```
.message_debug = str
```

The setter sending a message with logging level `DEBUG`.

```
.message_emergency = str
```

The setter sending a message with logging level `EMERGENCY`.

```
.message_error = str
```

The setter sending a message with logging level `ERROR`.

```
.message_info = str
```

The setter sending a message with logging level `INFO`.

```
.message_notice = str
```

The setter sending a message with logging level `NOTICE`.

```
.message_warning = str
```

The setter sending a message with logging level `WARNING`.

# Engine classes

## LoggerEngineStdout

A class that formats the message using the `LogFormatter` class and sends the result to STDOUT.

### Import

```
from jsktoolbox.logstool.engines import LoggerEngineStdout
```

### Constructor

```
LoggerEngineStdout(name: Optional[str], formatter: Optional[LogFormatter], buffered: bool = False)
```

Arguments:

- **name** - _optional string name, should usually be copied from `LoggerEngine.name`._
- **formatter** - _optional object of an formatters classes._
- **buffered** - _the flag enabling the use of a buffered messaging strategy._

### Public methods

```
.send(message: str) -> None
```

Method that sends a formatted message to STDOUT.

### Public properties

```
.name -> Optional[str]
```

The property that returns a name string if assigned, otherwise `None`.

### Public setters

```
.name = Optional[str]
```

The setter thet allows you to assign an name string or `None`.

## LoggerEngineStderr

A class that formats the message using the `LogFormatter` class and sends the result to STDERR.

### Import

```
from jsktoolbox.logstool.engines import LoggerEngineStderr
```

### Constructor

```
LoggerEngineStderr(name: Optional[str], formatter: Optional[LogFormatter], buffered: bool = False)
```

Arguments:

- **name** - _optional string name, should usually be copied from `LoggerEngine.name`._
- **formatter** - _optional object of an formatters classes._
- **buffered** - _the flag enabling the use of a buffered messaging strategy._

### Public methods

```
.send(message: str) -> None
```

Method that sends a formatted message to STDERR.

### Public properties

```
.name -> Optional[str]
```

The property that returns a name string if assigned, otherwise `None`.

### Public setters

```
.name = Optional[str]
```

The setter thet allows you to assign an name string or `None`.

## LoggerEngineFile

A class that formats the message using the `LogFormatter` class and writes the result to a file.

### Import

```
from jsktoolbox.logstool.engines import LoggerEngineFile
```

### Constructor

```
LoggerEngineFile(name: Optional[str], formatter: Optional[LogFormatter], buffered: bool = False)
```

Arguments:

- **name** - _optional string name, should usually be copied from `LoggerEngine.name`._
- **formatter** - _optional object of an formatters classes._
- **buffered** - _the flag enabling the use of a buffered messaging strategy._

### Public methods

```
.send(message: str) -> None
```

Method that sends a formatted message to FILE.

### Public properties

```
.name -> Optional[str]
```

The property that returns a name string if assigned, otherwise `None`.

```
.logdir -> Optional[str]
```

Returns the log directory path.

```
.logfile -> Optional[str]
```

Returns the log file name.

### Public setters

```
.name = Optional[str]
```

The setter thet allows you to assign an name string or `None`.

```
.logdir = str
```

Sets the log directory path, creates it if it does't exist.

```
.logfile = str
```

Sets the log file name, creates it if it does't exist.
The path to the log file is created by combining `.logdir` and `.logfile`.
If the file exists or has been created, `.logdir` and `.logfile` are updated after separating the path into the directory name and filename.
The setter may throw `FileExistsError` or `PermissionError` exceptions.

## LoggerEngineSyslog

A class that formats the message using the `LogFormatter` class and sends the result to the system syslog.

### Import

```
from jsktoolbox.logstool.engines import LoggerEngineSyslog
from jsktoolbox.logstool.keys import SysLogKeys
```

### Constructor

```
LoggerEngineSyslog(name: Optional[str], formatter: Optional[LogFormatter], buffered: bool = False)
```

Arguments:

- **name** - _optional string name, should usually be copied from `LoggerEngine.name`._
- **formatter** - _optional object of an formatters classes._
- **buffered** - _the flag enabling the use of a buffered messaging strategy._

### Public methods

```
.send(message: str) -> None
```

Method that sends a formatted message to Syslog.

### Public properties

```
.name -> Optional[str]
```

The property that returns a name string if assigned, otherwise `None`.

```
.facility -> int
```

Returns syslog facility.

```
.level -> int
```

Returns syslog level.

### Public setters

```
.name = Optional[str]
```

The setter thet allows you to assign an name string or `None`.

```
.facility = Union[int, str]
```

Sets syslog facility.

- **int** key from `SysLogKeys.facility_keys.values()` list
- **str** key from `SysLogKeys.facility_keys` list

```
.level = Union[int, str]
```

Sets syslog level.

- **int** key from `SysLogKeys.level_keys.values()` list
- **str** key from `SysLogKeys.level_keys` list

# Formatter classes

## LogFormatterNull

A class that formats the transmitted message.
If the `name` variable has been defined for the `LoggerEngine` class, the message will be preceded by the `[name]` prefix, otherwise it will be processed unchanged.

### Import

```
from jsktoolbox.logstool.formatters import LogFormatterNull
```

### Constructor

```
LogFormatterNull()
```

### Public methods

```
.format(message: str, name: str = None) -> str:
```

Arguments:

- **message** [str] - _message string to format_,
- **name** Optional[str] - _optional name string from `LoggerEngine` class_.

The method returns formatted message string.

## LogFormatterDateTime

A class that formats the transmitted message.
If the `name` variable has been defined for the `LoggerEngine` class, the message will be prefixed with `[name]`.
The processed message will be preceded by information about the current date and time in the format: `%Y-%m-%d %H:%M:%S`.

### Import

```
from jsktoolbox.logstool.formatters import LogFormatterDateTime
```

### Constructor

```
LogFormatterDateTime()
```

### Public methods

```
.format(message: str, name: str = None) -> str:
```

Arguments:

- **message** [str] - _message string to format_,
- **name** Optional[str] - _optional name string from `LoggerEngine` class_.

The method returns formatted message string.

## LogFormatterTime

A class that formats the transmitted message.
If the `name` variable has been defined for the `LoggerEngine` class, the message will be prefixed with `[name]`.
The processed message will be preceded by information about the current time in the format: `%H:%M:%S`.

### Import

```
from jsktoolbox.logstool.formatters import LogFormatterTime
```

### Constructor

```
LogFormatterTime()
```

### Public methods

```
.format(message: str, name: str = None) -> str:
```

Arguments:

- **message** [str] - _message string to format_,
- **name** Optional[str] - _optional name string from `LoggerEngine` class_.

The method returns formatted message string.

## LogFormatterTimestamp

A class that formats the transmitted message.
If the `name` variable has been defined for the `LoggerEngine` class, the message will be prefixed with `[name]`.
The processed message will be prefixed with the current timestamp rounded to an integer value.

### Import

```
from jsktoolbox.logstool.formatters import LogFormatterTimestamp
```

### Constructor

```
LogFormatterTimestamp()
```

### Public methods

```
.format(message: str, name: str = None) -> str:
```

Arguments:

- **message** [str] - _message string to format_,
- **name** Optional[str] - _optional name string from `LoggerEngine` class_.

The method returns formatted message string.

# Queue class

## LoggerQueue

A simple class that defines a queue of messages sent between the `LoggerClient` and `LoggerEngine` classes.

### Import

```
from jsktoolbox.logstool.queue import LoggerQueue
from jsktoolbox.logstool.keys import LogsLevelKeys
```

### Constructor

```
LoggerQueue()
```

### Public methods

```
.get() -> Optional[Tuple[str, str]]
```

Gets the queue item as a tuple(log_level: str, message: str) or `None` if the queue is empty.

```
.put(message: str, log_level: str = LogsLevelKeys.INFO)
```

Arguments:

- **message** [str] - _formatted message string_.
- **log_level** [str] - _logging level string from `LogsLevelKeys.keys` tuple_.

Queues a formatted message string with the specified logging level.
