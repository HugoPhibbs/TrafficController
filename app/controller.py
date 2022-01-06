from app.intersection import Intersection
from app.direction import Direction

class Controller:

    def __init__(self, _intersection : Intersection, _pass_durr):
        self.intersection : Intersection = _intersection
        self.pass_durr = _pass_durr
        self.next_direction = _intersection.head_direction

    def cycle(self):
        prev_cycle_durr = self.start_cycle(self.next_direction)
        self.end_cycle(prev_cycle_durr)

    def start_cycle(self, next_direction : Direction):
        cycle_durr = next_direction.empty(self.pass_durr)
        return cycle_durr

    def end_cycle(self, prev_cycle_durr):
        self.intersection.add_waiting_time(prev_cycle_durr)
        self.intersection.add_vehicles()
        self.next_direction = self.next_direction.next

    def start(self):
        self.cycle()


