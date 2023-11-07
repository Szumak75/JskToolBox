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

from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ARGS = "__args__"
    CONFIGURED_ARGS = "__cargs__"
    DESC_OPTS = "__desc_opts__"
    SHORT_OPTS = "__short_opts__"
    LONG_OPTS = "__long_opts__"
    PATHNAME = "__pathname__"
    SPLIT = "__split__"
    LIST = "__list__"
    EXISTS = "__exists__"
    ISFILE = "__is_file__"
    ISDIR = "__is_dir__"
    ISSYMLINK = "__is_symlink__"
    POSIXPATH = "__posix_path__"


class CommandLineParser(BData, NoDynamicAttributes):
    """Parser for command line options."""

    def __init__(self) -> None:
        """Constructor."""
        self._data[_Keys.CONFIGURED_ARGS] = {}
        self._data[_Keys.ARGS] = {}

    def configure_argument(
        self,
        short_arg: str,
        long_arg: str,
        desc_arg: Optional[Union[str, List, Tuple]] = None,
        has_value: bool = False,
    ) -> None:
        """Application command line argument configuration method and its description."""
        if _Keys.SHORT_OPTS not in self._data[_Keys.CONFIGURED_ARGS]:
            self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS] = ""
        if _Keys.LONG_OPTS not in self._data[_Keys.CONFIGURED_ARGS]:
            self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS] = []
        if _Keys.DESC_OPTS not in self._data[_Keys.CONFIGURED_ARGS]:
            self._data[_Keys.CONFIGURED_ARGS][_Keys.DESC_OPTS] = []

        self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS] += short_arg + (
            ":" if has_value else ""
        )
        self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS].append(
            long_arg + ("=" if has_value else "")
        )
        if desc_arg:
            if isinstance(desc_arg, str):
                self._data[_Keys.CONFIGURED_ARGS][_Keys.DESC_OPTS].append(
                    desc_arg
                )
            elif isinstance(desc_arg, (Tuple, List)):
                tmp = []
                for desc in desc_arg:
                    tmp.append(desc)
                if not tmp:
                    tmp = ""
                self._data[_Keys.CONFIGURED_ARGS][_Keys.DESC_OPTS].append(
                    tmp
                )
            else:
                self._data[_Keys.CONFIGURED_ARGS][_Keys.DESC_OPTS].append(
                    str(desc_arg)
                )

        else:
            self._data[_Keys.CONFIGURED_ARGS][_Keys.DESC_OPTS].append("")

    def parse_arguments(self) -> None:
        """Command line arguments parser."""
        try:
            opts, _ = getopt.getopt(
                sys.argv[1:],
                self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS],
                self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS],
            )
        except getopt.GetoptError as ex:
            print(f"Command line argument error: {ex}")
            sys.exit(2)

        for opt, value in opts:
            for short_arg, long_arg in zip(
                self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS],
                self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS],
            ):
                if opt in ("-" + short_arg, "--" + long_arg):
                    self.args[long_arg] = value

    def get_option(self, option: str) -> Optional[str]:
        """Get value of the option or None if it doesn't exist."""
        return self.args.get(option)

    @property
    def args(self) -> Dict:
        """Return parsed arguments dict."""
        return self._data[_Keys.ARGS]


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
        self._data[_Keys.PATHNAME] = pathname
        self._data[_Keys.SPLIT] = check_deep
        self._data[_Keys.LIST]: List = []
        # analysis
        self.__run__()

    def __run__(self) -> None:
        """Path analysis procedure."""
        query = Path(self._data[_Keys.PATHNAME])
        # check exists
        self._data[_Keys.EXISTS] = query.exists()
        if self._data[_Keys.EXISTS]:
            # check isfile
            self._data[_Keys.ISFILE] = query.is_file()
            # check isdir
            self._data[_Keys.ISDIR] = query.is_dir()
            # check issymlink
            self._data[_Keys.ISSYMLINK] = query.is_symlink()
            # resolve symlink
            self._data[_Keys.POSIXPATH] = str(query.resolve())

        if self._data[_Keys.SPLIT]:
            # split and analyse
            tmp = ""
            for item in self.path.split(os.sep):
                if item == "":
                    continue
                tmp += f"{os.sep}{item}"
                self._data[_Keys.LIST].append(PathChecker(tmp, False))

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
            for item in self._data[_Keys.LIST]:
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
        if _Keys.EXISTS in self._data:
            return self._data[_Keys.EXISTS]
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
        if _Keys.ISDIR in self._data:
            return self._data[_Keys.ISDIR]
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
        if _Keys.ISFILE in self._data:
            return self._data[_Keys.ISFILE]
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
        if _Keys.ISSYMLINK in self._data:
            return self._data[_Keys.ISSYMLINK]
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
        return self._data[_Keys.PATHNAME]

    @property
    def posixpath(self) -> Optional[str]:
        """Return path string."""
        if self.exists:
            return self._data[_Keys.POSIXPATH]
        return None

    def create(self) -> bool:
        """Create path procedure."""
        test_path = self.path
        file = True
        if self.path[-1] == os.sep:
            file = False
            test_path = self.path[:-1]
        for item in self._data[_Keys.LIST]:
            if item.exists:
                continue
            if item.path == test_path:
                # last element
                if file:
                    # touch file
                    with open(item.path, "w"):
                        pass
                else:
                    os.mkdir(item.path)
            else:
                os.mkdir(item.path)
        # check
        self._data[_Keys.LIST] = []
        self.__run__()

        return self.exists


# #[EOF]#######################################################################
