# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 27.06.2023

Purpose: Network class testing.
"""

import unittest

from jsktoolbox.netaddresstool.ipv4 import Network, Address, Netmask


class TestNetwork(unittest.TestCase):
    """Class rof testing IPv4 Network."""

    def test_01_network_create(self) -> None:
        """Test nr 1."""
        try:
            Network("192.168.1.1/24")
            Network("192.168.17.18/255.255.255.248")
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

    def test_02_network(self) -> None:
        """Test nr 2."""
        self.assertEqual(str(Network("192.168.1.1/24")), "192.168.1.0/24")

    def test_03_network_mask(self) -> None:
        """Test nr 3."""
        self.assertEqual(int(Network("192.168.1.1/24").mask), 24)

    def test_04_network_address(self) -> None:
        """Test nr 4."""
        self.assertEqual(str(Network("192.168.1.1/24").address), "192.168.1.1")

    def test_05_network_broadcast(self) -> None:
        """Test nr 5."""
        self.assertEqual(str(Network("192.168.1.1/24").broadcast), "192.168.1.255")

    def test_06_network_min_host(self) -> None:
        """Test nr 6."""
        self.assertEqual(str(Network("192.168.1.1/24").min), "192.168.1.1")

    def test_07_network_max_host(self) -> None:
        """Test nr 7."""
        self.assertEqual(str(Network("192.168.1.1/24").max), "192.168.1.254")

    def test_08_network_count(self) -> None:
        """Test nr 8."""
        self.assertEqual(Network("192.168.1.1/24").count, 254)

    def test_09_network_network(self) -> None:
        """Test nr 9."""
        self.assertEqual(str(Network("192.168.1.1/24").network), "192.168.1.0")

    def test_10_network_hosts(self) -> None:
        """Test nr 10."""
        self.assertEqual(
            len(Network("192.168.1.1/24").hosts),
            Network("192.168.1.1/24").count,
        )
        for idx in range(0, Network("192.168.1.1/24").count):
            self.assertTrue(
                Network("192.168.1.1/24").hosts[idx] == Address(f"192.168.1.{idx + 1}")
            )
        self.assertEqual(
            len(Network("192.168.1.1/31").hosts),
            Network("192.168.1.1/31").count,
        )

    def test_11_network_create_from_list(self) -> None:
        """Test nr 11."""
        try:
            Network(["192.168.18.37", "30"])
            Network(["192.168.74.98", "255.255.255.248"])
            Network([Address("192.168.1.1"), Netmask(24)])
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

    def test_12_address_in_network(self) -> None:
        """Test nr 12."""
        self.assertTrue(Address("192.168.0.12") in Network("192.168.0.0/24").hosts)

    def test_13_network_create_invalid_string(self) -> None:
        """Test nr 13."""
        with self.assertRaises(ValueError):
            Network("192.168.1.1")  # missing mask

    def test_14_network_create_invalid_list_length(self) -> None:
        """Test nr 14."""
        with self.assertRaises(ValueError):
            Network(["192.168.1.1"])  # type: ignore

    def test_15_network_contains_address(self) -> None:
        """Test nr 15."""
        network = Network("10.0.0.0/30")
        self.assertTrue(Address("10.0.0.1") in network.hosts)
        self.assertFalse(Address("10.0.0.4") in network.hosts)

    def test_16_network_min_max_small_subnet(self) -> None:
        """Test nr 16."""
        network = Network("10.0.0.0/31")
        self.assertEqual(str(network.min), "10.0.0.0")
        self.assertEqual(str(network.max), "10.0.0.1")


# #[EOF]#######################################################################
