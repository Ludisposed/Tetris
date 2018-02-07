from random import choice, randint

class Piece():
    PIECES = [[(0,1,1),(1,1,0)],
              [(1,1,0),(0,1,1)],
              [(1,0,0),(1,1,1)],
              [(0,0,1),(1,1,1)],
              [(0,1,0),(1,1,1)],
              [(1,1),(1,1)],
              [(1,1,1,1)]]

    def __init__(self, piece = None):
        if not piece:
            self.piece = choice(Piece.PIECES)
            rotate_time = randint(0,3)
            self.rotate(times = rotate_time)
        else:
            self.piece = piece

    @property
    def width(self):
        return len(self.piece[0])

    @property
    def height(self):
        return len(self.piece)

    def rotate(self, times=1):
        for i in range(times % 4):
            self.piece = [row[::-1] for row in zip(*self.piece)]

    def __str__(self):
       return '\n'.join(''.join(map(str,line)) for line in self.piece)

class Board():
    def __init__(self, width = 14, height = 25):
        self.max_height = height
        self.max_width = width
        self.board = [[0]*width for _ in range(height)]
        
    def clean_line(self):
        completed_lines = 0
        for i, line in enumerate(self.board):
          if line.count(0) == 0:
            completed_lines += 1
            del self.board[i]
            self.board.insert(0, [0 for _ in range(self.max_width)])
        return completed_lines

    def _drop(self, piece, offset):
        last_level = self.max_height - piece.height + 1
        for level in range(last_level):
            for i in range(piece.height):
                for j in range(piece.width):
                    if self.board[level+i][offset+j] == 1 and piece.piece[i][j] == 1:
                        return level - 1
        return last_level - 1

    def place_piece(self, piece, offset):
        level = self._drop(piece, offset)
        if level < 0:
            return True
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.piece[i][j] == 1:
                    self.board[level+i][offset+j] = piece.piece[i][j]
        return False

    def __str__(self):
       return '-' * self.max_width  + '\n' + \
              '\n'.join(''.join(map(str,line)) for line in self.board) + '\n' + \
              '-' * self.max_width
