# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 14.09.2023

  Purpose: Testing IPv6 Address class.
"""

import unittest
from jsktoolbox.netaddresstool.ipv6 import Address6
from jsktoolbox.netaddresstool.libs.words import Word16


class TestAddress6(unittest.TestCase):
    """Testing Address Class."""

    def setUp(self) -> None:
        """Configure the test engine."""
        self.o = Address6("1111:2222:3333:4444:5555:6666:7777:8888")

    def test_01_address_string(self) -> None:
        """Test nr 1."""
        self.assertEqual(
            str(self.o), "1111:2222:3333:4444:5555:6666:7777:8888"
        )

    def test_02_address_words(self) -> None:
        """Test nr 2."""
        self.assertEqual(len(self.o.words), 8)

    def test_03_set_from_list_of_integers(self) -> None:
        """Test nr 3."""
        self.o.words = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(str(self.o), "1:2:3:4:5:6:7:8")

    def test_04_set_from_list_of_string(self) -> None:
        """Test nr 4."""
        self.o.words = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.assertEqual(str(self.o), "1:2:3:4:5:6:7:8")

    def test_05_set_from_list_of_words(self) -> None:
        """Test nr 5."""
        self.o.words = [
            Word16("0xFF"),
            Word16("0"),
            Word16("0x0"),
            Word16("0"),
            Word16("0x0"),
            Word16("0"),
            Word16("0x0"),
            Word16("0xFFFF"),
        ]
        self.assertEqual(str(self.o), "ff::ffff")

    def test_06_set_from_int(self) -> None:
        """Test nr 6."""
        self.o.words = 4095
        self.assertEqual(str(self.o), "::fff")

    def test_07_set_from_string(self) -> None:
        """Test nr 7."""
        self.o.words = "1:0:0:0:0:0:0:1"
        self.assertEqual(str(self.o), "1::1")
        self.o.words = "::FF"
        self.assertEqual(int(self.o), 255)

    def test_08_address_equal(self) -> None:
        """Test nr 8."""
        self.assertTrue(
            Address6("2000:0:0:0:0:0:0:FF") == Address6("2000::FF")
        )
        self.assertFalse(Address6("::FA") == Address6("::FB"))

    def test_09_address_negative(self) -> None:
        """Test nr 9."""
        self.assertTrue(
            Address6("2000:0:0:0:0:0:0:FF") != Address6("2000::F")
        )
        self.assertFalse(Address6("::AA") != Address6("::AA"))

    def test_10_address_less(self) -> None:
        """Test nr 10."""
        self.assertTrue(
            Address6("2000:0:0:0:0:0:0:FF") < Address6("2000:1::FF")
        )
        self.assertFalse(Address6("::FB") < Address6("::FA"))
        self.assertFalse(Address6("::F") < Address6("::F"))

    def test_11_address_less_or_equal(self) -> None:
        """Test nr 11."""
        self.assertTrue(
            Address6("2000:0:0:0:0:0:0:FF") <= Address6("2000:1::FF")
        )
        self.assertTrue(
            Address6("2000:0:0:0:0:0:0:FF") <= Address6("2000::FF")
        )

    def test_12_address_greater(self) -> None:
        """Test nr 12."""
        self.assertTrue(
            Address6("2000:0:0:0:0:0:0:FF") > Address6("2000::FE")
        )
        self.assertFalse(Address6("::FA") > Address6("::FB"))

    def test_13_address_greater_or_equal(self) -> None:
        """Test nr 13."""
        self.assertTrue(
            Address6("2000:0:0:0:0:0:0:FF") >= Address6("2000::FE")
        )
        self.assertTrue(
            Address6("2000:0:0:0:0:0:0:FF") >= Address6("2000::FF")
        )

    def test_14_address_invalid(self) -> None:
        """Test nr 14."""
        with self.assertRaises(ValueError):
            Address6("::1::1")
        with self.assertRaises(ValueError):
            Address6("2000:0:0:0:0:0:0:FF:AA")
        with self.assertRaises(ValueError):
            Address6(-1)
        with self.assertRaises(ValueError):
            Address6([1, 2, 3])
        with self.assertRaises(TypeError):
            Address6(None) # type: ignore
        with self.assertRaises(TypeError):
            Address6({}) # type: ignore


# #[EOF]#######################################################################
