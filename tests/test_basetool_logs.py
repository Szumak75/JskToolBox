# -*- coding: utf-8 -*-
"""
  test_basetool_logs.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 4.10.2024, 12:43:33
  
  Purpose: 
"""
from types import NoneType
import unittest
from typing import Dict, List, Optional
from jsktoolbox.basetool.logs import BLoggerQueue, BLoggerEngine
from jsktoolbox.logstool.queue import LoggerQueue


class TestBLogs(unittest.TestCase):
    """Testing BLoggerQueue class."""

    def setUp(self) -> None:
        """Set up."""
        try:
            self.obj = BLoggerQueue()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_01_set(self) -> None:
        """Test nr 01."""
        try:
            self.obj.logs_queue = None
            self.obj.logs_queue = LoggerQueue()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")
        with self.assertRaises(TypeError):
            self.obj.logs_queue = "test"  # type: ignore

    def test_02_get(self) -> None:
        """Test nr 02."""
        self.assertTrue(isinstance(self.obj.logs_queue, NoneType))
        self.obj.logs_queue = LoggerQueue()
        self.assertTrue(isinstance(self.obj.logs_queue, LoggerQueue))


class TestBLoggerEngine(unittest.TestCase):
    """Testing BLoggerEngine class."""

    def setUp(self) -> None:
        """Set up."""
        try:
            self.obj = BLoggerEngine()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_01_set(self) -> None:
        """Test nr 01."""
        try:
            self.obj.name = "Test"
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")
        with self.assertRaises(TypeError):
            self.obj.name = 1  # type: ignore

    def test_02_get(self) -> None:
        """Test nr 02."""
        self.assertTrue(isinstance(self.obj.name, NoneType))
        self.obj.name = "Test"
        self.assertTrue(isinstance(self.obj.name, str))


# #[EOF]#######################################################################
