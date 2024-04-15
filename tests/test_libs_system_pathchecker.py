# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 06.09.2023

  Purpose: PathChecker testing class
"""

import unittest
from jsktoolbox.libs.system import PathChecker


class TestPathChecker(unittest.TestCase):
    """Test engine."""

    def test_01_create_object(self) -> None:
        """Test nr 1."""
        try:
            PathChecker("/tmp")
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: {ex}")

        with self.assertRaises(TypeError):
            PathChecker(None) # type: ignore
        with self.assertRaises(TypeError):
            PathChecker(10) # type: ignore
        with self.assertRaises(TypeError):
            PathChecker([]) # type: ignore
        with self.assertRaises(TypeError):
            PathChecker({}) # type: ignore
        with self.assertRaises(TypeError):
            PathChecker() # type: ignore

        with self.assertRaises(ValueError):
            PathChecker("")

    def test_02_path_exists(self) -> None:
        """Test nr 2."""
        self.assertTrue(PathChecker("/tmp").exists)
        self.assertTrue(PathChecker("/bin/sh").exists)

    def test_03_path_is_dir(self) -> None:
        """Test nr 3."""
        self.assertTrue(PathChecker("/tmp").is_dir)

    def test_04_path_is_file(self) -> None:
        """Test nr 4."""
        self.assertTrue(PathChecker("/bin/sh").is_file)

    def test_05_path_create_dir(self) -> None:
        """Test nr 5."""
        o = PathChecker("/tmp/dir/")
        if not o.exists:
            self.assertTrue(o.create())
            self.assertTrue(o.exists)
            self.assertTrue(o.is_dir)
            self.assertFalse(o.is_file)

    def test_06_path_create_file(self) -> None:
        """Test nr 6."""
        o = PathChecker("/tmp/file")
        if not o.exists:
            self.assertTrue(o.create())
            self.assertTrue(o.exists)
            self.assertFalse(o.is_dir)
            self.assertTrue(o.is_file)

    def test_07_path_split(self) -> None:
        """Test nr 7."""
        if PathChecker("/usr/bin/nm").exists:
            self.assertEqual(PathChecker("/usr/bin/nm").dirname, "/usr/bin")
            self.assertEqual(PathChecker("/usr/bin/nm").filename, "nm")


# #[EOF]#######################################################################
