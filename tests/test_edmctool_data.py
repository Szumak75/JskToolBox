# -*- coding: utf-8 -*-
"""
  test_edmctool_data.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2024, 16:02:38
  
  Purpose: 
"""

import unittest

from jsktoolbox.edmctool.stars import StarsSystem
from jsktoolbox.edmctool.data import RscanData


class TestRscanData(unittest.TestCase):
    """Tests for RscanData class."""

    def test_01_create(self) -> None:
        """Test creation of RscanData object."""
        data = RscanData()
        self.assertIsInstance(data, RscanData)
        self.assertIsInstance(data.stars_system, StarsSystem)
        self.assertIsInstance(data.jump_system, StarsSystem)


# #[EOF]#######################################################################
