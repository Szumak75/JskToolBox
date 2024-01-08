# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 05.09.2023

  Purpose: tests for Env class.
"""

import unittest
import os
from pathlib import Path
from jsktoolbox.libs.system import Env


class TestEnv(unittest.TestCase):
    """Env class."""

    def test_system_env_create(self) -> None:
        """Test nr 1."""
        try:
            Env()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_system_env_home_return(self) -> None:
        """Test nr 2."""
        self.assertIsInstance(Env().home, str)
        self.assertIsInstance(Env.home, str)
        self.assertEqual(Env().home, Env.home)
        self.assertEqual(os.getenv("HOME"), Env.home)

    def test_system_env_home_exists(self) -> None:
        """Test nr 3."""
        self.assertTrue(Path(Env.home).exists() and Path(Env.home).is_dir())

    def test_system_env_username_return(self) -> None:
        """Test nr 4."""
        self.assertIsInstance(Env().username, str)
        self.assertIsInstance(Env.username, str)
        self.assertEqual(Env().username, Env.username)
        self.assertEqual(os.getenv("USER"), Env.username)


# #[EOF]#######################################################################
