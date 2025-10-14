# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 08.05.2023

Purpose: Unit tests for the Raise class from the jsktoolbox.raisetool module.
"""

import unittest
import inspect
from typing import Any

from jsktoolbox.raisetool import Raise


class TestRaise(unittest.TestCase):
    """Test suite for the Raise utility class."""

    def test_message_formatting(self) -> None:
        """Test message formatting scenarios for Raise.message."""
        # 1. Test with message only
        self.assertEqual(Raise.message("test message"), "test message")

        # 2. Test with class name
        self.assertEqual(
            Raise.message("test message", self.__class__.__name__),
            "TestRaise: test message",
        )

        # 3. Test with class name and current frame
        frame = inspect.currentframe()
        # A more robust check that doesn't rely on a hardcoded line number
        formatted_message = Raise.message(
            "test message",
            class_name=self.__class__.__name__,
            currentframe=frame,
        )
        self.assertTrue(
            formatted_message.startswith(f"TestRaise.test_message_formatting [line:")
        )
        self.assertTrue(formatted_message.endswith("]: test message"))

    def test_error_returns_correct_exception_type(self) -> None:
        """Test that Raise.error returns an instance of the correct exception type."""
        test_cases = [
            AttributeError,
            ConnectionError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
            NotImplementedError,
            Exception,  # Default
        ]
        for exc_type in test_cases:
            with self.subTest(exception=exc_type):
                if exc_type == Exception:
                    err = Raise.error("test")
                    self.assertIsInstance(err, exc_type)
                else:
                    err = Raise.error("test", exc_type)
                    self.assertIsInstance(err, exc_type)

    def test_error_message_content(self) -> None:
        """Test the content of the message within the returned exception."""
        # 1. Test with a simple message
        error = Raise.error("simple error", ValueError)
        self.assertEqual(str(error), "[ValueError]: simple error")

        # 2. Test with class name context
        error = Raise.error("context error", ValueError, class_name="MyClass")
        self.assertEqual(str(error), "MyClass: [ValueError]: context error")

        # 3. Test with full context
        frame = inspect.currentframe()
        error = Raise.error(
            "full context",
            ValueError,
            class_name="MyClass",
            currentframe=frame,
        )
        # Robust check for the formatted message
        error_str = str(error)
        self.assertTrue(
            error_str.startswith("MyClass.test_error_message_content [line:")
        )
        self.assertTrue(error_str.endswith("]: [ValueError]: full context"))

    def test_error_with_invalid_argument_raises_typeerror(self) -> None:
        """Test that Raise.error raises a TypeError for invalid exception arguments."""
        invalid_args: list[Any] = [
            "not a type",
            123,
            ValueError("i am an instance"),
            object,  # Not an Exception subclass
        ]
        for arg in invalid_args:
            with self.subTest(argument=arg):
                with self.assertRaises(TypeError):
                    Raise.error("test message", arg)


# #[EOF]#######################################################################
