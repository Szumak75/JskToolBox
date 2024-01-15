# -*- coding: utf-8 -*-
"""
  widgets.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 15.01.2024, 10:42:01
  
  Purpose: custom tkinter widgets.

  VerticalScrolledFrame: https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8
"""

# try:
#     import tkinter as tk
# except ImportError:
#     import Tkinter as tk

import tkinter as tk
from tkinter import ttk
from typing import Any, Optional, List, Tuple, Union, Dict

from jsktoolbox.tktool.base import TkBase


class CreateToolTip(TkBase):
    """Create a tooltip for a given widget."""

    __id: Optional[str] = None
    __tw: Optional[tk.Toplevel] = None
    __waittime: int = None  # type: ignore
    __widget: tk.Misc = None  # type: ignore
    __wraplength: int = None  # type: ignore
    __text: Union[str, List, Tuple] = None  # type: ignore
    __textvariable: tk.StringVar = None  # type: ignore
    __label_attr: Dict[str, Any] = None  # type: ignore

    def __init__(
        self,
        widget: tk.Misc,
        text: Union[str, List, Tuple, tk.StringVar] = "widget info",
        wait_time: int = 500,
        wrap_length: int = 0,
        **kwargs,
    ) -> None:
        """Create class object."""
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

        self.__waittime = wait_time
        self.__wraplength = wrap_length
        self.__widget = widget

        # set message
        self.text = text
        self.__widget.bind("<Enter>", self.__enter)
        self.__widget.bind("<Leave>", self.__leave)
        self.__widget.bind("<ButtonPress>", self.__leave)

    def __enter(self, event: Optional[tk.Event] = None) -> None:
        """Call on <Enter> event."""
        self.__schedule()

    def __leave(self, event: Optional[tk.Event] = None) -> None:
        """Call on <Leave> event."""
        self.__unschedule()
        self.__hidetip()

    def __schedule(self) -> None:
        """Schedule method."""
        self.__unschedule()
        self.__id = self.__widget.after(self.__waittime, self.__showtip)

    def __unschedule(self) -> None:
        """Unschedule method."""
        __id = self.__id
        self.__id = None
        if __id:
            self.__widget.after_cancel(__id)

    def __showtip(self, event: Optional[tk.Event] = None) -> None:
        """Show tooltip."""
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
            wraplength=self.__wraplength,
        )
        for key in self.__label_attr.keys():
            label[key.lower()] = self.__label_attr[key]
        if isinstance(self.text, tk.StringVar):
            label["textvariable"] = self.text
        else:
            label["text"] = self.text
        label.pack(ipadx=1)

    def __hidetip(self) -> None:
        """Hide tooltip."""
        __tw = self.__tw
        self.__tw = None
        if __tw:
            __tw.destroy()

    @property
    def text(self) -> Union[str, tk.StringVar]:
        """Return text message."""
        if self.__text is None and self.__textvariable is None:
            self.__text = ""
        if self.__textvariable is None:
            if isinstance(self.__text, (List, Tuple)):
                tmp: str = ""
                for msg in self.__text:
                    tmp += msg if not tmp else f"\n{msg}"
                return tmp
            return self.__text
        else:
            return self.__textvariable

    @text.setter
    def text(self, value: Union[str, List, Tuple, tk.StringVar]) -> None:
        """Set text message object."""
        if isinstance(value, tk.StringVar):
            self.__textvariable = value
        else:
            self.__text = value


