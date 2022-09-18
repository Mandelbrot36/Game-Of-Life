class Stats:
    def __init__(self, goa):
        self.goa = goa
        self.num_of_frames = 0
        self.num_of_alives = 0

    def current_alive(self):
        x = self.goa.actual_space.count_alive()
        self.num_of_alives += x
        return x

    def percent_of_alive_current_cycle(self):
        y = self.goa.num_of_cycles * self.goa.size_x * self.goa.size_y
        return self.num_of_alives / y

    def reset(self):
        self.num_of_alives=0
        self.num_of_frames=0

