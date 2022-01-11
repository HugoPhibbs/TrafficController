import unittest

import numpy as np

from app.direction import Direction
from app.intersection import Intersection


class TestIntersection(unittest.TestCase):

    def setUp(self) -> None:
        pass
        n_waiting_list = [8, 6, 5, 2, 1]
        self.north_1 = Direction("North", n_waiting_list, 3)

        e_waiting_list = [3, 2, 2, 1, 0]
        self.west_1 = Direction("East", e_waiting_list, 2)

        s_waiting_list = [11, 10, 9, 9, 6, 5, 4, 4, 2, 1]
        self.south_1 = Direction("South", s_waiting_list, 4)

        w_waiting_list = [6, 6, 3, 2, 2]
        self.east_1 = Direction("West", w_waiting_list, 5)

        self.north_1.next = self.west_1
        self.west_1.next = self.south_1
        self.south_1.next = self.east_1
        self.east_1.next = self.north_1

        self.intersection_1 = Intersection(self.north_1)

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
        self.assertEqual(self.east_1.next, new_direction)
        self.assertEqual(5, self.intersection_1.num_directions)

        # Test with an intersection with only 2 directions
        self.north_1.next = self.east_1
        self.east_1.next = self.north_1
        self.intersection_1.head_direction = self.north_1
        self.intersection_1.add_direction(new_direction)
        self.assertEqual(3, self.intersection_1.num_directions)

    def test_remove_direction(self):
        # Add some more directions to make it more interesting
        direction_1 = Direction("new_1")
        direction_2 = Direction("new_2")
        self.intersection_1.add_direction(direction_1)
        self.intersection_1.add_direction(direction_2)

        self.assertTrue(6, self.intersection_1.num_directions)

        # Test with a direction that is the head of the circular linked list
        self.assertTrue(self.intersection_1.remove_direction(self.north_1))
        self.assertEqual(5, self.intersection_1.num_directions)

        # Test with a direction that is at the end of the circular linked list
        self.assertTrue(self.intersection_1.remove_direction(direction_2))

        # Test with a direction that is in the middle of the cyclic linked list
        self.assertTrue(self.intersection_1.remove_direction(self.south_1))

        # Test with a direction that is not in the linked list
        self.assertFalse(self.intersection_1.remove_direction(self.north_1))

        # Test with None input
        self.assertFalse(self.intersection_1.remove_direction(None))

        # Test with an intersection with 2 directions
        direction_1.next = direction_2
        direction_2.next = direction_1
        self.intersection_1.head_direction = direction_1
        self.assertRaises(AssertionError, self.intersection_1.remove_direction, direction_1)

    def test___contains__(self):
        # Test with None input
        self.assertFalse(None in self.intersection_1)

        # Test with a random object
        self.assertFalse("a string" in self.intersection_1)

        # Test with a Direction object that is not contained
        self.assertFalse(Direction("new_1") in self.intersection_1)

        # Test with a Direction that is at head of linked list
        self.assertTrue(self.north_1 in self.intersection_1)

        # Test with a Direction that is at the end of linked list
        self.assertTrue(self.east_1 in self.intersection_1)

        # Test with a Direction that is in the middle of the linked list
        self.assertTrue(self.south_1 in self.intersection_1)

    def test_list_length(self):
        direction_1 = Direction("new_1")

        # Test with an empty linked list
        self.assertEqual(0, Intersection.list_length(None))

        # Test with a cyclic linked list of length one, acyclic
        self.assertEqual(1, Intersection.list_length(direction_1))

        # Test with a cyclic linked list of length one, cyclic
        direction_1.next = direction_1
        self.assertEqual(1, Intersection.list_length(direction_1))

        # Test with a circular linked list with multiple entries
        self.assertEqual(4, Intersection.list_length(self.north_1))

        # Test with a cyclic, but not circular linked list with multiple entries
        self.east_1.next = self.west_1
        self.assertEqual(4, Intersection.list_length(self.north_1))

        # Test with a regular linked list (acyclic) with multiple entries
        self.east_1.next = None
        self.assertEqual(4, Intersection.list_length(self.north_1))

        # Test with a regular linked list (acyclic) with 2 entries
        self.west_1.next = None
        self.assertEqual(2, Intersection.list_length(self.north_1))

        # Test with a circular linked list with 2 entries
        self.west_1.next = self.north_1
        self.assertEqual(2, Intersection.list_length(self.north_1))

        # Test with a cyclic, but not circular linked list with 2 entries
        self.west_1.next = self.west_1
        self.assertEqual(2, Intersection.list_length(self.north_1))


    def test_list_is_circular(self):
        # Test with a linked list that is regular
        node_1 = Direction("node_1")
        node_2 = Direction("node_2")
        node_3 = Direction("node_3")
        node_4 = Direction("node_4")
        node_1.next = node_2
        node_2.next = node_3
        node_3.next = node_4
        self.assertFalse(Intersection.list_is_circular(node_1))

        # Test with a linked with one node
        node_1.next = None
        self.assertFalse(Intersection.list_is_circular(node_1))

        # Test with an input of None
        self.assertFalse(Intersection.list_is_circular(None))

        # Test with a linked list that is circular, but next points to itself
        node_1.next = node_1
        self.assertTrue(Intersection.list_is_circular(node_1))

        # Test with a linked list that is cyclic, but not circular
        node_1.next = node_2
        node_4.next = node_2
        self.assertFalse(Intersection.list_is_circular(node_1))

        # Test with a linked list that is circular, with 2 nodes
        node_2.next = node_1
        self.assertTrue(Intersection.list_is_circular(node_1))

        # Test with a linked list that is circular, with a length of more than 2
        node_2.next = node_3
        node_4.next = node_1
        self.assertTrue(Intersection.list_is_circular(node_1))

if __name__ == '__main__':
    unittest.main()
