from random import randint, choice
from copy import deepcopy

class SimpleTetrisPiece():
    PIECES = [[(0,0),(0,1)],
              [(0,0),(1,1)],
              [(0,1),(1,0)],
              [(0,1),(1,1)],
              [(1,1),(1,1)]]

    def __init__(self, piece = None):
        if not piece:
            self.piece = choice(SimpleTetrisPiece.PIECES)
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


class SimpleTetrisBoard():
    def __init__(self, width = 6, height = 2):
        self.max_height = height + 2
        self.max_width = width
        self.board = [[0] * self.max_width for _ in range(self.max_height)]

    def _clean_line(self):
        for i, line in enumerate(self.board):
          if line.count(0) == 0:
            del self.board[i]
            self.board.insert(0, [0 for _ in range(self.max_width)])

    def _reward(self):
        self._clean_line()
        reward = 0
        for i in range(2):
            if self.board[1].count(1) != 0:
                del self.board[-1]
                self.board.insert(0, [0 for _ in range(self.max_width)])
                reward -= 1
        return reward

    def _drop(self, piece, offset):
        last_level = self.max_height - piece.height + 1
        for level in range(last_level):
            for i in range(piece.height):
                for j in range(piece.width):
                    if self.board[level+i][offset+j] == 1 and piece.piece[i][j] == 1:
                        return level - 1
        return last_level - 1

    @property
    def state(self):
        return int(''.join(map(str,self.board[2] + self.board[3])), 2)

    def place_piece(self, piece, offset):
        level = self._drop(piece, offset)
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.piece[i][j] == 1:
                    self.board[level+i][offset+j] = piece.piece[i][j]
        reward = self._reward()
        return reward


class SimpleTetrisQLearning():
    def __init__(self):
        self.width = 6
        self.alpha = 0.02
        self.gamma = 0.8
        self.height = 0
        self.Q = [0 for _ in range(1 << (2 * self.width))]

    def crank(self, board, piece):
        best = -99999999
        loss = 0
        b = board
        for offset in range(board.max_width):
            for r in range(4):
                current_board = deepcopy(board)
                current_piece = deepcopy(piece)
                current_piece.rotate(r)
                if offset + current_piece.width < self.width:
                    reward = current_board.place_piece(current_piece, offset)
                    score = reward * 100 + self.gamma * self.Q[current_board.state]
                    if score > best:
                        loss = reward * (-1)
                        best = score
                        b = current_board

        self.Q[board.state] = (1 - self.alpha) * self.Q[board.state] + self.alpha * best
        self.height += loss

        return b

    def train(self):
        for game in range(1<<13):
            score = 1000
            self.height = 0
            board = SimpleTetrisBoard(width = self.width)
            for i in range(10000):
                piece = SimpleTetrisPiece()
                board = self.crank(board, piece)
            if game % 10 == 0:
                print("{} {}".format(game, self.height))

if __name__ == "__main__":
    t = SimpleTetrisQLearning()
    t.train()
