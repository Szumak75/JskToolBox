# -*- coding: utf-8 -*-
"""
test_nettool.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 29.08.2025, 09:22:47

Purpose:
"""


import unittest
from jsktoolbox.nettool import Pinger, Tracert


class TestNetTool(unittest.TestCase):
    """Testing NetTool module."""

    def setUp(self) -> None:
        """Configure the test engine."""
        self.pinger = Pinger()
        self.tracert = Tracert()

    def test_01_ping_localhost(self) -> None:
        """Test nr 1: Ping localhost."""
        result = self.pinger.is_alive("127.0.0.1")
        self.assertTrue(result)

    def test_02_tracert_localhost(self) -> None:
        """Test nr 2: Tracert localhost."""
        result = self.tracert.execute("127.0.0.1")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "")
        # Localhost tracert should return only one hop with no address.

    def test_03_ping_invalid_ip(self) -> None:
        """Test nr 3: Ping invalid IP."""
        result = self.pinger.is_alive("192.168.255.255")
        self.assertFalse(result)

    # def test_04_tracert_invalid_ip(self) -> None:
    #     """Test nr 4: Tracert invalid IP."""
    #     result = self.tracert.execute("256.256.256.256")
    #     self.assertIsInstance(result, list)
    #     self.assertEqual(len(result), 0)
    #     # Invalid IP tracert should return empty list.


# #[EOF]#######################################################################
