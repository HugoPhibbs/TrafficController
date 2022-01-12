from app.direction import Direction


class Intersection:
    """
    Object to represent the state of a traffic-intersection

    Contains methods to manage the directions of this intersection, (CRUD actions)

    Attributes
        head_direction head to the linked list made of Direction objects
        num_directions length of the Direction linked list
    """
    __num_directions: int

    def __init__(self, head):
        """
        Initializer for an Intersection object

        :param head: Direction object for the head of the linked list for this intersection
        """
        self.head_direction = head

    @property
    def avg_waiting_time(self) -> float:
        """
        Finds the average waiting time per vehicle for this intersection

        :return: float as described
        """
        curr = self.head_direction.next
        total_waiting_time = self.head_direction.cum_waiting_time
        while curr is not self.head_direction:
            total_waiting_time += curr.num_vehicles
            curr = curr.next
        return total_waiting_time / self.num_vehicles

    @property
    def num_vehicles(self) -> int:
        """
        Finds the number of vehicles that are at this intersection

        :return: int as described
        """
        curr = self.head_direction.next
        total_vehicles = self.head_direction.num_vehicles
        while curr is not self.head_direction:
            total_vehicles += curr.num_vehicles
            curr = curr.next
        return total_vehicles

    @property
    def head_direction(self) -> Direction:
        """
        Getter for the head_direction Direction object for this intersection

        :return: Direction object as described
        """
        return self._head_direction

    @head_direction.setter
    def head_direction(self, head_direction: Direction) -> None:
        """
        Sets the head_direction attribute for this Class. Makes sure that it is acceptable before doing so

        Throws an error if the head_direction is not cyclic

        :param head_direction: Direction object to be set as the head_direction for this Class
        :return: None
        """
        assert Intersection.list_is_circular(head_direction)
        self._head_direction = head_direction
        self.__set_num_directions()

    @property
    def num_directions(self) -> int:
        """
        Getter for num_directions of this intersection.

        Made read only because num_direction is essential for other methods to function correctly

        :return: number of directions for this intersection
        """
        return self.__num_directions

    def __set_num_directions(self) -> None:
        """
        Sets the number of directions for this Intersection object.

        The length of an inputted linked list must be more than 2, and be cyclic

        :return:
        """
        num = Intersection.list_length(self.head_direction)
        assert num >= 2
        self.__num_directions = num

    @staticmethod
    def list_is_circular(head: Direction) -> bool:
        """
        Determines if a linked list is circular or not. By definition a linked list is circular if it contains a cycle, and the
        cycle is the length of the linked list itself.


        While some algorithms online for this assume that the linked list is either acyclic or circular, this one can account
        for an inputted linked list that is either cyclic, acyclic or circular

        :param head: Object that is the head of a linked list
        :return: bool if a linked list is circular or not
        """
        if head is None:
            return False
        cache = set()
        curr = head.next
        if curr is None:
            return False
        if curr.next is head:
            return True
        while curr is not None:
            if curr is head:
                return True
            elif curr in cache:
                return False
            else:
                cache.add(curr)
            curr = curr.next
        return False

    @staticmethod
    def list_length(head: Direction) -> int:
        """
        Calculates the length of a linked list, works for regular, circular and cyclic linked lists\

        :param head: Direction object that is the head of a linked list
        :return: int for the length of a linked list as described
        """
        if head is None:
            return 0
        cache = set()
        curr = head.next
        length = 1
        if curr is None:
            return length
        if curr is head:
            return 1
        if curr.next is head:
            return 2
        while curr is not None:
            if curr is head or curr in cache:
                return length
            else:
                cache.add(curr)
                length += 1
            curr = curr.next
        return length

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

    def __contains__(self, item) -> bool:
        """
        Checks if an Intersection contains an object.

        Really just checks if inputted item is in the Direction linked list belonging to this Intersection

        :param item: object to be checked if it is contained in this Intersection
        :return: bool if item is contained in this Intersection or not
        """
        if isinstance(item, Direction):
            curr = self.head_direction
            i = 1
            while i <= self.num_directions:
                if curr is item:
                    return True
                curr = curr.next
                i += 1
        return False

    def remove_direction(self, direction) -> bool:
        """
        Removes a direction from this intersection

        :param direction: Direction object to be removed from this Intersection
        :return: Boolean if the inputted Direction object was removed or not
        """
        i = 1
        assert self.__num_directions > 2, "Cannot remove a direction from intersection with only 2 directions!"
        if self.head_direction == direction:
            curr_direction = self.head_direction
            while i < self.__num_directions:
                i += 1
                curr_direction = curr_direction.next
            curr_direction.next = self.head_direction.next
            self.head_direction = curr_direction
            return True
        else:
            prev_direction = self.head_direction
            curr_direction = self.head_direction.next
            while i <= self.__num_directions:
                if curr_direction == direction:
                    prev_direction.next = curr_direction.next
                    self.__num_directions -= 1
                    return True
                else:
                    curr_direction = curr_direction.next
                    prev_direction = prev_direction.next
                i += 1
            return False

    def add_direction(self, new_direction: Direction) -> None:
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
        i = 0
        while i <= self.num_directions:
            curr_direction.add_vehicles()
            curr_direction = curr_direction.next
            i += 1
