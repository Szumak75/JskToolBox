# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 25.08.2023

  Purpose: Connector interfaces module.
"""

import socket
import ssl
import sys
import posix
import time
import binascii
import select
import hashlib

from abc import ABC, abstractmethod
from typing import List, Union, Optional
from inspect import currentframe


from jsktoolbox.libs.base_data import BData
from jsktoolbox.raisetool import Raise
from jsktoolbox.netaddresstool.ipv4 import Address
from jsktoolbox.netaddresstool.ipv6 import Address6
from jsktoolbox.attribtool import ReadOnlyClass


class IConnector(ABC):
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
    def address(self) -> Optional[Union[Address, Address6]]:
        """Get host address."""

    @address.setter
    @abstractmethod
    def address(self, ip_address: Union[Address, Address6]) -> None:
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

    IPADDR = "host"
    PORT = "port"
    USER = "login"
    PASS = "password"
    OPTIONS = "opt"
    TIMEOUT = "timeout"
    SOCKET = "__socket__"
    ERRORS = "__err__"
    SSL = "__ssl__"


class API(IConnector, BData):
    """MikroTik RouterOS API connector class."""

    def __init__(
        self,
        ip_address: Optional[Union[Address, Address6]] = None,
        port: Optional[int] = 8728,
        login: Optional[str] = None,
        password: Optional[str] = None,
        timeout: float = 60.0,
        use_ssl: bool = False,
    ):
        """Constructor."""
        self._data[_Keys.OPTIONS] = "+cet1024w"
        self._data[_Keys.TIMEOUT] = float(timeout)
        self._data[_Keys.ERRORS] = []
        self._data[_Keys.SSL] = use_ssl
        if ip_address:
            self.address = ip_address
        if port is not None:
            self.port = port
        if login is not None:
            self.login = login
        if password is not None:
            self.password = password

    def __talk(self, words: List) -> Optional[List]:
        if self.__write_sentence(words) == 0:
            return
        r = []
        while 1:
            i = self.__read_sentence()
            if len(i) == 0:
                continue
            reply = i[0]
            attrs = {}
            for w in i[1:]:
                j = w.find("=", 1)
                if j == -1:
                    attrs[w] = ""
                else:
                    attrs[w[:j]] = w[j + 1 :]
            r.append((reply, attrs))
            if reply == "!done":
                return r

    def __write_sentence(self, words: List) -> int:
        ret = 0
        for w in words:
            self.__write_word(w)
            ret += 1
        self.__write_word("")
        return ret

    def __read_sentence(self) -> List:
        r = []
        while 1:
            w = self.__read_word()
            if w == "":
                return r
            r.append(w)

    def __write_word(self, word: str) -> None:
        self.__write_len(len(word))
        self.__write_str(word)

    def __read_word(self) -> Union[str, bytes]:
        ret = self.__read_str(self.__read_len())
        return ret

    def __write_len(self, value: int) -> None:
        if value < 0x80:
            self.__write_byte((value).to_bytes(1, sys.byteorder))
        elif value < 0x4000:
            value |= 0x8000
            self.__write_byte(
                ((value >> 8) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte((value & 0xFF).to_bytes(1, sys.byteorder))
        elif value < 0x200000:
            value |= 0xC00000
            self.__write_byte(
                ((value >> 16) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte(
                ((value >> 8) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte((value & 0xFF).to_bytes(1, sys.byteorder))
        elif value < 0x10000000:
            value |= 0xE0000000
            self.__write_byte(
                ((value >> 24) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte(
                ((value >> 16) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte(
                ((value >> 8) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte((value & 0xFF).to_bytes(1, sys.byteorder))
        else:
            self.__write_byte((0xF0).to_bytes(1, sys.byteorder))
            self.__write_byte(
                ((value >> 24) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte(
                ((value >> 16) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte(
                ((value >> 8) & 0xFF).to_bytes(1, sys.byteorder)
            )
            self.__write_byte((value & 0xFF).to_bytes(1, sys.byteorder))

    def __read_len(self) -> int:
        char = ord(self.__read_str(1))
        if (char & 0x80) == 0x00:
            pass
        elif (char & 0xC0) == 0x80:
            char &= ~0xC0
            char <<= 8
            char += ord(self.__read_str(1))
        elif (char & 0xE0) == 0xC0:
            char &= ~0xE0
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
        elif (char & 0xF0) == 0xE0:
            char &= ~0xF0
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
        elif (char & 0xF8) == 0xF0:
            char = ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
        return char

    def __write_str(self, string: str) -> None:
        n = 0
        while n < len(string):
            r = self._data[_Keys.SOCKET].send(bytes(string[n:], "UTF-8"))
            if r == 0:
                raise Raise.error(
                    "connection closed by remote end",
                    RuntimeError,
                    self._c_name,
                    currentframe(),
                )
            n += r

    def __write_byte(self, string: bytes) -> None:
        n = 0
        while n < len(string):
            r = self._data[_Keys.SOCKET].send(string[n:])
            if r == 0:
                raise Raise.error(
                    "connection closed by remote end",
                    RuntimeError,
                    self._c_name,
                    currentframe(),
                )
            n += r

    def __read_str(self, length: int) -> Union[str, bytes]:
        ret = ""
        while len(ret) < length:
            s = self._data[_Keys.SOCKET].recv(length - len(ret))
            if s == b"":
                raise Raise.error(
                    "connection closed by remote end",
                    RuntimeError,
                    self._c_name,
                    currentframe(),
                )
            if s >= (128).to_bytes(1, "big"):
                return s
            ret += s.decode(sys.stdout.encoding, "replace")
        return ret

    def __get_socket(self) -> bool:
        """Try to open client socket for communications."""
        res = socket.getaddrinfo(
            str(self.address),
            self.port,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM,
        )
        af, socktype, proto, canonname, sa = res[0]

        # try to create socket
        try:
            skt = socket.socket(af, socktype, proto)
        except socket.error as ex:
            self._data[_Keys.SOCKET] = None
            self._data[_Keys.ERRORS].append(f"socket creation error: {ex}")
            return False
        except Exception as ex:
            self._data[_Keys.SOCKET] = None
            self._data[_Keys.ERRORS].append(f"socket creation error: {ex}")
            return False

        # set ssl if needed
        if self._data[_Keys.SSL]:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            self._data[_Keys.SOCKET] = context.wrap_socket(skt)
            # self._data[_Keys.SOCKET] = ssl.wrap_socket(
            # skt,
            # ssl_version=ssl.PROTOCOL_TLSv1_2,
            # ciphers="ECDHE-RSA-AES256-GCM-SHA384",
            # )
        else:
            self._data[_Keys.SOCKET] = skt

        # try to connect
        try:
            self._data[_Keys.SOCKET].connect(sa)
        except socket.error as ex:
            self._data[_Keys.SOCKET] = None
            self._data[_Keys.ERRORS].append(f"socket connection error: {ex}")
            return False
        except Exception as ex:
            self._data[_Keys.SOCKET] = None
            self._data[_Keys.ERRORS].append(f"socket connection error: {ex}")
            return False
        return True

    def __connect(self) -> bool:
        """connection method."""
        # get socket
        if not self.__get_socket():
            self._data[_Keys.ERRORS].append("could not open socket")
            return False

        # try to login
        for repl, attrs in self.__talk(
            [
                "/login",
                f"=name={self._data[_Keys.USER]}",
                f"=password={self._data[_Keys.PASS]}",
            ]
        ):
            if repl == "!trap":
                return False
            elif "=ret" in attrs.keys():
                chal = binascii.unhexlify(
                    (attrs["=ret"]).encode(sys.stdout.encoding)
                )
                md = hashlib.md5()
                md.update(b"\x00")
                md.update(self._data[_Keys.PASS].encode(sys.stdout.encoding))
                md.update(chal)
                for repl2, attrs2 in self.__talk(
                    [
                        "/login",
                        f"=name={self._data[_Keys.USER]}",
                        "=response=00"
                        + binascii.hexlify(md.digest()).decode(
                            sys.stdout.encoding
                        ),
                    ]
                ):
                    if repl2 == "!trap":
                        return False

        return True

    def connect(self) -> bool:
        """Try to connect."""
        if self.address is None:
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
        try:
            self._data[_Keys.SOCKET].close()
            return True
        except Exception as ex:
            self._data[_Keys.ERRORS].append(f'close error: "{ex}"')

        return False

    def errors(self) -> List[str]:
        """Get list of errors after executed commands."""
        return self._data[_Keys.ERRORS]

    def execute(self, commands: Union[str, List]) -> bool:
        """Execute commands."""

    @property
    def address(self) -> Optional[Union[Address, Address6]]:
        """Get host address property."""
        if _Keys.IPADDR not in self._data:
            self._data[_Keys.IPADDR] = None
        return self._data[_Keys.IPADDR]

    @address.setter
    def address(self, ip_address: Union[Address, Address6]) -> None:
        """Set host address setter."""
        if ip_address:
            if isinstance(ip_address, (Address, Address6)):
                self._data[_Keys.IPADDR] = ip_address
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
        try:
            self._data[_Keys.SOCKET].settimeout(2)
        except Exception:
            # socket is closed
            return False

        try:
            self.__talk("/system/identity/print")
        except (socket.timeout, IndexError, BrokenPipeError):
            self._data[_Keys.ERRORS].append(
                "RouterOS does not respond, closing socket."
            )
            self.disconnect()
            return False
        return True

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
    def password(self, passwd: str) -> None:
        """Set password property."""
        if passwd is not None and not isinstance(passwd, str):
            raise Raise.error(
                f"Expected int type, received: '{type(passwd)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.PASS] = passwd

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


class SSH(IConnector, BData):
    """SSH connector class."""

    def __init__(
        self,
        ip_address: Optional[Union[Address, Address6]] = None,
        port: Optional[int] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Constructor."""
        if ip_address:
            self.address = ip_address
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
    def address(self) -> Optional[Union[Address, Address6]]:
        """Get host address property."""
        if _Keys.IPADDR not in self._data:
            self._data[_Keys.IPADDR] = None
        return self._data[_Keys.IPADDR]

    @address.setter
    def address(self, ip_address: Union[Address, Address6]) -> None:
        """Set host address setter."""
        if ip_address:
            if isinstance(ip_address, (Address, Address6)):
                self._data[_Keys.IPADDR] = ip_address
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
    def password(self, passwd: str) -> None:
        """Set password property."""
        if passwd is not None and not isinstance(passwd, str):
            raise Raise.error(
                f"Expected int type, received: '{type(passwd)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.PASS] = passwd

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
