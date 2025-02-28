# -*- coding: utf-8 -*-
"""
  test_tktool.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.02.2025, 22:00:45
  
  Purpose: Tests for tktool
"""

import unittest
import inspect
import tkinter as tk

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
            self.assertNotEqual(self.cb.get_clipboard(), "to jest test xsel 2")
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
            self.assertNotEqual(self.cb.get_clipboard(), "to jest test xclip 2")
            self.assertEqual(self.cb.get_clipboard(), "to jest test xclip")


class TkClipTest(unittest.TestCase):
    """Class for testing TkClip clipboard operations."""

    def setUp(self) -> None:
        """Setup for TkClipTest."""
        try:
            # win = tk.Tk()
            # self.cb = _TkClip(win)
            self.cb = _TkClip()
            # win.mainloop()
        except Exception as e:
            self.fail(f"Failed to create TkClip instance: {e}")

    def test_is_tool(self) -> None:
        """Test nr 01."""
        self.assertTrue(self.cb.is_tool)

    def test_copy_paste(self) -> None:
        """Test nr 02."""
        if self.cb.is_tool:
            self.cb.set_clipboard("to jest test tkclip")
            self.assertNotEqual(self.cb.get_clipboard(), "to jest test tkclip 2")
            self.assertEqual(self.cb.get_clipboard(), "to jest test tkclip")


class QtClipTest(unittest.TestCase):
    """Class for testing QtClip clipboard operations."""

    def setUp(self) -> None:
        """Setup for QtClipTest."""
        try:
            self.cb = _QtClip()
        except Exception as e:
            self.fail(f"Failed to create QtClip instance: {e}")

    def test_is_tool(self) -> None:
        """Test nr 01."""
        self.assertTrue(self.cb.is_tool)

    def test_copy_paste(self) -> None:
        """Test nr 02."""
        if self.cb.is_tool:
            self.cb.set_clipboard("to jest test qt clip")
            self.assertNotEqual(self.cb.get_clipboard(), "to jest test qt clip 2")
            self.assertEqual(self.cb.get_clipboard(), "to jest test qt clip")


class CollectiveTest(unittest.TestCase):
    """Class for testing clipboard operations."""

    def test_over_different_classes(self) -> None:
        """Test nr 01."""
        var: str = "this is collective test."
        cb = None
        if _XClip().is_tool:
            cb = _XClip()
        elif _XSel().is_tool:
            cb = _XSel()

        if cb:
            cb.set_clipboard(var)

            if _XClip().is_tool:
                test = _XClip()
                self.assertEqual(test.get_clipboard(), var)

            if _XSel().is_tool:
                test = _XSel()
                self.assertEqual(test.get_clipboard(), var)

            if _QtClip().is_tool:
                test = _QtClip()
                self.assertEqual(test.get_clipboard(), var)

            # TkClip
            # if _TkClip().is_tool:
            #     _TkClip().set_clipboard(var)
            #     test = _TkClip()
            #     self.assertEqual(test.get_clipboard(), var)
            # win = tk.Tk()
            # if _TkClip(win).is_tool:
            #     _TkClip(win).set_clipboard(var)
            #     test = _TkClip(win)
            #     self.assertEqual(test.get_clipboard(), var)


# #[EOF]#######################################################################
