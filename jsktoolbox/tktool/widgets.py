# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide reusable Tk/ttk widgets such as status bars, tooltips, and scrollable frames.

The module centralises convenience components that enhance Tkinter UIs with common patterns like
status reporting, hover hints, and vertically scrolling containers.

VerticalScrolledFrame based on https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8
"""


import tkinter as tk
from tkinter import Toplevel, ttk
from typing import Any, Optional, List, Tuple, Union, Dict

from ..attribtool import ReadOnlyClass
from ..basetool import BData

from .base import TkBase


class _StatusBarMixin(BData):
    """Mixin for status bar widgets.

    Defines common properties and methods for status bar implementations.
    """

    class __Keys(object, metaclass=ReadOnlyClass):
        """Read-only class for defining constant keys.

        Prevents modification of class attributes after definition, ensuring immutability of key values.
        """

        STATUS: str = "__status__"
        LABEL: str = "__label__"
        SIZEGRIP: str = "__sizegrip__"

    def set(self, value: str) -> None:
        """Update the status label text.

        ### Arguments:
        * value: str - Text displayed inside the status label.

        ### Returns:
        None - Performs widget update side effects.

        ### Raises:
        * None: Tkinter handles rendering errors internally.
        """
        self._status.set(value)
        self._status_label.update_idletasks()

    def clear(self) -> None:
        """Reset the status label to an empty string.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs widget update side effects.

        ### Raises:
        * None: Tkinter handles rendering errors internally.
        """
        self._status.set("")
        self._status_label.update_idletasks()

    @property
    def _status(self) -> tk.StringVar:
        """Return the internal status StringVar.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        tk.StringVar - The StringVar instance that holds the status text.

        ### Raises:
        * None: Accessors return cached references only.
        """
        obj: Optional[tk.StringVar] = self._get_data(key=self.__Keys.STATUS)
        if obj is None:
            obj = tk.StringVar()
        return obj

    @_status.setter
    def _status(self, value: tk.StringVar) -> None:
        """Set the internal status StringVar.

        ### Arguments:
        * value: tk.StringVar - The StringVar instance to store as the status variable.

        ### Returns:
        None - Updates the internal reference for the status variable.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        self._set_data(
            key=self.__Keys.STATUS, value=value, set_default_type=tk.StringVar
        )

    @property
    def _status_label(self) -> Union[tk.Label, ttk.Label]:
        """Return the internal status label widget.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Union[tk.Label, ttk.Label] - The Label instance that displays the status text.

        ### Raises:
        * None: Accessors return cached references only.
        """
        obj: Optional[Union[tk.Label, ttk.Label]] = self._get_data(
            key=self.__Keys.LABEL
        )
        if obj is None:
            obj = tk.Label()
        return obj

    @_status_label.setter
    def _status_label(self, value: Union[tk.Label, ttk.Label]) -> None:
        """Set the internal status label widget.

        ### Arguments:
        * value: Union[tk.Label, ttk.Label] - The Label instance to store as the status label.

        ### Returns:
        None - Updates the internal reference for the status label widget.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        self._set_data(
            key=self.__Keys.LABEL,
            value=value,
            set_default_type=Union[tk.Label, ttk.Label],
        )

    @property
    def _sizegrip(self) -> ttk.Sizegrip:
        """Return the internal size grip widget.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        ttk.Sizegrip - The Sizegrip instance that provides resizing functionality.

        ### Raises:
        * None: Accessors return cached references only.
        """
        obj: Optional[ttk.Sizegrip] = self._get_data(key=self.__Keys.SIZEGRIP)
        if obj is None:
            obj = ttk.Sizegrip()
        return obj

    @_sizegrip.setter
    def _sizegrip(self, value: ttk.Sizegrip) -> None:
        """Set the internal size grip widget.

        ### Arguments:
        * value: ttk.Sizegrip - The Sizegrip instance to store as the size grip.

        ### Returns:
        None - Updates the internal reference for the size grip widget.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        self._set_data(
            key=self.__Keys.SIZEGRIP, value=value, set_default_type=ttk.Sizegrip
        )


