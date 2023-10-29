# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: Main class for creating and processes config files.
"""

import os
import sys
from typing import List, Dict, Tuple, Optional, Union, Any
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.configtool.libs.file import FileProcessor
from jsktoolbox.configtool.libs.data import DataProcessor


class Config(BData, NoDynamicAttributes):
    """Config main class."""

    def __init__(self, filename: str, main_section_name: str) -> None:
        """Constructor."""
        self.data["fp"] = FileProcessor()
        self.data["dp"] = DataProcessor()
        self.__fp.file = filename
        self.__dp.main_section = main_section_name

    @property
    def __fp(self) -> FileProcessor:
        """Return FileProcessor object."""
        return self.data["fp"]

    @property
    def __dp(self) -> DataProcessor:
        """Return DataProcessor object."""
        return self.data["dp"]


# #[EOF]#######################################################################
