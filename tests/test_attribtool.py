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

    def test_01_readonlyclass(self) -> None:
        """Test nr 01."""
        from jsktoolbox.attribtool import ReadOnlyClass

        class A(object, metaclass=ReadOnlyClass):
            VAR: int = 1

        self.assertTrue(A.VAR, 1)

        with self.assertRaises(AttributeError):
            A.VAR = 2


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

    def test_set_the_wrong_attribute(self) -> None:
        """Test nr 2."""
        try:
            self.workclass.abc = 1
            self.workclass.abc = "test"
        except Exception as ex:
            self.assertTrue(isinstance(ex, AttributeError))
        else:
            self.fail("No exception thrown.")


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

    def test_set_the_wrong_attribute(self) -> None:
        """Test nr 2."""
        try:
            self.workclass.abc = 1
            self.workclass.abc = "test"
        except Exception as ex:
            self.assertTrue(isinstance(ex, AttributeError))
        else:
            self.fail("No exception thrown.")


# #[EOF]#######################################################################
