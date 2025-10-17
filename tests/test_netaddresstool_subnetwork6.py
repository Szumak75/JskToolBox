# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 30.06.2023

Purpose: Testing SubNetwork calculator.
"""

import unittest

from jsktoolbox.netaddresstool import Network6, Prefix6, SubNetwork6


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
        subnets = SubNetwork6(Network6("fd00::1/125"), Prefix6(128))
        self.assertEqual(len(list(subnets.iter_subnets())), 8)

    def test_03_sub_network_validate_ranges(self) -> None:
        """Test nr 3."""
        subnets = list(SubNetwork6(Network6("fd00::/124"), Prefix6(126)).iter_subnets())
        self.assertEqual(str(subnets[0]), "fd00::/126")
        self.assertEqual(str(subnets[-1]), "fd00::c/126")
        self.assertTrue(all(subnet.prefix == Prefix6(126) for subnet in subnets))

    def test_04_sub_network_invalid_prefix(self) -> None:
        """Test nr 4."""
        with self.assertRaises(ValueError):
            SubNetwork6(Network6("fd00::/120"), Prefix6(112))

    def test_05_sub_network_deprecated_warning(self) -> None:
        """Test nr 5."""
        subnets = SubNetwork6(Network6("fd00::/125"), Prefix6(128))
        with self.assertWarns(DeprecationWarning):
            result = subnets.subnets()
        self.assertEqual(len(result), 8)

    def test_06_iter_subnets_no_limit(self) -> None:
        """Test nr 6."""
        iterator = SubNetwork6(Network6("fd00::/124"), Prefix6(126)).iter_subnets(
            limit=None
        )
        first = next(iterator)
        self.assertEqual(str(first), "fd00::/126")


# #[EOF]#######################################################################
