# -*- coding: utf-8 -*-
"""
  test_edmctool_math.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2024, 16:03:19
  
  Purpose: 
"""

import unittest

from queue import SimpleQueue
from typing import List

from jsktoolbox.edmctool.stars import StarsSystem
from jsktoolbox.edmctool.data import RscanData
from jsktoolbox.edmctool.math import (
    Euclid,
    AlgAStar,
    AlgGeneric,
    AlgGenetic,
    AlgGenetic2,
    AlgSimulatedAnnealing,
    AlgTsp,
)


class TestEuclid(unittest.TestCase):
    """Tests for Euclid class."""

    def test_01_create(self) -> None:
        """Test creation of Euclid object."""
        euclid = Euclid(queue=SimpleQueue(), r_data=RscanData())
        self.assertIsInstance(euclid, Euclid)

    def test_02_distance(self) -> None:
        """Test distance calculation."""
        euclid = Euclid(queue=SimpleQueue(), r_data=RscanData())
        self.assertIsNotNone(euclid.distance([0, 0, 0], [1, 1, 1]))
        self.assertGreater(euclid.distance([0, 0, 0], [1, 1, 1]), 1)

        a: float = euclid.distance([0, 0, 0], [1, 1, 1])
        euclid.benchmark()
        b: float = euclid.distance([0, 0, 0], [1, 1, 1])
        self.assertEqual(a, b)


class TestPathFinderAlg(unittest.TestCase):
    """Tests for  path finder algorithms."""

    def setUp(self) -> None:
        # add initial point
        self.start = StarsSystem()
        self.start.name = "Sol"
        self.start.star_pos = [0, 0, 0]
        self.math = Euclid(queue=SimpleQueue(), r_data=RscanData())
        self.math.benchmark()
        # add points list
        self.points: List[StarsSystem] = []
        for point in [
            # (200, 0, 0),
            (50, 0, 0),
            (40, 0, 0),
            (30, 0, 0),
            (20, 0, 0),
            (10, 0, 0),
        ]:
            tmp = StarsSystem()
            tmp.name = f"Star_{point[0]}"
            tmp.star_pos = list(point)
            self.points.append(tmp)

    def test_01_generic(self) -> None:
        """Test nr 01."""
        try:
            alg = AlgGeneric(
                log_queue=SimpleQueue(),
                start=self.start,
                systems=self.points,
                jump_range=50,
                euclid_alg=self.math,
                plugin_name="test",
            )
            alg.run()
        except Exception as e:
            self.fail(e)

        self.assertEqual(alg.final_distance, 50.0)
        self.assertEqual(len(alg.get_final), 5)
        self.assertEqual(alg.get_final[0].pos_x, 10)
        self.assertEqual(alg.get_final[1].pos_x, 20)
        self.assertEqual(alg.get_final[2].pos_x, 30)
        self.assertEqual(alg.get_final[3].pos_x, 40)
        self.assertEqual(alg.get_final[4].pos_x, 50)

    def test_02_genetic(self) -> None:
        """Test nr 02."""
        try:
            alg = AlgGenetic(
                log_queue=SimpleQueue(),
                start=self.start,
                systems=self.points,
                jump_range=50,
                euclid_alg=self.math,
                plugin_name="test",
            )
            alg.run()
        except Exception as e:
            self.fail(e)

        self.assertEqual(alg.final_distance, 50.0)
        self.assertEqual(len(alg.get_final), 5)
        self.assertEqual(alg.get_final[0].pos_x, 10)
        self.assertEqual(alg.get_final[1].pos_x, 20)
        self.assertEqual(alg.get_final[2].pos_x, 30)
        self.assertEqual(alg.get_final[3].pos_x, 40)
        self.assertEqual(alg.get_final[4].pos_x, 50)

    def test_03_genetic2(self) -> None:
        """Test nr 03."""
        try:
            alg = AlgGenetic2(
                log_queue=SimpleQueue(),
                start=self.start,
                systems=self.points,
                jump_range=50,
                euclid_alg=self.math,
                plugin_name="test",
            )
            alg.run()
        except Exception as e:
            self.fail(e)

        self.assertEqual(alg.final_distance, 50.0)
        self.assertEqual(len(alg.get_final), 5)
        self.assertEqual(alg.get_final[0].pos_x, 10)
        self.assertEqual(alg.get_final[1].pos_x, 20)
        self.assertEqual(alg.get_final[2].pos_x, 30)
        self.assertEqual(alg.get_final[3].pos_x, 40)
        self.assertEqual(alg.get_final[4].pos_x, 50)

    def test_04_a_star(self) -> None:
        """Test nr 04."""
        try:
            alg = AlgAStar(
                log_queue=SimpleQueue(),
                start=self.start,
                systems=self.points,
                jump_range=50,
                euclid_alg=self.math,
                plugin_name="test",
            )
            alg.run()
        except Exception as e:
            self.fail(e)

        self.assertEqual(alg.final_distance, 50.0)
        self.assertEqual(len(alg.get_final), 5)
        self.assertEqual(alg.get_final[0].pos_x, 10)
        self.assertEqual(alg.get_final[1].pos_x, 20)
        self.assertEqual(alg.get_final[2].pos_x, 30)
        self.assertEqual(alg.get_final[3].pos_x, 40)
        self.assertEqual(alg.get_final[4].pos_x, 50)

    def test_05_sa(self) -> None:
        """Test nr 05."""
        try:
            alg = AlgSimulatedAnnealing(
                log_queue=SimpleQueue(),
                start=self.start,
                systems=self.points,
                jump_range=50,
                euclid_alg=self.math,
                plugin_name="test",
            )
            alg.run()
        except Exception as e:
            self.fail(e)

        self.assertEqual(alg.final_distance, 50.0)
        self.assertEqual(len(alg.get_final), 5)
        self.assertEqual(alg.get_final[0].pos_x, 10)
        self.assertEqual(alg.get_final[1].pos_x, 20)
        self.assertEqual(alg.get_final[2].pos_x, 30)
        self.assertEqual(alg.get_final[3].pos_x, 40)
        self.assertEqual(alg.get_final[4].pos_x, 50)

    def test_06_tsp(self) -> None:
        """Test nr 06."""
        try:
            alg = AlgTsp(
                log_queue=SimpleQueue(),
                start=self.start,
                systems=self.points,
                jump_range=50,
                euclid_alg=self.math,
                plugin_name="test",
            )
            alg.run()
        except Exception as e:
            self.fail(e)

        self.assertEqual(alg.final_distance, 50.0)
        self.assertEqual(len(alg.get_final), 5)
        self.assertEqual(alg.get_final[0].pos_x, 10)
        self.assertEqual(alg.get_final[1].pos_x, 20)
        self.assertEqual(alg.get_final[2].pos_x, 30)
        self.assertEqual(alg.get_final[3].pos_x, 40)
        self.assertEqual(alg.get_final[4].pos_x, 50)


# #[EOF]#######################################################################
