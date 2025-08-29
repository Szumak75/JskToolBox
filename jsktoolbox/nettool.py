# -*- coding: utf-8 -*-
"""
nettool.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 29.08.2025, 08:39:50

Purpose: Sets of classes for various network operations.
"""

import os
import re
import socket
import subprocess

from inspect import currentframe
from typing import Optional, Dict, List
from socket import getaddrinfo
from re import Pattern

from .basetool.data import BData
from .attribtool import ReadOnlyClass
from .attribtool import NoDynamicAttributes
from .netaddresstool.ipv4 import Address
from .netaddresstool.ipv6 import Address6
from .raisetool import Raise

try:
    # For Python < 3.12
    from distutils.spawn import find_executable
except ImportError:
    # For Python >= 3.12
    from shutil import which as find_executable


class _Keys(object, metaclass=ReadOnlyClass):
    """Private Keys definition class.

    For internal purpose only.
    """

    CMD: str = "cmd"
    COMMAND: str = "__command_found__"
    COMMANDS: str = "__commands__"
    MULTIPLIER: str = "__multiplier__"
    OPTS: str = "opts"
    TIMEOUT: str = "__timeout__"


class Pinger(BData):
    """Pinger class for testing ICMP echo."""

    def __init__(self, timeout: int = 1) -> None:
        """Constructor.

        Arguments:
        - timeout [int] - timeout in seconds
        """
        self._set_data(key=_Keys.TIMEOUT, value=timeout, set_default_type=int)
        self._set_data(key=_Keys.COMMANDS, value=[], set_default_type=List)
        self._set_data(key=_Keys.MULTIPLIER, value=1, set_default_type=int)

        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "fping",
                _Keys.MULTIPLIER: 1000,
                _Keys.OPTS: "-AaqR -B1 -r2 -t{} {} >/dev/null 2>&1",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                # FreeBSD ping
                _Keys.CMD: "ping",
                _Keys.MULTIPLIER: 1000,
                _Keys.OPTS: "-Qqo -c3 -W{} {} >/dev/null 2>&1",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                # Linux ping
                _Keys.CMD: "ping",
                _Keys.MULTIPLIER: 1,
                _Keys.OPTS: "-q -c3 -W{} {} >/dev/null 2>&1",
            }
        )
        tmp: Optional[tuple] = self.__is_tool
        if tmp:
            (command, multiplier) = tmp
            self._set_data(key=_Keys.COMMAND, value=command, set_default_type=str)
            self._set_data(key=_Keys.MULTIPLIER, value=multiplier)

    def is_alive(self, ip: str) -> bool:
        """Check ICMP echo response."""
        command: Optional[str] = self._get_data(key=_Keys.COMMAND)
        timeout: int = self._get_data(key=_Keys.TIMEOUT)  # type: ignore
        multiplier: int = self._get_data(key=_Keys.MULTIPLIER)  # type: ignore
        if command is None:
            raise Raise.error(
                "Command for testing ICMP echo not found.",
                ChildProcessError,
                self._c_name,
                currentframe(),
            )
        if (
            os.system(
                command.format(
                    int(timeout * multiplier),
                    str(Address(ip)),
                )
            )
        ) == 0:
            return True
        return False

    @property
    def __is_tool(self) -> Optional[tuple]:
        """Check system command."""
        for cmd in self._get_data(key=_Keys.COMMANDS):  # type: ignore
            if find_executable(cmd[_Keys.CMD]) is not None:
                test_cmd: str = f"{cmd[_Keys.CMD]} {cmd[_Keys.OPTS]}"
                multiplier: int = cmd[_Keys.MULTIPLIER]
                if (
                    os.system(
                        test_cmd.format(
                            int(self._get_data(key=_Keys.TIMEOUT) * multiplier),  # type: ignore
                            "127.0.0.1",
                        )
                    )
                    == 0
                ):
                    return test_cmd, multiplier
        return None


class Tracert(BData):
    """Tracert class for testing route to IPv4 address."""

    def __init__(self) -> None:
        """Constructor."""
        self._set_data(key=_Keys.COMMANDS, value=[], set_default_type=List)
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "traceroute",
                _Keys.OPTS: "-I -q2 -S -e -w1 -n -m 10",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "traceroute",
                _Keys.OPTS: "-P UDP -q2 -S -e -w1 -n -m 10",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "traceroute",
                _Keys.OPTS: "-I -q2 -e -w1 -n -m 10",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "traceroute",
                _Keys.OPTS: "-U -q2 -e -w1 -n -m 10",
            }
        )
        self._set_data(
            key=_Keys.COMMAND, value=self.__is_tool, set_default_type=Optional[Dict]
        )

    @property
    def __is_tool(self) -> Optional[Dict]:
        """Check system commend."""
        for cmd in self._get_data(key=_Keys.COMMANDS):  # type: ignore
            if find_executable(cmd[_Keys.CMD]) is not None:
                if (
                    os.system(
                        "{} {} {} > /dev/null 2>&1".format(
                            cmd[_Keys.CMD], cmd[_Keys.OPTS], "127.0.0.1"
                        )
                    )
                    == 0
                ):
                    out = {}
                    out.update(cmd)
                    return out
        return None

    def execute(self, ip: str) -> List[str]:
        """Traceroute to given IPv4 address."""
        command: Optional[Dict] = self._get_data(key=_Keys.COMMAND)
        if command is None:
            raise Raise.error(
                "Command for testing traceroute not found.",
                ChildProcessError,
                self._c_name,
                currentframe(),
            )
        out: List[str] = []
        args: List[str] = []
        args.append(command[_Keys.CMD])
        args.extend(command[_Keys.OPTS].split(" "))
        args.append(str(Address(ip)))

        # TODO:
        # traceroute to 192.168.255.255 (192.168.255.255), 10 hops max, 60 byte packets
        # 1  * *
        # 2  * *
        # 3  * *
        # 4  * *
        # 5  * *
        # 6  * *
        # 7  * *
        # 8  * *
        # 9  * *
        # 10  * *

        with subprocess.Popen(
            args,
            env={
                "PATH": "/bin:/sbin:/usr/bin:/usr/sbin",
            },
            stdout=subprocess.PIPE,
        ) as proc:
            if proc.stdout is not None:
                for line in proc.stdout:
                    out.append(line.decode("utf-8"))
        return out


