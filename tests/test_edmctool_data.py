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

    def test_02_jump_system_default_persistence(self) -> None:
        """Setter should replace None with fresh StarsSystem instance."""
        data = RscanData()
        default_ref = data.jump_system
        data.jump_system = None
        self.assertIsNot(data.jump_system, None)
        self.assertIsInstance(data.jump_system, StarsSystem)
        self.assertIsNot(
            data.jump_system,
            default_ref,
            msg="None setter should allocate new object",
        )

    def test_03_stars_system_default_persistence(self) -> None:
        """Setter should replace None with fresh StarsSystem instance."""
        data = RscanData()
        default_ref = data.stars_system
        data.stars_system = None
        self.assertIsNot(data.stars_system, None)
        self.assertIsInstance(data.stars_system, StarsSystem)
        self.assertIsNot(
            data.stars_system,
            default_ref,
            msg="None setter should allocate new object",
        )

    def test_04_custom_assignment_preserved(self) -> None:
        """Setters must keep explicit StarsSystem instances."""
        data = RscanData()
        custom_jump = StarsSystem(name="Jump Target")
        custom_main = StarsSystem(name="Current System")
        data.jump_system = custom_jump
        data.stars_system = custom_main
        self.assertIs(data.jump_system, custom_jump)
        self.assertIs(data.stars_system, custom_main)


# #[EOF]#######################################################################