class StatusBarTkFrame(tk.Frame, TkBase, _StatusBarMixin):
    """Tkinter status bar frame.

    Renders a label-driven status bar with a size grip for resizing actions.
    """

    def __init__(self, master: Optional[tk.Misc], *args, **kwargs) -> None:
        """Initialise the Tkinter status bar.

        ### Arguments:
        * master: tk.Misc - Parent widget that owns this frame.
        * *args: Any - Positional arguments forwarded to `tk.Frame`.
        * **kwargs: Any - Keyword arguments forwarded to `tk.Frame`.

        ### Returns:
        None - Constructor configures widget state.

        ### Raises:
        * None: Construction relies on Tkinter widget creation only.
        """
        tk.Frame.__init__(self, master, *args, **kwargs)

        self._status = tk.StringVar()
        self._status.set("Status Bar")
        self._status_label = tk.Label(
            self, bd=1, relief=tk.FLAT, anchor=tk.W, textvariable=self._status
        )
        self._status_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.TRUE, padx=5, pady=1)

        # size grip
        self._sizegrip = ttk.Sizegrip(self)
        self._sizegrip.pack(side=tk.RIGHT, anchor=tk.SE)


class StatusBarTtkFrame(ttk.Frame, TkBase, _StatusBarMixin):
    """ttk status bar frame.

    Provides a themed status label with an optional size grip.
    """

    def __init__(self, master: Optional[tk.Misc], *args, **kwargs) -> None:
        """Initialise the ttk status bar.

        ### Arguments:
        * master: tk.Misc - Parent widget that owns this frame.
        * *args: Any - Positional arguments forwarded to `ttk.Frame`.
        * **kwargs: Any - Keyword arguments forwarded to `ttk.Frame`.

        ### Returns:
        None - Constructor configures widget state.

        ### Raises:
        * None: Construction relies on ttk widget creation only.
        """
        ttk.Frame.__init__(self, master, *args, **kwargs)

        self._status = tk.StringVar()
        self._status.set("Status Bar")
        self._status_label = ttk.Label(self, anchor=tk.W, textvariable=self._status)
        self._status_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.TRUE, padx=5, pady=1)

        # size grip
        self._sizegrip = ttk.Sizegrip(self)
        self._sizegrip.pack(side=tk.RIGHT, anchor=tk.SE)


