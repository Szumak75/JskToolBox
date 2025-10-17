# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 03.12.2023

Purpose: Connectors module testing class.
"""

import os
import subprocess
import unittest

from jsktoolbox.devices import API, SSH
from jsktoolbox.netaddresstool import Address, Address6


_ENDPOINTS_ENV = os.environ.get("JSKTOOLBOX_ROUTEROS_ENDPOINTS")
if _ENDPOINTS_ENV:
    ROUTEROS_ENDPOINTS = [
        item.strip() for item in _ENDPOINTS_ENV.split(",") if item.strip()
    ]
else:
    ROUTEROS_ENDPOINTS = [
        "10.5.5.254",
        "10.144.0.105",
    ]

ROUTEROS_LOGIN = os.environ.get("JSKTOOLBOX_ROUTEROS_LOGIN", "devel")
ROUTEROS_PASSWORD = os.environ.get("JSKTOOLBOX_ROUTEROS_PASSWORD", "mojehaslo")
ROUTEROS_PORT = int(os.environ.get("JSKTOOLBOX_ROUTEROS_PORT", "8728"))


def _is_endpoint_alive(ip_address: str) -> bool:
    """Return True when endpoint responds to a single ping."""
    count_flag = "-c" if os.name != "nt" else "-n"
    command = ["ping", count_flag, "1", ip_address]
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=3,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


class TestConnectors(unittest.TestCase):
    """Tests for connectors."""

    def test_01_connector(self) -> None:
        """Test nr 01."""
        try:
            API()
            SSH()
        except Exception as ex:
            self.fail(msg=f"Exception was thrown: {ex}")

    def test_02_host(self) -> None:
        """Test nr 02."""
        for obj in (API(), SSH()):
            obj.address = Address("192.168.1.1")
            self.assertIsInstance(obj.address, Address)
            self.assertEqual(obj.address, Address("192.168.1.1"))
            obj.address = Address6("1111:2222:3333:4444:5555:6666:7777:8888")
            self.assertIsInstance(obj.address, Address6)
            self.assertEqual(
                obj.address,
                Address6("1111:2222:3333:4444:5555:6666:7777:8888"),
            )

    def test_03_port(self) -> None:
        """Test nr 03."""
        for obj in (API(), SSH()):
            obj.port = 1234
            self.assertIsInstance(obj.port, int)
            self.assertEqual(obj.port, 1234)

    def test_04_user(self) -> None:
        """Test nr 04."""
        for obj in (API(), SSH()):
            obj.login = "admin"
            self.assertIsInstance(obj.login, str)
            self.assertEqual(obj.login, "admin")

    def test_05_pass(self) -> None:
        """Test nr 05."""
        for obj in (API(), SSH()):
            obj.password = "admin"
            self.assertIsInstance(obj.password, str)
            self.assertEqual(obj.password, "admin")

    def test_06_connect(self) -> None:
        """Verify API connectivity against available RouterOS endpoints."""
        if not ROUTEROS_ENDPOINTS:
            self.skipTest("No RouterOS endpoints configured for API tests.")

        reachable = []
        failures = {}

        for ip in ROUTEROS_ENDPOINTS:
            if not _is_endpoint_alive(ip):
                failures[ip] = "endpoint unreachable (ping)"
                continue

            obj = API(
                ip_address=Address(ip),
                port=ROUTEROS_PORT,
                login=ROUTEROS_LOGIN,
                password=ROUTEROS_PASSWORD,
                timeout=5.0,
            )
            connected = False
            try:
                if not obj.connect():
                    failures[ip] = f"connect() returned False: {obj.errors()}"
                    continue
                connected = True
                reachable.append(ip)
                self.assertTrue(obj.is_alive, msg=f"{ip}: broken connection")
                self.assertTrue(
                    obj.execute("/system/identity/print"),
                    msg=f"{ip}: command execution failed",
                )
                self.assertEqual(
                    len(obj.errors()),
                    0,
                    msg=f"{ip}: {obj.errors()}",
                )
            except AssertionError:
                raise
            except Exception as ex:
                failures[ip] = str(ex)
            finally:
                if connected:
                    try:
                        obj.disconnect()
                    except Exception:
                        pass

        if not reachable:
            details = [f"{ip} -> {error}" for ip, error in failures.items()] or [
                "no endpoint responded"
            ]
            self.skipTest(
                "No active RouterOS endpoints. Details: " + "; ".join(details)
            )


# #[EOF]#######################################################################
