# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 07.05.2023

  Purpose: For testing classes that restrict the dynamic creation
  of attributes in inheriting classes.
"""

import unittest


class TestNoNewAttributes(unittest.TestCase):
    """Testing NoNewAttributes class."""

    def setUp(self) -> None:
        """Setting up testing engine."""
        from toolbox.attribtool import NoNewAttributes

        class Example(NoNewAttributes):
            """Example testing class."""

            __variable = None

            @property
            def variable(self):
                return self.__variable

            @variable.setter
            def variable(self, value):
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
        from toolbox.attribtool import NoDynamicAttributes

        class Example(NoDynamicAttributes):
            """Example testing class."""

            __variable = None

            @property
            def variable(self):
                return self.__variable

            @variable.setter
            def variable(self, value):
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
