# -*- coding: utf-8 -*-
"""
  test_edmctool_stars.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2024, 16:14:11
  
  Purpose: 
"""

import unittest

from typing import List
from jsktoolbox.edmctool.stars import StarsSystem


class TestStarsSystem(unittest.TestCase):
    """Tests for StarsSystem class."""

    def test_01_create(self) -> None:
        """Test creation of StarsSystem object."""
        data = StarsSystem(name="Sol", star_pos=[0, 0, 0])
        self.assertIsInstance(data, StarsSystem)
        self.assertEqual(data.name, "Sol")
        self.assertEqual(data.pos_x, 0)
        self.assertEqual(data.pos_y, 0)
        self.assertEqual(data.pos_z, 0)
        self.assertEqual(data.star_pos, [0, 0, 0])
        self.assertIsInstance(data.star_pos, List)


# #[EOF]#######################################################################
