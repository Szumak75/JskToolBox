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
from typing import Any, Optional


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


class VerticalScrolledTkFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' property to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

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


class VerticalScrolledTtkFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' property to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

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
