# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: ConfigTool testing class.
"""

import unittest
from jsktoolbox.configtool.main import Config


class TestConfig(unittest.TestCase):
    """ConfigTool testing class."""

    def test_01_create_object(self):
        """Test nr 01."""
        file: str = "/tmp/test/config.01.ini"
        sname: str = "TEST"
        try:
            Config(file, sname)
        except Exception:
            self.fail("somenting is very wrong.")


# #[EOF]#######################################################################
