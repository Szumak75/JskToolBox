# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 24.06.2023

Purpose: Netmask class testing.
"""

import unittest

from jsktoolbox.netaddresstool.ipv4 import Netmask
from jsktoolbox.netaddresstool.libs.octets import Octet


class TestNetmask(unittest.TestCase):
    """Class for testing Netmask."""

    def test_01_netmask_create(self) -> None:
        """Test nr 1."""
        try:
            Netmask("255.255.255.255")
            Netmask("30")
            Netmask(16)
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

    def test_02_netmask_check_conversion(self) -> None:
        """Test nr 2."""
        tab = {
            0: "0.0.0.0",
            1: "128.0.0.0",
            2: "192.0.0.0",
            3: "224.0.0.0",
            4: "240.0.0.0",
            5: "248.0.0.0",
            6: "252.0.0.0",
            7: "254.0.0.0",
            8: "255.0.0.0",
            9: "255.128.0.0",
            10: "255.192.0.0",
            11: "255.224.0.0",
            12: "255.240.0.0",
            13: "255.248.0.0",
            14: "255.252.0.0",
            15: "255.254.0.0",
            16: "255.255.0.0",
            17: "255.255.128.0",
            18: "255.255.192.0",
            19: "255.255.224.0",
            20: "255.255.240.0",
            21: "255.255.248.0",
            22: "255.255.252.0",
            23: "255.255.254.0",
            24: "255.255.255.0",
            25: "255.255.255.128",
            26: "255.255.255.192",
            27: "255.255.255.224",
            28: "255.255.255.240",
            29: "255.255.255.248",
            30: "255.255.255.252",
            31: "255.255.255.254",
            32: "255.255.255.255",
        }

        for key, val in tab.items():
            self.assertEqual(tab[key], str(Netmask(key)))
            self.assertEqual(tab[key], str(Netmask(tab[key])))
            self.assertEqual(key, int(Netmask(key)))
            self.assertEqual(key, int(Netmask(tab[key])))
            self.assertEqual(key, int(Netmask(val)))
            self.assertEqual(tab[key], str(Netmask(val)))

    def test_03_netmask_create_from_list(self) -> None:
        """Test nr 3."""
        self.assertEqual(32, int(Netmask([255, 255, 255, 255])))
        self.assertEqual(32, int(Netmask(["255", "255", "255", "255"])))
        self.assertEqual(
            32,
            int(Netmask([Octet(255), Octet(255), Octet(255), Octet(255)])),
        )

    def test_04_netmask_invalid_values(self) -> None:
        """Test nr 4."""
        with self.assertRaises(ValueError):
            Netmask(256)
        with self.assertRaises(ValueError):
            Netmask("255.255.255.256")
        with self.assertRaises(ValueError):
            Netmask("256.255.255.255")
        with self.assertRaises(ValueError):
            Netmask("127.0.0.1")
        with self.assertRaises(ValueError):
            Netmask("255.254.255.0")
        with self.assertRaises(ValueError):
            Netmask("255.253.0.0")

    def test_05_netmask_octets_property(self) -> None:
        """Test nr 5."""
        mask = Netmask(24)
        self.assertEqual([str(octet) for octet in mask.octets], ["255", "255", "255", "0"])

    def test_06_netmask_invalid_octet_list_length(self) -> None:
        """Test nr 6."""
        with self.assertRaises(ValueError):
            Netmask([255, 255, 255])  # type: ignore

    def test_07_netmask_cidr_string_assignment(self) -> None:
        """Test nr 7."""
        mask = Netmask("24")
        self.assertEqual(str(mask), "255.255.255.0")
        mask.cidr = "30"
        self.assertEqual(int(mask), 30)


# #[EOF]#######################################################################
