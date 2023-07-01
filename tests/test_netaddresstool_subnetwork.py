#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 30.06.2023

  Purpose: Testing SubNetwork calculator.
"""

import unittest

from toolbox.netaddresstool.ipv4 import Network, Netmask, SubNetwork


class TestSubNetwork(unittest.TestCase):
    """Class for testing SubNetwork calculator."""

    def test_subnetwork_creare(self):
        """Test nr 1."""
        try:
            SubNetwork(Network("192.168.1.1/24"), Netmask(30))
        except Exception as ex:
            self.fail(f"Unexpected exception was throw: '{ex}'")

    def test_subnetwork_list_count(self):
        """Test nr 2."""
        self.assertEqual(
            len(SubNetwork(Network("192.168.1.1/24"), Netmask(30)).subnets),
            64,
        )


if __name__ == "__main__":
    unittest.main()


# #[EOF]#######################################################################
