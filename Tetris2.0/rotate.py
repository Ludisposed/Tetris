from tkinter import *
from random import randint, choice


class Piece():
    def __init__(self, piece):
        self.piece = piece
        self.random_rotate()

    @property
    def width(self):
        return len(self.piece[0])

    @property
    def height(self):
        return len(self.piece)

    def rotate(self, times=1):
        for i in range(times % 4):
            self.piece = [row[::-1] for row in zip(*self.piece)]
    
    def random_rotate(self):
        self.rotate(randint(0,3))
    
    #get coordinates of '#' which will used in draw on canvas
    '''
    such as
        ##
         ##
        [('#','#','.'),('.','#','#')]
    coordinates for # will be (0,0),(0,1),(1,1),(1,2)
    but the right is          (0,0),(1,0),(1,1),(2,1)
    SO we have to switch the `x` and `y`
    '''
    def positions(self):
        return [(j,i) for i in range(self.height) for j in range(self.width) if self.piece[i][j] == "#"]
    
    # Debugging purposes
    def __str__(self):
       return '\n'.join(''.join(line) for line in self.piece)

class Game:

    def __init__(self):
        root = Tk()

        self.board = Canvas(root, width = 300, height = 500)
        self.board.pack()

        self.width, self.height = 50, 50

        self.piece = Piece([('#','#','.'),('.','#','#')])
        self.pieces = []
        self.add_piece(0)

        root.bind('<Key>', self.callback)
        mainloop()

    def add_piece(self, start_place):
        positions = self.piece.positions()
        self.pieces = []
        for pos in positions:
          x,y = pos
          self.pieces.append(self.board.create_rectangle(x * self.width + start_place, y * self.height + start_place, \
                       (x + 1) * self.width + start_place, (y + 1) *  self.height + start_place, fill="blue"))
       

    def remove_piece(self):
        for piece in self.pieces:
            self.board.delete(piece)
        self.pieces = []

    def callback(self, event):

        print(event.char)
        if event.char in ["a", "\uf702"]:
          print("go left")
        elif event.char in ["d", "\uf703"]:
          print("go right")
        elif event.char in ["s", "\uf701"]:
          print("rotate")
          self.piece.rotate()
          self.remove_piece()
          self.add_piece(0)

if __name__ == "__main__":
    game = Game()
