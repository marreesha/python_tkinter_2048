from tkinter import *
from tkinter import messagebox
import random


class Board:
    bg_color = {
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#feb277',
        '16': '#fd945b',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#ebdb91',
        '256': '#edcc61',
        '512': '#f2b179',
        '1024': '#f59563',
        '2048': '#edc22e',
    }
    color = {
        '2': '#776e65',
        '4': '#776e65',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#8c7761',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }
    SIZE = 4

    def __init__(self):
        self.n = Board.SIZE
        self.window = Tk()
        self.window.title('2048 Game')
        self.gameArea = Frame(self.window, bg='#bbada0')
        self.board = []
        self.gridCell = [[0] * Board.SIZE for _ in range(Board.SIZE)]
        self.compress = False
        self.merge = False
        self.moved = False
        self.score = 0

        for i in range(Board.SIZE):
            rows = []
            for j in range(Board.SIZE):
                l = Label(self.gameArea, text='', bg='#ccbfb4',
                          font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)
                rows.append(l)
            self.board.append(rows)
        self.gameArea.grid()

    def reverse(self):
        for ind in range(Board.SIZE):
            i = 0
            j = Board.SIZE - 1
            while i < j:
                self.gridCell[ind][i], self.gridCell[ind][j] = self.gridCell[ind][j], self.gridCell[ind][i]
                i += 1
                j -= 1

    def transpose(self):
        self.gridCell = [list(i) for i in zip(*self.gridCell)]

    def compressGrid(self):
        self.compress = False
        temp = [[0] * Board.SIZE for _ in range(Board.SIZE)]
        for i in range(Board.SIZE):
            cnt = 0
            for j in range(Board.SIZE):
                if self.gridCell[i][j]:
                    temp[i][cnt] = self.gridCell[i][j]
                    if cnt != j:
                        self.compress = True
                    cnt += 1
        self.gridCell = temp

    def mergeGrid(self):
        self.merge = False
        for i in range(Board.SIZE):
            for j in range(Board.SIZE - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j]:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True

    def random_cell(self):
        cells = []
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if not self.gridCell[i][j]:
                    cells.append((i, j))
        curr = random.choice(cells)
        self.gridCell[curr[0]][curr[1]] = 2

    def can_merge(self):
        for i in range(Board.SIZE):
            for j in range(Board.SIZE - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1]:
                    return True

        for i in range(Board.SIZE - 1):
            for j in range(Board.SIZE):
                if self.gridCell[i + 1][j] == self.gridCell[i][j]:
                    return True
        return False

    def paintGrid(self):
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if not self.gridCell[i][j]:
                    self.board[i][j].config(text='', bg='#ccbfb4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                                            bg=self.bg_color.get(str(self.gridCell[i][j])),
                                            fg=self.color.get(str(self.gridCell[i][j])))
        lbl = Label(self.gameArea, text=f'Score: {self.score}',
                    bg='#eee4da', fg='#776e65', font=('arial', 22, 'bold'))
        lbl.grid(column=0, row=Board.SIZE + 1, columnspan=Board.SIZE, padx=7, pady=7)


class Game:
    def __init__(self, gamepanel):
        self.gamepanel = gamepanel
        self.end = False
        self.win = False

    def start(self):
        self.gamepanel.random_cell()
        self.gamepanel.random_cell()
        self.gamepanel.paintGrid()
        self.gamepanel.window.bind('<Key>', self.link_keys)
        self.gamepanel.window.mainloop()

    def link_keys(self, event):
        if self.end or self.win:
            return
        self.gamepanel.compress = False
        self.gamepanel.merge = False
        self.gamepanel.moved = False
        presed_key = event.keysym
        if presed_key == 'Up':
            self.gamepanel.transpose()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.transpose()
        elif presed_key == 'Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()
        elif presed_key == 'Left':
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
        elif presed_key == 'Right':
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
        else:
            pass
        self.gamepanel.paintGrid()
        flag = 0
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if self.gamepanel.gridCell[i][j] == 2048:
                    flag = 1
                    break
        if flag:  # found 2048
            self.win = True
            messagebox.showinfo('2048', message='You Win!!')
            print("win")
            return
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if not self.gamepanel.gridCell[i][j]:
                    flag = 1
                    break
        if not (flag or self.gamepanel.can_merge()):
            self.end = True
            messagebox.showinfo('2048', 'Game Over!!!')
            print("Over")
        if self.gamepanel.moved:
            self.gamepanel.random_cell()

        self.gamepanel.paintGrid()


gamepanel = Board()
game2048 = Game(gamepanel)
game2048.start()