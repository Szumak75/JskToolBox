# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 01.09.2023

Purpose: for testing DData class
"""

import unittest
from typing import Dict, List, Optional, Any
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
        # Test deprecated parameter warning - pass as keyword argument
        with self.assertWarns(DeprecationWarning):
            self.assertTrue(
                self.obj._get_data("TEST", set_default_type=Optional[str]) is None
            )

        # Set type constraint via _set_data
        self.obj._set_data("TEST", "abc", set_default_type=str)
        self.assertEqual(self.obj._get_data("TEST"), "abc")

        # Type mismatch should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data("TEST", 12)

        # Set type constraint and get with default value
        self.obj._set_data("TEST2", 10, set_default_type=int)
        self.assertTrue(self.obj._get_data("TEST2") == 10)

        # Clear TEST3 value but keep type constraint, then test default_value type check
        self.obj._set_data("TEST3", "value", set_default_type=str)
        self.obj._clear_data("TEST3")
        with self.assertRaises(TypeError):
            # int default for str type should raise TypeError
            self.obj._get_data("TEST3", default_value=10)

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

    def test_14_reset_type(self) -> None:
        """Test nr 14."""
        self.obj._set_data(key="test1", value=100, set_default_type=int)
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value="abc")
        # Attempting to overwrite type constraint should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value="abc", set_default_type=str)
        # Attempting to set with mismatched value and new type should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value=200, set_default_type=str)
        # Proper way: delete first, then set with new type
        try:
            self.obj._delete_data(key="test1")
            self.obj._set_data(key="test1", value="abc", set_default_type=str)
        except Exception as ex:
            self.fail(ex)

    def test_15_set_data_with_none_type(self) -> None:
        """Test nr 15: Setting data with set_default_type=None should not register type."""
        # Set value without type constraint
        self.obj._set_data(key="test1", value=100, set_default_type=None)
        self.assertEqual(self.obj._get_data("test1"), 100)

        # Should allow changing value to different type when no constraint
        try:
            self.obj._set_data(key="test1", value="abc", set_default_type=None)
            self.assertEqual(self.obj._get_data("test1"), "abc")
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

    def test_16_preserve_type_on_none(self) -> None:
        """Test nr 16: Setting set_default_type=None should preserve existing type."""
        # Register type constraint
        self.obj._set_data(key="test1", value=100, set_default_type=int)

        # Setting with None should preserve type constraint
        try:
            self.obj._set_data(key="test1", value=200, set_default_type=None)
            self.assertEqual(self.obj._get_data("test1"), 200)
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

        # Type should still be enforced
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value="abc", set_default_type=None)

    def test_17_type_constraint_same_type(self) -> None:
        """Test nr 17: Setting same type constraint should work."""
        self.obj._set_data(key="test1", value=100, set_default_type=int)

        # Setting same type should work
        try:
            self.obj._set_data(key="test1", value=200, set_default_type=int)
            self.assertEqual(self.obj._get_data("test1"), 200)
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

    def test_18_get_data_default_value_type_check(self) -> None:
        """Test nr 18: _get_data should check default_value type against registered type."""
        # Register type constraint
        self.obj._set_data(key="test1", value=100, set_default_type=int)

        # Getting non-existent key with matching default_value type should work
        result = self.obj._get_data("test2", default_value=50)
        self.assertEqual(result, 50)

        # Delete test1 to test default_value on registered but deleted key
        self.obj._delete_data("test1")

        # Re-register type
        self.obj._set_data(key="test1", value=100, set_default_type=int)
        self.obj._clear_data("test1")  # Clear value but keep type

        # Default value with correct type should work
        result = self.obj._get_data("test1", default_value=42)
        self.assertEqual(result, 42)

    def test_19_optional_type(self) -> None:
        """Test nr 19: Optional[str] type support."""
        # Set with Optional[str] type
        self.obj._set_data(key="test1", value="hello", set_default_type=Optional[str])
        self.assertEqual(self.obj._get_data("test1"), "hello")

        # None should be valid for Optional types
        try:
            self.obj._set_data(key="test1", value=None, set_default_type=None)
            self.assertIsNone(self.obj._get_data("test1"))
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

        # Non-string should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value=123, set_default_type=None)

    def test_20_dict_with_types(self) -> None:
        """Test nr 20: Dict[str, int] type support."""
        # Set with Dict[str, int] type
        test_dict = {"a": 1, "b": 2, "c": 3}
        self.obj._set_data(
            key="test1", value=test_dict, set_default_type=Dict[str, int]
        )
        self.assertEqual(self.obj._get_data("test1"), test_dict)

        # Valid dict update
        try:
            self.obj._set_data(
                key="test1", value={"x": 10, "y": 20}, set_default_type=None
            )
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

        # Invalid value type should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data(
                key="test1", value={"x": "not an int"}, set_default_type=None
            )

    def test_21_optional_list(self) -> None:
        """Test nr 21: Optional[List[str]] type support."""
        # Set with Optional[List[str]] type
        test_list = ["a", "b", "c"]
        self.obj._set_data(
            key="test1", value=test_list, set_default_type=Optional[List[str]]
        )
        self.assertEqual(self.obj._get_data("test1"), test_list)

        # None should be valid
        try:
            self.obj._set_data(key="test1", value=None, set_default_type=None)
            self.assertIsNone(self.obj._get_data("test1"))
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

        # List with wrong element type should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data(
                key="test1", value=[1, 2, 3], set_default_type=None  # ints not strings
            )

    def test_22_list_any(self) -> None:
        """Test nr 22: List[Any] type support."""
        # Set with List[Any] type - should accept any list
        self.obj._set_data(
            key="test1", value=[1, "string", 3.14, None], set_default_type=List[Any]
        )
        result = self.obj._get_data("test1")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)

        # Any list should be valid
        try:
            self.obj._set_data(
                key="test1", value=["a", {"b": 2}, [3, 4]], set_default_type=None
            )
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

        # Non-list should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data(key="test1", value="not a list", set_default_type=None)

    def test_23_nested_optional_dict(self) -> None:
        """Test nr 23: Dict[str, Optional[int]] type support."""
        # Set with Dict[str, Optional[int]]
        test_dict = {"a": 1, "b": None, "c": 3}
        self.obj._set_data(
            key="test1", value=test_dict, set_default_type=Dict[str, Optional[int]]
        )
        self.assertEqual(self.obj._get_data("test1"), test_dict)

        # Update with valid data
        try:
            self.obj._set_data(
                key="test1", value={"x": None, "y": 42}, set_default_type=None
            )
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

        # Invalid value (string instead of int/None) should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data(
                key="test1", value={"x": "not an int"}, set_default_type=None
            )

    def test_24_default_value_with_optional_type(self) -> None:
        """Test nr 24: default_value validation with Optional types."""
        # Register Optional[str] type
        self.obj._set_data(key="test1", value="hello", set_default_type=Optional[str])
        self.obj._clear_data("test1")

        # None default should work for Optional
        result = self.obj._get_data("test1", default_value=None)
        self.assertIsNone(result)

        # String default should work for Optional[str]
        result = self.obj._get_data("test1", default_value="default")
        self.assertEqual(result, "default")

        # Invalid type default should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._get_data("test1", default_value=123)

    def test_25_list_of_dicts(self) -> None:
        """Test nr 25: List[Dict[str, int]] type support."""
        # Set with complex nested type
        test_data = [{"a": 1}, {"b": 2, "c": 3}]
        self.obj._set_data(
            key="test1", value=test_data, set_default_type=List[Dict[str, int]]
        )
        self.assertEqual(self.obj._get_data("test1"), test_data)

        # Update with valid data
        try:
            self.obj._set_data(key="test1", value=[{"x": 10}], set_default_type=None)
        except Exception as ex:
            self.fail(f"Unexpected exception: {ex}")

        # Invalid nested structure should raise TypeError
        with self.assertRaises(TypeError):
            self.obj._set_data(
                key="test1", value=[{"x": "not an int"}], set_default_type=None
            )


# #[EOF]#######################################################################
