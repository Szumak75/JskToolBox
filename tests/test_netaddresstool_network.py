# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 27.06.2023

Purpose: Network class testing.
"""

import unittest

from jsktoolbox.netaddresstool.ipv4 import (
    Network,
    Address,
    Netmask,
    SubNetwork,
)


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
        network = Network("192.168.1.1/24")
        hosts = list(network.iter_hosts())
        self.assertEqual(len(hosts), network.count)
        for idx, host in enumerate(hosts, start=1):
            self.assertEqual(host, Address(f"192.168.1.{idx}"))
        small_network = Network("192.168.1.1/31")
        self.assertEqual(len(list(small_network.iter_hosts())), small_network.count)

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
        self.assertIn(
            Address("192.168.0.12"),
            list(Network("192.168.0.0/24").iter_hosts()),
        )

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
        hosts = list(network.iter_hosts())
        self.assertIn(Address("10.0.0.1"), hosts)
        self.assertNotIn(Address("10.0.0.4"), hosts)

    def test_16_network_min_max_small_subnet(self) -> None:
        """Test nr 16."""
        network = Network("10.0.0.0/31")
        self.assertEqual(str(network.min), "10.0.0.0")
        self.assertEqual(str(network.max), "10.0.0.1")

    def test_17_iter_hosts_limit_enforced(self) -> None:
        """Test nr 17."""
        network = Network("192.168.1.1/24")
        with self.assertRaises(ValueError):
            list(network.iter_hosts(limit=10))

    def test_18_hosts_deprecated_warning(self) -> None:
        """Test nr 18."""
        network = Network("10.0.0.0/30")
        with self.assertWarns(DeprecationWarning):
            result = network.hosts()
        self.assertEqual(len(result), network.count)

    def test_19_iter_subnets_limit_enforced(self) -> None:
        """Test nr 19."""
        subnets = SubNetwork(Network("10.0.0.0/24"), Netmask(28))
        with self.assertRaises(ValueError):
            list(subnets.iter_subnets(limit=2))

    def test_20_iter_subnets_yields_all(self) -> None:
        """Test nr 20."""
        subnets = SubNetwork(Network("10.0.0.0/24"), Netmask(26))
        generated = list(subnets.iter_subnets())
        self.assertEqual(len(generated), 4)
        self.assertEqual(str(generated[0]), "10.0.0.0/26")
        self.assertEqual(str(generated[-1]), "10.0.0.192/26")

    def test_21_iter_hosts_no_limit(self) -> None:
        """Test nr 21."""
        network = Network("10.0.0.0/16")
        iterator = network.iter_hosts(limit=None)
        self.assertEqual(next(iterator), Address("10.0.0.1"))

    def test_22_iter_subnets_no_limit(self) -> None:
        """Test nr 22."""
        subnets = SubNetwork(Network("10.0.0.0/24"), Netmask(27))
        iterator = subnets.iter_subnets(limit=None)
        first = next(iterator)
        self.assertEqual(str(first), "10.0.0.0/27")


# #[EOF]#######################################################################
