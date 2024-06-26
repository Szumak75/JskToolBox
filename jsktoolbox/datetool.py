# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 02.12.2023

  Purpose: Sets of classes for various date/time operations.
"""

from time import time
from datetime import datetime, timezone, timedelta
from typing import Optional, Union
from inspect import currentframe

from jsktoolbox.attribtool import NoNewAttributes
from jsktoolbox.raisetool import Raise


class DateTime(NoNewAttributes):
    """DateTime class for generating various datetime structures."""

    @classmethod
    def now(cls, tz: Optional[timezone] = None) -> datetime:
        """Return datetime.datetime.now() object.

        ### Arguments:
        tz [datetime.timezone] - datetime.timezone.utc for UTC, default None for current set timezone.
        """
        return datetime.now(tz=tz)

    @classmethod
    def datetime_from_timestamp(
        cls,
        timestamp_seconds: Union[int, float],
        tz: Optional[timezone] = None,
    ) -> datetime:
        """Returns datetime from timestamp int."""
        if not isinstance(timestamp_seconds, (int, float)):
            raise Raise.error(
                f"Expected int or float type, received: '{type(timestamp_seconds)}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return datetime.fromtimestamp(timestamp_seconds, tz=tz)

    @classmethod
    def elapsed_time_from_seconds(cls, seconds: Union[int, float]) -> timedelta:
        """Convert given seconds to timedelta structure."""
        if not isinstance(seconds, (int, float)):
            raise Raise.error(
                f"Expected int or float type, received: '{type(seconds)}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return timedelta(seconds=seconds)

    @classmethod
    def elapsed_time_from_timestamp(
        cls, seconds: Union[int, float], tz: Optional[timezone] = None
    ) -> timedelta:
        """Generate date/time timedelta with elapsed time, from given timestamp to now.

        ### WARNING:
        Returns the timedelta accurate to the second.
        """
        if not isinstance(seconds, (int, float)):
            raise Raise.error(
                f"Expected int or float type, received: '{type(seconds)}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        out: timedelta = cls.now(tz=tz) - datetime.fromtimestamp(seconds, tz=tz)
        return timedelta(days=out.days, seconds=out.seconds)


class Timestamp(NoNewAttributes):
    """Timestamp class for getting current timestamp."""

    @classmethod
    @property
    def now(cls) -> int:
        """Return current timestamp as int."""
        return int(time())

    @classmethod
    def from_string(cls, date_string: str, format: str) -> int:
        """Returns timestamp from string in strptime format.

        ### Arguments
        * date_string [str] - date/time string to parse,
        * format [str] - string with date/time format, for example: '%Y-%m-%d'

        ### Returns
        timestamp as int
        """
        try:
            element: datetime = datetime.strptime(date_string, format)
        except ValueError as ex:
            raise Raise.error(f"{ex}", ValueError, cls.__qualname__, currentframe())
        except Exception as ex:
            raise ex

        return int(datetime.timestamp(element))


# #[EOF]#######################################################################
