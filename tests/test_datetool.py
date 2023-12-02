# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 02.12.2023

  Purpose: For testing classes from datetool module.
"""

import unittest
import time

from jsktoolbox.datetool import Timestamp


class TestDateTool(unittest.TestCase):
    """Test class for DateTool module."""

    def test_01_Timestamp(self):
        """Test nr 01."""
        self.assertIsInstance(Timestamp.now, int)
        tnow = Timestamp.now
        now = int(time.time())
        self.assertTrue(tnow < now + 2 and tnow > now - 2)


# #[EOF]#######################################################################
