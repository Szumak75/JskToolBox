#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 23.06.2023

  Purpose: for testing Octet class.
"""

import unittest
from jsktoolbox.netaddresstool.libs.octets import Octet


class TestOctet(unittest.TestCase):
    """Testing Octet class."""

    def setUp(self):
        """Configure the test engine."""
        self.o = Octet(0)

    def test_create_proper_object_from_int(self):
        """Test nr 1."""
        self.assertIsInstance(Octet(1), Octet)

    def test_create_proper_object_from_str(self):
        """Test nr 2."""
        self.assertIsInstance(Octet("255"), Octet)

    def test_set_proper_value(self):
        """Test nr 3."""
        try:
            for i in range(0, 256):
                self.o.value = i
        except Exception as ex:
            self.fail(f"Unexpected exception war raised: {ex}")

    def test_set_proper_value_str(self):
        """Test nr 4."""
        try:
            self.o.value = "1"
            self.o.value = "10"
            self.o.value = "192"
            self.o.value = "255"
        except Exception as ex:
            self.fail(f"Unexpected exception was raised: {ex}")

    def test_set_invalid_value(self):
        """Test nr 5."""
        with self.assertRaises(ValueError):
            self.o.value = -1
            self.o.value = 256

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
        self.assertEqual(str(self.o), "123")

    def test_set_proper_value_of_octet(self):
        """Test nr 11."""
        try:
            self.o.value = Octet(13)
        except Exception as ex:
            self.fail(f"Unexpected exception was raised: {ex}")
        self.assertEqual(self.o.value, 13)

    def test_octets_equal(self):
        """Test nr 12."""
        self.assertTrue(Octet(10) == Octet(10))
        self.assertFalse(Octet(10) == Octet(11))

    def test_octets_negative(self):
        """Test nr 13."""
        self.assertTrue(Octet(2) != Octet(3))
        self.assertFalse(Octet(12) != Octet(12))

    def test_octets_less(self):
        """Test nr 14."""
        self.assertTrue(Octet(193) < Octet(194))
        self.assertFalse(Octet(194) < Octet(193))

    def test_octets_less_or_equal(self):
        """Test nr 15."""
        self.assertTrue(Octet(7) <= Octet(7))
        self.assertTrue(Octet(1) <= Octet(7))
        self.assertFalse(Octet(194) <= Octet(193))

    def test_octets_qreater(self):
        """Test nr 16."""
        self.assertTrue(Octet(19) > Octet(14))
        self.assertFalse(Octet(1) > Octet(3))

    def test_octets_greater_or_equal(self):
        """Test nr 17."""
        self.assertTrue(Octet(7) >= Octet(7))
        self.assertTrue(Octet(10) >= Octet(7))
        self.assertFalse(Octet(19) >= Octet(193))


if __name__ == "__main__":
    unittest.main()


# #[EOF]#######################################################################
