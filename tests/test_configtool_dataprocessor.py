# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 29.10.2023

Purpose:
"""

import unittest
from jsktoolbox.configtool.libs.data import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Tests for DataProcessor class."""

    def setUp(self) -> None:
        """Set up test."""
        try:
            self.dp = DataProcessor()
        except Exception as ex:
            self.fail(ex)

    def test_01_add_section(self) -> None:
        """Test nr 01."""
        try:
            self.dp.main_section = "TEST"
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")

    def test_02_get_sections_tuple(self) -> None:
        """Test nr 02."""
        self.dp.main_section = "TEST"
        test = tuple(["TEST"])
        self.assertEqual(self.dp.sections, test)

    def test_03_add_section(self) -> None:
        """Test nr 03."""
        self.dp.main_section = "TEST"
        try:
            self.dp.add_section("S1")
            self.dp.add_section("S2")
            self.dp.add_section("S3")
            self.dp.add_section("S4")
            self.dp.add_section("S1")
            self.dp.add_section("S2")
            self.dp.add_section("S3")
            self.dp.add_section("S4")
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")

        test = tuple(sorted(["TEST", "S1", "S2", "S3", "S4"]))
        self.assertEqual(self.dp.sections, test, msg=f"{self.dp._data}")

    def test_04_add_value_to_section(self) -> None:
        """Test nr 04."""
        self.dp.main_section = "TEST"
        try:
            self.dp.set(section="TEST", varname="var01", value="To jest test 1")
            self.dp.set(
                section="TEST",
                varname="var02",
                value="To jest test 2",
                desc="comment",
            )
            self.dp.set(section="TEST", varname="var01", value="To jest test 3")
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")
        # self.fail(msg=f"{self.dp._data}")

    def test_05_add_section_comment(self) -> None:
        """Test nr 05."""
        self.dp.main_section = "TEST"
        try:
            self.dp.set(section="TEST", desc="To jest test")
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")
        # self.fail(msg=f"{self.dp._data}")

    def test_06_get_value(self) -> None:
        """Test nr 06."""
        self.dp.main_section = "TEST"
        try:
            self.dp.set(section="TEST", varname="var01", value=1)
            self.dp.set(section="TEST", varname="var02", value=2, desc="comment")
            self.dp.set(section="TEST", varname="var01", value=3)
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")

        try:
            value = self.dp.get(section="TEST", varname="var01")
            self.assertEqual(value, 3)
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")

    def test_07_get_description(self) -> None:
        """Test nr 07."""
        self.dp.main_section = "TEST"
        try:
            self.dp.set(section="TEST", desc="Example comment for section TEST.")
            self.dp.set(section="TEST", desc="Second line comment.")
            self.dp.set(section="TEST", varname="var01", value=1, desc="comment 01")
            self.dp.set(section="TEST", varname="var02", value=2, desc="comment 02")
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")

        try:
            value = self.dp.get(section="TEST", varname="var01", desc=True)
            self.assertEqual(value, "comment 01")
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")

        try:
            value = self.dp.get(section="TEST", desc=True)
            self.assertEqual(
                value,
                [
                    "Example comment for section TEST.",
                    "Second line comment.",
                ],
            )
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")

        # self.fail(msg=f"dump:{self.dp._data}")
        # self.fail(msg=f"dump:{value}")

    def test_08_dump_data(self) -> None:
        """Test nr 08."""
        expectation = """[TEST]
# Example comment for section TEST.
# Second line comment.
var01 = 1
var02 = 2 # comment 02
# -----<end of section: 'TEST'>-----
[TEST2]
var01 = 1
var02 = 2 # comment 02
# -----<end of section: 'TEST2'>-----
"""
        self.dp.main_section = "TEST"
        try:
            self.dp.set(section="TEST", desc="Example comment for section TEST.")
            self.dp.set(section="TEST", desc="Second line comment.")
            self.dp.set(section="TEST", varname="var01", value=1)
            self.dp.set(section="TEST", varname="var02", value=2, desc="comment 02")
            self.dp.add_section("TEST2")
            self.dp.set(section="TEST2", varname="var01", value=1)
            self.dp.set(section="TEST2", varname="var02", value=2, desc="comment 02")
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{self.dp._data}")

        data: str = ""
        try:
            data = self.dp.dump
            self.assertEqual(data, expectation)
        except Exception as ex:
            self.fail(msg=f"{ex}\ndump:{data}")

    def test_09_set_without_name_raises(self) -> None:
        """Test nr 09."""
        self.dp.main_section = "TEST"
        with self.assertRaisesRegex(ValueError, "Variable name is required"):
            self.dp.set(section="TEST", varname=None, value="value")

    def test_10_dump_without_main_section_raises(self) -> None:
        """Test nr 10."""
        with self.assertRaisesRegex(KeyError, "Main section is not set"):
            _ = self.dp.dump

    def test_11_get_missing_section_raises(self) -> None:
        """Test nr 11."""
        self.dp.main_section = "TEST"
        with self.assertRaisesRegex(KeyError, "Given section name: 'OTHER' not found"):
            self.dp.get("OTHER")

    def test_12_get_missing_variable_returns_none(self) -> None:
        """Test nr 12."""
        self.dp.main_section = "TEST"
        self.dp.set(section="TEST", varname="var01", value="value")
        self.assertIsNone(self.dp.get("TEST", "missing"))
        self.assertIsNone(self.dp.get("TEST", "missing", desc=True))

    def test_13_main_section_converts_non_string_values(self) -> None:
        """Test nr 13."""
        self.dp.main_section = 123  # type: ignore[assignment]
        self.assertEqual(self.dp.main_section, "123")
        self.assertIn("123", self.dp.sections)

    def test_14_add_section_and_get_section_sanitize_name(self) -> None:
        """Test nr 14."""
        section_name = self.dp.add_section(" [TEST2]\n")
        self.assertEqual(section_name, "TEST2")
        found = self.dp.get_section("TEST2")
        self.assertIsNotNone(found)
        assert found is not None
        self.assertEqual(found.name, "TEST2")

    def test_15_get_section_returns_none_for_missing_entry(self) -> None:
        """Test nr 15."""
        self.dp.main_section = "TEST"
        self.assertIsNone(self.dp.get_section("MISSING"))

    def test_16_set_updates_existing_variable_description_only(self) -> None:
        """Test nr 16."""
        self.dp.main_section = "TEST"
        self.dp.set(section="TEST", varname="var01", value="value", desc="desc01")
        self.dp.set(section="TEST", varname="var01", desc="desc02")
        self.assertEqual(self.dp.get("TEST", "var01"), "value")
        self.assertEqual(self.dp.get("TEST", "var01", desc=True), "desc02")

    def test_17_set_clears_existing_value_and_description(self) -> None:
        """Test nr 17."""
        self.dp.main_section = "TEST"
        self.dp.set(section="TEST", varname="var01", value="value", desc="desc01")
        self.dp.set(section="TEST", varname="var01", value=None, desc=None)
        self.assertIsNone(self.dp.get("TEST", "var01"))
        self.assertIsNone(self.dp.get("TEST", "var01", desc=True))

    def test_18_data_processor_typed_storage(self) -> None:
        """Test nr 18."""
        self.assertEqual(self.dp.sections, tuple())
        self.assertIsNone(self.dp.main_section)
        with self.assertRaises(TypeError):
            self.dp._set_data(key="__data__", value=["invalid"])  # type: ignore[list-item]

        self.dp.main_section = "TEST"
        self.dp.add_section("NEXT")
        self.assertEqual(self.dp.sections, ("NEXT", "TEST"))


# #[EOF]#######################################################################
