# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 01.09.2023

  Purpose: for testing DData class
"""

import unittest
from typing import Dict
from jsktoolbox.libs.base_data import BData


class TestDData(unittest.TestCase):
    """Testing DData container class."""

    def setUp(self) -> None:
        """Set up."""
        try:
            self.obj = BData()
        except Exception as ex:
            self.fail(f"Unexpected exception was throw: '{ex}'")

    def test_obj_instance(self) -> None:
        """Test nr 1."""
        self.assertIsInstance(self.obj, BData)

    def test_return_dict(self) -> None:
        """Test nr 2."""
        self.assertIsInstance(self.obj.data, Dict)

    def test_set_dict_key_and_return_it(self) -> None:
        """Test nr 3."""
        self.obj.data["test"] = 1
        self.assertTrue("test" in self.obj.data)
        try:
            self.assertEqual(self.obj.data["test"], 1)
        except Exception as ex:
            self.fail(f"Unexpected exception was throw: '{ex}'")

    def test_cleanup_dict(self) -> None:
        """Test nr 4."""
        self.obj.data["test"] = 2
        self.obj.data = None
        self.test_obj_instance()

    def test_set_attributes(self) -> None:
        """Test nr 5."""
        try:
            self.obj.test = 1
        except AttributeError:
            return
        self.fail("Exception wasn't throw.")

    def test_set_dict_from_dict(self) -> None:
        """Test nr 6."""
        self.obj.data["test1"] = 1
        self.obj.data = {
            "test2": 2,
            "test3": 3,
        }
        self.assertTrue(len(self.obj.data.keys()) == 3)
        self.assertTrue("test1" in self.obj.data)
        self.assertTrue("test2" in self.obj.data)
        self.assertTrue("test3" in self.obj.data)
        self.obj.data["test3"] = 4
        self.assertTrue(self.obj.data["test1"] == 1)
        self.assertTrue(self.obj.data["test2"] == 2)
        self.assertTrue(self.obj.data["test3"] == 4)

    def test_set_invalid_type(self) -> None:
        """Test nr 7."""
        with self.assertRaises(AttributeError):
            self.obj.data = 1


# #[EOF]#######################################################################
