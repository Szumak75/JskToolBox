# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 30.10.2023

Purpose:
"""

import unittest
from jsktoolbox.configtool.libs.data import SectionModel, VariableModel


class TestDataModel(unittest.TestCase):
    """Test for Data Model classes."""

    def test_01_create_object(self) -> None:
        """Test nr 01."""
        obj = None
        try:
            obj = SectionModel()
            obj.parser("[TEST]\n")
        except Exception as ex:
            self.fail(msg=f"{ex}\n{obj}")
        try:
            obj = VariableModel()
        except Exception as ex:
            self.fail(msg=f"{ex}\n{obj}")

    def test_02_SectionModel_creation_error(self) -> None:
        """Test nr 02."""
        with self.assertRaises(ValueError):
            SectionModel("")
        with self.assertRaises(ValueError):
            SectionModel("[]\n")
        with self.assertRaises(ValueError):
            obj = SectionModel()
            obj.name = " [] \n"

    def test_03_name_check(self) -> None:
        """Test nr 03."""
        src = "[TEST]\n"
        expectation = "TEST"
        obj = SectionModel(src)
        self.assertEqual(obj.name, expectation)

    def test_04_search(self) -> None:
        """Test nr 04."""
        src = "[TEST]"
        name = "TEST"
        obj = SectionModel(src)
        self.assertTrue(obj.search(name))


# #[EOF]#######################################################################
