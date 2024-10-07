# -*- coding: utf-8 -*-
"""
  test_basetool_threads.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 7.10.2024, 11:36:25
  
  Purpose: 
"""
from time import sleep
import unittest
from typing import Optional
from threading import Thread, Event
from queue import Queue, Empty

from jsktoolbox.basetool.threads import ThBaseObject


class TestThBase(unittest.TestCase):
    """Tests for ThBaseObject class."""

    def test_01_create_and_start(self) -> None:
        """Test nr 01."""

        class ThTest(ThBaseObject, Thread):
            """Testing class."""

            def __init__(self, qcom: Queue) -> None:
                Thread.__init__(self, name=self._c_name)
                self._stop_event = Event()
                self.daemon = True
                self.sleep_period = 0.1
                self._set_data(key="test", value=20, set_default_type=int)
                self._set_data(key="queue", value=qcom, set_default_type=Queue)

            def run(self) -> None:
                """Run method."""
                qcom: Optional[Queue] = self._get_data(key="queue")
                if qcom and self._stop_event:
                    while not self._stop_event.is_set():  # type: ignore
                        try:
                            item: int = qcom.get_nowait()
                            if isinstance(item, int):
                                self._set_data(key="test", value=item + self.value)
                        except Empty:
                            self._sleep(self.sleep_period)

            @property
            def value(self) -> int:
                return self._get_data(key="test")  # type: ignore

        # preparing test
        qcom = Queue()
        qcom.put(100)
        # create object
        try:
            th: ThTest = ThTest(qcom=qcom)
        except Exception as e:
            self.fail(f"{e}")
        # start
        try:
            th.start()
        except Exception as e:
            self.fail(f"{e}")
        # receive answer
        self.assertEqual(th.value, 120)
        # stop
        try:
            th.stop()
        except Exception as e:
            self.fail(f"{e}")
        # join thread
        try:
            while th.is_alive():
                sleep(0.1)
            th.join()
        except Exception as e:
            self.fail(f"{e}")


# #[EOF]#######################################################################
