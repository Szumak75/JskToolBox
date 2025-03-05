# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 30.06.2023

Purpose: Testing SubNetwork calculator.
"""

import unittest

from jsktoolbox.netaddresstool.ipv4 import Network, Netmask, SubNetwork


class TestSubNetwork(unittest.TestCase):
    """Class for testing SubNetwork calculator."""

    def test_01_sub_network_create(self) -> None:
        """Test nr 1."""
        try:
            SubNetwork(Network("192.168.1.1/24"), Netmask(30))
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_02_sub_network_list_count(self) -> None:
        """Test nr 2."""
        self.assertEqual(
            len(SubNetwork(Network("192.168.1.1/24"), Netmask(30)).subnets),
            64,
        )


# #[EOF]#######################################################################
