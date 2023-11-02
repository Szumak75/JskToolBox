# ConfigTool

The project contains classes that enable common operations on configuration files.

## Public classes
1. [Config](https://github.com/Szumak75/JskToolBox/blob/master/docs/ConfigTool.md#config)

## Config

The main project class.

### Import
```
from jsktoolbox.configtool.main import Config
```

### Constructor
```
Config(filename: str, main_section_name: str, auto_create: bool = False)
```
- filename [str] -- *path to config file*
- main_section_name [str] -- *name of main configuration section in config file*
- auto_create [bool] -- *automatic file creation flag, attempts to create the file if it does not exist when the class object is created. Default value: False*

### Public methods
```
.file_exists() -> bool
```
Returns True if config file exists.

```
.load() -> bool
```
Open the configuration file, if it exists, and load its parsed content into the internal data structure.
The method returns True on success.

```
.save() -> bool
```

```
.get()
```

```
.set()
```

