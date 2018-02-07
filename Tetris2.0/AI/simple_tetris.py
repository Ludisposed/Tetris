from random import randint, choice
from copy import deepcopy
import os
import pickle


class SimpleTetrisGame():
    def __init__(self, width = 6):
        self.width = width

    def generate_piece(self):
        return  (randint(0,3) << self.width) + randint(1, 3)

    def piece_width(self, piece):
        return 2 if ((piece >> self.width) | (piece & ((1 << self.width) - 1))) > 1 else 1

    def rotate(self, piece):
        p = piece >> self.width
        q = piece & ((1 << self.width) - 1)

        return ((p & 0b10) << (self.width - 1)) + (p & 0b1) + ((q & 0b10) << self.width) + ((q & 0b1) << 1)

    def place_piece(self, state, piece, offset):
        if offset + self.piece_width(piece) >= self.width:
            return state, 0

        piece <<= offset
        while (piece & state) or ((piece << self.width) & state):
            piece <<= self.width

        s = piece | state

        full_line = (1 << self.width) - 1

        if (s & (full_line << self.width)) == (full_line << self.width):
            s = (s & full_line) | ((s >> (2 * self.width)) << self.width)

        if (s & full_line) == full_line:
            s >>= self.width

        reward = 0

        while s >> (2 * self.width):
            s >>= self.width
            reward += 1

        return s, reward

class SimpleTetrisQLearning():
    def __init__(self, model_path = "model/simple_tetris_Q"):
        self.width = 6
        self.alpha = 0.02
        self.gamma = 0.8
        self.height = 0
        self.model_path = model_path
        self.tetris = SimpleTetrisGame(width = self.width)
        self.read_dataset()


    def crank(self, state, piece):
        best = -99999999
        loss = 0
        p = piece
        best_s = state
        for offset in range(self.width):
            for _ in range(4):
                p = self.tetris.rotate(p)
                s, reward = self.tetris.place_piece(state, p, offset)
                if s != state:
                    score = reward * (-100) + self.gamma * self.Q[s]
                    if score > best:
                        loss = reward
                        best = score
                        best_s = s

        self.Q[state] = (1 - self.alpha) * self.Q[state] + self.alpha * best
        self.height += loss

        return best_s

    def train(self):
        for game in range(1<<13):
            state = 0
            self.height = 0
            for i in range(10000):
                piece = self.tetris.generate_piece()
                state = self.crank(state, piece)
            self.archive += [self.height]
            self.save_dataset()
            if game % 50 == 0:
                print("{} {}".format(game, self.height))

    def save_dataset(self):
        with open(self.model_path, 'wb+') as f:
            pickle.dump((self.Q, self.archive), f, -1)
            

    def read_dataset(self):
        if not os.path.isfile(self.model_path):
            self.Q = [0 for _ in range(1 << (2 * self.width))]
            self.archive = []
        else:
            with open(self.model_path, 'rb') as f:
                self.Q, self.archive = pickle.load(f)


if __name__ == "__main__":
    t = SimpleTetrisQLearning()
    t.train()


