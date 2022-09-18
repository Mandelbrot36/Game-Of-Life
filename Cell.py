
class Cell:
    def __init__(self):
        self.alive = False

    def change_state(self):
        self.alive = not self.alive


