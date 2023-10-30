# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: DataProcessor class for processing dataset operations.
"""

from inspect import currentframe
from typing import Dict, List, Tuple, Optional, Union, Any
from abc import ABC, abstractmethod
from copy import copy
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData


class IModel(ABC):
    """Model class interface."""

    @property
    @abstractmethod
    def dump(self) -> List[str]:
        """Dump data."""

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """Get name property."""

    @name.setter
    @abstractmethod
    def name(self, name: str) -> None:
        """Set name property."""

    @abstractmethod
    def parser(self, value: str) -> None:
        """Parser method."""

    @abstractmethod
    def search(self, name: str) -> bool:
        """Search method."""


class SectionModel(BData, IModel, NoDynamicAttributes):
    """SectionModel class."""

    def __init__(self, name: Optional[str] = None) -> None:
        """Constructor."""
        self._data["name"] = None
        self._data["variables"]: List[VariableModel] = []
        self.parser(name)

    def __repr__(self) -> str:
        """Return representation class string."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        """Return formated string."""
        return f"[{self.name}]"

    @property
    def dump(self) -> List[Any]:
        """Dump data."""
        tmp = []
        tmp.append(self)
        for item in self._data["variables"]:
            tmp.append(item)
        return copy(tmp)

    def parser(self, value: str) -> None:
        """Parser method."""
        if value is None:
            return
        tmp = f"{value}".strip("[] \n")
        if tmp:
            self._data["name"] = tmp
        else:
            raise Raise.error(
                f"String name expected, '{tmp}' received.",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )

    def search(self, name: str) -> bool:
        """Search method."""
        return self.name == name

    @property
    def name(self) -> Optional[str]:
        """Get name property."""
        return self._data["name"]

    @name.setter
    def name(self, name: str) -> None:
        """Set name property."""
        self.parser(name)


class VariableModel(BData, IModel, NoDynamicAttributes):
    """VariableModel class."""

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[Union[str, int, float, List]] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Constructor."""
        self._data["name"] = name
        self._data["value"] = value
        self._data["desc"] = desc

    def __repr__(self) -> str:
        """Return representation class string."""
        tmp = ""
        tmp += f"name='{self.name}', " if self.name else ""
        if isinstance(self.value, (int, float)):
            tmp += f"value={self.value}, " if self.value else ""
        elif isinstance(self.value, (List, Tuple)):
            tmp += f"value=[{self.value}], " if self.value else ""
        else:
            tmp += f"value='{self.value}', " if self.value else ""
        tmp += f"desc='{self.desc}'" if self.desc else ""
        return f"{self.__class__.__name__}({tmp})"

    def __str__(self) -> str:
        """Return formated string."""
        tmp = ""
        tmp += f"{self.name} = " if self.name else ""
        if isinstance(self.value, (int, float)):
            tmp += f"{self.value}" if self.value else ""
        elif isinstance(self.value, (List, Tuple)):
            tmp += f"[{self.value}]" if self.value else ""
        else:
            tmp += f'"{self.value}"' if self.value else ""
        if tmp:
            tmp += f" # {self.desc}" if self.desc else ""
        else:
            tmp += f"# {self.desc}" if self.desc else "#"
        return tmp

    @property
    def desc(self) -> Optional[str]:
        """Get descrption property."""
        return self._data["desc"]

    @desc.setter
    def desc(self, desc: Optional[str]) -> None:
        """Set description property."""

    @property
    def dump(self) -> List[Any]:
        """Dump data."""

    @property
    def name(self) -> Optional[str]:
        """Get name property."""
        return self._data["name"]

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Set name property."""

    def parser(self, value: str) -> None:
        """Parser method."""

    def search(self, name: str) -> bool:
        """Search method."""

    @property
    def value(self) -> Optional[Union[str, int, float, List]]:
        """Get value property."""
        return self._data["value"]

    @value.setter
    def value(self, value: Optional[Union[str, int, float, List]]) -> None:
        """Set value property."""


class DataProcessor(BData, NoDynamicAttributes):
    """DataProcessor class."""

    def __init__(self) -> None:
        """Constructor."""
        self._data["data"] = {}
        self._data["desckey"] = "__description__"

    @property
    def main_section(self) -> Optional[str]:
        """Return main section name."""
        if "main" not in self._data:
            self._data["main"] = None
        return self._data["main"]

    @main_section.setter
    def main_section(self, name: str) -> None:
        """Set main section name."""
        if not isinstance(name, str):
            name = str(name)
        self._data["main"] = name
        self.add_section(name)

    @property
    def sections(self) -> Tuple:
        """Return sections keys tuple."""
        return tuple(sorted(self._data["data"]))

    def add_section(self, name: str) -> None:
        """Add section key to dataset."""
        if not isinstance(name, str):
            name = str(name)
        if name not in self._data["data"]:
            self._data["data"][name] = []

    def set(
        self,
        section: str,
        key: str = None,
        value: Any = None,
        desc: str = None,
    ) -> None:
        """Set data to [section]->[key]."""
        if section in self.sections:
            if key is not None:
                test = False
                for item in self._data["data"][section]:
                    if key in item:
                        item[key] = value if value is not None else ""
                        if desc is not None:
                            item[self._data["desckey"]] = desc
                        test = True
                        break
                if not test:
                    self._data["data"][section].append(
                        {
                            key: value,
                            self._data["desckey"]: desc,
                        }
                    )
            elif desc is not None:
                self._data["data"][section].append(
                    {self._data["desckey"]: desc}
                )
        else:
            raise Raise.error(
                f"Given section name: '{section}' not found.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    def get(
        self, section: str, key: str = None, desc: bool = False
    ) -> Optional[Any]:
        """Return value."""
        if section in self.sections:
            if key is not None:
                if desc:
                    # Return description for key
                    for item in self._data["data"][section]:
                        if key in item:
                            return item[self._data["desckey"]]
                else:
                    # Return value for key
                    for item in self._data["data"][section]:
                        if key in item:
                            return item[key]
            else:
                # Return list of description for section
                out = []
                for item in self._data["data"][section]:
                    if (
                        len(item.keys()) == 1
                        and self._data["desckey"] in item
                    ):
                        out.append(item[self._data["desckey"]])
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
        if section in self._data["data"]:
            out += f"[{section}]\n"
            for item in self._data["data"][section]:
                if len(item.keys()) == 1:
                    if (
                        self._data["desckey"] in item
                        and item[self._data["desckey"]] is not None
                    ):
                        out += f"# {item[self._data['desckey']]}\n"
                    else:
                        out += "#\n"
                else:
                    desc = None
                    keys = []
                    for key in item.keys():
                        if key == self._data["desckey"]:
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
