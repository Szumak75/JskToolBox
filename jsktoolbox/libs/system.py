# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 05.09.2023

  Purpose: various classes of interaction with the system.
"""

import os
import inspect
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData


class Env(NoDynamicAttributes):
    """Environment class."""

    @classmethod
    @property
    def home(cls) -> str:
        """Return home dir name."""
        return os.getenv("HOME")

    @classmethod
    @property
    def username(cls) -> str:
        """Return login name."""
        return os.getenv("USER")


class PathChecker(BData, NoDynamicAttributes):
    """PathChecker class for filesystem path."""

    def __init__(self, pathname: str) -> None:
        """Constructor."""
        if pathname is None:
            raise Raise.error(
                "pathname as string expected, not None.",
                TypeError,
                self.__class__.__name__,
                inspect.currentframe(),
            )
        if not isinstance(pathname, str):
            raise Raise.error(
                f"pathname as string expected, '{type(pathname)}' received.",
                TypeError,
                self.__class__.__name__,
                inspect.currentframe(),
            )
        if isinstance(pathname, str) and len(pathname) == 0:
            raise Raise.error(
                "pathname cannot be an empty string.",
                ValueError,
                self.__class__.__name__,
                inspect.currentframe(),
            )
        self.data["pathname"] = pathname
        # analysis
        self.__run__()

    def __run__(self) -> None:
        """Path analysis procedure."""

    @property
    def exists(self) -> bool:
        """Return path exists flag."""

    @property
    def isdir(self) -> bool:
        """Return path isdir flag."""

    @property
    def isfile(self) -> bool:
        """Return path isfile flag."""

    def create(self) -> bool:
        """Create path procedure."""
        return False


# #[EOF]#######################################################################
