# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide lightweight base mixins shared by Tk widgets in the toolkit.
"""

from ..attribtool import NoDynamicAttributes


class TkBase(NoDynamicAttributes):
    """Base class for classes derived from Tk."""

    _name = None
    _tkloaded = None
    _w = None
    _windowingsystem_cached = None
    child = None
    children = None
    master = None
    tk = None
    widgetName = None


# #[EOF]#######################################################################
