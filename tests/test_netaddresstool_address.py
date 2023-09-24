# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 23.06.2023

  Purpose: Testing IPv4 Address class.
"""

import unittest
from jsktoolbox.netaddresstool.ipv4 import Address
from jsktoolbox.netaddresstool.libs.octets import Octet


class TestAddress(unittest.TestCase):
    """Testing Address Class."""

    def setUp(self):
        """Configure the test engine."""
        self.o = Address("192.168.1.1")

    def test_01_address_string(self):
        """Test nr 1."""
        self.assertEqual(str(self.o), "192.168.1.1")

    def test_02_address_octets(self):
        """Test nr 2."""
        self.assertEqual(len(self.o.octets), 4)

    def test_03_set_from_list_of_integers(self):
        """Test nr 3."""
        self.o.octets = [192, 168, 2, 4]
        self.assertEqual(str(self.o), "192.168.2.4")

    def test_04_set_from_list_of_strings(self):
        """Test nr 4."""
        self.o.octets = ["192", "168", "7", "19"]
        self.assertEqual(str(self.o), "192.168.7.19")

    def test_05_set_from_list_of_octets(self):
        """Test nr 5."""
        self.o.octets = [Octet(192), Octet(168), Octet(2), Octet(4)]
        self.assertEqual(str(self.o), "192.168.2.4")

    def test_06_set_from_int(self):
        """Test nr 6."""
        self.o.octets = 167837700
        self.assertEqual(str(self.o), "10.1.0.4")

    def test_07_set_from_str(self):
        """Test nr 7."""
        self.o.octets = "10.1.1.7"
        self.assertEqual(str(self.o), "10.1.1.7")

    def test_08_address_equal(self):
        """Test nr 8."""
        self.assertTrue(Address("192.168.1.1") == Address("192.168.1.1"))
        self.assertFalse(Address("10.1.1.12") == Address("18.19.20.21"))

    def test_09_address_negative(self):
        """Test nr 9."""
        self.assertTrue(Address("192.168.1.1") != Address("192.168.1.2"))
        self.assertFalse(Address("10.1.1.2") != Address("10.1.1.2"))

    def test_10_address_less(self):
        """Test nr 10."""
        self.assertTrue(Address("192.168.1.2") < Address("192.168.1.3"))
        self.assertTrue(Address("191.168.1.2") < Address("192.168.1.2"))
        self.assertTrue(Address("192.167.1.2") < Address("192.168.1.2"))
        self.assertTrue(Address("192.168.0.2") < Address("192.168.1.2"))
        self.assertFalse(Address("192.168.1.2") < Address("192.168.1.1"))
        self.assertFalse(Address("192.168.1.2") < Address("191.168.1.2"))
        self.assertFalse(Address("192.168.1.2") < Address("192.167.1.2"))
        self.assertFalse(Address("192.168.1.2") < Address("192.168.0.2"))

    def test_11_address_less_or_equal(self):
        """Test nr 11."""
        self.assertTrue(Address("192.168.1.2") <= Address("192.168.1.3"))
        self.assertTrue(Address("192.168.1.2") <= Address("192.168.1.2"))
        self.assertTrue(Address("191.168.1.2") <= Address("192.168.1.2"))
        self.assertTrue(Address("191.168.1.2") <= Address("191.168.1.2"))
        self.assertTrue(Address("192.167.1.2") <= Address("192.168.1.2"))
        self.assertTrue(Address("192.167.1.2") <= Address("192.167.1.2"))
        self.assertTrue(Address("192.168.0.2") <= Address("192.168.1.2"))
        self.assertTrue(Address("192.168.0.2") <= Address("192.168.0.2"))
        self.assertFalse(Address("192.168.1.2") <= Address("192.168.1.1"))
        self.assertFalse(Address("192.168.1.2") <= Address("191.168.1.2"))
        self.assertFalse(Address("192.168.1.2") <= Address("192.167.1.2"))
        self.assertFalse(Address("192.168.1.2") <= Address("192.168.0.2"))

    def test_12_address_greater(self):
        """Test nr 12."""
        self.assertFalse(Address("192.168.1.2") > Address("192.168.1.3"))
        self.assertFalse(Address("191.168.1.2") > Address("192.168.1.2"))
        self.assertFalse(Address("192.167.1.2") > Address("192.168.1.2"))
        self.assertFalse(Address("192.168.0.2") > Address("192.168.1.2"))
        self.assertTrue(Address("192.168.1.2") > Address("192.168.1.1"))
        self.assertTrue(Address("192.168.1.2") > Address("191.168.1.2"))
        self.assertTrue(Address("192.168.1.2") > Address("192.167.1.2"))
        self.assertTrue(Address("192.168.1.2") > Address("192.168.0.2"))

    def test_13_address_greater_or_equal(self):
        """Test nr 13."""
        self.assertFalse(Address("192.168.1.2") >= Address("192.168.1.3"))
        self.assertFalse(Address("191.168.1.2") >= Address("192.168.1.2"))
        self.assertFalse(Address("192.167.1.2") >= Address("192.168.1.2"))
        self.assertFalse(Address("192.168.0.2") >= Address("192.168.1.2"))
        self.assertTrue(Address("192.168.1.2") >= Address("192.168.1.1"))
        self.assertTrue(Address("192.168.1.2") >= Address("191.168.1.2"))
        self.assertTrue(Address("192.168.1.2") >= Address("192.167.1.2"))
        self.assertTrue(Address("192.168.1.2") >= Address("192.168.0.2"))
        self.assertTrue(Address("192.168.1.2") >= Address("192.168.1.2"))
        self.assertTrue(Address("191.168.1.2") >= Address("191.168.1.2"))
        self.assertTrue(Address("192.167.1.2") >= Address("192.167.1.2"))
        self.assertTrue(Address("192.168.0.2") >= Address("192.168.0.2"))

    def test_14_invalid_address(self):
        """Test nr 14."""
        with self.assertRaises(ValueError):
            Address("192.168.3.4.5")

        with self.assertRaises(ValueError):
            Address("192.168.3")


if __name__ == "__main__":
    unittest.main()


# #[EOF]#######################################################################
