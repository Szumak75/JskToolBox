# -*- coding: utf-8 -*-
"""
  systemtool.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 6.09.2024, 19:53:44
  
  Purpose: various classes of interaction with the system.
"""


import os
import sys
import getopt
import tempfile
import subprocess

from inspect import currentframe
from pathlib import Path
from typing import Optional, Union, List, Tuple, Dict, Any

from jsktoolbox.attribtool import NoDynamicAttributes

from .attribtool import NoDynamicAttributes, ReadOnlyClass
from .raisetool import Raise
from .basetool.data import BData


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ARGS: str = "__args__"
    CONFIGURED_ARGS: str = "__conf_args__"
    DESC_OPTS: str = "__desc_opts__"
    EXAMPLE_OPTS: str = "__ex_opts__"
    EXISTS: str = "__exists__"
    HOME: str = "__home__"
    IS_DIR: str = "__is_dir__"
    IS_FILE: str = "__is_file__"
    IS_SYMLINK: str = "__is_symlink__"
    LIST: str = "__list__"
    LONG_OPTS: str = "__long_opts__"
    PATH_NAME: str = "__pathname__"
    POSIXPATH: str = "__posix_path__"
    SHORT_OPTS: str = "__short_opts__"
    SPLIT: str = "__split__"
    TMP: str = "__tmp__"


class CommandLineParser(BData):
    """Parser for command line options."""

    def __init__(self) -> None:
        """Constructor."""
        self._data[_Keys.CONFIGURED_ARGS] = {}
        self._data[_Keys.ARGS] = {}

    def configure_argument(
        self,
        short_arg: Optional[str],
        long_arg: str,
        desc_arg: Optional[Union[str, List, Tuple]] = None,
        has_value: bool = False,
        example_value: Optional[str] = None,
    ) -> None:
        """Application command line argument configuration method and its description.

        ### Arguments:
        * short_arg [Optional[str]] - optional one character string,
        * long_arg [str] - required one word string,
        * desc_arg [Optional[Union[str, List, Tuple]]] - optional argument description,
        * has_value [bool] - flag, if 'True' argument takes a value, default = False,
        * example_value [Optional[str]] - example value for argument description.
        """
        if _Keys.SHORT_OPTS not in self._data[_Keys.CONFIGURED_ARGS]:
            self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS] = ""
        if _Keys.LONG_OPTS not in self._data[_Keys.CONFIGURED_ARGS]:
            self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS] = []
        if _Keys.DESC_OPTS not in self._data[_Keys.CONFIGURED_ARGS]:
            self._data[_Keys.CONFIGURED_ARGS][_Keys.DESC_OPTS] = []
        if _Keys.EXAMPLE_OPTS not in self._data[_Keys.CONFIGURED_ARGS]:
            self._data[_Keys.CONFIGURED_ARGS][_Keys.EXAMPLE_OPTS] = []

        if not short_arg:
            short_arg = "_"

        if not long_arg:
            raise Raise.error(
                f"A long argument name is required.",
                AttributeError,
                self._c_name,
                currentframe(),
            )

        self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS] += short_arg + (
            ":" if has_value else ""
        )
        self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS].append(
            long_arg + ("=" if has_value else "")
        )

        tmp: Union[str, List] = ""
        if desc_arg:
            if isinstance(desc_arg, str):
                tmp = desc_arg
            elif isinstance(desc_arg, (Tuple, List)):
                tmp = []
                for desc in desc_arg:
                    tmp.append(desc)
                if not tmp:
                    tmp = ""
            else:
                tmp = str(desc_arg)
        self._data[_Keys.CONFIGURED_ARGS][_Keys.DESC_OPTS].append(tmp)

        tmp = ""
        if example_value:
            if isinstance(example_value, str):
                tmp = example_value

        self._data[_Keys.CONFIGURED_ARGS][_Keys.EXAMPLE_OPTS].append(tmp)

    def parse_arguments(self) -> bool:
        """Command line arguments parser."""
        # replace ':' if exists in short option string
        short_mod = str(self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS]).replace(
            ":", ""
        )
        long_mod = []
        for item in self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS]:
            long_mod.append(item.replace("=", ""))

        try:
            opts, _ = getopt.getopt(
                sys.argv[1:],
                self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS],
                self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS],
            )
        except getopt.GetoptError as ex:
            print(f"Command line argument error: {ex}")
            return False

        for opt, value in opts:
            for short_arg, long_arg in zip(
                short_mod,
                long_mod,
            ):
                if opt in ("-" + short_arg, "--" + long_arg):
                    self.args[long_arg] = value
        return True

    def get_option(self, option: str) -> Optional[str]:
        """Get value of the option or None if it doesn't exist."""
        out: Optional[Any] = self.args.get(option)
        if out is None:
            return None
        return str(out)

    def dump(self) -> Dict[str, Any]:
        """Dump configured data structure as Dict:
        {'long opt name':{'short':str, 'has_value':bool, 'description':str, 'example':str}}
        """
        out: Dict[str, Any] = {}
        short_mod: str = str(
            self._data[_Keys.CONFIGURED_ARGS][_Keys.SHORT_OPTS]
        ).replace(":", "")

        for short_arg, long_arg, desc_arg, ex_arg in zip(
            short_mod,
            self._data[_Keys.CONFIGURED_ARGS][_Keys.LONG_OPTS],
            self._data[_Keys.CONFIGURED_ARGS][_Keys.DESC_OPTS],
            self._data[_Keys.CONFIGURED_ARGS][_Keys.EXAMPLE_OPTS],
        ):
            out[long_arg] = {
                "short": short_arg if short_arg != "_" else "",
                "has_value": True if long_arg[-1] == "=" else False,
                "description": desc_arg,
                "example": ex_arg,
            }
        return out

    @property
    def args(self) -> Dict[str, Any]:
        """Return parsed arguments dict."""
        return self._data[_Keys.ARGS]


