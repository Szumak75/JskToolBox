# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide lightweight base mixins shared by Tk widgets in the toolkit.

Tk modules rely on these helpers to align Tkinter widget attributes with the broader toolkit
conventions, reducing boilerplate for derived classes.
"""

from typing import Any, Optional
from ..attribtool import ReadOnlyClass
from ..basetool import BData


class _Keys(object, metaclass=ReadOnlyClass):
    """Container for canonical Tkinter widget attribute keys.

    This class serves as a centralized reference for standard Tkinter widget attributes,
    ensuring consistency across the toolkit.
    """

    NAME = "__name__"
    TK_LOADED = "-_tkloaded__"
    W = "__w__"
    WINDOWING_SYSTEM_CACHED = "__windowing_system_cached__"
    CHILD = "__child__"
    CHILDREN = "__children__"
    MASTER = "__master__"
    TK = "__tk__"
    WIDGET_NAME = "__widget_name__"


class TkBase(BData):
    """Common Tk widget mixin.

    Disables dynamic attribute assignment and documents the canonical Tkinter attributes expected on
    toolkit widgets.
    """

    @property
    def _name(self) -> Optional[Any]:
        """The name of this widget."""
        return self._get_data(key=_Keys.NAME)

    @_name.setter
    def _name(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.NAME, value=value)

    @property
    def _tkloaded(self) -> Optional[Any]:
        """Indicates if the widget has been loaded into the Tk environment."""
        return self._get_data(key=_Keys.TK_LOADED)

    @_tkloaded.setter
    def _tkloaded(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.TK_LOADED, value=value)

    @property
    def _w(self) -> Optional[Any]:
        """The Tkinter widget identifier."""
        return self._get_data(key=_Keys.W)

    @_w.setter
    def _w(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.W, value=value)

    @property
    def _windowingsystem_cached(self) -> Optional[Any]:
        """Cached windowing system information."""
        return self._get_data(key=_Keys.WINDOWING_SYSTEM_CACHED)

    @_windowingsystem_cached.setter
    def _windowingsystem_cached(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.WINDOWING_SYSTEM_CACHED, value=value)

    @property
    def child(self) -> Optional[Any]:
        """The child widget."""
        return self._get_data(key=_Keys.CHILD)

    @child.setter
    def child(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.CHILD, value=value)

    @property
    def children(self) -> Optional[Any]:
        """The children widgets."""
        return self._get_data(key=_Keys.CHILDREN)

    @children.setter
    def children(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.CHILDREN, value=value)

    @property
    def master(self) -> Optional[Any]:
        """The master widget."""
        return self._get_data(key=_Keys.MASTER)

    @master.setter
    def master(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.MASTER, value=value)

    @property
    def tk(self) -> Optional[Any]:
        """The Tkinter root widget."""
        return self._get_data(key=_Keys.TK)

    @tk.setter
    def tk(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.TK, value=value)

    @property
    def widgetName(self) -> Optional[Any]:
        """The widget name."""
        return self._get_data(key=_Keys.WIDGET_NAME)

    @widgetName.setter
    def widgetName(self, value: Optional[Any]) -> None:
        self._set_data(key=_Keys.WIDGET_NAME, value=value)


# #[EOF]#######################################################################
