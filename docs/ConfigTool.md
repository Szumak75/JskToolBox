# ConfigTool

The project contains classes that enable common operations on configuration files.

## Public classes
1. [Config](https://github.com/Szumak75/JskToolBox/blob/1.0.5/docs/ConfigTool.md#config)

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
Opens the configuration file, try create it if it does't exist, and saves the content from the internal data structure.
The method returns True on success.

```
.get(section: str, varname: Optional[str] = None, desc: bool = False) -> Any
```
Gets data from the configuration section.
Arguments:
- section [str] - required section name,
- varname [str] - optional variable name to return,
- desc [bool] - flag informing about the intention to obtain a description.
If the 'desc' flag is set to 'False', the method returns a value of the appropiate type assigned to the variable name.
If the 'desc' flag is set to 'True', there are two different cases for this method:
- if the 'varname' is specified, the method will return variable description as string,
- if the 'varname' defaults to 'None', the method will return description placed in the section, not related to any 'varname', as a list of strings.

```
.set(section: str, varname: Optional[str] = None, value: Optional[Any] = None, desc: Optional[str] = None)
```
Sets data to the configuration section.
Arguments:
- section [str] - required section name,
- varname [str] - optional variable name to set,
- value [str|int|float|list] - optional value to set into 'varname'
- desc [str] - optional description.
The method has several different variants of operation.
If 'varname' is defined, 'value' and 'desc' will be assigned to 'varname' depending on which of these arguments is used.
If 'varname' is set to 'None', then 'desc' will be set as the section description.
Comments:
- setting 'varname' without defining the 'value' and 'desc' removes the variable value and description, if this data was previously assigned in the configuration file,
- setting 'varname' without defining the 'value' or the 'desc' updates the defined argument,
- providing a value without specifying 'varname' makes no sense and such an item will not be included in the configuration file.

### Usage example

Create configuration file from class 'Config':
```
from jsktoolbox.configtool.main import Config
file='/tmp/example.ini'
section='TEST'

obj = Config(file, section)

# main section description
obj.set(section, desc='This is example configuration file,')
obj.set(section, desc="showing how to use the 'Config' class.")

# add subsection description
obj.set('SUBTEST', desc='This is subsection description')

# add a bundle of subsection variables with different types
obj.set('SUBTEST', varname='test01', value=1)
obj.set('SUBTEST', varname='test02', value=3.14, desc='PI number')
obj.set('SUBTEST', varname='test03', value='example string')
obj.set('SUBTEST', varname='test04', value=False)

# add variable to the main section
obj.set(section, varname='test01', value=[1, 'a', True], desc='a list value')

# write configuration file
obj.save()
```

The structure of the created configuration file:
```
[TEST]
# This is example configuration file,
# showing how to use the 'Config' class.
test01 = [1, 'a', True] # a list value
# :::::<End of section: 'TEST'>:::::

[SUBTEST]
# This is subsection description
test01 = 1
test02 = 3.14 # PI number
test03 = "example string"
test04 = False
# :::::<End of section: 'SUBTEST'>:::::

```

Loading a previously created file:
```
from jsktoolbox.configtool.main import Config
file='/tmp/example.ini'
section='TEST'

obj = Config(file, section)

# loading file
if obj.file_exists and obj.load():
    # getting 'SUBTEST' variables
    var01 = obj.get('SUBTEST', varname='test01')
    var02 = obj.get('SUBTEST', varname='test02')
    var03 = obj.get('SUBTEST', varname='test03')
    var04 = obj.get('SUBTEST', varname='test04')

    # getting main section variable
    var05 = obj.get(section, varname='test01')

    print(f"var01: {var01}, type: {type(var01)}")
    print(f"var02: {var02}, type: {type(var02)}")
    print(f"var03: {var03}, type: {type(var03)}")
    print(f"var04: {var04}, type: {type(var04)}")
    print(f"var05: {var05}, type: {type(var05)}")

    # getting non existing variable
    print(f"If the variable does't exist, method returns: {obj.get('SUBTEST', varname='test05')}")
```

Output:
```
var01: 1, type: <class 'int'>
var02: 3.14, type: <class 'float'>
var03: example string, type: <class 'str'>
var04: False, type: <class 'bool'>
var05: [1, 'a', True], type: <class 'list'>
If the variable does't exist, method returns: None
```
