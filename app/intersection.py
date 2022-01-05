import numpy as np
from direction import Direction


class Intersection:
    """
    Object to represent the state of a traffic-intersection

    Contains methods to manage the directions of this intersection, (CRUD actions)

    Attributes
        __head_direction head to the __directions linked list
        num_directions  length of __directions linked list
    """
    head_direction: Direction = None
    num_directions: int = 0

    def __init__(self, _head_direction, _num_directions : int):
        self.head_direction = _head_direction
        self.num_directions = _num_directions

    def add_waiting_time(self, prev_cycle_durr : int) -> None:
        """
        Adds waiting time to each of the vehicles in this intersection

        :param prev_cycle_durr: integer for the duration of the previous cycle
        :return: None
        """
        curr_direction = self.head_direction
        i = 1
        while i <= self.num_directions:
            curr_direction.add_waiting_time(prev_cycle_durr)
            curr_direction = curr_direction.next
            i += 1



    def add_direction(self, new_direction: Direction):
        """
        Adds a new direction to this intersection.

        Adds this to the end of the cyclic linked list, so that the new directions next direction is the head

        :param new_direction: new Direction object to be added
        :return: True, by convention
        """
        i = 1
        curr_direction = self.head_direction
        while i < self.num_directions:
            curr_direction = curr_direction.next
        curr_direction.next = new_direction
        new_direction.next = self.head_direction
        self.num_directions += 1

    def add_vehicles(self) -> None:
        """
        Adds vehicles to each of the directions for this intersection
        :return: None
        """
        curr_direction = self.head_direction
        for i in range(0, self.num_directions):
            curr_direction.add_vehicles()
