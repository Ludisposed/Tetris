import unittest
from random import choice

PIECES = [[[".", "#", "."],
           ["#", "#", "#"]],
          
          [["#", ".", "."],
           ["#", "#", "#"]],
          
          [[".", ".", "#"],
           ["#", "#", "#"]],
    
          [["#", "#", "."],
           [".", "#", "#"]],
    
          [[".", "#", "#"],
           ["#", "#", "."]],

          [["#", "#"],
           ["#", "#"]],

          [["#", "#", "#", "#"]]]

class _2DList:
    def __init__(self, list_=None):
        if list_ is None:
            list_ = []
        self.data = list(list_)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
       return '\n'.join(''.join(line) for line in self.data)

    @property
    def width(self):
        return len(self.data[0])

    @property
    def height(self):
        return len(self.data)

    @staticmethod
    def new_piece(self):
        return choice(PIECES)

    @staticmethod
    def new_board(self, fill, width, height):
        return [[fill]*width for __ in range(height)]


class Piece(_2DList):
    def __init__(self):
        super().__init__(self.new_piece(self))
    
    def rotate(self, times=1):
        for i in range(times):
            self.data = [row[::-1] for row in zip(*self)]


class Board(_2DList):
    def __init__(self, width, height):
        super().__init__(self.new_board('.', width, height))

    def completed_line(self):
        for i, line in enumerate(self):
            if line.count('.') == 0:
                yield i

    def drop(self, piece, offset):
        last_level = self.max_height - piece.height + 1
        for level in range(last_level):
            for i in range(piece.height):
                for j in range(piece.width):
                    if self.board[level+i][offset+j] == "#" and piece.piece[i][j] == "#":
                        return level - 1
        return last_level - 1

    def clear_line(self, index):
        del self[index]
        self.data.insert(0, ['.'] * self.width)

    def place_piece(self, piece, pos):
        level, offset = pos
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.piece[i][j] == "#":
                    self[level+i][offset+j] = piece.piece[i][j]

# Single player Tetris game
def tetris():
    board = Board(10, 20)
    
    while board._in_bounds():
        piece = Piece()
        while piece._not_dropped():
            # user_input
            # game_tick
            pass
        
if __name__ == '__main__':
    tetris()

# TODO Multiplayer Tetris
# TODO Optimal AI
# TODO Sprites?
