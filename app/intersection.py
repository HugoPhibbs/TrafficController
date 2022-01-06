from app.direction import Direction


class Intersection:
    """
    Object to represent the state of a traffic-intersection

    Contains methods to manage the directions of this intersection, (CRUD actions)

    Attributes
        __head_direction head to the __directions linked list
        num_directions  length of __directions linked list
    """
    head_direction: Direction = None
    __num_directions: int = 0

    def __init__(self, _head_direction, _num_directions: int):
        self.head_direction = _head_direction
        self.__num_directions = Intersection.calc_num_directions(_head_direction)

    @staticmethod
    def calc_num_directions(head_direction : Direction) -> int:
        """
        Calculates the number of Directions for a given cyclic Direction linked list object

        :param head_direction: Direction object that points to the front of the cyclic linked list
        :return: int for the number of objects in the cyclic linked list
        """
        if head_direction is None:
            return 0
        num = 1
        curr_direction = head_direction.next
        while curr_direction is not head_direction:
            num += 1
            curr_direction = curr_direction.next
        return num

    def set_head_direction(self, head_direction : Direction):
        # Check if length is not 0
        pass

    def list_is_cyclic(self):
        pass

    def set_num_directions(self):
        pass

    def add_waiting_time(self, prev_cycle_durr: int) -> None:
        """
        Adds waiting time to each of the vehicles in this intersection

        :param prev_cycle_durr: integer for the duration of the previous cycle. Must be >= 0, otherwise an error is thrown
        :return: None
        """
        curr_direction = self.head_direction
        i = 1
        assert prev_cycle_durr >= 0
        while i <= self.__num_directions:
            curr_direction.add_waiting_time(prev_cycle_durr)
            curr_direction = curr_direction.next
            i += 1

    def remove_direction(self, direction) -> bool:
        """
        Removes a direction from this intersection

        :param direction: Direction object to be removed from this Intersection
        :return: Boolean if the inputted Direction object was removed or not
        """
        i = 1
        if self.head_direction == direction:
            curr_direction = self.head_direction
            while i < self.__num_directions:
                i += 1
                curr_direction = curr_direction.next
            curr_direction.next = self.head_direction.next
            self.head_direction = self.head_direction
            self.__num_directions -= 1
            return True
        else:
            prev_direction = self.head_direction
            curr_direction = self.head_direction.next
            while i <= self.__num_directions:
                if curr_direction == direction:
                    prev_direction.next = curr_direction.next
                    return True
                else:
                    curr_direction = curr_direction.next
                    prev_direction = prev_direction.next
                i += 1
            self.__num_directions -= 1
            return False

    def add_direction(self, new_direction: Direction):
        """
        Adds a new direction to this intersection.

        Adds this to the end of the cyclic linked list, so that the new directions next direction is the head

        :param new_direction: new Direction object to be added
        :return: True, by convention
        """
        i = 1
        curr_direction = self.head_direction
        while i < self.__num_directions:
            curr_direction = curr_direction.next
            i += 1
        curr_direction.next = new_direction
        new_direction.next = self.head_direction
        self.__num_directions += 1

    def add_vehicles(self) -> None:
        """
        Adds vehicles to each of the directions for this intersection
        :return: None
        """
        curr_direction = self.head_direction
        for i in range(0, self.__num_directions):
            curr_direction.add_vehicles()
