class QLearning():
    def __init__(self, model_path=""):
        self.width = 6
        self.height = 6
        self.score = 0
        self.model_path = model_path
        self.gamma = 0.8 # discount factor
        self.alpha = 0.02 # learning rate
        self.archive = []
        self.Q = [0 for _ in range(1 << (self.width * self.height))]

    def crank(self, state, piece):
        game_over = 0
        best_reward = 0
        best = -99999999
        best_state = state
        for offset in range(self.width):
            for _ in range(4):
                piece = self.rotate(piece)
                s, reward, finish = self.place_piece(state, piece, offset)
                if s != state:
                    sc = reward * 100 + self.gamma * self.Q[s]
                    if sc > best:
                        best_reward = reward
                        best = sc
                        best_state = s
                        game_over = finish

        self.Q[state] = (1-self.alpha) * self.Q[state] + self.alpha * best
        self.score += best_reward

        return best_state, game_over

    def train(self):
        for game in range(1 << 13):
            state = 0
            self.score = 0
            for i in range(10000):
                piece = self.random_piece()
                state,game_over = self.crank(state, piece)
                if game_over:
                    break
            self.archive += [self.score]
            self.save_dataset()

            if game % 50 == 0:
                print("{} {}".format(game, self.score))

    def test(self):
        for i in range(10):
            piece = self.random_piece()
            print("piece")
            p = "{:036b}".format(piece)
            for i in range(6):
                print(p[i*6:(i+1)*6])
            state,game_over = self.crank(state, piece)
            print("state")
            s = "{:036b}".format(state)
            for i in range(6):
                print(s[i*6:(i+1)*6])

    def random_piece(self):
        pieces = [[3,3],[6,3],[3,6],[4,7],[1,7],[0,15],[2,7]]
        piece = choice(pieces)
        return piece[0] << self.width + piece[1]

    def piece_width(self, piece):
        p = 0
        for i in range(4):
            p |= (piece >> (i * self.width)) & ((1 << self.width) - 1)

        for i in range(3,-1,-1):
            if p & (1 << i):
                return i + 1

    def rotate(self, piece):
        p = 0
        for i in range(3,-1,-1):
            current_line = (piece >> (i * self.width)) & ((1 << self.width) - 1)
            if current_line:
                p += ((current_line & 0b1) << (3-i)) + ((current_line & 0b10) << (self.width - 1 + (3-i))) +\
                     ((current_line & 0b1) << (2 * self.width - 2 + (3-i))) + ((current_line & 0b10) << (3 * self.width - 3 + (3-i)))
        return p

    def place_piece(self, state, piece, offset):
        if offset + self.piece_width(piece) > self.width:
            return state, 0
        piece <<= offset

        while (piece & state) or ((piece << self.width) & state):
            piece <<= self.width

        s = piece | state
        full_line = (1 << self.width) - 1

        cleaned_line = 0

        for i in range(self.height-1,-1,-1):
            if (s & (full_line << (i * self.width))) == (full_line << (i * self.width)):
                cleaned_line += 1
                s = (s >> ((i + 1) * self.width)) << (i * self.width) | (s & ((1 << (i * self.width)) - 1))

        if s >> (self.height * self.width):
            return s, 0, 1
        reward = {0: 1, 1:400, 2:4000, 3:40000, 4:400000}[cleaned_line]
        return s, reward, 0

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
    q = QLearning()
    q.test()

