from tkinter import *
from random import randint, choice


class Piece():
    PIECES = (((0, 0), (1, 0), (0, 1), (1, 1)),  # square
              ((0, 0), (1, 0), (2, 0), (3, 0)),  # line
              ((2, 0), (0, 1), (1, 1), (2, 1)),  # right el
              ((0, 0), (0, 1), (1, 1), (2, 1)),  # left el
              ((0, 1), (1, 1), (1, 0), (2, 0)),  # right wedge
              ((0, 0), (1, 0), (1, 1), (2, 1)),  # left wedge
              ((1, 0), (0, 1), (1, 1), (2, 1)))  # symmetrical wedge

    def __init__(self):
        self.positions = choice(Piece.PIECES)
        self.random_rotate()
        self.boxes = self.add_boxes()

    def add_boxes(self):
        boxes = []
        for pos in self.positions:
            x, y = pos
            boxes.append(self.board.create_rectangle(x * self.width + start_place,
                                                           y * self.height + start_place,
                                                           (x + 1) * self.width + start_place,
                                                           (y + 1) *  self.height + start_place,
                                                           fill="blue"))
        return boxes

    def remove_boxes(self):
        for piece in self.pieces:
            self.board.delete(piece)
        self.pieces = []

    def rotate(self, times=1):
        for i in range(times % 4):
            self.piece = [row[::-1] for row in zip(*self.positions)]
    
    def random_rotate(self):
        self.rotate(randint(0,3))

class Game:
    def __init__(self):
        root = Tk()

        self.board = Canvas(root, width = 300, height = 500)
        self.board.pack()

        self.width, self.height = 50, 50

        self.piece = Piece()

        root.bind('<Key>', self.callback)
        mainloop()

    def callback(self, event):
        # print(event.char)
        if event.char in ["a", "\uf702"]:
            self.move_piece(-10)
        elif event.char in ["d", "\uf703"]:
            self.move_piece(10)
        elif event.char in ["s", "\uf701"]:
            self.piece.rotate()

if __name__ == "__main__":
    game = Game()







