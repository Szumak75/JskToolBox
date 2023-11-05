# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 05.09.2023

  Purpose: various classes of interaction with the system.
"""

import os
import sys
import getopt

from inspect import currentframe
from pathlib import Path
from typing import Optional, Union, List, Tuple, Dict

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData


class Keys(NoDynamicAttributes):
    """Keys definition class.

    For internal purpose only.
    """

    @staticmethod
    @property
    def ARGS() -> str:
        """Return ARGS Key."""
        return "__args__"

    @staticmethod
    @property
    def CONFIGURED_ARGS() -> str:
        """Return CONFIGURED_ARGS Key."""
        return "__cargs__"

    @staticmethod
    @property
    def DESC_OPTS() -> str:
        """Return DESC_OPTS Key."""
        return "__desc_opts__"

    @staticmethod
    @property
    def SHORT_OPTS() -> str:
        """Return SHORT_OPTS Key."""
        return "__short_opts__"

    @staticmethod
    @property
    def LONG_OPTS() -> str:
        """Return LONG_OPTS Key."""
        return "__long_opts__"


class CommandLineParser(BData, NoDynamicAttributes):
    """Parser for command line options."""

    def __init__(self) -> None:
        """Constructor."""
        self._data[Keys.CONFIGURED_ARGS] = {}
        self._data[Keys.ARGS] = {}

    def configure_argument(
        self,
        short_arg: str,
        long_arg: str,
        desc_arg: Union[str, List, Tuple],
        has_value: bool = False,
    ) -> None:
        """Application command line argument configuration method and its description."""
        if Keys.SHORT_OPTS not in self._data[Keys.CONFIGURED_ARGS]:
            self._data[Keys.CONFIGURED_ARGS][Keys.SHORT_OPTS] = ""
        if Keys.LONG_OPTS not in self._data[Keys.CONFIGURED_ARGS]:
            self._data[Keys.CONFIGURED_ARGS][Keys.LONG_OPTS] = []
        if Keys.DESC_OPTS not in self._data[Keys.CONFIGURED_ARGS]:
            self._data[Keys.CONFIGURED_ARGS][Keys.DESC_OPTS] = []

        self._data[Keys.CONFIGURED_ARGS][Keys.SHORT_OPTS] += short_arg + (
            ":" if has_value else ""
        )
        self._data[Keys.CONFIGURED_ARGS][Keys.LONG_OPTS].append(
            long_arg + ("=" if has_value else "")
        )
        if desc_arg:
            if isinstance(desc_arg, str):
                self._data[Keys.CONFIGURED_ARGS][Keys.DESC_OPTS].append(
                    desc_arg
                )
            elif isinstance(desc_arg, (Tuple, List)):
                for desc in desc_arg:
                    self._data[Keys.CONFIGURED_ARGS][Keys.DESC_OPTS].append(
                        desc
                    )

    def parse_arguments(self) -> None:
        """Command line arguments parser."""
        try:
            opts, _ = getopt.getopt(
                sys.argv[1:],
                self._data[Keys.CONFIGURED_ARGS][Keys.SHORT_OPTS],
                self._data[Keys.CONFIGURED_ARGS][Keys.LONG_OPTS],
            )
        except getopt.GetoptError as ex:
            print(f"Command line argument error: {ex}")
            sys.exit(2)

        for opt, value in opts:
            for short_arg, long_arg in zip(
                self._data[Keys.CONFIGURED_ARGS][Keys.SHORT_OPTS],
                self._data[Keys.CONFIGURED_ARGS][Keys.LONG_OPTS],
            ):
                if opt in ("-" + short_arg, "--" + long_arg):
                    self.args[long_arg] = value

    def get_option(self, option: str) -> Optional[str]:
        """Get value of the option or None if it doesn't exist."""
        return self.args.get(option)

    @property
    def args(self) -> Dict:
        """Return parsed arguments dict."""
        return self._data[Keys.ARGS]


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

    def __init__(self, pathname: str, check_deep: bool = True) -> None:
        """Constructor."""
        if pathname is None:
            raise Raise.error(
                "pathname as string expected, not None.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        if not isinstance(pathname, str):
            raise Raise.error(
                f"pathname as string expected, '{type(pathname)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        if isinstance(pathname, str) and len(pathname) == 0:
            raise Raise.error(
                "pathname cannot be an empty string.",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data["pathname"] = pathname
        self._data["split"] = check_deep
        self._data["list"]: List = []
        # analysis
        self.__run__()

    def __run__(self) -> None:
        """Path analysis procedure."""
        query = Path(self._data["pathname"])
        # check exists
        self._data["exists"] = query.exists()
        if self._data["exists"]:
            # check isfile
            self._data["isfile"] = query.is_file()
            # check isdir
            self._data["isdir"] = query.is_dir()
            # check issymlink
            self._data["issymlink"] = query.is_symlink()
            # resolve symlink
            self._data["posixpath"] = str(query.resolve())

        if self._data["split"]:
            # split and analyse
            tmp = ""
            for item in self.path.split(os.sep):
                if item == "":
                    continue
                tmp += f"{os.sep}{item}"
                self._data["list"].append(PathChecker(tmp, False))

    def __str__(self) -> str:
        """Return class data as string."""
        return (
            "PathChecker("
            f"'pathname': '{self.path}', "
            f"'exists': '{self.exists}', "
            f"'is_dir': '{self.is_dir if self.exists else ''}', "
            f"'is_file': '{self.is_file if self.exists else ''}', "
            f"'is_symlink': '{self.is_symlink if self.exists else ''}', "
            f"'posixpath': '{self.posixpath if self.exists else ''}'"
            ")"
        )

    def __repr__(self) -> str:
        """Return string representation."""
        return f"PathChecker('{self.path}')"

    @property
    def dirname(self) -> Optional[str]:
        """Return dirname from path."""
        if self.exists:
            last = None
            for item in self._data["list"]:
                if item.is_dir:
                    last = item.path
            return last
        return None

    @property
    def filename(self) -> Optional[str]:
        """Return filename from path."""
        if self.exists and self.is_file:
            tmp = self.path.split(os.sep)
            if len(tmp) > 0:
                if tmp[-1] != "":
                    return tmp[-1]
        return None

    @property
    def exists(self) -> bool:
        """Return path exists flag."""
        if "exists" in self._data:
            return self._data["exists"]
        else:
            raise Raise.error(
                "Unexpected exception",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def is_dir(self) -> bool:
        """Return path isdir flag."""
        if "isdir" in self._data:
            return self._data["isdir"]
        else:
            raise Raise.error(
                "Unexpected exception",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def is_file(self) -> bool:
        """Return path isfile flag."""
        if "isfile" in self._data:
            return self._data["isfile"]
        else:
            raise Raise.error(
                "Unexpected exception",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def is_symlink(self) -> bool:
        """Return path issymlink flag."""
        if "issymlink" in self._data:
            return self._data["issymlink"]
        else:
            raise Raise.error(
                "Unexpected exception",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def path(self) -> str:
        """Return path string."""
        return self._data["pathname"]

    @property
    def posixpath(self) -> Optional[str]:
        """Return path string."""
        if self.exists:
            return self._data["posixpath"]
        return None

    def create(self) -> bool:
        """Create path procedure."""
        test_path = self.path
        file = True
        if self.path[-1] == os.sep:
            file = False
            test_path = self.path[:-1]
        for item in self._data["list"]:
            if item.exists:
                continue
            if item.path == test_path:
                # last element
                if file:
                    # touch file
                    with open(item.path, "w") as fp:
                        pass
                else:
                    os.mkdir(item.path)
            else:
                os.mkdir(item.path)
        # check
        self._data["list"] = []
        self.__run__()

        return self.exists


# #[EOF]#######################################################################
