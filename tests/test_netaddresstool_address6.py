# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 14.09.2023

Purpose: Testing IPv6 Address class.
"""

import unittest
from jsktoolbox.netaddresstool import Address6, Word16


class TestAddress6(unittest.TestCase):
    """Testing Address Class."""

    def setUp(self) -> None:
        """Configure the test engine."""
        self.o = Address6("1111:2222:3333:4444:5555:6666:7777:8888")

    def test_01_address_string(self) -> None:
        """Test nr 1."""
        self.assertEqual(str(self.o), "1111:2222:3333:4444:5555:6666:7777:8888")

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
        self.assertTrue(Address6("2000:0:0:0:0:0:0:FF") == Address6("2000::FF"))
        self.assertFalse(Address6("::FA") == Address6("::FB"))

    def test_09_address_negative(self) -> None:
        """Test nr 9."""
        self.assertTrue(Address6("2000:0:0:0:0:0:0:FF") != Address6("2000::F"))
        self.assertFalse(Address6("::AA") != Address6("::AA"))

    def test_10_address_less(self) -> None:
        """Test nr 10."""
        self.assertTrue(Address6("2000:0:0:0:0:0:0:FF") < Address6("2000:1::FF"))
        self.assertFalse(Address6("::FB") < Address6("::FA"))
        self.assertFalse(Address6("::F") < Address6("::F"))

    def test_11_address_less_or_equal(self) -> None:
        """Test nr 11."""
        self.assertTrue(Address6("2000:0:0:0:0:0:0:FF") <= Address6("2000:1::FF"))
        self.assertTrue(Address6("2000:0:0:0:0:0:0:FF") <= Address6("2000::FF"))

    def test_12_address_greater(self) -> None:
        """Test nr 12."""
        self.assertTrue(Address6("2000:0:0:0:0:0:0:FF") > Address6("2000::FE"))
        self.assertFalse(Address6("::FA") > Address6("::FB"))

    def test_13_address_greater_or_equal(self) -> None:
        """Test nr 13."""
        self.assertTrue(Address6("2000:0:0:0:0:0:0:FF") >= Address6("2000::FE"))
        self.assertTrue(Address6("2000:0:0:0:0:0:0:FF") >= Address6("2000::FF"))

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
            Address6(None)  # type: ignore
        with self.assertRaises(TypeError):
            Address6({})  # type: ignore

    def test_15_words_from_compressed_address(self) -> None:
        """Test nr 15."""
        addr = Address6("2001:db8::1")
        self.assertEqual(
            [int(word) for word in addr.words],
            [2001, 3512, 0, 0, 0, 0, 0, 1],
        )

    def test_16_set_words_from_hex_strings(self) -> None:
        """Test nr 16."""
        self.o.words = ["0x2001", "db8", "0", "0", "0", "0", "0", "0x0001"]
        self.assertEqual(str(self.o), "2001:db8::1")

    def test_17_set_words_invalid_length(self) -> None:
        """Test nr 17."""
        with self.assertRaises(ValueError):
            self.o.words = ["2001", "db8"]  # type: ignore

    def test_18_set_words_invalid_literal(self) -> None:
        """Test nr 18."""
        with self.assertRaises(ValueError):
            self.o.words = ["zzzz"] * 8  # type: ignore

    def test_19_integer_roundtrip(self) -> None:
        """Test nr 19."""
        original = Address6("abcd:ef12::1")
        self.assertEqual(Address6(int(original)).__str__(), str(original))


# #[EOF]#######################################################################
