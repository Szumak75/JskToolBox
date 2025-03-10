# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 02.12.2023

Purpose: For testing classes from datetool module.
"""

import unittest
import time
import datetime

from jsktoolbox.datetool import Timestamp, DateTime


class TestDateTool(unittest.TestCase):
    """Test class for DateTool module."""

    def test_01_Timestamp(self) -> None:
        """Test nr 01."""
        self.assertIsInstance(Timestamp.now(), int)
        self.assertIsInstance(Timestamp.now(float), float)
        self.assertIsInstance(Timestamp.now(int), int)
        now1 = Timestamp.now()
        now2 = int(time.time())
        self.assertTrue(now1 < now2 + 2 and now1 > now2 - 2)

    def test_02_datetime_from_timestamp(self) -> None:
        """Test nr 02."""
        self.assertIsInstance(
            DateTime.datetime_from_timestamp(Timestamp.now()), datetime.datetime
        )
        now = Timestamp.now()
        d_time = DateTime.datetime_from_timestamp(now)
        d_test = datetime.datetime.now()
        self.assertTrue(
            d_time.year == d_test.year
            and d_time.month == d_test.month
            and d_time.day == d_test.day
            and d_time.hour == d_test.hour
            and d_time.minute == d_test.minute
            and (d_time.second == d_test.second or d_time.second == d_test.second + 1)
        )

    def test_03_datetime_now(self) -> None:
        """Test nr 03."""
        self.assertIsInstance(DateTime.now(), datetime.datetime)

    def test_04_datetime_elapsed_time_from_seconds(self) -> None:
        """Test nr 04."""
        self.assertIsInstance(
            DateTime.elapsed_time_from_seconds(10.01), datetime.timedelta
        )
        td = datetime.timedelta(seconds=10)
        self.assertTrue(td == DateTime.elapsed_time_from_seconds(10))
        self.assertEqual(str(DateTime.elapsed_time_from_seconds(10)), "0:00:10")
        with self.assertRaises(TypeError):
            DateTime.elapsed_time_from_seconds("20")  # type: ignore

    def test_05_datetime_elapsed_time_from_timestamp(self) -> None:
        """Test nr 05."""
        self.assertIsInstance(
            DateTime.elapsed_time_from_seconds(Timestamp.now()), datetime.timedelta
        )
        td = datetime.timedelta(seconds=1)
        now = Timestamp.now() - 1
        self.assertTrue(td == DateTime.elapsed_time_from_timestamp(now))
        self.assertEqual(str(DateTime.elapsed_time_from_timestamp(now)), "0:00:01")
        with self.assertRaises(TypeError):
            DateTime.elapsed_time_from_timestamp("20")  # type: ignore

    def test_06_timestamp_from_string(self) -> None:
        """Test nr 06."""
        self.assertTrue(
            Timestamp.from_string("1970-01-01 01:00", "%Y-%m-%d %H:%M") == 0
        )
        self.assertFalse(Timestamp.from_string("2004-07-28", "%Y-%m-%d") == 0)
        with self.assertRaises(ValueError):
            Timestamp.from_string("2004-07-28", "Y-m-d")


# #[EOF]#######################################################################
