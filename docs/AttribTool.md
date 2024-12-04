# AttribTool

The project contains base classes that limit the possibility of adding new attributes without their prior declaration inside classes inheriting from them or their objects.

Classes throw an AttributeError exception when trying to add an undefined attribute to a derived class or its object.

## Public classes

1. [NoDynamicAttributes](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/AttribTool.md#nodynamicattributes)
1. [NoNewAttributes](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/AttribTool.md#nonewattributes)
1. [ReadOnlyClass](https://github.com/Szumak75/JskToolBox/blob/1.1.0/docs/AttribTool.md#readonlyclass)

## Usage examples

### NoDynamicAttributes

```
from jsktoolbox.attribtool import NoDynamicAttributes

class Example(NoDynamicAttributes):
    __name = None

    def __init__(self):
        self.__name = self.__class__.__name__

if __name__ == "__main__":
    obj = Example()
    obj.data = "abc"
```

Output:

```
% python3 example.py
Traceback (most recent call last):
  File "/home/szumak/Projects/JskToolBox/example.py", line 11, in <module>
    obj.data = "abc"
    ^^^^^^^^
  File "/home/szumak/Projects/JskToolBox/jsktoolbox/attribtool.py", line 63, in __setattr__
    raise AttributeError(
AttributeError: Cannot add new attribute 'data' to Example object
```

### NoNewAttributes

```
from jsktoolbox.attribtool import NoNewAttributes

class Example(NoNewAttributes):
    __name = None

    def __init__(self):
        self.__name = self.__class__.__name__
        self.__data = 1

if __name__ == "__main__":
    obj = Example()
```

Output:

```
% python3 example.py
Traceback (most recent call last):
  File "/home/szumak/Projects/JskToolBox/example.py", line 11, in <module>
    obj = Example()
          ^^^^^^^^^
  File "/home/szumak/Projects/JskToolBox/example.py", line 8, in __init__
    self.__data = 1
    ^^^^^^^^^^^
  File "/home/szumak/Projects/JskToolBox/jsktoolbox/attribtool.py", line 30, in __setattr__
    raise AttributeError(
AttributeError: Undefined attribute _Example__data cannot be added to <__main__.Example object at 0x7fac9b183c50>
```

### ReadOnlyClass

```
#!/usr/bin/env python3
from jsktoolbox.attribtool import ReadOnlyClass


class A(object, metaclass=ReadOnlyClass):
    FOO = "don't change me"


if __name__ == "__main__":
    print(A.FOO)
    A.FOO = 1
```

Output:

```
% ./example.py
don't change me
Traceback (most recent call last):
  File "/home/szumak/Projects/JskToolBox/./example.py", line 11, in <module>
    A.FOO = 1
    ^^^^^
  File "/home/szumak/Projects/JskToolBox/jsktoolbox/attribtool.py", line 78, in __setattr__
    raise AttributeError(f"Read only attribute: {name}.")
AttributeError: Read only attribute: FOO.
```
