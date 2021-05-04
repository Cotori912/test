from tkinter import Frame, Label, CENTER
import random

import control
import go as a


def gen():
    return random.randint(0, a.GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {a.KEY_UP: control.up, a.KEY_DOWN: control.down,
                         a.KEY_LEFT: control.left, a.KEY_RIGHT: control.right,
                         a.KEY_UP_ALT: control.up, a.KEY_DOWN_ALT: control.down,
                         a.KEY_LEFT_ALT: control.left, a.KEY_RIGHT_ALT: control.right,
                         a.KEY_H: control.left, a.KEY_L: control.right,
                         a.KEY_K: control.up, a.KEY_J: control.down}

        self.grid_cells = []
        self.init_grid()
        self.matrix = control.new_game(a.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=a.BACKGROUND_COLOR_GAME,
                           width=a.SIZE, height=a.SIZE)
        background.grid()

        for i in range(a.GRID_LEN):
            grid_row = []
            for j in range(a.GRID_LEN):
                cell = Frame(background, bg=a.BACKGROUND_COLOR_CELL_EMPTY,
                             width=a.SIZE / a.GRID_LEN,
                             height=a.SIZE / a.GRID_LEN)
                cell.grid(row=i, column=j, padx=a.GRID_PADDING,
                          pady=a.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=a.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=a.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(a.GRID_LEN):
            for j in range(a.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=a.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=a.BACKGROUND_COLOR_DICT[new_number],
                                                    fg=a.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == a.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = control.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                if control.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=a.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=a.BACKGROUND_COLOR_CELL_EMPTY)
                if control.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=a.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=a.BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2


game_grid = GameGrid()
