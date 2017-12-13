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
    
    def positions(self):
        return [(j,i) for i in range(self.height) for j in range(self.width) if self.piece[i][j] == "#"]
    
    # Debugging purposes
    def __str__(self):
       return '\n'.join(''.join(line) for line in self.piece)

BLOCK_WIDTH = 10

class Game:
    def __init__(self, board):#board is canvas
        self.pieces = self.all_pieces()
        self.board = board
        self.current_piece = None

    def add_new_piece(self):
        #when piece drop down set self.current_piece back to None 
        if not self.current_piece:
            self.current_piece = Piece(self.random_piece())
        positions = self.current_piece.positions()
        piece = []
        for pos in positions:
            p = board.create_rectangle(pos[0] * BLOCK_WIDTH, \
                pos[1] * BLOCK_WIDTH, BLOCK_WIDTH, BLOCK_WIDTH, fill="blue")
            piece.append(p)
        return piece

    def rotate(self):
        self.current_piece.rotate()
        #remove the canvas piece from canvas first
        #self.add_new_piece()
    
    def random_piece(self):
        return choice(self.pieces)

    def all_pieces(self):
        pieces = [[('.','#','#'),('#','#','.')],
                  [('#','#','.'),('.','#','#')],
                  [('#','#','#'),('.','.','#')],
                  [('#','#','#'),('#','.','.')],
                  [('#','#','#'),('.','#','.')],
                  [('#','#'),('#','#')],
                  [('#','#','#','#')]]
        return pieces

