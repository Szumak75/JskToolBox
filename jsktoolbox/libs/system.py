# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 05.09.2023

  Purpose: various classes of interaction with the system.
"""
import os
from jsktoolbox.attribtool import NoDynamicAttributes


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


# #[EOF]#######################################################################
