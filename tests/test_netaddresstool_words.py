# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 14.09.2023

  Purpose: for testing Word16 class.
"""

import unittest
from jsktoolbox.netaddresstool.libs.words import Word16


class TestWord16(unittest.TestCase):
    """Testing Word16 class."""

    def setUp(self):
        """Configure the test engine."""
        self.o = Word16(0)

    def test_create_proper_object_from_int(self):
        """Test nr 1."""
        self.assertIsInstance(Word16(1), Word16)

    def test_create_proper_object_from_str(self):
        """Test nr 2."""
        self.assertIsInstance(Word16("0x000a"), Word16)

    def test_set_proper_value(self):
        """Test nr 3."""
        try:
            for i in range(0, 65536):
                self.o.value = i
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

    def test_set_proper_value_str(self):
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

    def test_set_invalid_value(self):
        """Test nr 5."""
        with self.assertRaises(ValueError):
            self.o.value = -1
            self.o.value = 65536

    def test_set_invalid_value_str(self):
        """Test nr 6."""
        with self.assertRaises(ValueError):
            self.o.value = "-10"
            self.o.value = "270"

    def test_set_invalid_type_float(self):
        """Test nr 7."""
        with self.assertRaises(TypeError):
            self.o.value = 2.1

    def test_set_invalid_type_string(self):
        """Test nr 8."""
        with self.assertRaises(TypeError):
            self.o.value = "test"

    def test_set_invalid_type_binary(self):
        """Test nr 9."""
        with self.assertRaises(TypeError):
            self.o.value = b"1"

    def test_string_representation(self):
        """Test nr 10."""
        self.o.value = 123
        self.assertEqual(str(self.o), "7b")

    def test_set_proper_value_of_octet(self):
        """Test nr 11."""
        try:
            self.o.value = Word16(13)
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")
        self.assertEqual(self.o.value, 13)

    def test_octets_equal(self):
        """Test nr 12."""
        self.assertTrue(Word16(10) == Word16(10))
        self.assertFalse(Word16(10) == Word16(11))

    def test_octets_negative(self):
        """Test nr 13."""
        self.assertTrue(Word16(2) != Word16(3))
        self.assertFalse(Word16(12) != Word16(12))

    def test_octets_less(self):
        """Test nr 14."""
        self.assertTrue(Word16(193) < Word16(194))
        self.assertFalse(Word16(194) < Word16(193))

    def test_octets_less_or_equal(self):
        """Test nr 15."""
        self.assertTrue(Word16(7) <= Word16(7))
        self.assertTrue(Word16(1) <= Word16(7))
        self.assertFalse(Word16(194) <= Word16(193))

    def test_octets_qreater(self):
        """Test nr 16."""
        self.assertTrue(Word16(19) > Word16(14))
        self.assertFalse(Word16(1) > Word16(3))

    def test_octets_greater_or_equal(self):
        """Test nr 17."""
        self.assertTrue(Word16(7) >= Word16(7))
        self.assertTrue(Word16(10) >= Word16(7))
        self.assertFalse(Word16(19) >= Word16(193))


# #[EOF]#######################################################################