class HostResolvableChecker(NoDynamicAttributes):
    """Class to check if a hostname or IP address is resolvable."""

    @staticmethod
    def is_resolvable(host: str) -> bool:
        """Check if the given host (hostname or IP) is resolvable.

        Args:
            host (str): The hostname or IP address to check.

        Returns:
            bool: True if the host is resolvable, False otherwise.
        """
        try:
            getaddrinfo(host, None)
            return True
        except Exception:
            return False

    @staticmethod
    def is_ip_address(host: str) -> bool:
        """Check if the given host is a valid IP address (IPv4 or IPv6).

        Args:
            host (str): The hostname or IP address to check.

        Returns:
            bool: True if the host is a valid IP address, False otherwise.
        """
        try:
            Address(host)
            return True
        except Exception:
            pass

        try:
            Address6(host)
            return True
        except Exception:
            pass

        return False

    @staticmethod
    def is_hostname(host: str) -> bool:
        """Check if the given host is a valid hostname.

        Args:
            host (str): The hostname or IP address to check.

        Returns:
            bool: True if the host is a valid hostname, False otherwise.
        """
        if HostResolvableChecker.is_ip_address(host):
            return False

        # Basic regex for hostname validation
        hostname_regex: Pattern[str] = re.compile(
            r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
        )

        return bool(hostname_regex.match(host))

    @staticmethod
    def validate_host(host: str) -> Optional[str]:
        """Validate if the given host is either a resolvable hostname or a valid IP address.

        Args:
            host (str): The hostname or IP address to validate.

        Returns:
            Optional[str]: None if valid, otherwise an error message.
        """
        if HostResolvableChecker.is_ip_address(host):
            return None

        if HostResolvableChecker.is_hostname(host):
            if HostResolvableChecker.is_resolvable(host):
                return None
            else:
                return f"Hostname '{host}' is not resolvable."

        return f"'{host}' is neither a valid IP address nor a valid hostname."

    @staticmethod
    def ip_from_hostname(hostname: str) -> Optional[str]:
        """Get the first resolved IP address for the given hostname.

        Args:
            hostname (str): The hostname to resolve.

        Returns:
            Optional[str]: The first resolved IP address, or None if not resolvable.
        """
        try:
            addr_info = getaddrinfo(hostname, None)
            if addr_info:
                return f"{addr_info[0][4][0]}"
            return None
        except Exception:
            return None

    @staticmethod
    def validate_hosts(hosts: List[str]) -> Dict[str, Optional[str]]:
        """Validate a list of hosts.

        Args:
            hosts (list[str]): List of hostnames or IP addresses to validate.

        Returns:
            dict[str, Optional[str]]: Dictionary with hosts as keys and validation results as values.
        """
        results = {}
        for host in hosts:
            results[host] = HostResolvableChecker.validate_host(host)
        return results

    @staticmethod
    def filter_valid_hosts(hosts: List[str]) -> List[str]:
        """Filter and return only valid hosts from the given list.

        Args:
            hosts (list[str]): List of hostnames or IP addresses to filter.

        Returns:
            list[str]: List of valid hosts.
        """
        return [
            host for host in hosts if HostResolvableChecker.validate_host(host) is None
        ]

    @staticmethod
    def filter_invalid_hosts(hosts: List[str]) -> Dict[str, str]:
        """Filter and return only invalid hosts from the given list along with error messages.

        Args:
            hosts (list[str]): List of hostnames or IP addresses to filter.

        Returns:
            dict[str, str]: Dictionary with invalid hosts as keys and error messages as values.
        """
        results = {}
        for host in hosts:
            error = HostResolvableChecker.validate_host(host)
            if error is not None:
                results[host] = error
        return results

    @staticmethod
    def ip4_from_hostname(hostname: str) -> Optional[Address]:
        """Resolve and return the first IPv4 address for the given hostname.

        Args:
            hostname (str): The hostname to resolve.

        Returns:
            Optional[str]: The first resolved IPv4 address, or None if not resolvable.
        """
        try:
            addr_info = getaddrinfo(hostname, None, family=socket.AF_INET)
            if addr_info:
                return Address(addr_info[0][4][0])
            return None
        except Exception:
            return None

    @staticmethod
    def ip6_from_hostname(hostname: str) -> Optional[Address6]:
        """Resolve and return the first IPv6 address for the given hostname.

        Args:
            hostname (str): The hostname to resolve.

        Returns:
            Optional[str]: The first resolved IPv6 address, or None if not resolvable.
        """
        try:
            addr_info = getaddrinfo(hostname, None, family=socket.AF_INET6)
            if addr_info:
                return Address6(addr_info[0][4][0])
            return None
        except Exception:
            return None


# #[EOF]#######################################################################