class Env(BData):
    """Environment class."""

    def __init__(self) -> None:
        """Initialize Env class."""
        home: Optional[str] = os.getenv("HOME")
        if home is None:
            home = os.getenv("HOMEPATH")
            if home is not None:
                home = f"{os.getenv('HOMEDRIVE')}{home}"
        self._set_data(key=_Keys.HOME, set_default_type=str, value=home)

        tmp: Optional[str] = os.getenv("TMP")
        if tmp is None:
            tmp = os.getenv("TEMP")
            if tmp is None:
                tmp = tempfile.gettempdir()
        self._set_data(key=_Keys.TMP, set_default_type=str, value=tmp)

    @property
    def home(self) -> str:
        """Returns home dir name."""
        return self._get_data(key=_Keys.HOME, default_value="")  # type: ignore

    @property
    def tmpdir(self) -> str:
        """Returns tmp dir name."""
        return self._get_data(key=_Keys.TMP, default_value="")  # type: ignore

    @property
    def username(self) -> str:
        """Returns login name."""
        tmp: Optional[str] = os.getenv("USER")
        if tmp:
            return tmp
        return ""

    def os_arch(self) -> str:
        """Return multiplatform os architecture."""
        os_arch = "32-bit"
        if os.name == "nt":
            output = subprocess.check_output(
                ["wmic", "os", "get", "OSArchitecture"]
            ).decode()
            os_arch = output.split()[1]
        else:
            output: str = subprocess.check_output(["uname", "-m"]).decode()
            if "x86_64" in output:
                os_arch = "64-bit"
            else:
                os_arch = "32-bit"
        return os_arch

    @property
    def is_64bits(self) -> bool:
        """Check 64bits platform."""
        return sys.maxsize > 2**32


# class Env(NoDynamicAttributes):
#     """Environment class."""

#     @classmethod
#     @property
#     def home(cls) -> str:
#         """Return home dir name."""
#         tmp: Optional[str] = os.getenv("HOME")
#         if tmp:
#             return tmp
#         return ""

#     @classmethod
#     @property
#     def username(cls) -> str:
#         """Return login name."""
#         tmp: Optional[str] = os.getenv("USER")
#         if tmp:
#             return tmp
#         return ""