class CreateToolTip(TkBase):
    """Tooltip manager for Tk widgets.

    Attaches hover-driven handlers that display timed toplevel hints for a target widget.
    """

    __id: Optional[str] = None
    __tw: Optional[tk.Toplevel] = None
    __wait_time: int = None  # type: ignore
    __widget: tk.Misc = None  # type: ignore
    __wrap_length: int = None  # type: ignore
    __text: Union[str, List[str], Tuple[str]] = None  # type: ignore
    __text_variable: tk.StringVar = None  # type: ignore
    __label_attr: Dict[str, Any] = None  # type: ignore

    def __init__(
        self,
        widget: tk.Misc,
        text: Union[str, List[str], Tuple[str], tk.StringVar] = "widget info",
        wait_time: int = 500,
        wrap_length: int = 0,
        **kwargs,
    ) -> None:
        """Initialise the tooltip manager.

        ### Arguments:
        * widget: tk.Misc - Widget that triggers tooltip display on hover.
        * text: Union[str, List[str], Tuple[str], tk.StringVar] - Tooltip message or Tk variable.
        * wait_time: int - Delay in milliseconds before the tooltip appears.
        * wrap_length: int - Maximum tooltip line width in pixels; 0 keeps Tk defaults.
        * **kwargs: Any - Extra keyword arguments forwarded to the tooltip label configuration.

        ### Returns:
        None - Constructor stores configuration and binds widget events.

        ### Raises:
        * None: Tkinter propagates runtime errors when they occur.
        """
        # set default attributes
        self.__label_attr = {
            "justify": tk.LEFT,
            "bg": "white",
            "relief": tk.SOLID,
            "borderwidth": 1,
        }
        # update attributes
        if kwargs:
            self.__label_attr.update(kwargs)

        self.__wait_time = wait_time
        self.__wrap_length = wrap_length
        self.__widget = widget

        # set message
        self.text = text
        self.__widget.bind("<Enter>", self.__enter)
        self.__widget.bind("<Leave>", self.__leave)
        self.__widget.bind("<ButtonPress>", self.__leave)

    def __enter(self, event: Optional[tk.Event] = None) -> None:
        """Handle the `<Enter>` event.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload supplied by the binding.

        ### Returns:
        None - Schedules tooltip presentation.

        ### Raises:
        * None: Scheduling operations route through Tkinter.
        """
        self.__schedule()

    def __leave(self, event: Optional[tk.Event] = None) -> None:
        """Handle the `<Leave>` event.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload supplied by the binding.

        ### Returns:
        None - Cancels any pending tooltip display and hides the tip.

        ### Raises:
        * None: Tkinter handles cancellation routines internally.
        """
        self.__unschedule()
        self.__hidetip()

    def __schedule(self) -> None:
        """Schedule tooltip presentation.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Registers a timed callback via `widget.after`.

        ### Raises:
        * None: Tkinter handles scheduling errors internally.
        """
        self.__unschedule()
        self.__id = self.__widget.after(self.__wait_time, self.__showtip)

    def __unschedule(self) -> None:
        """Cancel scheduled tooltip presentation.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Removes any pending `after` callbacks.

        ### Raises:
        * None: Tkinter handles cancellation failures internally.
        """
        __id: Optional[str] = self.__id
        self.__id = None
        if __id:
            self.__widget.after_cancel(__id)

    def __showtip(self, event: Optional[tk.Event] = None) -> None:
        """Display the tooltip window.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload supplied by the binding.

        ### Returns:
        None - Creates a transient toplevel with the tooltip label.

        ### Raises:
        * None: Tkinter manages window creation behaviour.
        """
        __x: int = 0
        __y: int = 0
        __cx: int
        __cy: int
        __x, __y, __cx, __cy = self.__widget.bbox("insert")  # type: ignore
        __x += self.__widget.winfo_rootx() + 25
        __y += self.__widget.winfo_rooty() + 20
        # creates a toplevel window
        self.__tw = tk.Toplevel(self.__widget)
        # Leaves only the label and removes the app window
        self.__tw.wm_overrideredirect(True)
        self.__tw.wm_geometry(f"+{__x}+{__y}")
        label = tk.Label(
            self.__tw,
            wraplength=self.__wrap_length,
        )
        for key in self.__label_attr.keys():
            label[key.lower()] = self.__label_attr[key]
        if isinstance(self.text, tk.StringVar):
            label["textvariable"] = self.text
        else:
            label["text"] = self.text
        label.pack(ipadx=1)

    def __hidetip(self) -> None:
        """Hide the tooltip window.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Destroys the transient toplevel when present.

        ### Raises:
        * None: Tkinter handles destruction errors internally.
        """
        __tw: Optional[Toplevel] = self.__tw
        self.__tw = None
        if __tw:
            __tw.destroy()

    @property
    def text(self) -> Union[str, tk.StringVar]:
        """Return the tooltip text or Tk variable.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Union[str, tk.StringVar] - Current text payload, flattened when a list or tuple is provided.

        ### Raises:
        * None: Text retrieval is free of side effects.
        """
        if self.__text is None and self.__text_variable is None:
            self.__text = ""
        if self.__text_variable is None:
            if isinstance(self.__text, (List, Tuple)):
                tmp: str = ""
                for msg in self.__text:
                    tmp += msg if not tmp else f"\n{msg}"
                return tmp
            return self.__text
        else:
            return self.__text_variable

    @text.setter
    def text(self, value: Union[str, List[str], Tuple[str], tk.StringVar]) -> None:
        """Set the tooltip text content.

        ### Arguments:
        * value: Union[str, List[str], Tuple[str], tk.StringVar] - Tooltip message or Tk variable.

        ### Returns:
        None - Updates internal references for future tooltip displays.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        if isinstance(value, tk.StringVar):
            self.__text_variable = value
        else:
            self.__text = value


class _VerticalScrolledMixin(BData):
    """Mixin for vertical scrolled frame widgets.

    Defines common properties and methods for scrollable frame implementations.
    """

    class __Keys(object, metaclass=ReadOnlyClass):
        """Read-only class for defining constant keys.

        Prevents modification of class attributes after definition, ensuring immutability of key values.
        """

        INTERIOR: str = "__interior__"
        INTERIOR_ID: str = "__interior_id__"
        CANVAS: str = "__canvas__"
        VSCROLLBAR: str = "__vscrollbar__"

    @property
    def _interior(self) -> Union[tk.Frame, ttk.Frame]:
        """Return the interior frame container.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Union[tk.Frame, ttk.Frame] - The frame that should receive child widgets.
        """
        obj: Optional[Union[tk.Frame, ttk.Frame]] = self._get_data(
            key=self.__Keys.INTERIOR
        )
        if obj is None:
            obj = tk.Frame()
        return obj

    @_interior.setter
    def _interior(self, value: Union[tk.Frame, ttk.Frame]) -> None:
        """Set the interior frame container.

        ### Arguments:
        * value: Union[tk.Frame, ttk.Frame] - The frame to set as the interior container.

        ### Returns:
        None - Updates internal reference for the interior frame.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        self._set_data(
            key=self.__Keys.INTERIOR,
            value=value,
            set_default_type=Union[tk.Frame, ttk.Frame],
        )

    @property
    def _interior_id(self) -> int:
        """Return the interior frame's canvas window ID.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        int - The canvas item ID for the interior frame, or 0 if not available.

        ### Raises:
        * None: Accessors return cached references only.
        """
        obj: Optional[int] = self._get_data(
            key=self.__Keys.INTERIOR_ID, default_value=0
        )
        if obj is None:
            return 0
        return obj

    @_interior_id.setter
    def _interior_id(self, value: int) -> None:
        """Set the interior frame's canvas window ID.

        ### Arguments:
        * value: int - The canvas item ID to associate with the interior frame.

        ### Returns:
        None - Updates internal reference for the interior frame's canvas ID.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        self._set_data(key=self.__Keys.INTERIOR_ID, value=value, set_default_type=int)

    @property
    def _canvas(self) -> tk.Canvas:
        """Return the canvas widget.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        tk.Canvas - The canvas that provides the scrolling mechanism.
        """
        obj: Optional[tk.Canvas] = self._get_data(key=self.__Keys.CANVAS)
        if obj is None:
            obj = tk.Canvas()
        return obj

    @_canvas.setter
    def _canvas(self, value: tk.Canvas) -> None:
        """Set the canvas widget.

        ### Arguments:
        * value: tk.Canvas - The canvas to set as the scrolling mechanism.

        ### Returns:
        None - Updates internal reference for the canvas widget.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        self._set_data(key=self.__Keys.CANVAS, value=value, set_default_type=tk.Canvas)

    @property
    def _vscrollbar(self) -> Union[tk.Scrollbar, ttk.Scrollbar]:
        """Return the vertical scrollbar widget.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Union[tk.Scrollbar, ttk.Scrollbar] - The scrollbar that controls vertical scrolling.

        ### Raises:
        * None: Accessors return cached references only.
        """
        obj: Optional[Union[tk.Scrollbar, ttk.Scrollbar]] = self._get_data(
            key=self.__Keys.VSCROLLBAR
        )
        if obj is None:
            obj = tk.Scrollbar()
        return obj

    @_vscrollbar.setter
    def _vscrollbar(self, value: Union[tk.Scrollbar, ttk.Scrollbar]) -> None:
        """Set the vertical scrollbar widget.

        ### Arguments:
        * value: Union[tk.Scrollbar, ttk.Scrollbar] - The scrollbar to set as the vertical scroller.

        ### Returns:
        None - Updates internal reference for the vertical scrollbar widget.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        self._set_data(
            key=self.__Keys.VSCROLLBAR,
            value=value,
            set_default_type=Union[tk.Scrollbar, ttk.Scrollbar],
        )


class VerticalScrolledTkFrame(tk.Frame, TkBase, _VerticalScrolledMixin):
    """Scrollable Tk frame container.

    Provides a canvas-driven vertical scroller and exposes an interior frame for child widgets.
    """

    def __init__(self, master: tk.Misc, *args, **kw) -> None:
        """Initialise the vertical scrolled Tk frame.

        ### Arguments:
        * master: tk.Misc - Parent widget container.
        * *args: Any - Additional positional arguments passed to `tk.Frame`.
        * **kw: Any - Additional keyword arguments passed to `tk.Frame`.

        ### Returns:
        None - Constructor configures the scrolling container and event bindings.
        """
        tk.Frame.__init__(self, master, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        # vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self._vscrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self._canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=self._vscrollbar.set
        )
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self._vscrollbar.config(command=self._canvas.yview)

        # Reset the view
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        # self.interior = interior = ttk.Frame(canvas)
        self._interior = tk.Frame(self._canvas)
        self._interior_id: int = self._canvas.create_window(
            0, 0, window=self._interior, anchor=tk.NW
        )

        # Configure Events
        self._interior.bind("<Configure>", self.__configure_interior)
        self._canvas.bind("<Configure>", self.__configure_canvas)
        self._canvas.bind("<Enter>", self.__bind_mouse)
        self._canvas.bind("<Leave>", self.__unbind_mouse)

    @property
    def interior(self) -> tk.Frame:
        """Return the interior frame container.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        tk.Frame - Frame that should receive child widgets.

        ### Raises:
        * None: Accessors return cached references only.
        """
        return self._interior  # type: ignore

    def __configure_interior(self, event: Optional[tk.Event] = None) -> None:
        """Recompute the canvas scroll region from interior frame geometry.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload from `<Configure>`.

        ### Returns:
        None - Updates canvas scroll region and optional width synchronisation.
        """
        # Update the scrollbar to match the size of the inner frame.
        self._canvas.config(
            scrollregion=(
                0,
                0,
                self._interior.winfo_reqwidth(),
                self._interior.winfo_reqheight(),
            )
        )
        if self._interior.winfo_reqwidth() != self._canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self._canvas.config(width=self._interior.winfo_reqwidth())

    def __configure_canvas(self, event: Optional[tk.Event] = None) -> None:
        """Synchronise the interior frame width with the visible canvas width.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload from `<Configure>`.

        ### Returns:
        None - Updates canvas window item width when dimensions differ.
        """
        if self._interior.winfo_reqwidth() != self._canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self._canvas.itemconfigure(
                self._interior_id, width=self._canvas.winfo_width()
            )

    def __bind_mouse(self, event: Optional[tk.Event] = None) -> None:
        """Bind global mouse wheel handlers when cursor enters the canvas.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload from `<Enter>`.

        ### Returns:
        None - Registers wheel bindings for Linux and Windows/macOS patterns.
        """
        self._canvas.bind_all("<4>", self.__on_mousewheel)
        self._canvas.bind_all("<5>", self.__on_mousewheel)
        self._canvas.bind_all("<MouseWheel>", self.__on_mousewheel)

    def __unbind_mouse(self, event: Optional[tk.Event] = None) -> None:
        """Remove global mouse wheel handlers when cursor leaves the canvas.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload from `<Leave>`.

        ### Returns:
        None - Unregisters wheel bindings installed by `__bind_mouse`.
        """
        self._canvas.unbind_all("<4>")
        self._canvas.unbind_all("<5>")
        self._canvas.unbind_all("<MouseWheel>")

    def __on_mousewheel(self, event: tk.Event) -> None:
        """Translate mouse wheel events into vertical scrolling.

        Linux relies on `event.num` while Windows and macOS provide `event.delta`.

        ### Arguments:
        * event: tk.Event - Mouse wheel event emitted by Tkinter.

        ### Returns:
        None - Adjusts the canvas viewport in response to the event.

        ### Raises:
        * None: Scroll handling defers to Tkinter canvas methods.
        """
        if event.num == 4 or event.delta > 0:
            self._canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self._canvas.yview_scroll(1, "units")


class VerticalScrolledTtkFrame(ttk.Frame, TkBase, _VerticalScrolledMixin):
    """Scrollable ttk frame container.

    Uses a Tk canvas plus a themed frame to offer vertical scrolling for child widgets.
    """

    def __init__(self, master: tk.Misc, *args, **kw) -> None:
        """Initialise the vertical scrolled ttk frame.

        ### Arguments:
        * master: tk.Misc - Parent widget container.
        * *args: Any - Additional positional arguments passed to `ttk.Frame`.
        * **kw: Any - Additional keyword arguments passed to `ttk.Frame`.

        ### Returns:
        None - Constructor configures the scrolling container and event bindings.
        """
        ttk.Frame.__init__(self, master, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        # vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._vscrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self._canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=self._vscrollbar.set
        )
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self._vscrollbar.config(command=self._canvas.yview)

        # Reset the view
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        # self.interior = interior = ttk.Frame(canvas)
        self._interior = ttk.Frame(self._canvas)
        self._interior_id: int = self._canvas.create_window(
            0, 0, window=self._interior, anchor=tk.NW
        )

        # Configure Events
        self._interior.bind("<Configure>", self.__configure_interior)
        self._canvas.bind("<Configure>", self.__configure_canvas)
        self._canvas.bind("<Enter>", self.__bind_mouse)
        self._canvas.bind("<Leave>", self.__unbind_mouse)

    @property
    def interior(self) -> ttk.Frame:
        """Return the interior frame container.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        ttk.Frame - Themed frame that should receive child widgets.

        ### Raises:
        * None: Accessors return cached references only.
        """
        return self._interior  # type: ignore

    def __configure_interior(self, event: Optional[tk.Event] = None) -> None:
        """Recompute the canvas scroll region from interior frame geometry.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload from `<Configure>`.

        ### Returns:
        None - Updates canvas scroll region and optional width synchronisation.
        """
        # Update the scrollbar to match the size of the inner frame.
        self._canvas.config(
            scrollregion=(
                0,
                0,
                self._interior.winfo_reqwidth(),
                self._interior.winfo_reqheight(),
            )
        )
        if self._interior.winfo_reqwidth() != self._canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self._canvas.config(width=self._interior.winfo_reqwidth())

    def __configure_canvas(self, event: tk.Event) -> None:
        """Synchronise the interior frame width with the visible canvas width.

        ### Arguments:
        * event: tk.Event - Tkinter event payload from `<Configure>`.

        ### Returns:
        None - Updates canvas window item width when dimensions differ.
        """
        if self._interior.winfo_reqwidth() != self._canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self._canvas.itemconfigure(
                self._interior_id, width=self._canvas.winfo_width()
            )

    def __bind_mouse(self, event: Optional[tk.Event] = None) -> None:
        """Bind global mouse wheel handlers when cursor enters the canvas.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload from `<Enter>`.

        ### Returns:
        None - Registers wheel bindings for Linux and Windows/macOS patterns.
        """
        self._canvas.bind_all("<4>", self.__on_mousewheel)
        self._canvas.bind_all("<5>", self.__on_mousewheel)
        self._canvas.bind_all("<MouseWheel>", self.__on_mousewheel)

    def __unbind_mouse(self, event: Optional[tk.Event] = None) -> None:
        """Remove global mouse wheel handlers when cursor leaves the canvas.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload from `<Leave>`.

        ### Returns:
        None - Unregisters wheel bindings installed by `__bind_mouse`.
        """
        self._canvas.unbind_all("<4>")
        self._canvas.unbind_all("<5>")
        self._canvas.unbind_all("<MouseWheel>")

    def __on_mousewheel(self, event: tk.Event) -> None:
        """Translate mouse wheel events into vertical scrolling.

        Linux relies on `event.num` while Windows and macOS provide `event.delta`.

        ### Arguments:
        * event: tk.Event - Mouse wheel event emitted by Tkinter.

        ### Returns:
        None - Adjusts the canvas viewport in response to the event.

        ### Raises:
        * None: Scroll handling defers to Tkinter canvas methods.
        """
        if event.num == 4 or event.delta > 0:
            self._canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self._canvas.yview_scroll(1, "units")


# #[EOF]#######################################################################
