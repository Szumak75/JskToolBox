# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 17.11.2023

Purpose:
"""

import unittest
import sys

from jsktoolbox.systemtool import CommandLineParser


class TestCommandLineParser(unittest.TestCase):
    """Test for CommandLineParser class."""

    def setUp(self) -> None:
        """Set up tests."""
        self.parser = CommandLineParser()
        self.parser.configure_option(None, "avar", "a var desc")
        self.parser.configure_option("b", "bvar", "b var desc")
        self.parser.configure_option("c", "cvar", "c var desc")
        self.parser.configure_option("d", "dvar", "d var desc", has_value=True)
        self.parser.configure_option("e", "evar", "e var desc", has_value=True)
        self.parser.configure_option("f", "fvar", "f var desc", has_value=True)
        self.parser.configure_option("g", "gvar", "g var desc", has_value=True)

    def test_01_create_parser(self) -> None:
        """Test nr 01."""
        try:
            CommandLineParser()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_02_getting_single_args_undefined(self) -> None:
        """Test nr 02."""
        self.parser.parse()
        self.assertTrue(self.parser.get_option("avar") is None)
        self.assertTrue(self.parser.get_option("bvar") is None)
        self.assertTrue(self.parser.get_option("cvar") is None)
        self.assertTrue(self.parser.get_option("dvar") is None)
        self.assertTrue(self.parser.get_option("evar") is None)
        self.assertTrue(self.parser.get_option("fvar") is None)
        self.assertTrue(self.parser.get_option("gvar") is None)

    def test_03_getting_single_args_undefined(self) -> None:
        """Test nr 03."""
        sys.argv.append("--bvar")
        sys.argv.append("-c")
        self.parser.parse()
        self.assertTrue(self.parser.get_option("avar") is None)
        self.assertTrue(self.parser.get_option("bvar") is not None)
        self.assertTrue(self.parser.get_option("cvar") is not None)
        self.assertTrue(self.parser.get_option("dvar") is None)
        self.assertTrue(self.parser.get_option("evar") is None)
        self.assertTrue(self.parser.get_option("fvar") is None)
        self.assertTrue(self.parser.get_option("gvar") is None)

    def test_04_getting_short_args_with_value(self) -> None:
        """Test nr 04."""
        sys.argv.append("-d")
        sys.argv.append("10")
        self.parser.parse()
        self.assertTrue(self.parser.get_option("avar") is None)
        self.assertTrue(self.parser.get_option("bvar") is not None)
        self.assertTrue(self.parser.get_option("cvar") is not None)
        self.assertTrue(self.parser.get_option("dvar") is not None)
        self.assertEqual(self.parser.get_option("dvar"), "10")
        self.assertTrue(self.parser.get_option("evar") is None)
        self.assertTrue(self.parser.get_option("fvar") is None)
        self.assertTrue(self.parser.get_option("gvar") is None)

    def test_05_getting_long_args_with_value(self) -> None:
        """Test nr 05."""
        sys.argv.append("--evar=20")
        sys.argv.append("--fvar=/tmp/for test case.txt")
        sys.argv.append("--avar")
        self.parser.parse()
        self.assertTrue(self.parser.get_option("avar") is not None)
        self.assertTrue(self.parser.get_option("bvar") is not None)
        self.assertTrue(self.parser.get_option("cvar") is not None)
        self.assertTrue(self.parser.get_option("dvar") is not None)
        self.assertTrue(self.parser.get_option("evar") is not None)
        self.assertEqual(self.parser.get_option("evar"), "20")
        self.assertTrue(self.parser.get_option("fvar") is not None)
        self.assertEqual(self.parser.get_option("fvar"), "/tmp/for test case.txt")
        self.assertTrue(self.parser.get_option("gvar") is None)


# #[EOF]#######################################################################
