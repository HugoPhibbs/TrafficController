import numpy as np
from direction import Direction
from intersection import Intersection
from controller import Controller

# Pass Duration, time for a vehicle to pass through an intersection once given green
pass_durr = 1

n_waiting_list = [8, 6, 5, 2, 1]
north = Direction("North", n_waiting_list, 3)

e_waiting_list = [3, 2, 2, 1, 0]
east = Direction("East", e_waiting_list, 2)

s_waiting_list = [11, 10, 9, 9, 6, 5, 4, 4, 2, 1]
south = Direction("South", s_waiting_list, 4)

w_waiting_list = [6, 6, 3, 2, 2]
west = Direction("West", w_waiting_list, 5)

north.next = east
east.next = south
south.next = west
west.next = north

intersection = Intersection(north, 4)

controller = Controller(intersection, pass_durr)

controller.start()
