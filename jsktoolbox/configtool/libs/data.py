# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: DataProcessor class for processing dataset operations.
"""

from inspect import currentframe
from typing import Dict, List, Tuple, Optional, Union, Any, TypeVar
from abc import ABC, abstractmethod
from copy import copy
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData

TVariableModel = TypeVar("TVariableModel", bound="VariableModel")


class Keys(NoDynamicAttributes):
    """Keys definition class.

    For internal purpose only.
    """

    @classmethod
    @property
    def data(self) -> str:
        """Return data key."""
        return "data"

    @classmethod
    @property
    def desc(self) -> str:
        """Return desc key."""
        return "desc"

    @classmethod
    @property
    def description(self) -> str:
        """Return description key."""
        return "__description__"

    @classmethod
    @property
    def main(self) -> str:
        """Return main key."""
        return "main"

    @classmethod
    @property
    def name(self) -> str:
        """Return name key."""
        return "name"

    @classmethod
    @property
    def value(self) -> str:
        """Return value key."""
        return "value"

    @classmethod
    @property
    def variables(self) -> str:
        """Return variables key."""
        return "variables"


class IModel(ABC):
    """Model class interface."""

    @property
    @abstractmethod
    def dump(self) -> Union[List[str], TVariableModel]:
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
        self._data[Keys.name] = None
        self._data[Keys.variables]: List[VariableModel] = []
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
        for item in self._data[Keys.variables]:
            tmp.append(item.dump())
        return copy(tmp)

    def parser(self, value: str) -> None:
        """Parser method."""
        if value is None:
            return
        tmp = f"{value}".strip("[] \n")
        if tmp:
            self._data[Keys.name] = tmp
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
        return self._data[Keys.name]

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
        self._data[Keys.name] = name
        self._data[Keys.value] = value
        self._data[Keys.desc] = desc

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
        return self._data[Keys.desc]

    @desc.setter
    def desc(self, desc: Optional[str]) -> None:
        """Set description property."""
        self._data[Keys.desc] = desc

    @property
    def dump(self) -> TVariableModel:
        """Dump data."""
        return self

    @property
    def name(self) -> Optional[str]:
        """Get name property."""
        return self._data[Keys.name]

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Set name property."""
        self._data[Keys.name] = name.strip()

    def parser(self, value: str) -> None:
        """Parser method."""

    def search(self, name: str) -> bool:
        """Search method."""
        return self.name == name

    @property
    def value(self) -> Optional[Union[str, int, float, List]]:
        """Get value property."""
        return self._data[Keys.value]

    @value.setter
    def value(self, value: Optional[Union[str, int, float, List]]) -> None:
        """Set value property."""
        self._data[Keys.value] = value


class DataProcessor(BData, NoDynamicAttributes):
    """DataProcessor class."""

    def __init__(self) -> None:
        """Constructor."""
        self._data[Keys.data] = {}

    @property
    def main_section(self) -> Optional[str]:
        """Return main section name."""
        if Keys.main not in self._data:
            self._data[Keys.main] = None
        return self._data[Keys.main]

    @main_section.setter
    def main_section(self, name: str) -> None:
        """Set main section name."""
        if not isinstance(name, str):
            name = str(name)
        self._data[Keys.main] = name
        self.add_section(name)

    @property
    def sections(self) -> Tuple:
        """Return sections keys tuple."""
        return tuple(sorted(self._data[Keys.data]))

    def add_section(self, name: str) -> None:
        """Add section key to dataset."""
        if not isinstance(name, str):
            name = str(name)
        if name not in self._data[Keys.data]:
            self._data[Keys.data][name] = []

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
                for item in self._data[Keys.data][section]:
                    if key in item:
                        item[key] = value if value is not None else ""
                        if desc is not None:
                            item[Keys.description] = desc
                        test = True
                        break
                if not test:
                    self._data[Keys.data][section].append(
                        {
                            key: value,
                            Keys.description: desc,
                        }
                    )
            elif desc is not None:
                self._data[Keys.data][section].append(
                    {Keys.description: desc}
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
                    for item in self._data[Keys.data][section]:
                        if key in item:
                            return item[Keys.description]
                else:
                    # Return value for key
                    for item in self._data[Keys.data][section]:
                        if key in item:
                            return item[key]
            else:
                # Return list of description for section
                out = []
                for item in self._data[Keys.data][section]:
                    if len(item.keys()) == 1 and Keys.description in item:
                        out.append(item[Keys.description])
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
        if section in self._data[Keys.data]:
            out += f"[{section}]\n"
            for item in self._data[Keys.data][section]:
                if len(item.keys()) == 1:
                    if (
                        Keys.description in item
                        and item[Keys.description] is not None
                    ):
                        out += f"# {item[Keys.description]}\n"
                    else:
                        out += "#\n"
                else:
                    desc = None
                    keys = []
                    for key in item.keys():
                        if key == Keys.description:
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
