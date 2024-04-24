# -*- coding: utf-8 -*-
"""
  test_libs_queues.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 24.04.2024, 10:24:50
  
  Purpose: 
"""

import unittest
from typing import Dict, List, Optional
from jsktoolbox.libs.queues import EmptyError, Fifo


class TestQueues(unittest.TestCase):
    """Test for Queues class."""

    def test_01_create_object(self) -> None:
        """Test nr 01."""
        try:
            Fifo()
        except Exception as ex:
            self.fail(ex)

    def test_02_put_and_get_data(self) -> None:
        """Test nr 02."""
        tmp = Fifo()

        # put in
        try:
            tmp.put(1)
            tmp.put(2)
            tmp.put("abc")
        except Exception as e:
            self.fail(e)

        # get from
        try:
            tmp.pop()
            tmp.pop()
            tmp.pop()
        except Exception as e:
            self.fail(e)

        # empty test
        with self.assertRaises(EmptyError):
            tmp.pop()

    def test_03_check_data(self) -> None:
        """Test nr 03."""
        tmp = Fifo()
        tmp.put(1)
        tmp.put("abc")
        self.assertTrue(tmp.pop() == 1)
        self.assertTrue(tmp.pop() == "abc")


# #[EOF]#######################################################################
