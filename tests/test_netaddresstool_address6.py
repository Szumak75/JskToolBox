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

    def setUp(self):
        """Configure the test engine."""
        self.o = Address6("1111:2222:3333:4444:5555:6666:7777:8888")

    def test_address_string(self):
        """Test nr 1."""
        self.assertEqual(
            str(self.o), "1111:2222:3333:4444:5555:6666:7777:8888"
        )

    def test_address_octets(self):
        """Test nr 2."""
        self.assertEqual(len(self.o.words), 8)

    def test_set_from_list_of_integers(self):
        """Test nr 3."""
        self.o.words = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(str(self.o), "1:2:3:4:5:6:7:8")


# #[EOF]#######################################################################
