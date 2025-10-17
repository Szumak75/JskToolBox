# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 30.06.2023

Purpose: Testing SubNetwork calculator.
"""

import unittest

from jsktoolbox.netaddresstool import Network, Netmask, SubNetwork


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
        subnets = SubNetwork(Network("192.168.1.1/24"), Netmask(30))
        self.assertEqual(len(list(subnets.iter_subnets())), 64)

    def test_03_sub_network_validate_ranges(self) -> None:
        """Test nr 3."""
        subnets = list(SubNetwork(Network("10.0.0.0/24"), Netmask(26)).iter_subnets())
        self.assertEqual(str(subnets[0]), "10.0.0.0/26")
        self.assertEqual(str(subnets[-1]), "10.0.0.192/26")
        self.assertTrue(all(int(subnet.mask) == 26 for subnet in subnets))

    def test_04_sub_network_invalid_mask(self) -> None:
        """Test nr 4."""
        with self.assertRaises(ValueError):
            SubNetwork(Network("10.0.0.0/26"), Netmask(24))

    def test_05_sub_network_deprecated_warning(self) -> None:
        """Test nr 5."""
        subnets = SubNetwork(Network("192.168.1.0/24"), Netmask(30))
        with self.assertWarns(DeprecationWarning):
            result = subnets.subnets()
        self.assertEqual(len(result), 64)


# #[EOF]#######################################################################
