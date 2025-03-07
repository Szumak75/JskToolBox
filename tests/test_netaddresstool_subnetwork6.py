# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 30.06.2023

Purpose: Testing SubNetwork calculator.
"""

import unittest

from jsktoolbox.netaddresstool.ipv6 import Network6, Prefix6, SubNetwork6


class TestSubNetwork6(unittest.TestCase):
    """Class for testing SubNetwork6 calculator."""

    def test_01_sub_network_create(self) -> None:
        """Test nr 1."""
        try:
            SubNetwork6(Network6("fd00::1/125"), Prefix6(128))
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_02_sub_network_list_count(self) -> None:
        """Test nr 2."""
        self.assertEqual(
            len(SubNetwork6(Network6("fd00::1/125"), Prefix6(128)).subnets),
            8,
        )


# #[EOF]#######################################################################
