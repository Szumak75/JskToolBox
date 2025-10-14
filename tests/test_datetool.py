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
        """Test Timestamp.now() method.

        This test checks if Timestamp.now() returns the correct types (int, float)
        and if the returned timestamp is accurate within a small margin.
        """
        self.assertIsInstance(Timestamp.now(), int)
        self.assertIsInstance(Timestamp.now(float), float)
        self.assertIsInstance(Timestamp.now(int), int)
        now1 = Timestamp.now()
        now2 = int(time.time())
        self.assertTrue(now1 < now2 + 2 and now1 > now2 - 2)

    def test_02_datetime_from_timestamp(self) -> None:
        """Test DateTime.datetime_from_timestamp() method.

        This test ensures that the method correctly converts a Unix timestamp
        to a datetime object and that the resulting datetime is accurate.
        """
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
        """Test DateTime.now() method.

        This test verifies that DateTime.now() returns a datetime.datetime object.
        """
        self.assertIsInstance(DateTime.now(), datetime.datetime)

    def test_04_datetime_elapsed_time_from_seconds(self) -> None:
        """Test DateTime.elapsed_time_from_seconds() method.

        This test checks if the method correctly converts seconds to a timedelta object
        and handles invalid (string) input by raising a TypeError.
        """
        self.assertIsInstance(
            DateTime.elapsed_time_from_seconds(10.01), datetime.timedelta
        )
        td = datetime.timedelta(seconds=10)
        self.assertTrue(td == DateTime.elapsed_time_from_seconds(10))
        self.assertEqual(str(DateTime.elapsed_time_from_seconds(10)), "0:00:10")
        with self.assertRaises(TypeError):
            DateTime.elapsed_time_from_seconds("20")  # type: ignore

    def test_05_datetime_elapsed_time_from_timestamp(self) -> None:
        """Test DateTime.elapsed_time_from_timestamp() method.

        This test verifies that the method correctly calculates the elapsed time
        from a timestamp and handles invalid (string) input by raising a TypeError.
        """
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
        """Test Timestamp.from_string() method.

        This test checks if the method correctly converts a formatted string to a timestamp
        and raises a ValueError for an invalid format.
        """
        self.assertTrue(
            Timestamp.from_string("1970-01-01 01:00", "%Y-%m-%d %H:%M") == 0
        )
        self.assertFalse(Timestamp.from_string("2004-07-28", "%Y-%m-%d") == 0)
        with self.assertRaises(ValueError):
            Timestamp.from_string("2004-07-28", "Y-m-d")

    def test_07_timestamp_month_timestamp_tuple(self) -> None:
        """Test Timestamp.month_timestamp_tuple() method.

        This comprehensive test verifies the functionality of month_timestamp_tuple(),
        ensuring it correctly returns a tuple of start and end timestamps for a given month.
        It checks for presence, return type, and element count. It also validates handling
        of different input types (timestamps, datetime objects) and gracefully fails for invalid
        inputs. The test confirms the accuracy of the returned timestamps for regular months,
        the Unix epoch, and leap years.
        """
        # check if the method present
        self.assertTrue(hasattr(Timestamp, "month_timestamp_tuple"))

        # check if the method returns tuple
        self.assertIsInstance(Timestamp.month_timestamp_tuple(), tuple)

        # check if the method returns two element tuple
        self.assertEqual(len(Timestamp.month_timestamp_tuple()), 2)

        # check the argument type: positive
        try:
            Timestamp.month_timestamp_tuple(0)
            Timestamp.month_timestamp_tuple(datetime.datetime(1970, 1, 1, 0, 0, 0))
        except Exception as e:
            self.fail()

        # check the argument type: negative
        with self.assertRaises(TypeError):
            Timestamp.month_timestamp_tuple("2015-03-24")  # type: ignore

        # check returned tuple
        try:
            start, end = Timestamp.month_timestamp_tuple(
                DateTime.datetime_from_timestamp(0, tz=datetime.timezone.utc)
            )
        except Exception as e:
            self.fail("Unexpected exception")
        self.assertEqual(int(start), 0)
        self.assertEqual(int(end), 2678399)

        dec_2023 = datetime.datetime(2023, 12, 15, tzinfo=datetime.timezone.utc)
        start_ts, end_ts = Timestamp.month_timestamp_tuple(dec_2023)

        # Expected values for December 2023 UTC
        expected_start = datetime.datetime(
            2023, 12, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
        ).timestamp()
        expected_end = datetime.datetime(
            2023, 12, 31, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc
        ).timestamp()

        self.assertEqual(start_ts, expected_start)
        self.assertEqual(end_ts, expected_end)

        # Test for a leap year (February 2024)
        feb_2024 = datetime.datetime(2024, 2, 10, tzinfo=datetime.timezone.utc)
        start_ts_leap, end_ts_leap = Timestamp.month_timestamp_tuple(feb_2024)

        expected_start_leap = datetime.datetime(
            2024, 2, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
        ).timestamp()
        expected_end_leap = datetime.datetime(
            2024, 2, 29, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc
        ).timestamp()

        self.assertEqual(start_ts_leap, expected_start_leap)
        self.assertEqual(end_ts_leap, expected_end_leap)


# #[EOF]#######################################################################
