# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.05.2023

  Purpose: For testing Raise class
"""

import unittest
import inspect

from jsktoolbox.raisetool import Raise


class TestRaise(unittest.TestCase):
    """Tests for Raise class."""

    def test_create_class_instance(self) -> None:
        """Test nr 1."""
        obj = Raise()
        self.assertTrue(obj, Raise)

    def test_returning_message_from_instance(self) -> None:
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

    def test_returning_message_from_class(self) -> None:
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

    def test_returning_attribute_error(self) -> None:
        """Test nr 4."""
        self.assertIsInstance(Raise.error("test", AttributeError), AttributeError)

    def test_returning_connection_error(self) -> None:
        """Test nr 5."""
        self.assertIsInstance(Raise.error("test", ConnectionError), ConnectionError)

    def test_returning_key_error(self) -> None:
        """Test nr 6."""
        self.assertIsInstance(Raise.error("test", KeyError), KeyError)

    def test_returning_os_error(self) -> None:
        """Test nr 7."""
        self.assertIsInstance(Raise.error("test", OSError), OSError)

    def test_returning_syntax_error(self) -> None:
        """Test nr 8."""
        self.assertIsInstance(Raise.error("test", SyntaxError), SyntaxError)

    def test_returning_type_error(self) -> None:
        """Test nr 9."""
        self.assertIsInstance(Raise.error("test", TypeError), TypeError)

    def test_returning_value_error(self) -> None:
        """Test nr 10."""
        self.assertIsInstance(Raise.error("test", ValueError), ValueError)

    def test_returning_index_error(self) -> None:
        """Test nr 11."""
        self.assertIsInstance(Raise.error("test", IndexError), IndexError)

    def test_returning_not_implemented_error(self) -> None:
        """Test nr 12."""
        self.assertIsInstance(
            Raise.error("test", NotImplementedError), NotImplementedError
        )

    def test_returning_custom_error(self) -> None:
        """Test nr 13."""
        self.assertIsInstance(
            Raise.error("test"),
            Exception,
        )
        self.assertIsInstance(
            Raise.error("test", ValueError),
            ValueError,
        )
        self.assertIsInstance(
            Raise.error("test", IndexError),
            IndexError,
        )


# #[EOF]#######################################################################
