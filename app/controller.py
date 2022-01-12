from app.intersection import Intersection
from app.direction import Direction


class Controller:
    """
    Class to control an Intersection object for this Application

    Attributes
        intersection: Intersection object that is being controlled
        pass_durr: int for the amount of time that it takes for a vehicle to exit an intersection
        next_direction: Direction object for the next Direction that will be emptied
        should_wait: bool for if a user would like to wait in real time for a cycle to finish or not. Sleep refers to
        actually sleeping the application using sleep(time)
    """
    __should_wait : bool = False

    def __init__(self, _intersection: Intersection, _pass_durr):
        """
        Initializer for a Controller object

        :param _intersection: Intersection object to be set to this object
        :param _pass_durr: int for the length of time that it takes for a car to exit the intersection being controlled
        """
        self.intersection: Intersection = _intersection
        self.pass_durr = _pass_durr
        self.next_direction = _intersection.head_direction

    def cycle(self) -> None:
        """
        Handles cycling through to the next direction, emptying this direction

        :return: None
        """
        prev_cycle_durr = self.__start_cycle(self.next_direction)
        self.__end_cycle(prev_cycle_durr)

    @property
    def should_wait(self) -> bool:
        """
        Getter method for should_wait for a Controller object

        :return: bool for the value of should_wait
        """
        return self.__should_wait

    @should_wait.setter
    def should_wait(self, new_val : bool) -> None:
        """
        Setter method for should_wait for a Controller object, new value must be a boolean

        :param new_val: bool for the new val to be set as should_wait
        :return: None
        """
        assert isinstance(new_val, bool)
        self.__should_wait = new_val

    def __start_cycle(self, next_direction: Direction) -> None:
        """
        Handles starting the next cycle of traffic from a direction

        :param next_direction: Direction object to be emptied
        :return:
        """
        cycle_durr = next_direction.cycle(self.pass_durr, should_sleep=self.should_wait)
        return cycle_durr

    def __end_cycle(self, prev_cycle_durr) -> None:
        """
        Ends the current cycle of traffic

        :param prev_cycle_durr: float for the length of the previous cycle of traffic
        :return: None
        """
        self.intersection.add_waiting_time(prev_cycle_durr)
        self.intersection.add_vehicles()
        self.next_direction = self.next_direction.next
