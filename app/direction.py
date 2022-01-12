from time import sleep
import numpy as np
from numpy import ndarray


class Direction:
    """
    Class representing a Direction object.

    Essentially, a direction is one way a vehicle can enter an intersection.

    Directions form nodes in a circular linked list that makes up a complete intersection

    Attributes
        next: the next Direction object in the linked list as described
        waiting_times: ndarray representing the waiting times of each of the vehicles in this intersection
        name: str for the name of this intersection
    """
    next = None
    waiting_times: ndarray = None
    __name: str = None

    def __init__(self, _name: str, _waiting_times: list = [], _avg_flow: int = 0, _cycle_size: int = 0.5):
        """
        Initializer for a Direction object

        :param _name: string for the name of this Direction for ease of identification
        :param _waiting_times: list for the current waiting times for this direction
        :param _avg_flow: int for the average flow for this Direction per cycle
        :param _cycle_size: float for the proportion of vehicles to be emptied from this intersection per cycle
        """
        self.__name: str = _name
        self.waiting_times = np.array(_waiting_times)
        self.avg_flow: int = _avg_flow
        self.cycle_size = _cycle_size

    @property
    def cycle_size(self) -> float:
        """
        Getter method for the cycle size of this Direction object

        :return: float for cycle size
        """
        return self.__cycle_size

    @cycle_size.setter
    def cycle_size(self, val: float) -> None:
        """
        Setter for the cycle size of this Direction

        Must be a float between 0 and 1

        :param val: float for the value to be set as the cycle size of this Direction
        :return:
        """
        assert isinstance(val, float) and 0 < val < 1
        self.__cycle_size = val

    @property
    def cum_waiting_time(self) -> int:
        """
        Finds the total waiting time for this Direction

        :return: int for the total waiting time of this intersection
        """
        return np.sum(self.waiting_times)

    @property
    def name(self) -> str:
        """
        Getter method for the name of this Direction object

        :return: str for the name as described
        """
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Setter method for the name of this Direction object

        :param new_name: str for the new name to be set
        :return: None
        """
        self.__name = new_name

    @property
    def is_empty(self) -> bool:
        """
        Finds if this direction is empty of vehicles or not
        :return:
        """
        return self.num_vehicles == 0

    def cycle(self, p, should_sleep : bool = False) -> float:
        """
        Empties this direction for the required volume as specified by self.cycle_volume()

        :param p: the required time for a single vehicle to exit the intersection given a green light
        :param should_sleep bool if a user would like to sleep the application in real time to reflect the passing of
        traffic through the intersection. Useful for doing integration and performance testing
        :return: float for the total length of this cycle for this direction. Used to add waiting times to the rest of
        vehicles that are still waiting their turn
        """
        cycle_durr = 0
        if not self.is_empty:
            cycle_volume = self.cycle_volume()
            cycle_durr = cycle_volume * p
            self.waiting_times = self.waiting_times[cycle_volume:]
            if should_sleep:
                sleep(cycle_durr)
        return cycle_durr + 2  # To account for time to switch between directions

    @property
    def num_vehicles(self) -> int:
        """
        Returns the number of vehicles in this direction

        :return: integer as described
        """
        return self.waiting_times.size

    def add_waiting_time(self, waiting_time) -> None:
        """
        Adds waiting time to each vehicle for this particular direction of traffic

        :param waiting_time: the waiting time to be added to all cars for this direction
        :return: None
        """
        self.waiting_times += waiting_time

    def add_vehicles(self, num_vehicles: int = None) -> None:
        """
        Adds a set number of vehicles to the queue for this direction

        Assumes that a 'pod' of vehicles arrives in this direction all at once, which is basically what happens anyway.

        If num_vehicles is left empty, then it adds vehicles based on a normal distribution around the avg flow

        :param num_vehicles: number of vehicles to be added. Must be a positive integer
        :return: None
        """
        if num_vehicles is not None:
            assert isinstance(num_vehicles, int) and num_vehicles >= 0, \
                "Number of vehicles must be an integer greater than or equal to zero!"
        else:
            num_vehicles = int(abs(np.floor(np.random.normal(self.avg_flow))))
        np.concatenate((self.waiting_times, [0] * num_vehicles))

    def cycle_volume(self) -> int:
        """
        Returns the volume of vehicles to be emptied from this direction for a cycle
        of the traffic system for a particular direction

        Finds the volume of vehicles required to half the total waiting time of all vehicles
        for this particular direction

        :return: cycle volume as described
        """
        curr_total = self.cum_waiting_time
        req_total = int(curr_total * self.cycle_size)
        volume = 0
        i = 0
        while curr_total > req_total:
            volume += 1
            curr_total -= self.waiting_times[i]
        return volume
