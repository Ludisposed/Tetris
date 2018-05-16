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
        self.coordinates = [(y, x + 5 - len(self.piece[y]) // 2) 
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

    def rotated_coordinates(self, piece):
        min_y = min(self.coordinates, key=lambda x:x[0])[0]
        min_x = min(self.coordinates, key=lambda x:x[1])[1]
        return [(min_y + y, min_x + x) 
                for y in range(len(piece))
                for x in range(len(piece[y])) 
                if piece[y][x] == 1]


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
        new_coords = [(y + dy, x + dx) for y, x in self.current_piece.coordinates]
        if not self.collision(new_coords):
            self.place_piece(new_coords)
            return True
        return False

    def rotate_piece(self):
        rotated_piece = self.current_piece.rotate()
        rotated_coordinates = self.current_piece.rotated_coordinates(rotated_piece)

        if not self.collision(rotated_coordinates):
            self.place_piece(rotated_coordinates)
            self.current_piece.coordinates = rotated_coordinates
            self.current_piece.piece = rotated_piece

    def drop_piece(self):
        game_over = False
        score = 0

        if self.move_piece(0, 1):
            if self.move_piece(0, 1):
                self.move_piece(0, -1)
                return self.board, score, game_over

        self.current_piece = Piece()

        if self.collision(self.current_piece.coordinates, True):
            game_over = True
            score = -10

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

    def collision(self, coordinates, new_piece = False):
        for y, x in coordinates:
            if (y, x) not in self.current_piece.coordinates or new_piece:
                if y not in range(20) or x not in range(10) or self.board[y][x] != 0:
                    return True
        return False

    def place_piece(self,  new_coords):
        # DEBUG!
        print("Current coords:", self.current_piece.coordinates)
        print("New coords", new_coords)
        
        for y, x in self.current_piece.coordinates:
            self.board[y][x] = 0
        for y, x in new_coords: 
            self.board[y][x] = 1
        self.current_piece.coordinates = new_coords

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
        self.board = None
        self.action_size = 3
        self.state_size = 200

    def step(self, action):  
        if action == 0:
            self.board.move_piece(-1, 0)
        elif action == 1:
            self.board.move_piece(1, 0)
        elif action == 2:
            self.board.rotate_piece()
        
        state, reward, gameover = self.board.drop_piece()
        return state, reward, gameover, str(self.board)

    def reset(self):
        self.board = Board()

    def render(self, mode='human', close=False):
        # do render later
        pass