class VerticalScrolledFrame(tk.Misc):
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """

    def __init__(self, master, **kwargs) -> None:
        width = kwargs.pop("width", None)
        height = kwargs.pop("height", None)
        bg = kwargs.pop("bg", kwargs.pop("background", None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(
            self.outer,
            highlightthickness=0,
            width=width,
            height=height,
            bg=bg,
            # self.outer,
            # highlightthickness=0,
            # bg=bg,
            relief=tk.GROOVE,
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.canvas["yscrollcommand"] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb["command"] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # self.inner.pack(fill=tk.X)  # , expand=tk.TRUE)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor=tk.NW)
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None) -> None:
        x1: int
        y1: int
        x2: int
        y2: int
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height: int = self.canvas.winfo_height()
        self.canvas.config(scrollregion=(0, 0, x2, max(y2, height)))

    def _bind_mouse(self, event=None) -> None:
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None) -> None:
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event) -> None:
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def __str__(self) -> str:
        return str(self.outer)


class VerticalScrolledTkFrame(tk.Frame, TkBase):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' property to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    __vscrollbar: tk.Scrollbar = None  # type: ignore
    __canvas: tk.Canvas = None  # type: ignore
    __interior: tk.Frame = None  # type: ignore
    __interior_id: int = None  # type: ignore

    def __init__(self, parent: tk.Misc, *args, **kw) -> None:
        tk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        # vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.__canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=self.__vscrollbar.set
        )
        self.__canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.__vscrollbar.config(command=self.__canvas.yview)

        # Reset the view
        self.__canvas.xview_moveto(0)
        self.__canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        # self.interior = interior = ttk.Frame(canvas)
        self.__interior = tk.Frame(self.__canvas)
        self.__interior_id: int = self.__canvas.create_window(
            0, 0, window=self.__interior, anchor=tk.NW
        )

        # Configure Events
        self.__interior.bind("<Configure>", self.__configure_interior)
        self.__canvas.bind("<Configure>", self.__configure_canvas)
        self.__canvas.bind("<Enter>", self.__bind_mouse)
        self.__canvas.bind("<Leave>", self.__unbind_mouse)

    @property
    def interior(self) -> tk.Frame:
        """The interior property."""
        return self.__interior

    def __configure_interior(self, event) -> None:
        # Update the scrollbars to match the size of the inner frame.
        self.__canvas.config(
            scrollregion=(
                0,
                0,
                self.__interior.winfo_reqwidth(),
                self.__interior.winfo_reqheight(),
            )
        )
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.__canvas.config(width=self.__interior.winfo_reqwidth())

    def __configure_canvas(self, event: tk.Event) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.__canvas.itemconfigure(
                self.__interior_id, width=self.__canvas.winfo_width()
            )

    def __bind_mouse(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        self.__canvas.bind_all("<4>", self.__on_mousewheel)
        self.__canvas.bind_all("<5>", self.__on_mousewheel)
        self.__canvas.bind_all("<MouseWheel>", self.__on_mousewheel)

    def __unbind_mouse(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        self.__canvas.unbind_all("<4>")
        self.__canvas.unbind_all("<5>")
        self.__canvas.unbind_all("<MouseWheel>")

    def __on_mousewheel(self, event: tk.Event) -> None:
        """Linux uses event.num; Windows / Mac uses event.delta"""
        # print(f"{event}")
        # print(f"{type(event)}")
        if event.num == 4 or event.delta > 0:
            self.__canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.__canvas.yview_scroll(1, "units")


class VerticalScrolledTtkFrame(ttk.Frame, TkBase):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' property to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    __vscrollbar: ttk.Scrollbar = None  # type: ignore
    __canvas: tk.Canvas = None  # type: ignore
    __interior: ttk.Frame = None  # type: ignore
    __interior_id: int = None  # type: ignore

    def __init__(self, parent: tk.Misc, *args, **kw) -> None:
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        # vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.__canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=self.__vscrollbar.set
        )
        self.__canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.__vscrollbar.config(command=self.__canvas.yview)

        # Reset the view
        self.__canvas.xview_moveto(0)
        self.__canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        # self.interior = interior = ttk.Frame(canvas)
        self.__interior = ttk.Frame(self.__canvas)
        self.__interior_id: int = self.__canvas.create_window(
            0, 0, window=self.__interior, anchor=tk.NW
        )

        # Configure Events
        self.__interior.bind("<Configure>", self.__configure_interior)
        self.__canvas.bind("<Configure>", self.__configure_canvas)
        self.__canvas.bind("<Enter>", self.__bind_mouse)
        self.__canvas.bind("<Leave>", self.__unbind_mouse)

    @property
    def interior(self) -> ttk.Frame:
        """The interior property."""
        return self.__interior

    def __configure_interior(self, event) -> None:
        # Update the scrollbars to match the size of the inner frame.
        self.__canvas.config(
            scrollregion=(
                0,
                0,
                self.__interior.winfo_reqwidth(),
                self.__interior.winfo_reqheight(),
            )
        )
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.__canvas.config(width=self.__interior.winfo_reqwidth())

    def __configure_canvas(self, event: tk.Event) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.__canvas.itemconfigure(
                self.__interior_id, width=self.__canvas.winfo_width()
            )

    def __bind_mouse(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        self.__canvas.bind_all("<4>", self.__on_mousewheel)
        self.__canvas.bind_all("<5>", self.__on_mousewheel)
        self.__canvas.bind_all("<MouseWheel>", self.__on_mousewheel)

    def __unbind_mouse(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        self.__canvas.unbind_all("<4>")
        self.__canvas.unbind_all("<5>")
        self.__canvas.unbind_all("<MouseWheel>")

    def __on_mousewheel(self, event: tk.Event) -> None:
        """Linux uses event.num; Windows / Mac uses event.delta"""
        # print(f"{event}")
        # print(f"{type(event)}")
        if event.num == 4 or event.delta > 0:
            self.__canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.__canvas.yview_scroll(1, "units")


# #[EOF]#######################################################################
