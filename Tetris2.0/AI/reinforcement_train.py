from tetris_game import Piece, Board
from copy import deepcopy
import os
import pickle
import matplotlib.pyplot as plt
class QLearning():
    def __init__(self, model_path="model/Q_leaning"):
        self.width = 14
        self.height = 25
        self.score = 0
        self.model_path = model_path
        self.gamma = 0.8 # discount factor
        self.alpha = 0.1 # learning rate
        self.read_dataset()

    def board_2_state(self, board, offset):
        n = offset
        if offset + 4 > self.width:
            n = self.width - 4
            m = self.width
        else:
            m = n + 4
        rotate_board = [row for row in zip(*board)]   
        peaks = [0 for _ in range(0, 4)]
        for idx in range(n, m):
            row = rotate_board[idx]
            if row.count(1) > 0:
                peaks[idx] = len(row) - row.index(1)
                


    def crank(self, board, piece):
        game_over = 0
        best_reward = 0
        best = -99999999
        best_board = board
        for offset in range(self.width):
            for _ in range(4):
                current_board = deepcopy(board)
                piece.rotate()
                if offset + piece.width <= self.width:
                    before_state = self.board_2_state(current_board, offset)
                    finish = current_board.place_piece(piece, offset)
                    reward = self.get_reward(current_board.clean_line())
                    #if finish: reward -= 5000
                    if current_board.state not in self.Q:
                        self.Q[current_board.state] = 0
                    s = reward * 100 + self.gamma * self.Q[current_board.state]
                    if s > best:
                        best_reward = reward
                        best = s
                        best_board = current_board
                        game_over = finish

        if board.state not in self.Q:
            self.Q[board.state] = 0

        self.Q[board.state] = (1-self.alpha) * self.Q[board.state] + self.alpha * best
        self.score += best_reward

        return best_board, game_over

    def train(self):
        board = Board(self.width, self.height)
        train_times = 0
        while 1:
            self.score = 0
            board.restart()
            game_over = 0
            while not game_over:
                piece = Piece()
                board,game_over = self.crank(board, piece)
            train_times += 1
            self.archive += [self.score]
            self.save_dataset()

            if train_times % 50 == 0:
                print("Score: {} Train {} time".format(self.score, train_times))

    
    def evaluate(self):
        plt.plot(q.archive)
        plt.ylabel('scores')
        plt.show()

    def get_reward(self, completed_lines):
        return {0:1, 1:400, 2:4000, 3:40000, 4:400000}[completed_lines]

    def save_dataset(self):
        with open(self.model_path, 'wb+') as f:
            pickle.dump((self.Q, self.archive), f, -1)
            

    def read_dataset(self):
        if not os.path.isfile(self.model_path):
            self.Q = {}
            self.archive = []
        else:
            with open(self.model_path, 'rb') as f:
                self.Q, self.archive = pickle.load(f)

if __name__ == "__main__":
    q = QLearning("model/Q_leaning_14_25")
    q.train()
    #q.evaluate()
    
    


