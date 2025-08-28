# SystemTool

The project contains a set of classes enabling interaction with the operating system.

## Public classes

1. [CommandLineParser](https://github.com/Szumak75/JskToolBox/blob/1.1.4/docs/SystemTool.md#commandlineparser)
1. [PathChecker](https://github.com/Szumak75/JskToolBox/blob/1.1.4/docs/SystemTool.md#pathchecker)

## CommandLineParser

This class provides tools for configuring and maintaining a list of parameters passed from the command line.

### Import

```
from jsktoolbox.systemtool import CommandLineParser
```

### Constructor

```
CommandLineParser()
```

### Public methods

#### configure_option

```
.configure_option(short_arg, long_arg, desc_arg, has_value, example_value) -> None
```

##### Arguments

* short_arg [Optional[str]] - optional one character string,
* long_arg [str] - required one word string,
* desc_arg [Optional[Union[str, List, Tuple]]] - optional argument description,
* has_value [bool] - flag, if 'True' argument takes a value, default = False,
* example_value [Optional[str]] - example value for argument description.

The method creates and configures the application invocation argument passed in the comment line when it is launched.

#### parse

```
.parse() -> bool
```

The method processes the list of arguments passed on the command line.

#### has_option

```
.has_option() -> bool
```

The method that allows you to check whether an argument has been used.

#### get_option

```
.get_option(long_arg) -> Optional[str]
```

##### Arguments

* long_arg [str] - name of argument to get

The method checks if an argument with the name indicated by `long_arg` was passed. If the variable `has_value=True` is set in the configuration section, the string assigned to this flag in the comment line will be returned.
If the argument is not used, the method returns `None`.

#### help

```
.help() -> None
```

This is example method to print help message.

## PathChecker

This tool returns information about a given file system path. It allows you to attempt to create a non-existent path to a file or directory.

### Import

```
from jsktoolbox.systemtool import PathChecker
```

### Constructor

```
PathChecker(pathname:str, check_deep: bool = True)
```

### Public properties

#### dirname
```
.dirname -> Optional[str]
```

Returns dirname from path.

#### filename

```
.filename -> Optional[str]
```

Returns filename from path.

#### exists

```
.exists -> bool
```

Returns path exists flag.

#### is_dir

```
.is_dir -> bool
```

Returns path is_dir flag.

#### is_file

```
.is_file -> bool
```

Returns path is_file flag.

#### is_symlink

```
.is_symlink -> bool
```

Returns path is_symlink flag.

#### path

```
.path -> str
```

Returns path string.

#### posixpath

```
.posixpath -> str
```

Returns posix path string.

### Public methods

#### create

```
.create() -> bool
```

Attempts to create a non-existent path, if the path ends with a directory character, a directory will be created as the last element of the passed path, otherwise an empty file will be created.

The method returns True if the whole operation was successful.
