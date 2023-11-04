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

A class derived from "threading.Thread", for processing in another thread messages from "LoggerClient" through "LoggerQueue" and formatted using the configured "LoggerEngine" class.

## LoggerEngine

A container class that allows you to assign different engines for selected logging levels.

## LoggerClient

A class that defines a client API that allows sending messages with different logging levels.

# Engine classes
## LoggerEngineStdout

A class that formats the message using the 'LogFormatter' class and sends the result to STDOUT.

## LoggerEngineStderr

A class that formats the message using the 'LogFormatter' class and sends the result to STDERR.

## LoggerEngineFile

A class that formats the message using the 'LogFormatter' class and writes the result to a file.

## LoggerEngineSyslog

A class that formats the message using the 'LogFormatter' class and sends the result to the system syslog.

# Formatter classes
## LogFormatterNull

A class that formats the transmitted message.
If the 'name' variable has been defined for the 'LoggerEngine' class, the message will be preceded by the '[name]' prefix, otherwise it will be processed unchanged.

## LogFormatterDateTime

A class that formats the transmitted message.
If the 'name' variable has been defined for the 'LoggerEngine' class, the message will be prefixed with '[name]'.
The processed message will be preceded by information about the current date and time in the format: "%Y-%m-%d %H:%M:%S".

## LogFormatterTime

A class that formats the transmitted message.
If the 'name' variable has been defined for the 'LoggerEngine' class, the message will be prefixed with '[name]'.
The processed message will be preceded by information about the current time in the format: "%H:%M:%S".

## LogFormatterTimestamp

A class that formats the transmitted message.
If the 'name' variable has been defined for the 'LoggerEngine' class, the message will be prefixed with '[name]'.
The processed message will be prefixed with the current timestamp rounded to an integer value.

# Queue class
## LoggerQueue

A simple class that defines a queue of messages sent between the 'LoggerClient' and 'LoggerEngine' classes.
