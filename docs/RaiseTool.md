# RaiseTool

The project contains small class for formatting thrown exception messages.

The message can be formatted with information about the class, method, and line number where the exception was thrown.

## Public methods
```
Raise.message(message:str, class_name:Optional[str], currentframe:Optional[FrameType])-> str
Raise.error(message:str, exception:Exception, class_name:Optional[str], currentframe:Optional[FrameType])-> Exception
```

## Usage examples

```
import inspect
from jsktoolbox.raisetool import Raise


class Example:
    def __init__(self):
        print(f"1: {Raise.message('example message 1')}")
        print(
            f"2: {Raise.message('example message 2', self.__class__.__name__)}"
        )
        print(
            f"3: {Raise.message('example message 3', self.__class__.__name__, inspect.currentframe(), )}"
        )
        try:
            raise Raise.error(
                "example message 4",
                ValueError,
                self.__class__.__name__,
                inspect.currentframe(),
            )
        except ValueError as ex:
            print(f"4: {ex}")


if __name__ == "__main__":
    obj = Example()
```
Output:
```
1: example message 1
2: Example: example message 2
3: Example.__init__ [line:12]: example message 3
4: Example.__init__ [line:15]: [ValueError]: example message 4
```
