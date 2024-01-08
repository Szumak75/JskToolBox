# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.09.2023

  Purpose: testing IPv6 prefix
"""

import unittest
from jsktoolbox.netaddresstool.ipv6 import Prefix6


class TestPrefix6(unittest.TestCase):
    """Tests for Prefix6 class."""

    def test_01_create_from_int(self) -> None:
        """Test nr 1."""
        try:
            Prefix6(128)
        except Exception:
            self.fail(
                "Unexpected exception was thrown while creating the Prefix6 class object."
            )

    def test_02_create_from_str(self) -> None:
        """Test nr 2."""
        try:
            Prefix6("128")
        except Exception:
            self.fail(
                "Unexpected exception was thrown while creating the Prefix6 class object."
            )

    def test_03_return_int(self) -> None:
        """Test nr 3."""
        o = Prefix6(128)
        self.assertTrue(int(o) == 128)
        self.assertTrue(int(o.prefix) == 128)
        o = Prefix6("128")
        self.assertTrue(int(o) == 128)
        self.assertTrue(int(o.prefix) == 128)

    def test_04_return_str(self) -> None:
        """Test nr 4."""
        o = Prefix6(128)
        self.assertTrue(str(o) == "128")
        self.assertTrue(o.prefix == "128")
        o = Prefix6("128")
        self.assertTrue(str(o) == "128")
        self.assertTrue(o.prefix == "128")

    def test_05_create_invalid_prefix(self) -> None:
        """Test nr 5."""
        with self.assertRaises(ValueError):
            Prefix6(129)

        with self.assertRaises(ValueError):
            Prefix6(-1)

        with self.assertRaises(ValueError):
            Prefix6("test")

        with self.assertRaises(ValueError):
            Prefix6("test")

        with self.assertRaises(ValueError):
            Prefix6("02a")

    def test_06_create_valid_prefix(self) -> None:
        """Test nr 6."""
        try:
            for i in range(8, 129):
                Prefix6(i)
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")


# #[EOF]#######################################################################
