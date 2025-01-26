# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 01.09.2023

  Purpose: for testing DData class
"""

import unittest
from typing import Dict, List, Optional
from jsktoolbox.basetool.data import BData


class TestBData(unittest.TestCase):
    """Testing BData container class."""

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
        with self.assertRaises(TypeError):
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

    def test_09_reset_dict_with_different_types(self) -> None:
        """Test nr 9."""
        self.obj._set_data("test1", 12, int)
        with self.assertRaises(TypeError):
            self.obj._data = {"test1": "12"}

    def test_10_reset_dict_with_compatible_types(self) -> None:
        """Test nr 10."""
        self.obj._set_data("test1", 123, int)
        self.obj._set_data("test2", "xxx", str)
        try:
            self.obj._data = {"test1": 90, "test2": "aaa"}
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

    def test_11_set_list(self) -> None:
        """Test nr 11."""
        # first set
        self.obj._set_data(key="test1", value=[1, 2, 3], set_default_type=List)
        obj = self.obj._get_data(key="test1")
        if isinstance(obj, List):
            self.assertTrue(obj[0] == 1)
        else:
            self.fail(msg="Type error.")
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value=10)
        # second set
        self.obj._set_data(key="test1", value=[4, 5, 6])
        obj = self.obj._get_data(key="test1")
        if isinstance(obj, List):
            self.assertTrue(obj[0] == 4)
        else:
            self.fail(msg="Type error.")

    def test_12_set_dict(self) -> None:
        """Test nr 12."""
        # first set
        self.obj._set_data(
            key="test1", value={"a": 1, "b": 2, "c": 3}, set_default_type=Dict
        )
        obj = self.obj._get_data(key="test1")
        if isinstance(obj, Dict):
            self.assertTrue(obj["a"] == 1)
        else:
            self.fail(msg="Type error.")
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value=10)
        # second set
        self.obj._set_data(key="test1", value={"a": 4, "b": 5, "c": 6})
        obj = self.obj._get_data(key="test1")
        if isinstance(obj, Dict):
            self.assertTrue(obj["a"] == 4)
        else:
            self.fail(msg="Type error.")

    def test_13_del_data(self) -> None:
        """Test nr 13."""
        self.obj._set_data(key="test2", value=12.1, set_default_type=float)
        self.obj._set_data(key="test1", value=12, set_default_type=int)
        self.assertTrue(self.obj._get_data(key="test1") == 12)
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value="abc")
        self.obj._delete_data(key="test1")
        self.assertIsNone(self.obj._get_data(key="test1"))
        self.assertEqual(len(self.obj._data.keys()), 1)
        try:
            self.obj._set_data(key="test1", value="xxx")
        except Exception as ex:
            self.fail(ex)
        del self.obj._data
        self.assertTrue(isinstance(self.obj._data, Dict))
        self.assertEqual(len(self.obj._data.keys()), 0)


# #[EOF]#######################################################################
