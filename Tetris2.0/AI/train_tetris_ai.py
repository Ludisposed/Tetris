from random import choice, randint
from AI.ai_tetris import AIPlayer
class Piece():
    def __init__(self, piece = None):
        if not piece:
            self.piece = choice(TetrisTrain.PIECES)
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

class Board():
    def __init__(self, width = 14, height = 25):
        self.max_height = height
        self.max_width = width
        self.board = [[0]*width for _ in range(height)]
        
    def clean_line(self):
        completed_lines = 0
        for i, line in enumerate(self.board):
          if line.count(0) == 0:
            completed_lines += 1
            del self.board[i]
            self.board.insert(0, [0 for _ in range(self.max_width)])
        return completed_lines

    def __drop(self, piece, offset):
        last_level = self.max_height - piece.height + 1
        for level in range(last_level):
            for i in range(piece.height):
                for j in range(piece.width):
                    if self.board[level+i][offset+j] == 1 and piece.piece[i][j] == 1:
                        return level - 1
        return last_level - 1

    def place_piece(self, piece, offset):
        level = self.__drop(piece, offset)
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


class TetrisTrain:
    PIECES = [[(0,1,1),(1,1,0)],
              [(1,1,0),(0,1,1)],
              [(1,0,0),(1,1,1)],
              [(0,0,1),(1,1,1)],
              [(0,1,0),(1,1,1)],
              [(1,1),(1,1)],
              [(1,1,1,1)]]
    
    def __init__(self):
        self.ai_player = AIPlayer()
        self.MAX_PIECE = 1000
        self.pieces = [Piece() for _ in range(self.MAX_PIECE+1)]
        self.start()

    def start(self):
        self.board = Board()
        self.current_piece_index = 0
        self.score = 0
        self.piece_placed = 0
        self.current_piece = None
        self.next_piece = self.pieces[self.current_piece_index]

        
    def train(self):
        train_times = 0
        while 1:
            train_times += 1
            game_over = False
            max_clean = 0
            while self.piece_placed < self.MAX_PIECE:
                self.piece_placed += 1
                self.current_piece_index += 1
                
                completed_lines = self.play()
                print(self.board)
                print("{}/{}\nScore:{}\nTrain {} time".format(self.piece_placed, self.MAX_PIECE, self.score, train_times))

                if completed_lines < 0:
                    game_over = True
                    break
                elif completed_lines > max_clean:
                    max_clean = completed_lines
                
            self.MAX_PIECE += 100
            result = "Finish this turn Score: {} game over: {}\n".format(self.score, game_over)
            print(result)
            self.save_train_result(result)

            self.ai_player.save_dataset()
            self.ai_player.update(game_over, self.score)
            self.start()

    def play(self, next_piece_fixed = True):
        self.current_piece = Piece(self.next_piece.piece)
        if next_piece_fixed:
            self.next_piece = self.pieces[self.current_piece_index % len(self.pieces)]
        else:
            self.next_piece = Piece()

        self.ai_player.current_board = self.board.board
        self.ai_player.current_shape = self.current_piece.piece
        self.ai_player.next_shape = self.next_piece.piece

        next_move  = self.ai_player.next_move()
        rotate = next_move['rotate']
        offx = next_move['offx']

        self.current_piece.rotate(times = rotate)
        game_over = self.board.place_piece(self.current_piece, offx)
        
        if game_over:
            return -1
        else:
            completed_lines = self.board.clean_line()
            self.score += self.get_scores(completed_lines)
            return completed_lines
      

    def test(self):
        self.start()
        while 1:
            completed_lines = self.play(False)
            print(self.board)
            print("Score:{}".format(self.score))
            if completed_lines < 0:
                break            

    def save_train_result(self, data):
        with open("train.txt", 'a+') as f:
            f.write(data)  


    def get_scores(self, completed_lines):
        if completed_lines == 0:
            return 1
        elif completed_lines == 1:
            return 400
        elif completed_lines == 2:
            return 4000
        elif completed_lines == 3:
            return 40000
        elif completed_lines == 4:
            return 400000
        

if __name__ == "__main__":
    tetris = TetrisTrain()
    tetris.test()
    
    