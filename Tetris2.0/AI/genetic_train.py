from genetic import GeneticAI
import matplotlib.pyplot as plt
from tetris_game import Piece, Board

class TetrisTrain:
    
    def __init__(self):
        
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

    def train_genetic(self, model_path = "model/genetic"):
        self.ai_player = GeneticAI(model_path)
        train_times = 0
        while 1:
            completed_lines = self.play(False)
            
            if completed_lines < 0:
                train_times += 1
                print("Score:{}\nTrain {} time".format(self.score, train_times))
                self.ai_player.update(True, self.score)
                self.ai_player.save_dataset()
                if train_times > 0 and train_times % 50 == 0:
                    self.present(self.ai_player.archive)
                self.start()

    def train_genetic_with_limit(self, model_path = "model/genetic_limit"):
        self.ai_player = GeneticAI(model_path)
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
                
            #self.MAX_PIECE += 100

            self.ai_player.save_dataset()
            self.ai_player.update(game_over, self.score)
            # if train_times > 0 and train_times % 50 == 0:
            #     self.present(self.ai_player.archive)
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

    def present(self, archive):
        plt.plot(archive)
        plt.ylabel('scores')
        plt.show()

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
    tetris.train_genetic()
    
    
    