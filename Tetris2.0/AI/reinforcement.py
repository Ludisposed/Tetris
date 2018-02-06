class QLearning():
    def __init__(self):
        self.gamma = 0.8 # discount factor
        self.alpha = 0.02 # learning rate

    def crank(self, state, piece):
        Q[state] = (1-self.alpha) * Q[state] + self.alpha * best

    def train(self):
        for game in range(1 << 13):
            state = 0
            for i in range(10000):
                piece = self.random_piece()
                state = self.crank(state, piece)

class TDLearning():
    pass