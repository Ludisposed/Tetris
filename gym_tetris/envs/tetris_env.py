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
        self.piece = choice(Piece.PIECES)
        rotate_time = randint(0, 3)
        self.piece = self.rotate(times = rotate_time)
        self.coordinates = [(x + 5 - len(self.piece[y]) // 2, y) 
                            for y in range(len(self.piece))
                            for x in range(len(self.piece[y])) 
                            if self.piece[y][x] == 1]

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
        self.current_piece = Piece()
        self.place_piece(self.current_piece.coordinates)

    def move_piece(self, dx, dy):
        new_coords = [(x + dx, y + dy) for x, y in self.current_piece.coordinates]
        if not self.collision(new_coords):
            self.place_piece(new_coords)

    def rotate_piece(self):
        pass

    def drop_piece(self):
        game_over = False
        new_coords = [(x, y+1) for x, y in self.current_piece.coordinates]
        if not self.collision(new_coords):
            self.place_piece(new_coords)
        else:
            self.current_piece = Piece()
            if not self.collision(self.current_piece.coordinates):
                self.place_piece(self.current_piece.coordinates)
                game_over = True
        
        score = [0, 1, 5, 10, 20][self.clean_lines()]
        return self.board, score, game_over

    def restart(self):
        self.board = [[0]*self.max_width for _ in range(self.max_height)]
        
    def clean_lines(self):
        completed_lines = 0
        for i, line in enumerate(self.board):
            if line.count(0) == 0:
                completed_lines += 1
                del self.board[i]
                self.board.insert(0, [0 for _ in range(self.max_width)])
        return completed_lines

    def collision(self, coordinates):
        return all(y < 20 and x in range(0, 9) and self.board[x][y] == 0 for x, y in coordinates)

    def place_piece(self,  new_coords):
        for x, y in self.current_piece.coordinates:
            self.board[x][y] = 0

        for x, y in new_coords:
            self.board[x][y] = 1

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
        self.action_size = 3
        self.state_size = 200

    def step(self, action):  
        if action == 0:
            self.state.move_piece(-1, 0)
        elif action == 1:
            self.state.move_piece(1, 0)
        elif action == 2:
            self.state.rotate_piece()
        
        state, reward, gameover = self.state.drop_piece()
        return state, reward, gameover, state

    def reset(self):
        self.state = Board()

    def render(self, mode='human', close=False):
        # do render later
        pass

