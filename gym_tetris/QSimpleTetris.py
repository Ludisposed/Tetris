#!/usr/bin/python
import numpy as np
from random import randint

class QModel(object):
    def __init__(self, Q):
        self.Q = Q

    def predict(self, state):
        piece = bin(state)[2:-12]
        state = bin(state)[-12:]
        idx = (int(piece[:-6],2) * 3 + int(piece[-2:], 2)) * int(state, 2)
        return self.Q[idx]

    def update(self, state_memories, move_memories, reward_memories):
        #update the model
        #choose the best reword for each state update Q
        pass

class QAgent(object):
    def __init__(self, model_path = "simple_tetris_Q"):
        self.width = 6
        self.alpha = 0.1
        self.gamma = 0.8
        self.height = 0
        self.model_path = model_path
        self.read_dataset()

    def buildmodel(self):
        Q = self.read_dataset()
        self.model = QModel(Q)

    def next_move(self, state, render=False):
        mov = self.model.predict(state)
        return mov

    def update_model(self, state_memories, move_memories, reward_memories):
        self.model.update(state_memories, move_memories, reward_memories)
        self.save_dataset(self.model.Q)

    def save_dataset(self, Q):
        fd = open(self.model_path, 'wb+')
        pickle.dump((Q), fd, -1)
        fd.close()
            

    def read_dataset(self):
        if not os.path.isfile(self.model_path):
            Q = [0 for _ in range((1 << (2 * self.width)) * 12)], []
        else:
            fd = open(self.model_path, 'rb')
            Q = pickle.load(fd)
            fd.close()
        return Q

class QTrain(object):
    def __init__(self, episodes = 10000, epsilon = 0.2):
        self.epsilon = epsilon
        self.episodes = episodes
        self.agent = QAgent()

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return randint(0,23)
        else:
            return self.agent.next_move(state)

    def train(self):
        for i in range(self.episodes):
            #train env
            pass



