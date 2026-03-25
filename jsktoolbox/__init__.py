# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 19.09.2023

Purpose: JskToolBox - Comprehensive Python 3 library for building robust applications.

A collection of utility modules providing base classes, configuration management,
networking tools, logging infrastructure, and device-specific integrations.
"""

from typing import Tuple

__author__ = "Jacek 'Szumak' Kotlarski"
__version_info__: Tuple[int, int, int] = (1, 2, 3)  # Major, Minor, Patch
__suffix__: str = ""  # Optional suffix for pre-release versions
__version__: str = ".".join(map(str, __version_info__)) + __suffix__
