from Space import Space


class GameMaster:
    def __init__(self, space,  x, y):
        self.needed_to_keep_alive = x
        self.needed_to_born = y
        self.space = space
        # self.cells_to_change = []

    def check_neighbours(self, x_cord, y_cord):
        alives = 0
        for i in range(x_cord - 1, x_cord + 2):
            for j in range(y_cord - 1, y_cord + 2):

                if i < 0 or j < 0 or i >= self.space.x or j >= self.space.y or (i == x_cord and j == y_cord):
                    continue

                if self.space.grid[i][j].alive:
                    alives += 1

        return alives

    def check(self):
        cells_to_change = []
        for i in range(self.space.x):
            for j in range(self.space.y):
                actual = self.space.grid[i][j]
                num_of_alive_neighbours = self.check_neighbours(i, j)

                # Żywa bez odpowiedniej liczby sąsiadów umiera
                if actual.alive and num_of_alive_neighbours not in self.needed_to_keep_alive:
                    cells_to_change.append((i, j))

                # Martwa z odpowiednią ilością sąsiadów ożywa
                if not actual.alive and num_of_alive_neighbours in self.needed_to_born:
                    cells_to_change.append((i, j))

                # Reszta pozostaje

        return cells_to_change

    def change_space_state(self):

        for x, y in self.check():
            self.space.grid[x][y].change_state()



if __name__ == "__main__":
    space = Space(10, 10)
    master = GameMaster(space, [2,3], [3])
    master.space.roll_alive(10)
    print(master.space.count_alive())
    master.change_space_state()
    print(master.space.count_alive())

