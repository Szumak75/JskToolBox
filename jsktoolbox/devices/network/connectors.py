# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 25.08.2023

  Purpose: Connector interfaces module.
"""

from abc import ABC, abstractmethod
from typing import List, Union, Optional
from inspect import currentframe

from jsktoolbox.libs.base_data import BData
from jsktoolbox.raisetool import Raise
from jsktoolbox.netaddresstool.ipv4 import Address
from jsktoolbox.netaddresstool.ipv6 import Address6
from jsktoolbox.attribtool import ReadOnlyClass


class IConnect(ABC):
    """Conection class interface."""

    @abstractmethod
    def connect(self) -> bool:
        """Connection method."""

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect method."""

    @abstractmethod
    def errors(self) -> List:
        """Get list or errors after executed commands."""

    @abstractmethod
    def execute(self, commands: Union[str, List]) -> bool:
        """Execute method."""

    @property
    @abstractmethod
    def host(self) -> Optional[Union[Address, Address6]]:
        """Get host address."""

    @host.setter
    @abstractmethod
    def host(self, ip_address: Union[Address, Address6]) -> None:
        """Set host address."""

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        """Get alive flag from connected protocol."""

    @property
    @abstractmethod
    def login(self) -> Optional[str]:
        """Get login property."""

    @login.setter
    @abstractmethod
    def login(self, username: str) -> None:
        """Set login property."""

    @abstractmethod
    def outputs(self) -> List:
        """Get list of results after executed commands."""

    @property
    @abstractmethod
    def password(self) -> Optional[str]:
        """Get password property."""

    @password.setter
    @abstractmethod
    def password(self, passwordstring: str) -> None:
        """Set password property."""

    @property
    @abstractmethod
    def port(self) -> Optional[int]:
        """Get port property."""

    @port.setter
    @abstractmethod
    def port(self, port: int) -> None:
        """Set port property."""

    @property
    @abstractmethod
    def prototype(self) -> str:
        """Get protocol type property."""


class _Keys(object, metaclass=ReadOnlyClass):
    """Private Keys definition class.

    For internal purpose only.
    """

    HOST = "host"
    PORT = "port"
    USER = "login"
    PASS = "password"
    OPTIONS = "opt"
    TIMEOUT = "timeout"
    CH = "__connection_handler__"


