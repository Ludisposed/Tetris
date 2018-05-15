#!/usr/bin/python
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
            self.piece = self.rotate(times = rotate_time)
        else:
            self.piece = piece

        offset = 5 - len(self.piece[0]) // 2
        self.coordinate = (offset, 0)

    @property
    def width(self):
        return len(self.piece[0])

    @property
    def height(self):
        return len(self.piece)

    def rotate(self, times=1):
        piece = [p[:] for p in self.piece]
        for i in range(times % 4):
            piece = [row[::-1] for row in zip(*piece)]
        return piece

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

    def collision(self, piece, offset, level):
        for i in range(piece.height):
            for j in range(piece.width):
                if self.board[level+i][offset+j] == 1 and piece.piece[i][j] == 1:
                    return True
        return False

    def place_piece(self, piece, offset, level):
        if level == 0 and self.collision(piece, offset, level):
            return None
        board = [b[:] for b in self.board]
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.piece[i][j] == 1:
                    board[level+i][offset+j] = piece.piece[i][j]
        return board

    @property
    def state(self):
         return ''.join(str(self.board[i][j]) for j in range(self.max_width) for i in range(self.max_height))

    

    def __str__(self):
       return '-' * self.max_width  + '\n' + \
              '\n'.join(''.join(map(str,line)) for line in self.board) + '\n' + \
              '-' * self.max_width

class TetrisEnv(gym.Env):
    def __init__(self):
        self.__version__ = "0.1.0"
        self.state = None
        self.current_piece = None
        self.score = 0

    def step(self, action): 
        if action == 1:
            offset, level = self._move_left()
        elif action == 2:
            offset, level = self._move_right()
        elif action == 3:
            self._rotate()

        state, reward, gameover = self._move_down(offset, level)
        return state, reward, gameover, {}

    def reset(self):
        self.game = Board()
        self.score = 0
        self.state = self._state_after_add_new_piece()

    def _state_after_add_new_piece(self):
        self.current_piece = Piece()
        offset, level = self.current_piece.coordinate
        return self.game.place_piece(self.current_piece, offset, level)
    
    def _move_left(self):
        offset, level = self.current_piece.coordinate[0] - 1, self.current_piece.coordinate[1]
        if offset < 0 or self.game.collision(self.current_piece, offset, level):
            offset, level = self.current_piece.coordinate
        return offset, level

    def _move_right(self):
        offset, level = self.current_piece.coordinate[0] + 1, self.current_piece.coordinate[1]
        if offset + self.current_piece.width >= 10 or self.game.collision(self.current_piece, offset, level):
            offset, level = self.current_piece.coordinate
        return offset, level

    def _rotate(self):
        piece = self.current_piece.rotate()
        offset, level = self.current_piece.coordinate
        if not self.game.collision(piece, offset, level):
            self.current_piece.piece = piece

    def _move_down(self, offset, level):
        gameove = False
        reward  = 0
        level += 1
        if self.game.coordinate(self.current_piece, offset, level):
            level -= 1
            state = self.game.place_piece(self.current_piece, offset, level)
            
            if state is None:
                gameove = True
            else:
                self.game.board = state
                reward = self._score(self.game.clean_lines)
                state = self._state_after_add_new_piece()
                if state is None:
                    gameove = True
        else:
            state = self.game.place_piece(self.current_piece, offset, level)

        return state, reward, gameove

    def _score(self, clean_lines):
        return [0, 1, 10, 20, 50][clean_lines]

    def render(self, mode='human', close=False):
        # do render later
        pass

