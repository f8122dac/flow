from solver import *
from tkinter import Tk, Frame, Canvas, Button, LEFT
from tkinter.filedialog import askopenfilename, asksaveasfilename
from functools import reduce
import pickle, time

# TODO: support for rectangular(non-square) dimensions
DIM = 6
SIZE = 60
FONT = ("Courier", SIZE//4, "bold")
X_LIM, Y_LIM = DIM, DIM

class App:
    def __init__(self, master):
        self.master = master
        self.marked = tuple()
        self.pairs = []
        self.texts = []
        self.board = Canvas(self.master, width=X_LIM*SIZE, height=Y_LIM*SIZE)
        self.x_axis = Canvas(self.master, width=X_LIM*SIZE, height=SIZE//2)
        self.y_axis = Canvas(self.master, width=SIZE//2, height=Y_LIM*SIZE)
        self.buttonframe  = Frame(self.master)
        self.button1= Button(self.buttonframe, text="Solve", command=self.solve)
        self.button2= Button(self.buttonframe, text="Clear", command=self.clear)
        self.button3= Button(self.buttonframe, text="Save", command=self.save)
        self.button4= Button(self.buttonframe, text="Load", command=self.load)
        self.master.title("Flow Solver")
        self.master.bind("<Key>", self.key)
        self._draw_board()
        self._draw_axis()
        self.board.bind("<Button-1>", self.clicked)
        self.x_axis.grid(row=1, column=1)
        self.y_axis.grid(row=0, column=0)
        self.board.grid(row=0, column=1)
        self.buttonframe.grid(row=2, column=1)
        self.button1.pack(side=LEFT)
        self.button2.pack(side=LEFT)
        self.button3.pack(side=LEFT)
        self.button4.pack(side=LEFT)
        
    def _draw_board(self):
        for x in range(X_LIM):
            for y in range(Y_LIM):
                self.board.create_rectangle(SIZE*x, SIZE*y, SIZE*(x+1), SIZE*(y+1), fill="gray")

    def _draw_axis(self):
        for x in range(X_LIM):
            self.x_axis.create_rectangle(SIZE*x, 0, SIZE*(x+1), SIZE//2, fill="white")
            self.x_axis.create_text(SIZE*(x+0.5), SIZE//4, font=FONT, text=x)

        for y in range(Y_LIM):
            self.y_axis.create_rectangle(0, SIZE*y, SIZE//2, SIZE*(y+1), fill="white")
            self.y_axis.create_text(SIZE//4, SIZE*(y+0.5), font=FONT, text=(Y_LIM-1)-y)
            
    def _draw_text(self, pos, text):
        return self.board.create_text(SIZE*pos[0] + SIZE//2, SIZE*((Y_LIM-1)-pos[1]) + SIZE//2, font=FONT, fill="blue", text=text)

    def _append_pair(self, pos1, pos2):
        text = str(len(self.pairs))
        self.pairs.append((pos1, pos2))
        self.texts.append(( (pos1, pos2), 
                            (self._draw_text(pos1, text), self._draw_text(pos2, text)) ))

    def _pop_pair(self):
        _, text_pair = self.texts.pop()
        for text_id in text_pair:
            self.board.delete(text_id)
        return self.pairs.pop()

    def _mark(self, pos):
        self.marked = (pos, self._draw_text(pos, "*"))

    def _unmark(self):
        if self.marked:
            self.board.delete(self.marked[1])
            self.marked = tuple()

    def clicked(self, event):
        pos = (event.x//SIZE, (Y_LIM-1) - event.y//SIZE)
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
        self._unmark()
        self.pairs = []
        for _, text_pair in self.texts:
            for text in text_pair:
                self.board.delete(text)
        self.texts = []

    def save(self):
        fname = asksaveasfilename(filetypes=(("pickle files", "*.pkl"), ("All files", "*.*") ))
        if fname:
            with open(fname, "wb") as f:
                pickle.dump(self.pairs, f)

    def load(self):
        fname = askopenfilename(filetypes=(("pickle files", "*.pkl"), ("All files", "*.*") ))
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
        else:
            print("unsolvable")
        return game


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
