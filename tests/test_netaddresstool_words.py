# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 14.09.2023

Purpose: for testing Word16 class.
"""

import unittest
from jsktoolbox.netaddresstool import Word16


class TestWord16(unittest.TestCase):
    """Testing Word16 class."""

    def setUp(self) -> None:
        """Configure the test engine."""
        self.o = Word16(0)

    def test_01_create_proper_object_from_int(self) -> None:
        """Test nr 1."""
        self.assertIsInstance(Word16(1), Word16)

    def test_02_create_proper_object_from_str(self) -> None:
        """Test nr 2."""
        self.assertIsInstance(Word16("0x000a"), Word16)

    def test_03_set_proper_value(self) -> None:
        """Test nr 3."""
        try:
            for i in range(0, 65536):
                self.o.value = i
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

    def test_04_set_proper_value_str(self) -> None:
        """Test nr 4."""
        try:
            self.o.value = "1"
            self.o.value = "10"
            self.o.value = "192"
            self.o.value = "255"
            self.o.value = "0xffff"
            self.o.value = 0xA10F
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

    def test_05_set_invalid_value(self) -> None:
        """Test nr 5."""
        with self.assertRaises(ValueError):
            self.o.value = -1
            self.o.value = 65536

    def test_06_set_invalid_value_str(self) -> None:
        """Test nr 6."""
        with self.assertRaises(ValueError):
            self.o.value = "-10"
            self.o.value = "270"

    def test_07_set_invalid_type_float(self) -> None:
        """Test nr 7."""
        with self.assertRaises(TypeError):
            self.o.value = 2.1  # type: ignore

    def test_08_set_invalid_type_string(self) -> None:
        """Test nr 8."""
        with self.assertRaises(ValueError):
            self.o.value = "test"

    def test_09_set_invalid_type_binary(self) -> None:
        """Test nr 9."""
        with self.assertRaises(TypeError):
            self.o.value = b"1"  # type: ignore

    def test_10_string_representation(self) -> None:
        """Test nr 10."""
        self.o.value = 123
        self.assertEqual(str(self.o), "7b")

    def test_11_set_proper_value_of_octet(self) -> None:
        """Test nr 11."""
        try:
            self.o.value = Word16(13)
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")
        self.assertEqual(self.o.value, 13)

    def test_12_octets_equal(self) -> None:
        """Test nr 12."""
        self.assertTrue(Word16(10) == Word16(10))
        self.assertFalse(Word16(10) == Word16(11))

    def test_13_octets_negative(self) -> None:
        """Test nr 13."""
        self.assertTrue(Word16(2) != Word16(3))
        self.assertFalse(Word16(12) != Word16(12))

    def test_14_octets_less(self) -> None:
        """Test nr 14."""
        self.assertTrue(Word16(193) < Word16(194))
        self.assertFalse(Word16(194) < Word16(193))

    def test_15_octets_less_or_equal(self) -> None:
        """Test nr 15."""
        self.assertTrue(Word16(7) <= Word16(7))
        self.assertTrue(Word16(1) <= Word16(7))
        self.assertFalse(Word16(194) <= Word16(193))

    def test_16_octets_greater(self) -> None:
        """Test nr 16."""
        self.assertTrue(Word16(19) > Word16(14))
        self.assertFalse(Word16(1) > Word16(3))

    def test_17_octets_greater_or_equal(self) -> None:
        """Test nr 17."""
        self.assertTrue(Word16(7) >= Word16(7))
        self.assertTrue(Word16(10) >= Word16(7))
        self.assertFalse(Word16(19) >= Word16(193))

    def test_18_set_hexadecimal_without_prefix(self) -> None:
        """Test nr 18."""
        try:
            self.o.value = "db8"
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")
        self.assertEqual(self.o.value, int("db8", 16))

    def test_19_set_hexadecimal_mixed_case(self) -> None:
        """Test nr 19."""
        try:
            self.o.value = "AbCd"
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")
        self.assertEqual(self.o.value, int("abcd", 16))

    def test_20_set_value_with_whitespace(self) -> None:
        """Test nr 20."""
        try:
            self.o.value = "  00ff  "
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")
        self.assertEqual(self.o.value, 255)

    def test_21_empty_string_raise_value_error(self) -> None:
        """Test nr 21."""
        with self.assertRaises(ValueError):
            self.o.value = ""

    def test_22_invalid_hexadecimal_raise_value_error(self) -> None:
        """Test nr 22."""
        with self.assertRaises(ValueError):
            self.o.value = "0xgg"


# #[EOF]#######################################################################
