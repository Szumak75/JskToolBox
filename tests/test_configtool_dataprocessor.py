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


# #[EOF]#######################################################################
