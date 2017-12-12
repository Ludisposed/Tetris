from tkinter import Canvas, Label, Tk, StringVar
from random import choice

class Piece():
    PIECES = (
        ((0, 0), (1, 0), (0, 1), (1, 1)),     # square
        ((0, 0), (1, 0), (2, 0), (3, 0)),     # line
        ((2, 0), (0, 1), (1, 1), (2, 1)),     # right L
        ((0, 0), (0, 1), (1, 1), (2, 1)),     # left L
        ((0, 1), (1, 1), (1, 0), (2, 0)),     # right Z
        ((0, 0), (1, 0), (1, 1), (2, 1)),     # left Z
        ((1, 0), (0, 1), (1, 1), (2, 1)),     # T
    )
    
    def __init__(self, piece):
        self.piece = choice(Piece.PIECES)

    @property
    def width(self):
        return len(self.piece[0])

    @property
    def height(self):
        return len(self.piece)

    def move(self):
        pass

    def hard_drop(self):
        pass

    def drop_line(self):
        pass

    def rotate(self, times=1):
        for i in range(times % 4):
            self.piece = [row[::-1] for row in zip(*self.piece)]

class Tetris():
    WIDTH = 300
    HEIGHT = 500

    def __new__(self):
        self.level = 1
        self.score = 0
        self.speed = 500
        self.root = Tk()
        self.root.title('Tetris')

        self.status_var = StringVar()        
        self.status_var.set(f"Level: {self.level}, Score: {self.score}")        
        self.status = Label(self.root, 
                textvariable=self.status_var, 
                font=("Helvetica", 10, "bold"))
        self.status.pack()

        self.canvas = Canvas(
                self.root, 
                width = Tetris.WIDTH, 
                height = Tetris.HEIGHT
        )
        self.canvas.pack()

        self.root.bind("<Key>", self.handle_events)
        self.root.mainloop()

    def timer(self):
        pass

    def handle_events(self, event):
        pass

class Piece():
    pass

if __name__ == '__main__':
    game = Tetris()    
