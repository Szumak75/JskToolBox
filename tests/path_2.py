# -*- coding: utf-8 -*-
"""
path.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.10.2024, 00:00:38

Purpose:
"""

import math
from typing import Optional, List


def distance(point_1: List[float], point_2: List[float]) -> Optional[float]:
    """Calculate distance  between two points in 3D space"""
    try:
        return math.dist(point_1, point_2)
    except Exception as ex:
        print(f"{ex}")
    return None


class StarsSystem:

    star_pos: Optional[List[float]] = None

    def __init__(self, x: float, y: float, z: float) -> None:
        self.star_pos = [x, y, z]


class AlgAStar:

    __start: Optional[StarsSystem] = None
    __systems: Optional[List[StarsSystem]] = None
    __jump_range: Optional[int]
    __final: List[StarsSystem]

    def __init__(
        self, start: StarsSystem, systems: List[StarsSystem], jump_range: int
    ) -> None:
        self.__start = start
        self.__systems = systems
        self.__jump_range = jump_range
        self.__final = []

    def run(self) -> List[StarsSystem]:
        """Algorytm A* wyszukujący najkrótszą ścieżkę od punktu od punktu *start*
        poprzez punkty z listy *systems* przy założeniach:
         - boki grafu o długości przekraczającej *jump_range* mają zostać wykluczone z rozwiązania,
         - algorytm ma przejść przez jak największą liczbę punktów, w optymalnych warunkach przez wszystkie,
         - każdy z punktów *systems* łącznie z punktem startowym ma być odwiedzony tylko raz
         - wyznaczona lista punktów we właściwej kolejności bez punktu startowego umieszczona zostaje w zmiennej *self.__final*
        """

        return self.__final


if __name__ == "__main__":

    start = StarsSystem(0.0, 0.0, 0.0)
    systems: List[StarsSystem] = [
        StarsSystem(67.50000, -74.90625, -93.68750),
        StarsSystem(134.12500, 15.09375, -63.87500),
        StarsSystem(124.50000, 4.31250, -49.12500),
        StarsSystem(118.93750, -8.53125, -33.46875),
        StarsSystem(105.96875, -20.87500, -22.21875),
        StarsSystem(95.40625, -33.50000, -11.40625),
        StarsSystem(78.34375, -42.96875, -2.21875),
        StarsSystem(66.84375, -60.65625, -3.84375),
        StarsSystem(60.93750, -75.25000, 10.87500),
        StarsSystem(58.28125, -92.09375, 23.71875),
    ]
    jump_range = 150

    path_a_star = AlgAStar(start, systems, jump_range).run()


# #[EOF]#######################################################################
