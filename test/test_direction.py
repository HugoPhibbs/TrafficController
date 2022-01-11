import unittest

from app.direction import Direction


class TestDirection(unittest.TestCase):

    def setUp(self):
        self.direction_1 = Direction("direction_1", [], 3)

    def test_add_vehicles(self):
        # Test normally
        self.direction_1.add_vehicles(3)
        self.assertEqual(3, len(self.direction_1))

        # Test with negative input
        self.assertRaises(AssertionError, self.direction_1.add_vehicles, -1)
        self.assertRaises(AssertionError, self.direction_1.add_vehicles, -1.5)

        # Test with non-integer input
        self.assertRaises(AssertionError, self.direction_1.add_vehicles, 1.5)

        # Test with empty input, pretty much check that no errors are thrown
        self.direction_1.add_vehicles()
        self.direction_1.add_vehicles(2)

        # Test with string input
        self.assertRaises(AssertionError, self.direction_1.add_vehicles, "a string")

    def test_cycle_size(self):
        # Test normally
        self.direction_1.cycle_size = 0.1
        self.assertEqual(0.1, self.direction_1.cycle_size)

        def set_cycle_size(direction: Direction, val : any) -> None:
            """ Function to test cycle_size setter"""
            direction.cycle_size = val

        # Test boundaries
        self.assertRaises(AssertionError, set_cycle_size, self.direction_1, 1)
        self.assertRaises(AssertionError, set_cycle_size, self.direction_1, 0)
        self.assertRaises(AssertionError, set_cycle_size, self.direction_1, -1)
        self.assertRaises(AssertionError, set_cycle_size, self.direction_1, 2)

        # Test with None input
        self.assertRaises(AssertionError, set_cycle_size, self.direction_1, None)

        # Test with string input
        self.assertRaises(AssertionError, set_cycle_size, self.direction_1, "a string")
