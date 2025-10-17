# Tk Tool Module

**Source:** `jsktoolbox/tktool`

**High-Level Introduction:**  
`tktool` groups the foundational Tkinter utilities used across JskToolBox. It delivers mixins, layout helpers, clipboard integrations, and reusable widgets that reduce boilerplate in graphical tools. The unreliable `_TkClip` backend is intentionally omitted from this overview; rely on the remaining clipboard adapters exposed through `ClipBoard`.

## Getting Started

Import the classes needed for your UI layer. The package exposes lazy exports so Tkinter-heavy helpers are imported only when referenced, keeping headless scripts responsive.

```python
from jsktoolbox.tktool import (
    TkBase,
    Pack,
    Grid,
    Place,
    ClipBoard,
    StatusBarTkFrame,
    StatusBarTtkFrame,
    CreateToolTip,
)
```

The lazy loader ensures the Tk event loop is not initialised until you access a GUI-facing symbol.

---

## `base` Module

**Source:** `jsktoolbox/tktool/base.py`

**Module Introduction:**  
Provides a lightweight mixin that standardises common Tkinter attributes and prevents accidental dynamic attribute creation on toolkit widgets.

### `TkBase` Class

**Class Introduction:**  
Inherits from `NoDynamicAttributes` and documents the canonical Tk attributes (`master`, `children`, `widgetName`, etc.) expected on toolkit components. Subclassing `TkBase` keeps widget state predictable across the project.

**Signature:**

```python
class TkBase(NoDynamicAttributes)
```

- **Attributes:**
  - `_name`, `_w`: Internal identifiers assigned by Tkinter.
  - `_tkloaded`, `_windowingsystem_cached`: Cached interpreter metadata.
  - `child`, `children`, `master`, `tk`, `widgetName`: Standard widget references surfaced for derived classes.

**Usage Example:**

```python
class StatusDisplay(TkBase, tk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Ready").pack()
```

---

## `layout` Module

**Source:** `jsktoolbox/tktool/layout.py`

**Module Introduction:**  
Wraps Tkinter geometry manager constants inside read-only containers, making layout code expressive and typo-resistant.

### `Pack` Class

**Class Introduction:**  
Exposes namespaces for the `anchor`, `side`, and `fill` options used with `pack`.

- **Nested Containers:**
  - `Anchor`: `Pack.Anchor.N`, `Pack.Anchor.SW`, etc.
  - `Side`: `Pack.Side.LEFT`, `Pack.Side.TOP`, etc.
  - `Fill`: `Pack.Fill.BOTH`, `Pack.Fill.X`, etc.

**Usage Example:**

```python
label.pack(side=Pack.Side.RIGHT, anchor=Pack.Anchor.NE, fill=Pack.Fill.X)
```

### `Grid` Class

**Class Introduction:**  
Provides the `Sticky` enumeration mirroring the sticky parameter supported by the grid geometry manager.

- **Nested Containers:**
  - `Sticky`: `Grid.Sticky.N`, `Grid.Sticky.EW`, `Grid.Sticky.SE`, and more.

**Usage Example:**

```python
button.grid(row=0, column=1, sticky=Grid.Sticky.EW)
```

### `Place` Class

**Class Introduction:**  
Collects anchor constants for the `place` geometry manager, defining which portion of the widget aligns with supplied coordinates.

- **Nested Containers:**
  - `Anchor`: `Place.Anchor.CENTER`, `Place.Anchor.NW`, etc.

**Usage Example:**

```python
tooltip.place(x=10, y=20, anchor=Place.Anchor.NW)
```

---

## `tools` Module

**Source:** `jsktoolbox/tktool/tools.py`

**Module Introduction:**  
Implements cross-platform clipboard helpers that automatically pick a working backend among X11, Gtk, Qt, Windows, and macOS implementations. The problematic `_TkClip` backend is excluded from documentation and from recommended use.

### `ClipBoard` Class

