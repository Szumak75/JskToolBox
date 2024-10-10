# -*- coding: utf-8 -*-
"""
  test_edmctool_math.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2024, 16:03:19
  
  Purpose: 
"""

import unittest

from queue import SimpleQueue

from jsktoolbox.edmctool.stars import StarsSystem
from jsktoolbox.edmctool.data import RscanData
from jsktoolbox.edmctool.math import Euclid


class TestEuclid(unittest.TestCase):
    """Tests for Euclid class."""

    def test_01_create(self) -> None:
        """Test creation of Euclid object."""
        euclid = Euclid(queue=SimpleQueue(), r_data=RscanData())
        self.assertIsInstance(euclid, Euclid)

    def test_02_distance(self) -> None:
        """Test distance calculation."""
        euclid = Euclid(queue=SimpleQueue(), r_data=RscanData())
        self.assertIsNotNone(euclid.distance([0, 0, 0], [1, 1, 1]))
        self.assertGreater(euclid.distance([0, 0, 0], [1, 1, 1]), 1)

        a = euclid.distance([0, 0, 0], [1, 1, 1])
        euclid.benchmark()
        b = euclid.distance([0, 0, 0], [1, 1, 1])
        self.assertEqual(a, b)


# #[EOF]#######################################################################
