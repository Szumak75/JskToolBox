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
        self.assertEqual(
            str(Network("192.168.1.1/24").address), "192.168.1.1"
        )

    def test_05_network_broadcast(self) -> None:
        """Test nr 5."""
        self.assertEqual(
            str(Network("192.168.1.1/24").broadcast), "192.168.1.255"
        )

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
        self.assertEqual(
            str(Network("192.168.1.1/24").network), "192.168.1.0"
        )

    def test_10_network_hosts(self) -> None:
        """Test nr 10."""
        self.assertEqual(
            len(Network("192.168.1.1/24").hosts),
            Network("192.168.1.1/24").count,
        )
        for idx in range(0, Network("192.168.1.1/24").count):
            self.assertTrue(
                Network("192.168.1.1/24").hosts[idx]
                == Address(f"192.168.1.{idx + 1}")
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


# #[EOF]#######################################################################
