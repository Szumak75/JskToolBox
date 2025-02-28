# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 03.12.2023

  Purpose: Connectors module testing class.
"""

import unittest
import os

from jsktoolbox.devices.network.connectors import API, SSH
from jsktoolbox.netaddresstool.ipv4 import Address
from jsktoolbox.netaddresstool.ipv6 import Address6


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
        """Test nr 06."""
        ip = "10.5.5.254"
        if os.system(f"ping -c 1 {ip}") == 0:
            try:
                obj = API(
                    ip_address=Address(ip),
                    port=8728,
                    login="devel",
                    password="mojehaslo",
                )
                self.assertTrue(obj.connect(), msg="connection error")
                self.assertTrue(obj.is_alive, msg="broken connection")
                self.assertTrue(obj.execute("/system/identity/print"))
                self.assertTrue(obj.disconnect(), msg="disconnection error")
            except Exception as ex:
                self.fail(msg=f"Exception was thrown: {ex}")
            self.assertEqual(len(obj.errors()), 0, msg=f"{obj.errors()}")


# #[EOF]#######################################################################
