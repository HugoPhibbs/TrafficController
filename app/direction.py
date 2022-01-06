from time import sleep
import numpy as np

class Direction:
    next = None

    def __init__(self, _name : str, _waiting_times : list = [], _avg_flow : int = 0):
        self.__name : str = _name
        self.waiting_times = _waiting_times
        self.avg_flow : int = _avg_flow

    def empty(self, p) -> int:
        """
        Empties this direction for the required volume as specified by self.cycle_volume()

        :param p: the required time for a single vehicle to exit the intersection given a green light
        :return: the total length of this cycle for this direciton. Used to add waiting times to the rest of
        vehicles that are still waiting their turn
        """
        cycle_volume = self.cycle_volume()
        cycle_durr = cycle_volume * p
        self.waiting_times = self.waiting_times[cycle_volume:]
        sleep(cycle_durr)
        return cycle_durr

    def add_waiting_time(self, waiting_time) -> None:
        """
        Adds waiting time to each vehicle for this particular direction of traffic

        :param waiting_time: the waiting time to be added to all cars for this direction
        :return: None
        """
        self.waiting_times = np.add(self.waiting_times, waiting_time)

    def add_vehicles(self, num_vehicles : int = None) -> None:
        """
        Adds a set number of vehicles to the queue for this direction

        Assumes that a 'pod' of vehicles arrives in this direction all at once, which is basically what happens anyway.

        If num_vehicles is left empty, then it adds vehicles based on a normal distribution around the avg flow

        :param num_vehicles: number of vehicles to be added
        :return: None
        """

        if num_vehicles is None:
            num_vehicles = abs(np.floor(np.random.normal(self.avg_flow)))
        self.waiting_times.append([0] * num_vehicles)

    def cycle_volume(self) -> int:
        """
        Returns the volume of vehicles to be emptied from this direction for a cycle
        of the traffic system for a particular direction

        Finds the volume of vehicles required to half the total waiting time of all vehicles
        for this particular direction

        :return: cycle volume as described
        """
        curr_total = sum(self.waiting_times)
        req_total = curr_total // 2
        volume = 0
        i = 0
        while curr_total > req_total:
            volume += 1
            curr_total -= self.waiting_times[i]
        return volume
