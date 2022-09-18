import tkinter as tk
from tkinter import font, messagebox

from tkinter import filedialog
import pickle
import time
from Space import Space
from GameMaster import GameMaster
from GOA_STATS import Stats


class GameOfLife(tk.Frame):
    def __init__(self, parent, r=10, c=10, x=[2,3], y=[3]):
        super().__init__()
        self.parent = parent
        self.size_x = r
        self.size_y = c
        self.ntka = x       # needed_to_keep_alive
        self.ntb = y        # needed_to_born

        self.actual_space = Space(self.size_x, self.size_y)

        self.game_master = GameMaster(self.actual_space, self.ntka, self.ntb)
        self.stats = Stats(self)
        self.grid_of_buttons = []

        self.generate_next = True
        self.num_of_cycles = 0
        self.after_pause = False
        self.Initial()

    def Initial(self):

        self.parent['bg'] = "white"
        self.parent.title("Game Of Life")

        # TITLE
        title_frame = tk.Frame(self.parent, bg="white", padx=5, pady=5)
        title_frame.pack()
        title_font = font.Font(family="Terminal", size = 40)
        title = tk.Label(title_frame, text="Game of Life", font=title_font, fg = "black", bg = "white")
        title.pack()

        # DESCRIPTION
        description_font = font.Font(family="Fixedsys", size = 3)
        description_frame = tk.Frame(self.parent, bg = "white", pady=5)
        description_frame.pack()

        description1 = tk.Label(description_frame, text=f"The number of cells needed for a living cell to survive: ", font=description_font,
                                fg = "black", bg = "white")
        description1.grid(column=0, row=0, sticky = tk.W, ipady = 2)

        description2 = tk.Label(description_frame, text=f"The number of cells needed for a dead cell to be born: ", font=description_font,
                                fg = "black", bg = "white")
        description2.grid(column=0, row=1, sticky = tk.W)
        description1a = tk.Label(description_frame, text=f"{self.ntka}", font=description_font,
                                 fg = "black", bg = "white")
        description1a.grid(column=1, row=0, sticky=tk.E, ipady=2)
        description2a = tk.Label(description_frame, text=f"{self.ntb}", font=description_font,
                                 fg = "black", bg = "white")
        description2a.grid(column=1, row=1, sticky=tk.E)


        # BUTTONS
        buttons_frame = tk.Frame(self.parent, bg="white", padx=5, pady=7)
        buttons_frame.pack()

        self.start_button = tk.Button(buttons_frame, text="START", font=description_font, relief=tk.SOLID, bd=1,
                                      bg="white", fg="black", activebackground="black", activeforeground="white", command=self.start_game)
        self.start_button.grid(row = 0, column=0, ipadx=10, padx=1)

        self.pause_button = tk.Button(buttons_frame, text="PAUSE", font=description_font,  state=tk.DISABLED,
                                      relief=tk.SOLID, bd=1,
                                      bg="white", fg="black", activebackground="black", activeforeground="white", command=self.pause_game)
        self.pause_button.grid(row = 0, column=1, ipadx=10, padx=1)

        self.reset_button = tk.Button(buttons_frame, text="RESET", font=description_font, state=tk.NORMAL,
                                      relief=tk.SOLID, bd=1,
                                      bg="white", fg="black", activebackground="black", activeforeground="white", command=self.reset_game)
        self.reset_button.grid(row = 0, column=2, ipadx=10, padx=1)

        self.n_to_choice_entry = tk.Entry(buttons_frame, font=description_font, selectbackground="black", relief=tk.SOLID,
                                          bd=1, justify=tk.RIGHT, width=6)
        self.n_to_choice_entry.grid(row = 0, column=3, ipadx=8, ipady=2, padx=1)

        self.roll_cells_button = tk.Button(buttons_frame, text="ROLL", font=description_font,
                                           relief=tk.SOLID, bd=1, bg="white", fg="black", activebackground="black",
                                           activeforeground="white", command=self.roll_cells)
        self.roll_cells_button.grid(row = 0, column=4, ipadx=15, padx=1)

        # STATS
        stats_frame = tk.Frame(self.parent, bg="white", padx=5, pady=5)
        stats_frame.pack()

        text_current_alive_label = tk.Label(stats_frame, text="Number of currently living cells: ", font=description_font, fg="black", bg="white")
        text_until_alive_label = tk.Label(stats_frame, text="Percentage of viable cells in the current cycle: ", font=description_font, fg="black", bg="white")
        self.current_alive_label = tk.Label(stats_frame, text="0", font=description_font, fg="black", bg="white", width=9)
        self.until_alive_label = tk.Label(stats_frame, text="0", font=description_font, fg="black", bg="white", width=9)

        self.current_alive_label.grid(row=0, column=1, sticky=tk.E, ipadx= 10)
        text_current_alive_label.grid(row=0, column=0, sticky=tk.W, ipadx=30)
        self.until_alive_label.grid(row=1, column=1, sticky=tk.E, ipadx=10)
        text_until_alive_label.grid(row=1, column=0, sticky=tk.W, ipadx=30)

        self.build_grid()

    def build_grid(self):

        game_frame = tk.Frame(self.parent, height=self.size_x, width=self.size_y, borderwidth=1, relief=tk.FLAT)
        game_frame.pack(expand=1)
        self.grid_of_buttons = [[tk.Button(game_frame, bg="black", width=2, height=1, relief=tk.SOLID, bd=0.5) for _ in range(self.size_y)] for _ in range(self.size_x)]

        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid_of_buttons[i][j].grid(row=i, column=j, sticky=tk.NSEW)
                self.grid_of_buttons[i][j]["command"] = lambda i=i, j=j: self.switch_bg(self.grid_of_buttons[i][j])

    # static method
    def switch_bg(self, button):

        if button["bg"] == "black":
            button["bg"] = "white"
        else:
            button["bg"] = "black"

    def start_game(self):

        self.off_buttons()

        if self.num_of_cycles == 0:
            self.grid_to_space()

        if self.after_pause:
            self.grid_to_space()
            self.after_pause = False

        self.num_of_cycles += 1
        self.show_current_alive()
        self.show_until_alive()

        for x, y in self.game_master.check():
            self.game_master.space.grid[x][y].change_state()
            self.switch_bg(self.grid_of_buttons[x][y])

        if self.generate_next:
            self.after(100, self.start_game)
        else:
            self.on_buttons()
            self.after_pause = True

    def off_buttons(self):

        if self.grid_of_buttons[0][0] != tk.DISABLED:
            for i in range(self.size_x):
                for j in range(self.size_y):
                    self.grid_of_buttons[i][j].configure(state=tk.DISABLED)

        self.start_button.configure(state=tk.DISABLED)
        self.pause_button.configure(state=tk.NORMAL)
        self.roll_cells_button.configure(state=tk.DISABLED)

    def on_buttons(self):

        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid_of_buttons[i][j].configure(state=tk.NORMAL)

        self.reset_button.configure(state=tk.NORMAL)
        self.pause_button.configure(state=tk.DISABLED)
        self.start_button.configure(state=tk.NORMAL)
        self.roll_cells_button.configure(state=tk.NORMAL)
        self.generate_next = True

    def pause_game(self):
        self.generate_next = False

    def reset_game(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid_of_buttons[i][j].configure(bg="black")

        self.game_master.space.reset_grid()
        self.num_of_cycles = 0
        self.stats.reset()
        self.until_alive_label.configure(text="0")
        self.current_alive_label.configure(text="0")
        self.reset_button.configure(state=tk.NORMAL)
        self.generate_next = True

    def roll_cells(self):

        n = int(self.n_to_choice_entry.get())

        if n < self.size_x * self.size_y:
            self.reset_game()
            self.actual_space.roll_alive(n)
            self.space_to_grid()
        else:
            messagebox.showerror(title="Error",
                                 message=f"Allowed values: [{1}, {self.size_x * self.size_y - 1}]")

    def show_current_alive(self):
        self.current_alive_label.configure(text=self.stats.current_alive())

    def show_until_alive(self):
        self.until_alive_label.configure(text=f"{round(self.stats.percent_of_alive_current_cycle() * 100)} %")

    def grid_to_space(self):
        for i in range(self.size_x):
            for j in range(self.size_y):

                if self.grid_of_buttons[i][j]["bg"] == "white" and not self.actual_space.grid[i][j].alive:
                    self.actual_space.grid[i][j].change_state()

                if self.grid_of_buttons[i][j]["bg"] == "black" and self.actual_space.grid[i][j].alive:
                    self.actual_space.grid[i][j].change_state()

    def space_to_grid(self):
        for i in range(self.size_x):
            for j in range(self.size_y):

                if self.grid_of_buttons[i][j]["bg"] == "white" and not self.actual_space.grid[i][j].alive:
                    self.grid_of_buttons[i][j]["bg"] = "black"

                if self.grid_of_buttons[i][j]["bg"] == "black" and self.actual_space.grid[i][j].alive:
                    self.grid_of_buttons[i][j]["bg"] = "white"

    """
        def save_game(self):
            saved_board = self.actual_space.grid[:]
            t = time.localtime()[3:6]
            name = f"{t[0]}_{t[1]}_{t[2]}__{self.size_x}x{self.size_y}"
            with open(name, "wb") as fp:
                pickle.dump(saved_board, fp)
            messagebox.showinfo(title="Game of Life", message=f"Current state of board is saved in file {t[0]}_{t[1]}_{t[2]}__{self.size_x}x{self.size_y}")

        def load_game(self):
            filename = filedialog.askopenfilename(title="Open file")
            str_filename = f"{filename}"
            if str_filename[-5:-3] == str(self.size_x) and str_filename[-2:] == str(self.size_y):   # działa dobrze dopóki ładujemy board wielkosci dwucyfrowej
                with open(str_filename, "rb") as fp:
                    self.actual_space.grid = pickle.load(fp)
                self.space_to_grid()
                messagebox.showinfo(message="voila")
            else:
                messagebox.showerror(title="Game of Life", message=f"You can only load a space {self.size_x} x {self.size_y}")
        """


if __name__ == "__main__":
    print("GAME OF LIFE \n"
          "Choose your configuration")
    w = int(input("Number of rows in your space: "))
    c = int(input("Number of columns in your space: "))
    print("\nIn original Conway's Game of Life values below should be 2 and 3")
    x = input("The number of cells needed for a living cell to survive (separate by comma): ")
    print("\nIn original Conway's Game of Life value below should be 3")
    y = input("The number of cells needed for a dead cell to be born (separate by comma: ")
    x1 = [int(i) for i in x.split(',')]
    y1 = [int(i) for i in y.split(',')]

    root = tk.Tk()
    game = GameOfLife(root, w, c, x1, y1)
    root.mainloop()