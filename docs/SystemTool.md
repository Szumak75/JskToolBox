# SystemTool Module

**Source:** `jsktoolbox/systemtool.py`

**High-Level Introduction:**
Utility classes for command-line parsing, environment inspection, and filesystem path validation used by other toolboxes.

## Getting Started

```python
from jsktoolbox.systemtool import CommandLineParser, Env, PathChecker
```

---

## `CommandLineParser` Class

**Class Introduction:**
Configures short/long command-line options, parses `sys.argv`, and produces help output based on the registered metadata.

### `CommandLineParser.configure_option(short_arg, long_arg, desc_arg=None, has_value=False, example_value=None)`

**Detailed Description:**
Registers a command-line option, recording description, value requirements, and example text for help output.

**Signature:**
```python
configure_option(short_arg: Optional[str],
                 long_arg: str,
                 desc_arg: Optional[Union[str, List[str], Tuple[str, ...]]] = None,
                 has_value: bool = False,
                 example_value: Optional[str] = None) -> None
```

- **Arguments:**
  - `short_arg: Optional[str]` – Optional 1-character alias (pass `None` to skip).
  - `long_arg: str` – Long option without leading dashes.
  - `desc_arg: Optional[str | Sequence[str]]` – Description for help output.
  - `has_value: bool` – When `True`, the option expects a value.
  - `example_value: Optional[str]` – Sample value appended to usage text.
- **Returns:**
  - `None`
- **Raises:**
  - `AttributeError` – If `long_arg` is empty.

### `CommandLineParser.parse()`

**Detailed Description:**
Parses `sys.argv` according to the options configured with `configure_option`.

**Signature:**
```python
parse() -> bool
```

- **Returns:**
  - `bool` – `True` on success, `False` when parsing fails.

### `CommandLineParser.has_option(long_arg: str)`

**Detailed Description:**
Checks whether the long option was present on the command line.

**Signature:**
```python
has_option(long_arg: str) -> bool
```

### `CommandLineParser.get_option(long_arg: str)`

**Detailed Description:**
Returns the parsed value for a long option, when applicable.

**Signature:**
```python
get_option(long_arg: str) -> Optional[str]
```

### `CommandLineParser.help()`

**Detailed Description:**
Prints a formatted help summary, showing available options and their descriptions.

### Additional Helpers

- `parse_arguments()` – Deprecated alias of `parse()`.
- `.args` property – Parsed key/value dictionary.
- `.dump()` – Returns structured metadata for help generation.

---

## `Env` Class

**Class Introduction:**
Provides access to common environment variables, username, and platform architecture with safe fallbacks.

### Key Properties & Methods

- `Env.home` – Home directory string.
- `Env.tmpdir` – Temporary directory string.
- `Env.username` – Login name if available.
- `Env.os_arch()` – Returns architecture description (`64-bit`, `32-bit`, etc.) using platform-specific detection with fallback to `platform.architecture()`.
- `Env.is_64bits` – Boolean flag computed from `sys.maxsize`.

---

## `PathChecker` Class

**Class Introduction:**
Inspects filesystem paths, exposing metadata (exists, type) and optional recursive component analysis along with creation helpers.

### `PathChecker(pathname: str, check_deep: bool = True)`

**Signature:**
```python
PathChecker(pathname: str, check_deep: bool = True)
```

- **Raises:**
  - `TypeError` – When `pathname` is None or not a string.
  - `ValueError` – When `pathname` is empty.

### Properties

- `dirname` – Last existing directory component.
- `filename` – Filename when the path targets a file.
- `exists`, `is_dir`, `is_file`, `is_symlink` – Boolean flags.
- `path` – Original path string.
- `posixpath` – Resolved POSIX representation when the path exists.

### `PathChecker.create()`

**Detailed Description:**
Creates missing directories or touches the final file component. Useful for ensuring log directories or runtime output paths exist before writing.

**Signature:**
```python
create() -> bool
```

- **Returns:**
  - `bool` – `True` when the path exists after creation.

---

## Example Workflow

```python
from jsktoolbox.systemtool import CommandLineParser, Env, PathChecker

parser = CommandLineParser()
parser.configure_option('o', 'output', 'Output file', has_value=True)
parser.parse()
if parser.has_option('output'):
    out_path = PathChecker(parser.get_option('output'))
    if not out_path.exists:
        out_path.create()

env = Env()
print(f"Running as {env.username} on {env.os_arch()}")
```

---

**JskToolBox Project**