class PathChecker(BData):
    """PathChecker class for filesystem path."""

    def __init__(self, pathname: str, check_deep: bool = True) -> None:
        """Constructor."""
        if pathname is None:
            raise Raise.error(
                "Expected 'pathname' as string, not None.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(pathname, str):
            raise Raise.error(
                f"Expected 'pathname' as string, received: '{type(pathname)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if isinstance(pathname, str) and len(pathname) == 0:
            raise Raise.error(
                "'pathname' cannot be an empty string.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        # self._data[_Keys.PATH_NAME] = pathname
        # self._data[_Keys.SPLIT] = check_deep
        # self._data[_Keys.LIST] = []
        self._set_data(key=_Keys.PATH_NAME, value=pathname, set_default_type=str)
        self._set_data(key=_Keys.SPLIT, value=check_deep, set_default_type=bool)
        self._set_data(key=_Keys.LIST, value=[], set_default_type=List)

        # analysis
        self.__run__()

    def __run__(self) -> None:
        """Path analysis procedure."""
        query = Path(self._get_data(key=_Keys.PATH_NAME))  # type: ignore
        # check exists
        self._set_data(key=_Keys.EXISTS, value=query.exists(), set_default_type=bool)
        if self.exists:
            # check if is file
            self._set_data(
                key=_Keys.IS_FILE, value=query.is_file(), set_default_type=bool
            )
            # check if is dir
            self._set_data(
                key=_Keys.IS_DIR, value=query.is_dir(), set_default_type=bool
            )
            # check if is symlink
            self._set_data(
                key=_Keys.IS_SYMLINK, value=query.is_symlink(), set_default_type=bool
            )
            # resolve symlink
            self._set_data(
                key=_Keys.POSIXPATH, value=str(query.resolve()), set_default_type=str
            )

        if self._get_data(key=_Keys.SPLIT):
            # split and analyse
            tmp: str = ""
            tmp_list: List[PathChecker] = self._get_data(key=_Keys.LIST)  # type: ignore
            for item in self.path.split(os.sep):
                if item == "":
                    continue
                tmp += f"{os.sep}{item}"
                tmp_list.append(PathChecker(tmp, False))
            self._set_data(key=_Keys.LIST, value=tmp_list)

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
        tmp_list: List[PathChecker] = self._get_data(key=_Keys.LIST)  # type: ignore
        if self.exists:
            last: Optional[str] = None
            for item in tmp_list:
                if item.is_dir:
                    last = item.path
            return last
        return None

    @property
    def filename(self) -> Optional[str]:
        """Return filename from path."""
        if self.exists and self.is_file:
            tmp: list[str] = self.path.split(os.sep)
            if len(tmp) > 0:
                if tmp[-1] != "":
                    return tmp[-1]
        return None

    @property
    def exists(self) -> bool:
        """Return path exists flag."""
        return self._get_data(key=_Keys.EXISTS)  # type: ignore

    @property
    def is_dir(self) -> bool:
        """Return path is_dir flag."""
        return self._get_data(key=_Keys.IS_DIR)  # type: ignore

    @property
    def is_file(self) -> bool:
        """Return path is_file flag."""
        return self._get_data(key=_Keys.IS_FILE)  # type: ignore

    @property
    def is_symlink(self) -> bool:
        """Return path is_symlink flag."""
        return self._get_data(key=_Keys.IS_SYMLINK)  # type: ignore

    @property
    def path(self) -> str:
        """Return path string."""
        return self._get_data(key=_Keys.PATH_NAME)  # type: ignore

    @property
    def posixpath(self) -> Optional[str]:
        """Return path string."""
        if self.exists:
            return self._get_data(key=_Keys.POSIXPATH)  # type: ignore
        return None

    def create(self) -> bool:
        """Create path procedure."""
        tmp_list: List[PathChecker] = self._get_data(key=_Keys.LIST)  # type: ignore
        test_path: str = self.path
        file = True
        if self.path[-1] == os.sep:
            file = False
            test_path = self.path[:-1]
        for item in tmp_list:
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
        self._set_data(key=_Keys.LIST, value=[])
        self.__run__()

        return self.exists


# #[EOF]#######################################################################
