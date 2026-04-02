# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 29.10.2023

Purpose: Main class for creating and processes config files.
"""

import re
from inspect import currentframe
from typing import List, Dict, Optional, Any, Pattern

from ..attribtool import NoDynamicAttributes, ReadOnlyClass
from ..raisetool import Raise
from ..basetool import BData
from .libs.file import FileProcessor
from .libs.data import DataProcessor
from .libs.data import SectionModel


class Config(BData, NoDynamicAttributes):
    """High-level configuration manager combining data and file processors.

    ### Purpose:
    Loads, modifies, and saves INI-like configuration files.
    """

    class __Keys(object, metaclass=ReadOnlyClass):
        """Private key registry for Config storage."""

        DESC: str = "__desc__"
        DP: str = "__data_processor__"
        FP: str = "__file_processor__"
        RE_BOOL: str = "__re_bool__"
        RE_DESC: str = "__re_description__"
        RE_FALSE: str = "__re_false__"
        RE_FLOAT: str = "__re_float__"
        RE_INT: str = "__re_integer__"
        RE_LIST: str = "__re_list__"
        RE_SECTION: str = "__re_section__"
        RE_TRUE: str = "__re_true__"
        RE_VAR: str = "__re_variable__"
        VALUE: str = "__value__"
        VARNAME: str = "__varname__"

    def __init__(
        self,
        filename: str,
        main_section_name: str,
        auto_create: bool = False,
    ) -> None:
        """Initialise Config object.

        ### Arguments:
        * filename: str - Path to configuration file.
        * main_section_name: str - Name of the primary section.
        * auto_create: bool - Create file on demand when True.
        """
        self._set_data(
            key=self.__Keys.FP, value=FileProcessor(), set_default_type=FileProcessor
        )
        self._set_data(
            key=self.__Keys.DP, value=DataProcessor(), set_default_type=DataProcessor
        )
        self._set_data(
            key=self.__Keys.RE_SECTION,
            value=re.compile(r"\s{0,}\[.*\]\s{0,}"),
            set_default_type=re.Pattern,
        )
        self._set_data(
            key=self.__Keys.RE_DESC,
            value=re.compile(r"\s{0,}#"),
            set_default_type=re.Pattern,
        )
        self._set_data(
            key=self.__Keys.RE_VAR,
            value=re.compile(r"\s{0,}\S{1,}\s{0,}="),
            set_default_type=re.Pattern,
        )
        self._set_data(
            key=self.__Keys.RE_INT,
            value=re.compile(r"^\d{1,}$"),
            set_default_type=re.Pattern,
        )
        self._set_data(
            key=self.__Keys.RE_FLOAT,
            value=re.compile(r"^\d{1,}\.\d{1,}$"),
            set_default_type=re.Pattern,
        )
        self._set_data(
            key=self.__Keys.RE_BOOL,
            value=re.compile(r"^true|false|yes|no$", re.IGNORECASE),
            set_default_type=re.Pattern,
        )
        self._set_data(
            key=self.__Keys.RE_TRUE,
            value=re.compile(r"^true|yes$", re.IGNORECASE),
            set_default_type=re.Pattern,
        )
        self._set_data(
            key=self.__Keys.RE_FALSE,
            value=re.compile(r"^false|no$", re.IGNORECASE),
            set_default_type=re.Pattern,
        )
        self._set_data(
            key=self.__Keys.RE_LIST,
            value=re.compile(r"^\[.*\]$"),
            set_default_type=re.Pattern,
        )
        self.__fp.file = filename
        self.__dp.main_section = main_section_name
        if auto_create:
            if not self.__fp.file_exists:
                self.__fp.file_create()

    @property
    def __fp(self) -> FileProcessor:
        """Return FileProcessor object.

        ### Returns:
        [FileProcessor] - Underlying file helper.
        """
        obj: Optional[FileProcessor] = self._get_data(key=self.__Keys.FP)
        if obj is None:
            raise Raise.error(
                f"{self._c_name}.__fp not set.",
                AttributeError,
                self._c_name,
                currentframe(),
            )
        return obj

    @property
    def __dp(self) -> DataProcessor:
        """Return DataProcessor object.

        ### Returns:
        [DataProcessor] - Underlying data helper.
        """
        obj: Optional[DataProcessor] = self._get_data(key=self.__Keys.DP)  
        if obj is None:
            raise Raise.error(
                f"{self._c_name}.__dp not set.",
                AttributeError,
                self._c_name,
                currentframe(),
            )
        return obj  

    def __rx(self, key: str) -> Pattern[str]:
        """Return compiled regex stored in typed BData storage."""
        return self._get_data(key=key)  # type: ignore[return-value]

    @property
    def file_exists(self) -> bool:
        """Check if file exists.

        ### Returns:
        [bool] - True when configuration file exists.
        """
        return self.__fp.file_exists

    def __value_parser(self, item: str) -> Any:
        """Return proper type of value.

        ### Arguments:
        * item: str - Raw string token.

        ### Returns:
        [Any] - Parsed value converted to bool/int/float/list/str.
        """
        if self.__rx(self.__Keys.RE_BOOL).match(item):
            return True if self.__rx(self.__Keys.RE_TRUE).match(item) else False
        elif self.__rx(self.__Keys.RE_INT).match(item):
            return int(item)
        elif self.__rx(self.__Keys.RE_FLOAT).match(item):
            return float(item)
        elif self.__rx(self.__Keys.RE_LIST).match(item):
            out = []
            tmp: list[str] = [x.strip() for x in item.strip("[]").split(",")]
            for item in tmp:
                out.append(self.__value_parser(item))
            return out
        return str(item.strip("\"'"))

    def __var_parser(self, line: str) -> Dict:
        """Return dictionary describing a parsed variable line.

        ### Arguments:
        * line: str - Raw config line containing `key = value`.

        ### Returns:
        [Dict[str, Any]] - Mapping with varname, value, and description.

        ### Raises:
        * ValueError: Unexpected line format.
        """
        out: dict[str, Any] = {
            self.__Keys.VARNAME: None,
            self.__Keys.VALUE: None,
            self.__Keys.DESC: None,
        }
        tmp: list[str] = line.split("=", 1)
        if len(tmp) != 2:
            raise Raise.error(
                f"Unexpected config line format: '{line}'",
                ValueError,
                self._c_name,
                currentframe(),
            )
        out[self.__Keys.VARNAME] = tmp[0].strip()
        if not out[self.__Keys.VARNAME]:
            raise Raise.error(
                "Unexpected config line format: missing variable name.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        if len(tmp[1]) > 0:
            tmp = tmp[1].split("#", 1)
            # desc
            if len(tmp) == 2 and len(tmp[1]) > 0:
                out[self.__Keys.DESC] = tmp[1].strip()
            # value
            out[self.__Keys.VALUE] = self.__value_parser(tmp[0].strip())

        return out

    def load(self) -> bool:
        """Load config file to DataProcessor.

        ### Returns:
        [bool] - True when at least one line was processed.
        """
        test = False
        # 1. load file into list
        file: List[str] = self.__fp.readlines()
        section_name: str = ""
        if self.__dp.main_section is not None:
            section_name = self.__dp.main_section
        for line in file:
            # check section
            if self.__rx(self.__Keys.RE_SECTION).match(line):
                section_name = self.__dp.add_section(line)
            # check description
            elif self.__rx(self.__Keys.RE_DESC).match(line):
                self.__dp.set(section_name, desc=line.strip("# "))
            # check var
            elif self.__rx(self.__Keys.RE_VAR).match(line):
                out = self.__var_parser(line)
                self.__dp.set(
                    section=section_name,
                    varname=out[self.__Keys.VARNAME],
                    value=out[self.__Keys.VALUE],
                    desc=out[self.__Keys.DESC],
                )
            else:
                if "=" in line:
                    raise Raise.error(
                        f"Unexpected config line format: '{line}'",
                        ValueError,
                        self._c_name,
                        currentframe(),
                    )
                self.__dp.set(section_name, desc=line)
            test = True
        return test

    def save(self) -> bool:
        """Save config file from DataProcessor.

        ### Returns:
        [bool] - True after successful write.
        """
        test = False
        self.__fp.write(self.__dp.dump)
        test = True
        return test

    def get(
        self, section: str, varname: Optional[str] = None, desc: bool = False
    ) -> Any:
        """Get and return data.

        ### Arguments:
        * section: str - Section name.
        * varname: Optional[str] - Variable name.
        * desc: bool - Whether to fetch description.

        ### Returns:
        [Any] - Value or description depending on `desc`.
        """
        return self.__dp.get(section, varname, desc)

    def set(
        self,
        section: str,
        varname: Optional[str] = None,
        value: Optional[Any] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Set data.

        ### Arguments:
        * section: str - Section name.
        * varname: Optional[str] - Variable name.
        * value: Optional[Any] - Value payload.
        * desc: Optional[str] - Description text.
        """
        self.__dp.set(section, varname, value, desc)

    def has_section(self, section: str) -> bool:
        """Check section name in config file.

        ### Arguments:
        * section: str - Section name to validate.

        ### Returns:
        [bool] - True when section exists.

        ### Raises:
        * TypeError: Section name is not a string.
        """
        if not isinstance(section, str):
            raise Raise.error(
                f"Expected String type, received: '{type(section)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        return self.__dp.get_section(section) is not None

    def has_varname(self, section_name: str, varname: str) -> bool:
        """Check varname in section.

        ### Arguments:
        * section_name: str - Section name.
        * varname: str - Variable name.

        ### Returns:
        [bool] - True when variable exists.

        ### Raises:
        * TypeError: Variable name is not a string.
        """
        if not isinstance(varname, str):
            raise Raise.error(
                f"Expected String type, received: '{type(varname)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if self.has_section(section_name):
            tmp: Optional[SectionModel] = self.__dp.get_section(section_name)
            if tmp is not None:
                found_section: SectionModel = tmp
                return found_section.get_variable(varname) is not None
        return False

    @property
    def main_section_name(self) -> Optional[str]:
        """Return main section name string.

        ### Returns:
        [Optional[str]] - Name of the main section.
        """
        return self.__dp.main_section


# #[EOF]#######################################################################
