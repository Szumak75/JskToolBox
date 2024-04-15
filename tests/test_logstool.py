# -*- coding: utf-8 -*-
"""
  test_logstool.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 9.01.2024, 19:18:47
  
  Purpose: LogsTool testing suit.
"""

from unittest import TestCase

from jsktoolbox.libs.base_logs import LoggerQueue
from jsktoolbox.logstool.formatters import LogFormatterNull


class TestLogsTool(TestCase):
    """TestLogsTool class."""

    def test_01_logger_queue(self) -> None:
        """Test nr 01."""

        qlog1 = LoggerQueue()
        qlog2 = LoggerQueue()

        self.assertTrue(qlog1.get() is None)
        self.assertTrue(qlog2.get() is None)

        qlog2.put("test")

        self.assertTrue(qlog1.get() is None)
        self.assertTrue(qlog2.get() is not None)

        self.assertTrue(qlog1.get() is None)
        self.assertTrue(qlog2.get() is None)

    def test_02_log_formatter_null(self) -> None:
        """Test nr 02."""

        lf = LogFormatterNull()
        self.assertEqual(lf.format("test1"), "test1")
        self.assertEqual(lf.format("test2"), "test2")
        self.assertEqual(lf.format("test3"), "test3")
        self.assertEqual(lf.format("test", "abc"), "[abc]: test")


# #[EOF]#######################################################################
