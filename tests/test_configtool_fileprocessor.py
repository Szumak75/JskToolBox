# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose:
"""

import unittest
from jsktoolbox.configtool.libs.file import FileProcessor


class TestFileProcessor(unittest.TestCase):
    """Tests for FileProcessor class."""

    def test_01_create_object(self) -> None:
        """Test nr 01."""
        try:
            FileProcessor()
        except Exception:
            self.fail("somenting is very wrong.")

    def test_02_file(self) -> None:
        """Test nr 02."""
        file: str = "/tmp/test/config.02.ini"
        obj = FileProcessor()

        try:
            obj.file = file
        except Exception:
            self.fail("somenting is very wrong.")

        self.assertEqual(obj.file, file)

    def test_03_check_and_create_file(self) -> None:
        """Test nr 03."""
        file: str = "/tmp/test/config.03.ini"
        obj = FileProcessor()

        try:
            obj.file = file
        except Exception:
            self.fail("somenting is very wrong.")

        try:
            if not obj.file_exists:
                obj.file_create()
        except Exception as ex:
            self.fail(ex)
        self.assertTrue(obj.file_exists)

    def test_04_write_and_read_file(self) -> None:
        """Test nr 04."""
        data = """[TEST]
# description nr 1
# description nr 2
value01=1 # description nr 3
value02='some string'

[TEST01]
value01=10

"""
        file: str = "/tmp/test/config.04.ini"
        obj = FileProcessor()
        try:
            obj.file = file
        except Exception as ex:
            self.fail(msg=f"{ex}")

        try:
            if not obj.file_exists:
                obj.file_create()
        except Exception as ex:
            self.fail(ex)
        self.assertTrue(obj.file_exists)

        try:
            obj.write(data)
            out = obj.read()
            self.assertEqual(data, out)
        except Exception as ex:
            self.fail(msg=f"{ex}")


# #[EOF]#######################################################################
