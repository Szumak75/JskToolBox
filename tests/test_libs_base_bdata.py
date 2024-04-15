# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 01.09.2023

  Purpose: for testing DData class
"""

import unittest
from typing import Dict, Optional
from jsktoolbox.libs.base_data import BData


class TestDData(unittest.TestCase):
    """Testing DData container class."""

    def setUp(self) -> None:
        """Set up."""
        try:
            self.obj = BData()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_01_obj_instance(self) -> None:
        """Test nr 1."""
        self.assertIsInstance(self.obj, BData)

    def test_02_return_dict(self) -> None:
        """Test nr 2."""
        self.assertIsInstance(self.obj._data, Dict)

    def test_03_set_dict_key_and_return_it(self) -> None:
        """Test nr 3."""
        self.obj._data["test"] = 1
        self.assertTrue("test" in self.obj._data)
        try:
            self.assertEqual(self.obj._data["test"], 1)
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_04_cleanup_dict(self) -> None:
        """Test nr 4."""
        self.obj._data["test"] = 2
        self.obj._data = None
        self.test_01_obj_instance()

    def test_05_set_attributes(self) -> None:
        """Test nr 5."""
        try:
            self.obj.test = 1
        except AttributeError:
            return
        self.fail("Exception wasn't throw.")

    def test_06_set_dict_from_dict(self) -> None:
        """Test nr 6."""
        self.obj._data["test1"] = 1
        self.obj._data = {
            "test2": 2,
            "test3": 3,
        }
        self.assertTrue(len(self.obj._data.keys()) == 3)
        self.assertTrue("test1" in self.obj._data)
        self.assertTrue("test2" in self.obj._data)
        self.assertTrue("test3" in self.obj._data)
        self.obj._data["test3"] = 4
        self.assertTrue(self.obj._data["test1"] == 1)
        self.assertTrue(self.obj._data["test2"] == 2)
        self.assertTrue(self.obj._data["test3"] == 4)

    def test_07_set_invalid_type(self) -> None:
        """Test nr 7."""
        with self.assertRaises(AttributeError):
            self.obj._data = 1  # type: ignore

    def test_08_get_and_set_method(self) -> None:
        """Test nr 8."""
        self.assertTrue(self.obj._get_data("TEST", Optional[str]) is None)
        self.obj._set_data("TEST", "abc")
        self.assertEqual(self.obj._get_data("TEST"), "abc")
        with self.assertRaises(TypeError):
            self.obj._set_data("TEST", 12)
        self.assertTrue(self.obj._get_data("TEST2", int, 10) == 10)
        with self.assertRaises(TypeError):
            self.obj._get_data("TEST3", str, 10)


# #[EOF]#######################################################################
