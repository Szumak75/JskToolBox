# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: DataProcessor class for processing dataset operations.
"""

from inspect import currentframe
from typing import Dict, List, Tuple, Optional, Union, Any
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData


class DataProcessor(BData, NoDynamicAttributes):
    """DataProcessor class."""

    def __init__(self) -> None:
        """Constructor."""
        self.data["data"] = {}
        self.data["desckey"] = "__description__"

    @property
    def main_section(self) -> Optional[str]:
        """Return main section name."""
        if "main" not in self.data:
            self.data["main"] = None
        return self.data["main"]

    @main_section.setter
    def main_section(self, name: str) -> None:
        """Set main section name."""
        if not isinstance(name, str):
            name = str(name)
        self.data["main"] = name
        self.add_section(name)

    @property
    def sections(self) -> Tuple:
        """Return sections keys tuple."""
        return tuple(sorted(self.data["data"]))

    def add_section(self, name: str) -> None:
        """Add section key to dataset."""
        if not isinstance(name, str):
            name = str(name)
        if name not in self.data["data"]:
            self.data["data"][name] = []

    def set(
        self, section: str, key: str = None, value: Any = None, desc: str = None
    ) -> None:
        """Set data to [section]->[key]."""
        if section in self.sections:
            if key is not None:
                test = False
                for item in self.data["data"][section]:
                    if key in item:
                        item[key] = value if value is not None else ""
                        if desc is not None:
                            item[self.data["desckey"]] = desc
                        test = True
                        break
                if not test:
                    self.data["data"][section].append(
                        {
                            key: value,
                            self.data["desckey"]: desc,
                        }
                    )
            elif desc is not None:
                self.data["data"][section].append({self.data["desckey"]: desc})
        else:
            raise Raise.error(
                f"Given section name: '{section}' not found.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    def get(self, section: str, key: str = None, desc: bool = False) -> Optional[Any]:
        """Return value."""
        if section in self.sections:
            if key is not None:
                if desc:
                    # Return description for key
                    for item in self.data["data"][section]:
                        if key in item:
                            return item[self.data["desckey"]]
                else:
                    # Return value for key
                    for item in self.data["data"][section]:
                        if key in item:
                            return item[key]
            else:
                # Return list of description for section
                out = []
                for item in self.data["data"][section]:
                    if len(item.keys()) == 1 and self.data["desckey"] in item:
                        out.append(item[self.data["desckey"]])
                if out:
                    return out
            return None
        else:
            raise Raise.error(
                f"Given section name: '{section}' not found.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    def __dump(self, section: str) -> str:
        """Return formatted configuration data for section name."""
        out = ""
        if section in self.data["data"]:
            out += f"[{section}]\n"
            for item in self.data["data"][section]:
                if len(item.keys()) == 1:
                    if (
                        self.data["desckey"] in item
                        and item[self.data["desckey"]] is not None
                    ):
                        out += f"# {item[self.data['desckey']]}\n"
                    else:
                        out += "#\n"
                else:
                    desc = None
                    keys = []
                    for key in item.keys():
                        if key == self.data["desckey"]:
                            desc = item[key]
                        else:
                            keys.append(key)
                    for key in keys:
                        out += f"{key}={item[key]}"
                    if desc:
                        out += f" # {desc}"
                    out += "\n"
            out += "\n"
        else:
            raise Raise.error(
                f"Section name: '{section}' not found.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )
        return out

    @property
    def dump(self) -> str:
        """Return formated configuration data string."""
        out = ""

        # first section is a main section
        if self.main_section is None:
            raise Raise.error(
                "Main section is not set.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )
        out = self.__dump(self.main_section)

        # other sections
        for section in tuple(set(self.sections) ^ set([self.main_section])):
            out += self.__dump(section)

        return out


# #[EOF]#######################################################################
