# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 29.10.2023

Purpose: ConfigTool testing class.
"""

import unittest
from typing import List
from jsktoolbox.configtool.main import Config
from jsktoolbox.configtool.libs.file import FileProcessor


class TestConfig(unittest.TestCase):
    """ConfigTool testing class."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.filename = "/tmp/configtool/a/b/c/d/e/test.conf"
        self.conf_template = """# This is example config file for test purpose only.
[first]
# section 'first'
name = "tests"
enable = yes
list = [10, 20, 30]
level = 7 # value of level
# example section comments nr 01
# example section comments nr 02
# -----<end of section: 'first'>-----

[second]
# section 'second'
value = 18k
label=
# -----<end of section: 'second'>-----

"""
        # create config file
        try:
            fp = FileProcessor()
            fp.file = self.filename
            if fp.file_create():
                fp.write(self.conf_template)
        except Exception as ex:
            self.fail(msg=f"{ex}")

    def test_01_create_object(self) -> None:
        """Test nr 01."""
        file: str = "/tmp/test/config.01.ini"
        sname: str = "TEST"
        try:
            Config(file, sname)
        except Exception:
            self.fail("something is very wrong.")

    def test_02_config_read(self) -> None:
        """Test nr 02."""
        obj = None
        try:
            obj = Config(self.filename, "configtool")
            # config file was created in setUp
            self.assertTrue(obj.file_exists)
            # load config
            self.assertTrue(obj.load())
            # save config
            self.assertTrue(obj.save())
        except Exception as ex:
            self.fail(msg=f"{ex}")

    def test_03_save_and_read_check_types(self) -> None:
        """Test nr 03."""
        filename = "/tmp/test.ini"
        main_section = "TEST"

        # create config
        try:
            obj = Config(filename, main_section, auto_create=True)
            obj.set(
                main_section,
                varname="test01",
                value="test",
                desc="Set string data",
            )
            obj.set(
                main_section,
                varname="test02",
                value=123,
                desc="Set integer data",
            )
            obj.set(
                main_section,
                varname="test03",
                value=3.14,
                desc="Set float data",
            )
            obj.set(
                main_section,
                varname="test04",
                value=["a", 13, 45.18, True],
                desc="Set List data",
            )
            obj.set(
                main_section,
                varname="test05",
                value=False,
                desc="Set boolean data",
            )
            self.assertTrue(obj.save())
        except Exception as ex:
            self.fail(msg=f"{ex}")

        # get config
        try:
            obj = Config(filename, main_section)
            self.assertTrue(obj.load())
            self.assertTrue(obj.has_section(main_section))
            self.assertTrue(obj.has_varname(main_section, "test01"))
            test = obj.get(main_section, varname="test01")
            self.assertIsInstance(test, str, msg=f"get:{test}")
            self.assertTrue(test == "test", msg=f"get:{test}")
            test = obj.get(main_section, varname="test02")
            self.assertIsInstance(test, int, msg=f"get:{test}")
            self.assertTrue(test == 123, msg=f"get:{test}")
            test = obj.get(main_section, varname="test03")
            self.assertIsInstance(test, float, msg=f"get:{test}")
            self.assertTrue(test == 3.14, msg=f"get:{test}")
            test = obj.get(main_section, varname="test04")
            self.assertIsInstance(test, List, msg=f"get:{test}")
            # check list contents
            self.assertIsInstance(test[0], str, msg=f"get:{test[0]}")
            self.assertIsInstance(test[1], int, msg=f"get:{test[1]}")
            self.assertIsInstance(test[2], float, msg=f"get:{test[2]}")
            self.assertIsInstance(test[3], bool, msg=f"get:{test[3]}")
            self.assertTrue(test == ["a", 13, 45.18, True], msg=f"get:{test}")
            test = obj.get(main_section, varname="test05")
            self.assertIsInstance(test, bool, msg=f"get:{test}")
            self.assertTrue(test == False)

        except Exception as ex:
            self.fail(msg=f"{ex}")


# #[EOF]#######################################################################
