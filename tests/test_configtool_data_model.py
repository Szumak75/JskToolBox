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

    def test_04a_section_model_type_constraints(self) -> None:
        """Test nr 04a."""
        with self.assertRaises(TypeError):
            SectionModel(123)  # type: ignore[arg-type]

        obj = SectionModel("[TEST]")
        obj.name = None
        self.assertIsNone(obj.name)
        obj.name = " [NEXT] "
        self.assertEqual(obj.name, "NEXT")

        with self.assertRaises(TypeError):
            obj.name = 123  # type: ignore[assignment]

        with self.assertRaises(TypeError):
            obj._set_data(key="__variables__", value=["invalid"])  # type: ignore[list-item]

    def test_05_variable_model_name_validation(self) -> None:
        """Test nr 05."""
        obj = VariableModel()
        obj.name = "  example_name  "
        self.assertEqual(obj.name, "example_name")
        obj.name = None
        self.assertIsNone(obj.name)
        with self.assertRaisesRegex(ValueError, "Variable name cannot be empty"):
            obj.name = "   "

    def test_06_variable_model_parser_validation(self) -> None:
        """Test nr 06."""
        obj = VariableModel(name="var")
        obj.parser("  value  ")
        self.assertEqual(obj.value, "  value  ")
        with self.assertRaises(TypeError):
            obj.parser(123)  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "Variable value cannot be empty"):
            obj.parser("   ")

    def test_07_variable_model_string_and_repr(self) -> None:
        """Test nr 07."""
        obj = VariableModel(name="name", value=" 'value' ", desc="comment")
        self.assertEqual(str(obj), 'name = "value" # comment')
        self.assertEqual(
            repr(obj),
            "VariableModel(name='name', value=' 'value' ', desc='comment')",
        )

        obj.value = [1, "two", False]
        self.assertEqual(str(obj), "name = [1, 'two', False] # comment")

        obj = VariableModel(desc="section comment")
        self.assertEqual(str(obj), "# section comment")

    def test_08_variable_model_dump_and_search(self) -> None:
        """Test nr 08."""
        obj = VariableModel(name="name", value=7, desc="comment")
        self.assertIs(obj.dump, obj)
        self.assertTrue(obj.search("name"))
        self.assertFalse(obj.search("other"))

    def test_09_variable_model_type_constraints(self) -> None:
        """Test nr 09."""
        with self.assertRaises(TypeError):
            VariableModel(name=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            VariableModel(value={"a": 1})  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            VariableModel(desc=1)  # type: ignore[arg-type]

        obj = VariableModel(name="name", value="value", desc="comment")
        with self.assertRaises(TypeError):
            obj.name = 1  # type: ignore[assignment]
        with self.assertRaises(TypeError):
            obj.value = {"a": 1}  # type: ignore[assignment]
        with self.assertRaises(TypeError):
            obj.desc = 1  # type: ignore[assignment]

    def test_10_section_model_variable_operations(self) -> None:
        """Test nr 10."""
        obj = SectionModel(" [TEST] ")
        obj.set_variable(" var1 ", 1, "desc1")
        found = obj.get_variable("var1")
        self.assertIsNotNone(found)
        assert found is not None
        self.assertEqual(found.name, "var1")
        self.assertEqual(found.value, 1)
        self.assertEqual(found.desc, "desc1")

        obj.set_variable(" var1 ", None, None)
        found = obj.get_variable(" var1 ")
        self.assertIsNotNone(found)
        assert found is not None
        self.assertEqual(found.name, "var1")
        self.assertIsNone(found.value)
        self.assertIsNone(found.desc)
        self.assertIsNone(obj.get_variable("missing"))

    def test_11_section_model_dump_returns_copy(self) -> None:
        """Test nr 11."""
        obj = SectionModel("[TEST]")
        obj.set_variable("var1", 1, "desc1")
        dumped = obj.dump
        self.assertEqual(len(dumped), 2)
        self.assertIs(dumped[0], obj)
        self.assertIs(dumped[1], obj.variables[0])
        dumped.append("extra")
        self.assertEqual(len(obj.dump), 2)

    def test_12_section_model_variables_property_returns_typed_list(self) -> None:
        """Test nr 12."""
        obj = SectionModel("[TEST]")
        items = obj.variables
        self.assertIsInstance(items, list)
        items.append(VariableModel(name="var1", value=1))
        obj._set_data(key="__variables__", value=list(items))
        self.assertEqual(len(obj.variables), 1)
        self.assertEqual(obj.variables[0].name, "var1")


# #[EOF]#######################################################################
