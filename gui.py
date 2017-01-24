#!/usr/bin/env python3
from solver import *
from tkinter import Tk, Frame, Canvas, Button, LEFT, ROUND
from tkinter.filedialog import askopenfilename, asksaveasfilename
from functools import reduce
import pickle, time

# TODO: support for rectangular(non-square) dimensions
#       implement a way to change dimensions
DIM = 6
SIZE = 60
LINEWIDTH = 9
FONT = ("Courier", SIZE//4, "bold")
X_LIM, Y_LIM = DIM, DIM
FILETYPES = (("pickle files", "*.pkl"), ("All files", "*.*") )
COLORS = ["red", "tomato", "orange", "yellow", "lime green", "green", "cyan", "blue", "pink", "purple"]
COORCNV = lambda x, y: (x, (Y_LIM-1)-y)  # convert coordinate style from math to display

class App:
    def __init__(self, master):
        self.marked = tuple()
        self.pairs = []
        self.texts = []
        self.lines = []

        self.master = master
        self.master.title("Flow Solver")
        self.master.bind("<Key>", self.key)

        self.board = Canvas(self.master, width=X_LIM*SIZE, height=Y_LIM*SIZE)
        self._init_board()
        self.board.bind("<Button-1>", self.clicked)
        self.board.grid(row=0, column=1)

        self.x_axis = Canvas(self.master, width=X_LIM*SIZE, height=SIZE//2)
        self.y_axis = Canvas(self.master, width=SIZE//2, height=Y_LIM*SIZE)
        self._init_axis()
        self.x_axis.grid(row=1, column=1)
        self.y_axis.grid(row=0, column=0)

        self.buttonframe  = Frame(self.master)
        Button(self.buttonframe, text="Solve", command=self.solve).pack(side=LEFT)
        Button(self.buttonframe, text="Clear", command=self.clear).pack(side=LEFT)
        Button(self.buttonframe, text="Save", command=self.save).pack(side=LEFT)
        Button(self.buttonframe, text="Load", command=self.load).pack(side=LEFT)
        self.buttonframe.grid(row=2, column=1)
        
    def _init_board(self):
        for x in range(X_LIM):
            for y in range(Y_LIM):
                self.board.create_rectangle(SIZE*x, SIZE*y, SIZE*(x+1), SIZE*(y+1), fill="gray")

    def _init_axis(self):
        for x in range(X_LIM):
            self.x_axis.create_rectangle(SIZE*x, 0, SIZE*(x+1), SIZE//2, fill="white")
            self.x_axis.create_text(SIZE*x+SIZE//2, SIZE//4, font=FONT, text=x)
        for y in range(Y_LIM):
            self.y_axis.create_rectangle(0, SIZE*y, SIZE//2, SIZE*(y+1), fill="white")
            self.y_axis.create_text(SIZE//4, SIZE*y+SIZE//2, font=FONT, text=(Y_LIM-1)-y)
            
    def _draw_text(self, pos, text):
        pos = COORCNV(*pos)
        return self.board.create_text(SIZE*pos[0] + SIZE//2, SIZE*pos[1] + SIZE//2, font=FONT, fill="blue", text=text)

    def _draw_line(self, points, color):
        points = tuple( [int(SIZE*(v+.5)) for v in COORCNV(*pos)] for pos in points )
        return self.board.create_line(*points, fill=color, width=LINEWIDTH, joinstyle=ROUND)

    def _clear_line(self):
        if not self.lines:
            return
        for line in self.lines:
            self.board.delete(line)
        self.lines = []

    def _append_pair(self, pos1, pos2):
        self._clear_line()
        text = str(len(self.pairs))
        self.pairs.append((pos1, pos2))
        self.texts.append(( (pos1, pos2), 
                            (self._draw_text(pos1, text), self._draw_text(pos2, text)) ))

    def _pop_pair(self):
        self._clear_line()
        _, text_pair = self.texts.pop()
        for text_id in text_pair:
            self.board.delete(text_id)
        return self.pairs.pop()

    def _mark(self, pos):
        self._clear_line()
        self.marked = (pos, self._draw_text(pos, "*"))

    def _unmark(self):
        if self.marked:
            self.board.delete(self.marked[1])
            self.marked = tuple()

    def clicked(self, event):
        self._clear_line()
        pos = COORCNV(event.x//SIZE, event.y//SIZE)
        if pos in reduce(lambda a,b: a+b, self.pairs, tuple()):
            return
        if not self.marked :
            self._mark(pos)
        elif pos != self.marked[0]:
            self._append_pair(self.marked[0], pos)
            self._unmark()

    def key(self, event):
        name = event.char.upper() 
        if name == "D":
            if self.marked:
                self._unmark()
            else:
                pos = self._pop_pair()[0]
                self._mark(pos)
                
    def clear(self):
        self._clear_line()
        self._unmark()
        self.pairs = []
        for _, text_pair in self.texts:
            for text in text_pair:
                self.board.delete(text)
        self.texts = []

    def save(self):
        fname = asksaveasfilename(filetypes=FILETYPES)
        if fname:
            with open(fname, "wb") as f:
                pickle.dump(self.pairs, f)

    def load(self):
        fname = askopenfilename(filetypes=FILETYPES)
        if fname:
            self.clear()
            with open(fname, "rb") as f:
                for pair in pickle.load(f):
                    self._append_pair(*pair)

    def solve(self):
        if not self.pairs:
            return
        print("dimension:", DIM)
        print("length:", len(self.pairs))
        print("pairs:")
        for pair in self.pairs:
            print("\t{} -> {}".format(pair[0], pair[1]))
        print("\nsolving ...")
        try:
            game = Game(DIM, self.pairs)
            start = time.time()
            if game.solve():
                duration = time.time() - start
                print("DONE")
                print("time elapsed: {:d} mins  {:7.4f} secs".format(int(duration)//60, duration%60))
                print("\nsolution steps:")
                for index, steplist in enumerate(game.steps):
                    print("\t[{}] -> {}".format(index, steplist))
                print("="*50 + "\n")
                self.lines = [ self._draw_line(step_list, COLORS[k]) for k, step_list in enumerate(game.steps) ]
            else:
                print("unsolvable")
        except:
            print("EXCEPTION!!")


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()

