# LogsTool Module

**Source:** `jsktoolbox/logstool`

**High-Level Introduction:**
A modular logging toolkit offering queues, formatters, engines, and processor threads that coordinate message routing across stdout, stderr, file, and syslog targets.

## Getting Started

```python
from jsktoolbox.logstool import (
    LoggerClient,
    LoggerEngine,
    LoggerEngineStdout,
    LogFormatterNull,
    ThLoggerProcessor,
)
```

---

## `LoggerQueue` Class

**Class Introduction:**
In-memory FIFO buffer storing `(log_level, message)` tuples used to decouple clients and engines.

### `LoggerQueue.put(message: str, log_level: str = LogsLevelKeys.INFO)`

**Detailed Description:**
Appends a new log entry to the tail of the queue while validating the log level symbol.

**Signature:**

```python
put(message: str, log_level: str = LogsLevelKeys.INFO) -> None
```

- **Arguments:**
  - `message: str` – Log payload.
  - `log_level: str` – Level identifier from `LogsLevelKeys`.
- **Returns:**
  - `None` – Queue is mutated in place.
- **Raises:**
  - `KeyError` – When an unknown log level is provided.

### `LoggerQueue.get()`

**Detailed Description:**
Removes and returns the oldest queued entry if any are available.

**Signature:**

```python
get() -> Optional[tuple[str, ...]]
```

- **Returns:**
  - `Optional[tuple[str, ...]]` – Tuple `(level, message)` or `None` when empty.

---

## Key Container Classes

### `LogKeys`

**Class Introduction:**
Provides immutable attribute names shared by engines, queues, and clients to keep the logging state structure consistent.

- **Highlights:**
  - Centralises keys such as `__formatter__`, `__queue__`, and `__file__`.
  - Prevents accidental reassignment thanks to the `ReadOnlyClass` metaclass.

### `SysLogKeys`

**Class Introduction:**
Wraps `syslog` facilities and levels inside read-only namespaces while exposing convenient lookup dictionaries.

- **Highlights:**
  - Enables symbolic configuration like `LoggerEngineSyslog.level = "ERROR"`.
  - Offers `facility_keys` and `level_keys` maps for validation.

### `LogsLevelKeys`

**Class Introduction:**
Defines the set of supported semantic log levels that both clients and engines use for routing messages.

- **Highlights:**
  - Supplies canonical constants (`INFO`, `ERROR`, `DEBUG`, etc.).
  - Exposes the `keys` tuple for quick membership checks.

---

## Formatter Classes

### `LogFormatterNull`

**Class Introduction:**
Outputs raw messages, optionally prefixed with the logger name.

- **Signature:**
  ```python
  LogFormatterNull()
  ```
- **Usage Example:**
  ```python
  LogFormatterNull().format("message", name="app")
  # => "[app]: message"
  ```

### `LogFormatterDateTime`

**Class Introduction:**
Prefixes messages with the current local date and time.

### `LogFormatterTime`

**Class Introduction:**
Prefixes messages with the current local time (HH:MM:SS).

### `LogFormatterTimestamp`

**Class Introduction:**
Prefixes messages with a high-resolution timestamp from `Timestamp.now()`.

---

## Engine Classes

### `LoggerEngineStdout`

**Class Introduction:**
Writes formatted log records to standard output with optional buffering.

**Signature:**

```python
LoggerEngineStdout(name: Optional[str] = None,
                   formatter: Optional[BLogFormatter] = None,
                   buffered: bool = False)
```

- **Usage Example:**
  ```python
  engine = LoggerEngineStdout(name="app", formatter=LogFormatterNull())
  engine.send("Service started")
  ```

### `LoggerEngineStderr`

**Class Introduction:**
Mirror of `LoggerEngineStdout` targeting standard error.

### `LoggerEngineFile`

**Class Introduction:**
Appends formatted log entries to a configured file, creating directories as required.

- **Key Properties:**
  - `logdir` – Directory setter/ getter.
  - `logfile` – Ensures the target file exists.
  - `rotation_max_bytes` – Optional size threshold (in bytes) that triggers rotation.
  - `rotation_backup_count` – Number of rotated archives to keep (`app.log.0`, `app.log.1`, ...).

**Rotation Behaviour:**

- Rotation is disabled by default; enable it by setting both `rotation_max_bytes` and a positive `rotation_backup_count`.
- When the active log exceeds the configured size after a write, the engine shifts existing archives up (`.1` ← `.0`, etc.) and moves the current log to `.0` before writing the next entry.

**Usage Example:**

```python
engine = LoggerEngineFile(name="api", formatter=LogFormatterDateTime())
engine.logdir = "/var/log/myapp"
engine.logfile = "service.log"
engine.rotation_max_bytes = 256 * 1024  # rotate after 256 KiB
engine.rotation_backup_count = 5        # keep service.log.0 .. service.log.4
```

### `LoggerEngineSyslog`

**Class Introduction:**
Integrates with the system syslog daemon, supporting dynamic facility and level configuration.

- **Usage Example:**
  ```python
  engine = LoggerEngineSyslog(formatter=LogFormatterNull())
  engine.facility = "LOCAL0"
  engine.level = "ERROR"
  engine.send("Critical failure")
  ```

---

## Core Logging Classes

### `LoggerEngine`

**Class Introduction:**
Central dispatcher that manages the shared queue and routes messages to configured engines per log level.

**Key Methods:**

- `add_engine(log_level: str, engine: ILoggerEngine)` – Register engines per level.
- `send()` – Drain the queue and deliver messages.

**Default Behaviour:**

- Ships with stdout engines for `INFO`, `WARNING`, and `NOTICE`.
- Mirrors high-severity levels (`ERROR`, `CRITICAL`) to both stdout and stderr.
- Starts with a dedicated `LoggerQueue` instance exposed via `logs_queue`.

### `LoggerClient`

**Class Introduction:**
User-facing client responsible for enqueuing messages at various log levels.

- **Usage Example:**
  ```python
  engine = LoggerEngine()
  engine.add_engine(LogsLevelKeys.INFO, LoggerEngineStdout())
  client = LoggerClient(engine.logs_queue, name="web")
  client.message("Started")
  ```

**Severity Shortcut Properties:**

- `message_info`, `message_error`, etc. proxy the `message()` method for all available severities and perform the same validation.
- Getters return `None`; setters enqueue the message at the corresponding level.

### `ThLoggerProcessor`

**Class Introduction:**
Background thread that continuously drains the queue using a configured engine/client pair, ideal for asynchronous logging.

- **Typical Workflow:**

  ```python
  processor = ThLoggerProcessor()
  processor.logger_engine = engine
  processor.logger_client = client
  processor.start()
  ```

- **Runtime Requirements:**
  - The engine and client must be assigned before `start()`; otherwise, `Raise.error` raises `ValueError`.
  - Call `stop()` followed by `join()` to shut down gracefully.

---

## Example Workflow

```python
from jsktoolbox.logstool import (
    LoggerEngine,
    LoggerClient,
    LoggerEngineStdout,
    LogFormatterDateTime,
    ThLoggerProcessor,
    LogsLevelKeys,
)

engine = LoggerEngine()
engine.add_engine(
    LogsLevelKeys.INFO,
    LoggerEngineStdout(name="api", formatter=LogFormatterDateTime()),
)

client = LoggerClient(engine.logs_queue, name="api-client")
processor = ThLoggerProcessor()
processor.logger_engine = engine
processor.logger_client = client
processor.start()

client.message("Server initialised")
processor.stop()
processor.join()
```

---

**JskToolBox Project**
