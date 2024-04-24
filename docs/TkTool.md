# TkTool

The project contains classes useful for tkinter-based projects.

## Public classes

1. [CreateToolTip](https://github.com/Szumak75/JskToolBox/blob/1.0.18/docs/TkTool.md#createtooltip)
1. [VerticalScrolledTkFrame](https://github.com/Szumak75/JskToolBox/blob/1.0.18/docs/TkTool.md#verticalscrolledtkframe)
1. [VerticalScrolledTtkFrame](https://github.com/Szumak75/JskToolBox/blob/1.0.18/docs/TkTool.md#verticalscrolledttkframe)

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
    **kwargs
)
```

Arguments:

- **widget** [tk.Misc] - _Parent widget handler_
- **text** [Union[str, List[str], Tuple[str], tk.StringVar]] - _text displayed in tooltip_
- **wait_time** [int] - _delay of displaying tooltip [ms]_
- **wrap_length** [int] - _limit the number of characters on each line to the specified value.
                The default value of 0 means that lines will only be broken on newlines_

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

## VerticalScrolledTkFrame

Creates vertical scrolled Frame derived from tk.Frame

### Import

```
from jsktoolbox.tktool.widgets import VerticalScrolledTkFrame
```

## Example

```
import tkinter as tk
from jsktoolbox.tktool.widgets import (
    VerticalScrolledTkFrame,
    CreateToolTip,
)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollbar Test")
    root.geometry("400x500")
    root.minsize(width=300, height=400)

    frame = VerticalScrolledTkFrame(
        root, width=300, borderwidth=2, relief=tk.SUNKEN, background="light gray"
    )

    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)  # fill window

    for i in range(30):
        line = tk.Frame(frame.interior, borderwidth=1, relief=tk.GROOVE)

        line.pack(side=tk.TOP, fill=tk.X, anchor=tk.CENTER, expand=tk.TRUE)
        label = tk.Label(line, text="This is a label " + str(i))
        label.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X)

        text = tk.Entry(line, textvariable=tk.StringVar(value="text"))
        sv = tk.StringVar(value=f"text nr {i}")
        CreateToolTip(text, text=sv)
        sv.set(f"text nr {i+1}")
        text.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.X)

    root.mainloop()
```

## VerticalScrolledTtkFrame

Creates vertical scrolled Frame derived from ttk.Frame

### Import

```
from jsktoolbox.tktool.widgets import VerticalScrolledTtkFrame
```

### Example

```
import tkinter as tk
from tkinter import ttk
from jsktoolbox.tktool.widgets import (
    VerticalScrolledTtkFrame,
    CreateToolTip,
)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollbar Test")
    root.geometry("400x500")
    root.minsize(width=300, height=400)

    frame = VerticalScrolledTtkFrame(root, width=300, borderwidth=2, relief=tk.SUNKEN)

    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)  # fill window

    for i in range(30):
        line = ttk.Frame(frame.interior, borderwidth=1, relief=tk.GROOVE)

        line.pack(side=tk.TOP, fill=tk.X, anchor=tk.CENTER, expand=tk.TRUE)
        label = ttk.Label(line, text="This is a label " + str(i))
        label.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X)

        text = ttk.Entry(line, style="info.TEntry")
        text.insert(0, f"test {i}")

        sv = tk.StringVar()
        sv.set(f"text nr {i}")
        CreateToolTip(text, text=sv)
        sv.set(f"text nr {i+1}")
        text.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.X)

    root.mainloop()
```