class API(IConnect, BData):
    """MikroTik RouterOS API connector class."""

    def __init__(
        self,
        host: Optional[Union[Address, Address6]] = None,
        port: Optional[int] = 8728,
        login: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Constructor."""
        self._data[_Keys.OPTIONS] = "+cet1024w"
        self._data[_Keys.TIMEOUT] = float(60)
        if host:
            self.host = host
        if port is not None:
            self.port = port
        if login is not None:
            self.login = login
        if password is not None:
            self.password = password

    def __connect(self) -> bool:
        """connection method."""
        return False

    def connect(self) -> bool:
        """Try to connect."""
        if self.host is None:
            raise Raise.error(
                f"Host IP address is not set.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        if self.port is None:
            raise Raise.error(
                "Port is not set.", ValueError, self._c_name, currentframe()
            )
        if self.login is None:
            raise Raise.error(
                "Login is not set.", ValueError, self._c_name, currentframe()
            )
        if self.password is None:
            raise Raise.error(
                "Password is not set.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        return self.__connect()

    def disconnect(self) -> bool:
        """Terminate connection."""

    def errors(self) -> List:
        """Get list or errors after executed commands."""

    def execute(self, commands: Union[str, List]) -> bool:
        """Execute commands."""

    @property
    def host(self) -> Optional[Union[Address, Address6]]:
        """Get host address property."""
        if _Keys.HOST not in self._data:
            self._data[_Keys.HOST] = None
        return self._data[_Keys.HOST]

    @host.setter
    def host(self, ip_address: Union[Address, Address6]) -> None:
        """Set host address setter."""
        if ip_address:
            if isinstance(ip_address, (Address, Address6)):
                self._data[_Keys.HOST] = ip_address
            else:
                raise Raise.error(
                    f"Expected Address or Address6 type, received: '{type(ip_address)}'",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    @property
    def is_alive(self) -> bool:
        """Get alive flag from connected protocol."""

    @property
    def login(self) -> Optional[str]:
        """Get login property."""
        if _Keys.USER not in self._data:
            self._data[_Keys.USER] = None
        return self._data[_Keys.USER]

    @login.setter
    def login(self, username: str) -> None:
        """Set login property."""
        if username is not None and not isinstance(username, str):
            raise Raise.error(
                f"Expected int type, received: '{type(username)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.USER] = username

    def outputs(self) -> List:
        """Get list of results after executed commands."""

    @property
    def password(self) -> Optional[str]:
        """Get password property."""
        if _Keys.PASS not in self._data:
            self._data[_Keys.PASS] = None
        return self._data[_Keys.PASS]

    @password.setter
    def password(self, passwordstring: str) -> None:
        """Set password property."""
        if passwordstring is not None and not isinstance(
            passwordstring, str
        ):
            raise Raise.error(
                f"Expected int type, received: '{type(passwordstring)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.PASS] = passwordstring

    @property
    def port(self) -> Optional[int]:
        """Get port property."""
        if _Keys.PORT not in self._data:
            self._data[_Keys.PORT] = None
        return self._data[_Keys.PORT]

    @port.setter
    def port(self, port: int) -> None:
        """Set port property."""
        if port is not None:
            if isinstance(port, int):
                self._data[_Keys.PORT] = port
            else:
                raise Raise.error(
                    f"Expected int type, received: '{type(port)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    @property
    def prototype(self) -> str:
        """Get protocol type property."""
        return "API"


class SSH(IConnect, BData):
    """SSH connector class."""

    def __init__(
        self,
        host: Optional[Union[Address, Address6]] = None,
        port: Optional[int] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Constructor."""
        if host:
            self.host = host
        if port is not None:
            self.port = port
        if login is not None:
            self.login = login
        if password is not None:
            self.password = password

    def connect(self) -> bool:
        """Try to connect."""

    def disconnect(self) -> bool:
        """Terminate connection."""

    def errors(self) -> List:
        """Get list or errors after executed commands."""

    def execute(self, commands: Union[str, List]) -> bool:
        """Execute commands."""

    @property
    def host(self) -> Optional[Union[Address, Address6]]:
        """Get host address property."""
        if _Keys.HOST not in self._data:
            self._data[_Keys.HOST] = None
        return self._data[_Keys.HOST]

    @host.setter
    def host(self, ip_address: Union[Address, Address6]) -> None:
        """Set host address setter."""
        if ip_address:
            if isinstance(ip_address, (Address, Address6)):
                self._data[_Keys.HOST] = ip_address
            else:
                raise Raise.error(
                    f"Expected Address or Address6 type, received: '{type(ip_address)}'",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    @property
    def is_alive(self) -> bool:
        """Get alive flag from connected protocol."""

    @property
    def login(self) -> Optional[str]:
        """Get login property."""
        if _Keys.USER not in self._data:
            self._data[_Keys.USER] = None
        return self._data[_Keys.USER]

    @login.setter
    def login(self, username: str) -> None:
        """Set login property."""
        if username is not None and not isinstance(username, str):
            raise Raise.error(
                f"Expected int type, received: '{type(username)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.USER] = username

    def outputs(self) -> List:
        """Get list of results after executed commands."""

    @property
    def password(self) -> Optional[str]:
        """Get password property."""
        if _Keys.PASS not in self._data:
            self._data[_Keys.PASS] = None
        return self._data[_Keys.PASS]

    @password.setter
    def password(self, passwordstring: str) -> None:
        """Set password property."""
        if passwordstring is not None and not isinstance(
            passwordstring, str
        ):
            raise Raise.error(
                f"Expected int type, received: '{type(passwordstring)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.PASS] = passwordstring

    @property
    def port(self) -> Optional[int]:
        """Get port property."""
        if _Keys.PORT not in self._data:
            self._data[_Keys.PORT] = None
        return self._data[_Keys.PORT]

    @port.setter
    def port(self, port: int) -> None:
        """Set port property."""
        if port is not None:
            if isinstance(port, int):
                self._data[_Keys.PORT] = port
            else:
                raise Raise.error(
                    f"Expected int type, received: '{type(port)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    @property
    def prototype(self) -> str:
        """Get protocol type property."""
        return "SSH"


# #[EOF]#######################################################################
