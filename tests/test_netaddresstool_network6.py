# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 27.06.2023

Purpose: Network6 class testing.

https://www.juniper.net/us/en/research-topics/what-is-ipv4-vs-ipv6.html
"""

import unittest

from jsktoolbox.netaddresstool.ipv6 import Network6, Address6, Prefix6


class TestNetwork6(unittest.TestCase):
    """Class rof testing IPv6 Network."""

    def test_01_network_create(self) -> None:
        """Test nr 1."""
        try:
            Network6("fd00::1/125")
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

    def test_02_network(self) -> None:
        """Test nr 2."""
        self.assertEqual(str(Network6("fd00::1/125")), "fd00::/125")

    def test_03_network_prefix(self) -> None:
        """Test nr 3."""
        self.assertEqual(int(Network6("fd00::1/125").prefix), 125)

    def test_04_network_address(self) -> None:
        """Test nr 4."""
        self.assertEqual(str(Network6("fd00::1/125").address), "fd00::1")

    def test_05_network_min_host(self) -> None:
        """Test nr 5."""
        self.assertEqual(str(Network6("fd00::1/125").min), "fd00::")

    def test_06_network_max_host(self) -> None:
        """Test nr 6."""
        self.assertEqual(str(Network6("fd00::1/125").max), "fd00::7")

    def test_07_network_count(self) -> None:
        """Test nr 7."""
        self.assertEqual(Network6("fd00::1/125").count, 8)

    def test_08_network_network(self) -> None:
        """Test nr 8."""
        self.assertEqual(str(Network6("fd00::1/125").network), "fd00::")

    def test_09_network_hosts(self) -> None:
        """Test nr 9."""
        self.assertEqual(
            len(Network6("fd00::1/125").hosts),
            Network6("fd00::1/125").count,
        )
        for idx in range(0, Network6("fd00::1/125").count):
            self.assertTrue(
                Network6("fd00::1/125").hosts[idx] == Address6(f"fd00::{idx}")
            )

    def test_10_network_create_from_list(self) -> None:
        """Test nr 10."""
        try:
            Network6(["fd00::1", "125"])
            Network6([336294682933583715844663186250927177729, 125])
            Network6([Address6("fd00::1"), Prefix6(125)])
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

    def test_11_network_hosts_respect_order(self) -> None:
        """Test nr 11."""
        network = Network6("fd00::/126")
        hosts = network.hosts
        self.assertEqual(hosts[0], network.min)
        self.assertEqual(hosts[-1], network.max)
        self.assertEqual(len(hosts), network.count)

    def test_12_network_create_invalid_string(self) -> None:
        """Test nr 12."""
        with self.assertRaises(ValueError):
            Network6("fd00::1")  # missing prefix

    def test_13_network_create_invalid_list_length(self) -> None:
        """Test nr 13."""
        with self.assertRaises(ValueError):
            Network6(["fd00::1"])  # type: ignore

    def test_14_network_create_invalid_types(self) -> None:
        """Test nr 14."""
        with self.assertRaises(ValueError):
            Network6([Address6("fd00::1"), "not-a-prefix"])  # type: ignore


# #[EOF]#######################################################################
