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

    def test_01_Timestamp(self):
        """Test nr 01."""
        self.assertIsInstance(Timestamp.now, int)
        tnow = Timestamp.now
        now = int(time.time())
        self.assertTrue(tnow < now + 2 and tnow > now - 2)

    def test_02_datetime_from_timestamp(self):
        """Test nr 02."""
        self.assertIsInstance(
            DateTime.datetime_from_timestamp(Timestamp.now), datetime.datetime
        )
        tnow = Timestamp.now
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

    def test_03_datetime_now(self):
        """Test nr 03."""
        self.assertIsInstance(DateTime.now(), datetime.datetime)

    def test_04_datetime_elapsed_time_from_seconds(self):
        """Test nr 04."""
        self.assertIsInstance(
            DateTime.elapsed_time_from_seconds(10.01), datetime.timedelta
        )
        td = datetime.timedelta(seconds=10)
        self.assertTrue(td == DateTime.elapsed_time_from_seconds(10))
        self.assertEqual(str(DateTime.elapsed_time_from_seconds(10)), "0:00:10")
        with self.assertRaises(TypeError):
            DateTime.elapsed_time_from_seconds("20")

    def test_05_datetime_elapsed_time_from_timestamp(self):
        """Test nr 05."""
        self.assertIsInstance(
            DateTime.elapsed_time_from_seconds(Timestamp.now), datetime.timedelta
        )
        td = datetime.timedelta(seconds=1)
        tnow = Timestamp.now - 1
        self.assertTrue(td == DateTime.elapsed_time_from_timestamp(tnow))
        self.assertEqual(str(DateTime.elapsed_time_from_timestamp(tnow)), "0:00:01")
        with self.assertRaises(TypeError):
            DateTime.elapsed_time_from_timestamp("20")


# #[EOF]#######################################################################
