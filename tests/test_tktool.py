# -*- coding: utf-8 -*-
"""
  test_tktool.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.02.2025, 22:00:45
  
  Purpose: Tests for tktool
"""

import unittest
import inspect

from jsktoolbox.tktool.tools import (
    _XClip,
    _XSel,
    _WinClip,
    _GtkClip,
    _MacClip,
    _QtClip,
    _TkClip,
)


class XSelTest(unittest.TestCase):
    """Class for testing XSel clipboard operations."""

    def setUp(self) -> None:
        """Setup for XSelTest."""
        try:
            self.cb = _XSel()
        except Exception as e:
            self.fail(f"Failed to create XSel instance: {e}")

    def test_is_tool(self) -> None:
        """Test nr 01."""
        self.assertTrue(self.cb.is_tool)

    def test_copy_paste(self) -> None:
        """Test nr 02."""
        if self.cb.is_tool:
            self.cb.set_clipboard("to jest test xsel")
            self.assertEqual(self.cb.get_clipboard(), "to jest test xsel")


class XClipTest(unittest.TestCase):
    """Class for testing XClip clipboard operations."""

    def setUp(self) -> None:
        """Setup for XClipTest."""
        try:
            self.cb = _XClip()
        except Exception as e:
            self.fail(f"Failed to create XClip instance: {e}")

    def test_is_tool(self) -> None:
        """Test nr 01."""
        self.assertTrue(self.cb.is_tool)

    def test_copy_paste(self) -> None:
        """Test nr 02."""
        if self.cb.is_tool:
            self.cb.set_clipboard("to jest test xclip")
            self.assertEqual(self.cb.get_clipboard(), "to jest test xclip")


# #[EOF]#######################################################################
