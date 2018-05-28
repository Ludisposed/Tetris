#!/usr/bin/python
import gym
from random import choice, randint
import numpy as np

'''
Four pieces: 

00  00  01  01  11
01  11  10  11  11

'''

class SimpleTetrisEnv(gym.Env):
    def __init__(self):
        self.__version__ = "0.1.0"
        self.game_width = 6
        self._update_state()
        self.action_size = self.game_width * 4
        self.state_size = 2 * self.game_width
        self.viewer = None

    def step(self, action):
        offset, rotate_time = divmod(action, self.game_width)
        piece = self.state >> (2 * self.game_width)
        piece = self.rotate(piece, rotate_time)
        state = int(bin(self.state)[-12:],2)
        
        state, reward = self.place_piece(state, piece, offset)
        
        self._update_state(state)
        
        return piece << (2*self.game_width) + state, reward, False, ""

    def reset(self):
        self._update_state()
        return self.state

    def _update_state(self, state=0):
        piece = self.generate_piece()
        self.state = (piece << (2*self.game_width)) + state

    def render(self, mode='human', close=False):
        state = bin(self.state)[-12:]
        piece = bin(self.state)[2:-12]
        print("----")
        print(f"PIECE : {piece}")
        print("----")
        print(state[:6])
        print(state[6:])
        print("----")

    def generate_piece(self):
        return  (randint(0,3) << self.game_width) + randint(1, 3)

    def piece_width(self, piece):
        return 2 if ((piece >> self.game_width) | (piece & ((1 << self.game_width) - 1))) > 1 else 1

    def rotate(self, piece, time=1):
        for _ in range(time):
            p = piece >> self.game_width
            q = piece & ((1 << self.game_width) - 1)
            piece = ((p & 0b10) << (self.game_width - 1)) + (p & 0b1) + ((q & 0b10) << self.game_width) + ((q & 0b1) << 1)
        return piece

    def place_piece(self, state, piece, offset):
        if offset + self.piece_width(piece) > self.game_width:
            return state, 0

        piece <<= offset
        while (piece & state) or ((piece << self.game_width) & state):
            piece <<= self.game_width

        s = piece | state

        full_line = (1 << self.game_width) - 1

        if (s & (full_line << self.game_width)) == (full_line << self.game_width):
            s = (s & full_line) | ((s >> (2 * self.game_width)) << self.game_width)

        if (s & full_line) == full_line:
            s >>= self.game_width

        reward = 0

        while s >> (2 * self.game_width):
            s >>= self.game_width
            reward += 1

        return s, reward

if __name__ == "__main__":
    env = SimpleTetrisEnv()
    for i in range(10):
        env.step(randint(0,24))
        env.render()