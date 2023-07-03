# AttribTool

The project contains base classes that limit the possibility of adding new attributes without their prior declaration inside classes inheriting from them or their objects.

Classes throw an AttributeError exception when trying to add an undefined attribute to a derived class or its object.

## Usage examples

```
from toolbox.attribtool import NoDynamicAttributes

class Example(NoDynamicAttributes):
    __name = None

    def __init__(self):
        self.__name = self.__class__.__name__

if __name__ == "__main__":
    obj = Example()
    obj.data = "abc"
```
```
% ./example.py
Traceback (most recent call last):
  File "/home/szumak/Projects/ToolBox/AttribTool/./example.py", line 22, in <module>
    obj.data = "abc"
  File "/home/szumak/Projects/ToolBox/AttribTool/attribtool/ndattrib.py", line 22, in __setattr__
    raise AttributeError(
AttributeError: Cannot add new attribute 'data' to Example object
```

```
from toolbox.attribtool import NoNewAttributes

class Example(NoNewAttributes):
    __name = None

    def __init__(self):
        self.__name = self.__class__.__name__
        self.__data = 1

if __name__ == "__main__":
    obj = Example()
```
```
% ./example.py
Traceback (most recent call last):
  File "/home/szumak/Projects/ToolBox/AttribTool/./example.py", line 22, in <module>
    obj = Example()
  File "/home/szumak/Projects/ToolBox/AttribTool/./example.py", line 18, in __init__
    self.__data = 1
  File "/home/szumak/Projects/ToolBox/AttribTool/attribtool/nnattrib.py", line 24, in __setattr__
    raise AttributeError(
AttributeError: Undefined attribute _Example__data cannot be added to <__main__.Example object at 0x7f7129ccc2b0>
```
