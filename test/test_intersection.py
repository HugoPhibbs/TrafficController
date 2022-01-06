import unittest

import numpy as np

from app.direction import Direction
from app.intersection import Intersection


class TestIntersection(unittest.TestCase):

    def setUp(self) -> None:
        n_waiting_list = [8, 6, 5, 2, 1]
        self.north_1 = Direction("North", n_waiting_list, 3)

        e_waiting_list = [3, 2, 2, 1, 0]
        east = Direction("East", e_waiting_list, 2)

        s_waiting_list = [11, 10, 9, 9, 6, 5, 4, 4, 2, 1]
        south = Direction("South", s_waiting_list, 4)

        w_waiting_list = [6, 6, 3, 2, 2]
        self.west_1 = Direction("West", w_waiting_list, 5)

        self.north_1.next = east
        east.next = south
        south.next = self.west_1
        self.west_1.next = self.north_1

        self.intersection_1 = Intersection(self.north_1, 4)

    def test_add_waiting_time(self) -> None:
        inter_1 = self.intersection_1
        prev_cycle_durr = 3
        north_1 = inter_1.head_direction
        waiting_times_n_b = north_1.waiting_times
        west_1: Direction = north_1.next.next.next
        waiting_times_w_b = west_1.waiting_times
        inter_1.add_waiting_time(prev_cycle_durr)
        self.assertTrue(np.array_equal(north_1.waiting_times, np.add(waiting_times_n_b, prev_cycle_durr)))
        self.assertTrue(np.array_equal(west_1.waiting_times, np.add(waiting_times_w_b, prev_cycle_durr)))

    def test_add_direction(self) -> None:
        # Test normally
        new_direction = Direction("new", [1, 1], 3)
        self.intersection_1.add_direction(new_direction)
        self.assertEqual(new_direction.next, self.north_1)
        self.assertEqual(self.west_1.next, new_direction)

        # Test with a intersection with only 2 directions
        self.north_1.next = self.west_1

    def test_remove_direction(self):
        # Add some more directions to make it more interesting
        self.intersection_1.add_direction(Direction("new_1"))
        self.intersection_1.add_direction(Direction("new_2"))
        # Test with a direction that is the head of the cyclic linked list
        self.assertTrue(self.intersection_1.remove_direction(self.north_1))
        #self.
        # Test with a direction that is at the end of the cyclic linked list
        # Test with a direction that is in the middle of the cyclic linked list
        # Test with an intersection with 2 directions

    def test_calc_num_directions(self):
        # Test with a cyclic linked list of length one
        self.assertEqual(Intersection.calc_num_directions(Direction("new_1")), 1)
        # Test with an empty linked list
        self.assertEqual(Intersection.calc_num_directions(None), 0)
        # Test with a linked list with multiple entries
        self.assertEqual(self.intersection_1.calc_num_directions(self.north_1), 4)


if __name__ == '__main__':
    unittest.main()
