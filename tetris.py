from random import choice, randint

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
        self._position = None
    
    def rotate(self, times=1):
        for i in range(times):
            self.data = [row[::-1] for row in zip(*self)]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value


class Board(_2DList):
    def __init__(self, width, height):
        super().__init__(self.new_board(self, '.', width, height))

    def completed_line(self):
        for i, line in enumerate(self):
            if line.count('.') == 0:
                yield i

    def clear_line(self, index):
        del self[index]
        self.data.insert(0, ['.'] * self.width)

    def _can_drop(self, piece):
        random_num = randint(0, self.width - piece.width)
        position_on_board = []
        for i in range(piece.height):
            for j in range(piece.width):
                if piece[i][j] == "#":
                    if self.data[i][random_num+j] == '#':
                        return False, None
                    self.data[i][random_num+j] = piece[i][j]
                    position_on_board.append([i, random_num + j])
        return True, position_on_board

    def _can_lower(self, piece):
        return False

            
# Single player Tetris game
def tetris():
    score = 0
    board = Board(10, 20)
    
    while True:
        piece = Piece()
        succes, position = board._can_drop(piece)
        if succes:
            piece.position = position
            print(board)
            while board._can_lower(piece):
                # User input?
                # Lower piece a level after few ticks
                pass

            for i in board.completed_line():
                board.clear_line(i)
                score += 1

        # Game Over
        else:
            print("Game Over")
            break
        
if __name__ == '__main__':
    tetris()

# TODO Multiplayer Tetris
# TODO Optimal AI
# TODO Sprites?
