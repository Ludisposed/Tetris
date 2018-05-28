#!/usr/bin/python
import numpy as np
class QModel(object):
    def __init__(self, model_path = "simple_tetris_Q"):
        self.width = 6
        self.alpha = 0.1
        self.gamma = 0.8
        self.height = 0
        self.model_path = model_path
        self.read_dataset()

    def predict(self, state):
        piece = bin(state)[2:-12]
        state = bin(state)[-12:]
        idx = (int(piece[:-6],2) * 3 + int(piece[-2:], 2)) * int(state, 2)
        return self.Q[idx]

    def train(self):
        pass


    def save_dataset(self):
        with open(self.model_path, 'wb+') as f:
            pickle.dump((self.Q, self.archive), f, -1)
            

    def read_dataset(self):
        if not os.path.isfile(self.model_path):
            self.Q = [0 for _ in range((1 << (2 * self.width)) * 12)]
            self.archive = []
        else:
            with open(self.model_path, 'rb') as f:
                self.Q, self.archive = pickle.load(f)
