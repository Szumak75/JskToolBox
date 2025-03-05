# -*- coding: utf-8 -*-
"""
path_tests.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.10.2024, 09:26:00

Purpose:
"""

from typing import List
from queue import Queue, Empty

from jsktoolbox.edmctool.stars import StarsSystem
from jsktoolbox.edmctool.data import RscanData
from jsktoolbox.edmctool.math import (
    Euclid,
    AlgAStar,
    AlgGenetic,
    AlgTsp,
    AlgGenetic2,
    AlgSimulatedAnnealing,
)

if __name__ == "__main__":

    jump_range = 150
    qlog = Queue()
    rd = RscanData()
    rd.jump_range = jump_range

    euclid = Euclid(qlog, rd)
    euclid.benchmark()

    start = StarsSystem()
    start.star_pos = [0.0, 0.0, 0.0]

    systems: List[StarsSystem] = []

    for x, y, z in [
        (105.96875, -20.87500, -22.21875),
        (134.12500, 15.09375, -63.87500),
        (118.93750, -8.53125, -33.46875),
        (124.50000, 4.31250, -49.12500),
        (78.34375, -42.96875, -2.21875),
        (95.40625, -33.50000, -11.40625),
        (66.84375, -60.65625, -3.84375),
        (58.28125, -92.09375, 23.71875),
        (60.93750, -75.25000, 10.87500),
        (67.50000, -74.90625, -93.68750),
        (1.12500, 15.09375, -63.87500),
        (1180.93750, -8.53125, -33.46875),
        (12.50000, 4.31250, -49.12500),
        (7.34375, -42.96875, -2.21875),
        (995.40625, -33.50000, -11.40625),
        (6.84375, -60.65625, -3.84375),
    ]:
        tmp = StarsSystem()
        tmp.star_pos = [x, y, z]
        systems.append(tmp)

    # print(systems)

    alg = AlgAStar(
        start=start,
        systems=systems,
        jump_range=jump_range,
        log_queue=qlog,
        euclid_alg=euclid,
        plugin_name="test",
    )
    alg.run()
    count = 0
    for item in alg.get_final:
        count += 1
        print(f"{count}: {item}")
    print(f"Final distance: {alg.final_distance}")

    while True:
        try:
            item = qlog.get_nowait()
            for log in item.log:
                print(log)
        except Empty:
            break

# #[EOF]#######################################################################
