# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2026-02-28

Purpose: Validate Tk widget helper object creation and typed property behaviour.
"""

import unittest
import tkinter as tk

from jsktoolbox.tktool.widgets import (
    CreateToolTip,
    StatusBarTkFrame,
    StatusBarTtkFrame,
    VerticalScrolledTkFrame,
    VerticalScrolledTtkFrame,
)
from tkinter import ttk


class TestTkToolWidgets(unittest.TestCase):
    """Unit tests for Tk/ttk widget helper constructors."""

    root: tk.Tk

    @classmethod
    def setUpClass(cls) -> None:
        """Create shared Tk root for widget construction tests."""
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
        except Exception as ex:  # pragma: no cover - environment dependent
            raise unittest.SkipTest(f"Tk root unavailable: {ex}")

    @classmethod
    def tearDownClass(cls) -> None:
        """Destroy shared Tk root if it was created."""
        if hasattr(cls, "root"):
            try:
                cls.root.destroy()
            except Exception:
                pass

    def test_status_bar_tk_frame_creation(self) -> None:
        """Create StatusBarTkFrame and validate TkBase-backed properties."""
        widget = StatusBarTkFrame(self.root)
        self.assertIs(widget.master, self.root)
        self.assertIsInstance(widget.children, dict)
        widget.destroy()

    def test_status_bar_tk_frame_on_the_frame_creation(self) -> None:
        """Create StatusBarTkFrame and validate TkBase-backed properties."""
        frame = tk.Frame(self.root)
        widget = StatusBarTkFrame(frame)
        self.assertIs(widget.master, frame)
        self.assertIsInstance(widget.children, dict)
        widget.destroy()
        frame.destroy()

    def test_status_bar_ttk_frame_creation(self) -> None:
        """Create StatusBarTtkFrame and validate TkBase-backed properties."""
        widget = StatusBarTtkFrame(self.root)
        self.assertIs(widget.master, self.root)
        self.assertIsInstance(widget.children, dict)
        widget.destroy()

    def test_vertical_scrolled_tk_frame_creation(self) -> None:
        """Create VerticalScrolledTkFrame with valid interior container."""
        widget = VerticalScrolledTkFrame(self.root)
        self.assertIs(widget.master, self.root)
        self.assertIsInstance(widget.interior, tk.Frame)
        widget.destroy()

    def test_vertical_scrolled_ttk_frame_creation(self) -> None:
        """Create VerticalScrolledTtkFrame with valid interior container."""
        widget = VerticalScrolledTtkFrame(self.root)
        self.assertIs(widget.master, self.root)
        self.assertIsInstance(widget.interior, ttk.Frame)
        widget.destroy()

    def test_create_tooltip_creation_with_string(self) -> None:
        """Create tooltip manager bound to a Tk widget."""
        anchor = tk.Label(self.root, text="anchor")
        tooltip = CreateToolTip(anchor, text="tooltip")
        self.assertEqual(tooltip.text, "tooltip")
        anchor.destroy()

    def test_create_tooltip_creation_with_string_var(self) -> None:
        """Create tooltip manager with StringVar text source."""
        text_var = tk.StringVar(value="tooltip-var")
        anchor = tk.Label(self.root, text="anchor")
        tooltip = CreateToolTip(anchor, text=text_var)
        self.assertIs(tooltip.text, text_var)
        anchor.destroy()

    def test_master_property_rejects_invalid_type(self) -> None:
        """Reject invalid master assignment under strict BData typing."""
        widget = StatusBarTkFrame(self.root)
        with self.assertRaises(TypeError):
            widget.master = "invalid-master"  # type: ignore[assignment]
        widget.destroy()

    def test_children_property_rejects_invalid_mapping(self) -> None:
        """Reject invalid children mapping under strict BData typing."""
        widget = StatusBarTkFrame(self.root)
        with self.assertRaises(TypeError):
            widget.children = {"child": object()}  # type: ignore[assignment]
        widget.destroy()

    def test_children_property_accepts_widget_mapping(self) -> None:
        """Accept mapping with str keys and widget values."""
        widget = StatusBarTkFrame(self.root)
        child = tk.Frame(widget)
        widget.children = {"child": child}
        self.assertIn("child", widget.children)
        child.destroy()
        widget.destroy()


# #[EOF]#######################################################################
