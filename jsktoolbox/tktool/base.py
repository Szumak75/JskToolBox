# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide lightweight base mixins shared by Tk widgets in the toolkit.

Tk modules rely on these helpers to align Tkinter widget attributes with the broader toolkit
conventions, reducing boilerplate for derived classes.
"""

from typing import Any, Dict, Optional
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
    def _name(self) -> str:
        """The name of this widget."""
        value = self._get_data(key=_Keys.NAME, default_value="")
        if value is not None:
            return value
        return ""

    @_name.setter
    def _name(self, value: str) -> None:
        self._set_data(key=_Keys.NAME, value=value, set_default_type=str)

    @property
    def _tkloaded(self) -> bool:
        """Indicates if the widget has been loaded into the Tk environment."""
        value = self._get_data(key=_Keys.TK_LOADED, default_value=False)
        if value is not None:
            return value
        return False

    @_tkloaded.setter
    def _tkloaded(self, value: bool) -> None:
        self._set_data(key=_Keys.TK_LOADED, value=value, set_default_type=bool)

    @property
    def _w(self) -> str:
        """The Tkinter widget identifier."""
        value = self._get_data(key=_Keys.W, default_value="")
        if value is not None:
            return value
        return ""

    @_w.setter
    def _w(self, value: Optional[str]) -> None:
        self._set_data(key=_Keys.W, value=value, set_default_type=str)

    @property
    def _windowingsystem_cached(self) -> str:
        """Cached windowing system information."""
        value = self._get_data(key=_Keys.WINDOWING_SYSTEM_CACHED)
        if value is not None:
            return value
        return ""

    @_windowingsystem_cached.setter
    def _windowingsystem_cached(self, value: str) -> None:
        self._set_data(
            key=_Keys.WINDOWING_SYSTEM_CACHED, value=value, set_default_type=str
        )

    @property
    def child(self) -> Optional[Any]:
        """The child widget."""
        return self._get_data(key=_Keys.CHILD)

    @child.setter
    def child(self, value: Optional[Any]) -> None:
        if value is not None:
            self._set_data(
                key=_Keys.CHILD, value=value, set_default_type=Optional[type(value)]
            )
        else:
            self._set_data(key=_Keys.CHILD, value=value)

    @property
    def children(self) -> Dict[str, Any]:
        """The children widgets."""
        value = self._get_data(key=_Keys.CHILDREN, default_value={})
        if value is not None:
            return value
        return {}

    @children.setter
    def children(self, value: Dict[str, Any]) -> None:
        self._set_data(key=_Keys.CHILDREN, value=value, set_default_type=Dict[str, Any])

    @property
    def master(self) -> Optional[Any]:
        """The master widget."""
        return self._get_data(key=_Keys.MASTER)

    @master.setter
    def master(self, value: Optional[Any]) -> None:
        if value is not None:
            self._set_data(
                key=_Keys.MASTER, value=value, set_default_type=Optional[type(value)]
            )
        else:
            self._set_data(key=_Keys.MASTER, value=value)

    @property
    def tk(self) -> Optional[Any]:
        """The Tkinter root widget."""
        return self._get_data(key=_Keys.TK)

    @tk.setter
    def tk(self, value: Optional[Any]) -> None:
        if value is not None:
            self._set_data(
                key=_Keys.TK, value=value, set_default_type=Optional[type(value)]
            )
        else:
            self._set_data(key=_Keys.TK, value=value)

    @property
    def widgetName(self) -> str:
        """The widget name."""
        value = self._get_data(key=_Keys.WIDGET_NAME, default_value="")
        if value is not None:
            return value
        return ""

    @widgetName.setter
    def widgetName(self, value: str) -> None:
        self._set_data(key=_Keys.WIDGET_NAME, value=value, set_default_type=str)


# #[EOF]#######################################################################
