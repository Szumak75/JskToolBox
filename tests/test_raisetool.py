# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.05.2023

  Purpose: For testing Raise class
"""

import unittest
import inspect

from raisetool.formatter import Raise


class TestRaise(unittest.TestCase):
    """Tests for Raise class."""

    def test_create_class_instance(self):
        """Test nr 1."""
        obj = Raise()
        self.assertTrue(obj, Raise)

    def test_returning_message_from_instance(self):
        """Test nr 2."""
        obj = Raise()
        self.assertEqual(obj.message("test"), "test")
        self.assertEqual(
            obj.message("test", self.__class__.__name__), "TestRaise: test"
        )
        self.assertEqual(
            obj.message(
                "test",
                class_name=self.__class__.__name__,
                currentframe=inspect.currentframe(),
            ),
            "TestRaise.test_returning_message_from_instance [line:31]: test",
        )

    def test_returning_message_from_class(self):
        """Test nr 3."""
        self.assertEqual(Raise.message("test"), "test")
        self.assertEqual(
            Raise.message("test", self.__class__.__name__), "TestRaise: test"
        )
        self.assertEqual(
            Raise.message(
                "test",
                class_name=self.__class__.__name__,
                currentframe=inspect.currentframe(),
            ),
            "TestRaise.test_returning_message_from_class [line:46]: test",
        )

    def test_returning_attribute_error(self):
        """Test nr 4."""
        self.assertIsInstance(Raise.attribute_error("test"), AttributeError)

    def test_returning_connection_error(self):
        """Test nr 5."""
        self.assertIsInstance(
            Raise.connection_error("test"), ConnectionError
        )

    def test_returning_key_error(self):
        """Test nr 6."""
        self.assertIsInstance(Raise.key_error("test"), KeyError)

    def test_returning_os_error(self):
        """Test nr 7."""
        self.assertIsInstance(Raise.os_error("test"), OSError)

    def test_returning_syntax_error(self):
        """Test nr 8."""
        self.assertIsInstance(Raise.syntax_error("test"), SyntaxError)

    def test_returning_type_error(self):
        """Test nr 9."""
        self.assertIsInstance(Raise.type_error("test"), TypeError)

    def test_returning_value_error(self):
        """Test nr 10."""
        self.assertIsInstance(Raise.value_error("test"), ValueError)

    def test_returning_index_error(self):
        """Test nr 11."""
        self.assertIsInstance(Raise.index_error("test"), IndexError)

    def test_returning_not_implemented_error(self):
        """Test nr 12."""
        self.assertIsInstance(
            Raise.not_implemented_error("test"), NotImplementedError
        )


# #[EOF]#######################################################################
