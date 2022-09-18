from Cell import Cell
from random import sample


class Space:
    def __init__(self, j, k):
        self.grid = []
        self.x = j
        self.y = k

        self.make_grid()

    def make_grid(self):
        self.grid = [[Cell() for _ in range(self.y)] for _ in range(self.x)]

    def count_alive(self):
        alives = 0
        for i in range(self.x):
            for y in range(self.y):
                if self.grid[i][y].alive:
                    alives += 1
        return alives

    def reset_grid(self):
        self.grid.clear()
        self.make_grid()

    def roll_alive(self, n):
        self.reset_grid()
        board = [(x, y) for x in range(self.x) for y in range(self.y)]
        rolled = sample(board, n)
        for x, y in rolled:
            self.grid[x][y].change_state()


if __name__ == "__main__":

    x = Space(10, 10)
    x.roll_alive(10)
    print(x.count_alive())





