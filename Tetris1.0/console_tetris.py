import sys
from random import choice

from cf_tetris import Piece, Board

class Tetris:
    def __init__(self):
        self.pieces = self.all_pieces()
        self.board = Board(10,20)
        self.score = 0

    def play_game(self):
        
        print(self.board)
        print('Score: {}'.format(self.score))
        print()

        piece = self.random_piece()
        print(piece)

        rotate = input('Do you wanna rotate this piece [y/n]?')
        while rotate != 'n':
            piece.rotate()
            print(piece)
            rotate = input('Do you wanna rotate this piece [y/n]?')

        offset = int(input('Where you wanna place it off leftmost [0-{}]?'.format(10 - piece.width)))

        level = self.board.drop(piece, offset)
        if level < 0:
            print("[-] GAME OVER")
            sys.exit(0)
        self.board.place_piece(piece, (level, offset))

        self.update_score()
        
        print(self.board)

    def update_score(self):
        for i in self.board.completed_line():
            self.board.clear_line(i)
            self.score += 1

    def random_piece(self):
        return choice(self.pieces)

    def all_pieces(self):
        pieces = [[('.','#','#'),('#','#','.')],
                  [('#','.'),('#','#'),('.','#')],
                  [('.','#'),('#','#'),('#','.')],
                  [('#','#','.'),('.','#','#')],
                  [('#','.','.'),('#','#','#')],
                  [('#','#'),('#','.'),('#','.')],
                  [('#','#','#'),('.','.','#')],
                  [('.','#'),('.','#'),('#','#')],
                  [('.','.','#'),('#','#','#')],
                  [('#','.'),('#','.'),('#','#')],
                  [('#','#','#'),('#','.','.')],
                  [('#','#'),('.','#'),('.','#')],
                  [('.','#','.'),('#','#','#')],
                  [('#','.'),('#','#'),('#','.')],
                  [('#','#','#'),('.','#','.')],
                  [('.','#'),('#','#'),('.','#')],
                  [('#','#'),('#','#')],
                  [('#','#','#','#')],
                  [('#'),('#'),('#'),('#')]]

        return [Piece(piece) for piece in pieces]



if __name__ == "__main__":
    tetris = Tetris()
    while True:
        tetris.play_game()
    