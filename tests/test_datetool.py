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
        self.assertIsInstance(Timestamp.now_float(), float)
        self.assertIsInstance(Timestamp.now_int(), int)
        tnow = Timestamp.now()
        now = int(time.time())
        self.assertTrue(tnow < now + 2 and tnow > now - 2)

    def test_02_datetime_from_timestamp(self) -> None:
        """Test nr 02."""
        self.assertIsInstance(
            DateTime.datetime_from_timestamp(Timestamp.now()), datetime.datetime
        )
        tnow = Timestamp.now()
        dtime = DateTime.datetime_from_timestamp(tnow)
        dtest = datetime.datetime.now()
        self.assertTrue(
            dtime.year == dtest.year
            and dtime.month == dtest.month
            and dtime.day == dtest.day
            and dtime.hour == dtest.hour
            and dtime.minute == dtest.minute
            and (dtime.second == dtest.second or dtime.second == dtest.second + 1)
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
        tnow = Timestamp.now() - 1
        self.assertTrue(td == DateTime.elapsed_time_from_timestamp(tnow))
        self.assertEqual(str(DateTime.elapsed_time_from_timestamp(tnow)), "0:00:01")
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