**Class Introduction:**  
Serves as a façade over the available clipboard adapters, exposing unified `copy` and `paste` properties after a backend is selected.

### `ClipBoard.__init__()`

**Detailed Description:**  
Attempts to instantiate `_XClip`, `_XSel`, `_GtkClip`, `_QtClip`, `_WinClip`, and `_MacClip` (in that order). The first helper that reports availability is cached for subsequent operations. If none succeed, an informational message is printed.

**Signature:**

```python
def __init__(self) -> None
```

- **Returns:** `None` – Constructor triggers backend detection.
- **Raises:** None – Failures lead to a disabled clipboard tool.

### `ClipBoard.is_tool`

**Detailed Description:**  
Indicates whether a functional backend has been registered.

**Signature:**

```python
@property
def is_tool(self) -> bool
```

- **Returns:** `bool` – `True` when clipboard operations are available.

### `ClipBoard.copy`

**Detailed Description:**  
Returns the callable responsible for copying text. When no backend is active, a no-op lambda is returned after logging the issue.

**Signature:**

```python
@property
def copy(self) -> Callable[[str], None]
```

### `ClipBoard.paste`

**Detailed Description:**  
Returns the callable that retrieves clipboard text. In inactive scenarios, the property returns a lambda producing an empty string.

**Signature:**

```python
@property
def paste(self) -> Callable[[], str]
```

**Usage Example:**

```python
clipboard = ClipBoard()
if clipboard.is_tool:
    clipboard.copy("Copied from JskToolBox")
    text = clipboard.paste()
```

---

## `widgets` Module

**Source:** `jsktoolbox/tktool/widgets.py`

**Module Introduction:**  
Supplies reusable Tk and ttk widgets that encapsulate status bars, tooltips, and vertically scrollable frames, aligning them with toolkit mixins and conventions.

### `StatusBarTkFrame` Class

**Class Introduction:**  
Implements a Tk-based status bar with a configurable `StringVar` label and optional size grip.

- **Key Members:**
  - `__init__(master, *args, **kwargs)`: Builds the frame, label, and size grip.
  - `set(value: str)`: Updates the displayed message.
  - `clear()`: Resets the label to an empty string.

### `StatusBarTtkFrame` Class

**Class Introduction:**  
Provides the same API as `StatusBarTkFrame` but leverages ttk widgets for themed applications.

### `CreateToolTip` Class

**Class Introduction:**  
Attaches delayed tooltips to any Tk widget, managing scheduling (`wait_time`), wrapping (`wrap_length`), and display attributes.

- **Key Members:**
  - `__init__(widget, text="widget info", wait_time=500, wrap_length=0, **kwargs)`: Configures the tooltip and binds events.
  - `text` property: Accepts strings, iterables of strings (joined by newlines), or a `tk.StringVar`.

**Usage Example:**

```python
button = ttk.Button(root, text="Submit")
button.pack()
CreateToolTip(button, text="Send data to the server", wait_time=300)
```

### `VerticalScrolledTkFrame` Class

**Class Introduction:**  
Creates a scrollable container using a Tk canvas, vertical scrollbar, and an `interior` frame that receives child widgets.

- **Key Members:**
  - `interior` property: Returns the frame used to arrange child widgets.
  - Mouse wheel handlers: Ensure consistent scrolling across platforms.

**Usage Example:**

```python
scrolled = VerticalScrolledTkFrame(root)
scrolled.pack(fill=tk.BOTH, expand=True)
for idx in range(20):
    tk.Label(scrolled.interior, text=f"Item {idx}").pack(anchor=tk.W)
```

### `VerticalScrolledTtkFrame` Class

**Class Introduction:**  
The ttk counterpart to `VerticalScrolledTkFrame`, offering the same behaviour with themed controls.

**Usage Example:**

```python
scrolled = VerticalScrolledTtkFrame(root)
scrolled.pack(fill=tk.BOTH, expand=True)
ttk.Button(scrolled.interior, text="Action").grid(row=0, column=0, sticky=Grid.Sticky.W)
```

---
