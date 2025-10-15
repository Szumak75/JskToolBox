# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 07.05.2023

Purpose: For testing classes that restrict the dynamic creation
of attributes in inheriting classes.
"""

import unittest
from typing import Optional, Any


class TestReadOnlyClass(unittest.TestCase):
    """Testing ReadOnlyClass."""

    def test_01_read_only_class(self) -> None:
        """Test nr 01."""
        from jsktoolbox.attribtool import ReadOnlyClass

        class A(object, metaclass=ReadOnlyClass):
            VAR: int = 1

        self.assertTrue(A.VAR, 1)

        with self.assertRaisesRegex(AttributeError, "Read only attribute"):
            A.VAR = 2

    def test_02_read_only_prevents_new_attribute(self) -> None:
        """Test nr 02."""
        from jsktoolbox.attribtool import ReadOnlyClass

        class B(object, metaclass=ReadOnlyClass):
            VAR: int = 1

        with self.assertRaisesRegex(AttributeError, "Read only attribute"):
            setattr(B, "NEW_FIELD", 42)


class TestNoNewAttributes(unittest.TestCase):
    """Testing NoNewAttributes class."""

    def setUp(self) -> None:
        """Setting up testing engine."""
        from jsktoolbox.attribtool import NoNewAttributes

        class Example(NoNewAttributes):
            """Example testing class."""

            __variable = None

            @property
            def variable(self) -> Optional[Any]:
                return self.__variable

            @variable.setter
            def variable(self, value) -> None:
                self.__variable = value

        self.workclass = Example()

    def test_set_and_get_proper_attribute(self) -> None:
        """Test nr 1."""
        self.workclass.variable = 1
        self.assertEqual(self.workclass.variable, 1)
        self.workclass.variable = "abc"
        self.assertEqual(self.workclass.variable, "abc")

    def test_prevent_undefined_attribute(self) -> None:
        """Test nr 2."""
        with self.assertRaisesRegex(AttributeError, "Undefined attribute abc"):
            setattr(self.workclass, "abc", 1)


class TestNoDynamicAttributes(unittest.TestCase):
    """Testing NoDynamicAttributes class."""

    def setUp(self) -> None:
        """Setting up testing engine."""
        from jsktoolbox.attribtool import NoDynamicAttributes

        class Example(NoDynamicAttributes):
            """Example testing class."""

            __variable = None

            @property
            def variable(self) -> Optional[Any]:
                return self.__variable

            @variable.setter
            def variable(self, value) -> None:
                self.__variable = value

        self.workclass = Example()

    def test_set_and_get_proper_attribute(self) -> None:
        """Test nr 1."""
        self.workclass.variable = 1
        self.assertEqual(self.workclass.variable, 1)
        self.workclass.variable = "abc"
        self.assertEqual(self.workclass.variable, "abc")

    def test_prevent_dynamic_attribute(self) -> None:
        """Test nr 2."""
        with self.assertRaisesRegex(
            AttributeError, "Cannot add new attribute 'abc'"
        ):
            setattr(self.workclass, "abc", 1)


# #[EOF]#######################################################################
