# TkTool

The project contains classes useful for tkinter-based projects.

## Public classes
1. [CreateToolTip](https://github.com/Szumak75/JskToolBox/blob/master/docs/TkTool.md#createtooltip)
1. [VerticalScrolledTkFrame](https://github.com/Szumak75/JskToolBox/blob/master/docs/TkTool.md#verticalscrolledtkframe)
1. [VerticalScrolledTtkFrame](https://github.com/Szumak75/JskToolBox/blob/master/docs/TkTool.md#verticalscrolledttkframe)

## CreateToolTip

Creates a tooltip for a given widget.

### Import
```
from jsktoolbox.tktool.widgets import CreateToolTip
```

### Constructor
```
CreateToolTip(
    widget: tk.Misc, 
    text: Union[str, List[str], Tuple[str], tk.StringVar] = "widget info", 
    wait_time: int = 500, 
    wrap_length: int = 0, 
    **kwargs)
```
*widget*: tk.Misc -- Parent widget handler,
*text*: Union[str, List[str], Tuple[str], tk.StringVar] -- text displayed in tooltip,
*wait_time*: int -- delay of displaying tooltip [ms],
*wrap_length*: int -- Limit the number of characters on each line to the specified value.
                The default value of 0 means that lines will only be broken on newlines.

### Example
```
import tkinter as tk
from jsktoolbox.tktool.widgets import CreateToolTip

root = tk.Tk()
root.title("Example")
root.geometry("400x500")

label = tk.Label(root, text="Example text")
label.pack(side=tk.TOP)
CreateToolTip(label, text="Example tooltip", fg="red")

root.mainloop()
```
