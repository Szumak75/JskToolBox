# -*- coding: utf-8 -*-
"""
  test_basetool.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 5.09.2024, 22:07:07
  
  Purpose: 
"""


import unittest
from typing import Optional, Any, List, Dict


class TestBaseClasses(unittest.TestCase):
    """Testing BClasses."""

    def setUp(self) -> None:
        try:
            from jsktoolbox.basetool.classes import BClasses

            class A(BClasses):
                pass

            self.obj = A()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_01_names(self) -> None:
        """Test nr 01."""

        self.assertTrue(self.obj._c_name, "A")
        self.assertTrue(self.obj._f_name, "test_01_names")


class TestBData(unittest.TestCase):
    """Testing BData base class."""

    def setUp(self) -> None:
        try:
            from jsktoolbox.basetool.data import BData

            class A(BData):
                pass

            self.obj = A()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_01_obj_instance(self) -> None:
        """Test nr 1."""
        from jsktoolbox.basetool.data import BData

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
        self.obj._set_data(key="test1", value=[1, 2, 3], set_default_type=List)
        obj = self.obj._get_data(key="test1")
        if isinstance(obj, List):
            self.assertTrue(obj[0] == 1)
        else:
            self.fail(msg="Type error.")
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value=10)

    def test_12_set_dict(self) -> None:
        """Test nr 12."""
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


# #[EOF]#######################################################################
