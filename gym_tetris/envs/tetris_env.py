# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2018-05-14 17:34:44
# @Last Modified by:   Li Qin
# @Last Modified time: 2018-05-15 02:06:37

import gym

from random import choice, randint

class Piece(object):
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

class Board(object):
    def __init__(self, width = 10, height = 20):
        self.max_height = height
        self.max_width = width
        self.board = [[0]*width for _ in range(height)]

    def restart(self):
        self.board = [[0]*self.max_width for _ in range(self.max_height)]
        
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

    @property
    def state(self):
         return ''.join(str(self.board[i][j]) for j in range(self.max_width) for i in range(self.max_height))

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

class TetrisEnv(gym.Env):
    def __init__(self):
        self.__version__ = "0.1.0"
        self.state = None
        self.current_piece = None

    def step(self, action):
        '''
        Parameters
        ----------
        action : int

        TODO: define actions
        so we have actions: left, right, rotate

        Returns
        -------
        ob, reward, episode_over, info : tuple
            state (object) :
                game state after current action, state is just how board like right now
            reward (float) :
                reward from current action
                 * clean lines get positive reward
                 * game over get negtive reward
                 * else get 0 reward
            episode_over (bool) :
                is game over
            info (dict) :
                 debugging information.
        '''

        # do action(left, right, rotate) on current piece
        # current piece move down 1 step
        # check if current can't move more, if so check for clean line, and reward from clean line
        # return current board like, reward getted, and if game finished


        pass

    def reset(self):
        self.game = Board()
        self.current_piece = Piece()

        # add piece on the top center of board
        self.state = self.game.board

    def render(self, mode='human', close=False):
        # do render later
        pass

