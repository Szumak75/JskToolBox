# -*- coding: utf-8 -*-
"""
  system.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 7.10.2024, 14:25:00
  
  Purpose: EDMC plugins system classes.
"""

import os

from jsktoolbox.edmctool.logs import Directory
from jsktoolbox.systemtool import Env


class EnvLocal(Env):
    """Environmental class."""

    def __init__(self) -> None:
        """Initialize Env class."""
        super().__init__()

    def check_dir(self, directory: str) -> str:
        """Check if dir exists, return dir or else HOME."""
        if not Directory().is_directory(directory):
            return self.home
        return directory

    @property
    def plugin_dir(self) -> str:
        """Return plugin dir path."""
        return f"{os.path.dirname(os.path.dirname(__file__))}"


# #[EOF]#######################################################################
