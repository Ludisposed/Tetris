class Piece():
    def __init__(self, piece):
        self.piece = piece

    def rotate(self):
        self.piece = [row for row in zip(*self.piece)][::-1]
    
    def __str__(self):
        return '\n'.join(''.join(line) for line in self.piece)

class Board():
    def __init__(self):
        self.row_num = 20
        self.colum_num = 10
        self.board = [['.' for _ in range(self.colum_num)] for __ in range(self.row_num)]

    def completed_line(self):
        for i, line in enumerate(self.board):
            if line.count('.') == 0:
                yield i

    def clear_line(self, index):
        del self.board[index]
        self.board.append(['.' for _ in range(10)])

    def piece_fits(self, piece, pos):
        level, offset = pos
        piece_height = len(piece.piece)
        for y, line in enumerate(piece.piece):
            for x, block in enumerate(line):
                if piece.piece[y][x] == '#' and self.board[self.row_num + y - piece_height - level][offset + x] != '.':
                    return False
        return True

    def place_piece(self, best_rot, best_pos):
        print("--------")
        print(best_rot)
        print(best_pos)
        print("--------")
        level, offset = best_pos
        piece_height = len(best_rot)
        for y, line in enumerate(best_rot):
            for x, block in enumerate(line):
                if best_rot[y][x] != '.':
                    self.board[self.row_num + y - piece_height - level][offset + x] = best_rot[y][x]
        print('\n'.join(''.join(line) for line in self.board[-5:]))
        print("--------")
    
    def __str__(self):
        '''
        [*] Here is an error, so I changed the board logic

        Here is the original board like
        With [[".","#","."],["#","#","#"]], 
             [["#",".","."],["#","#","#"]]
        these two in it
        ######....
        .#...#....
        ..........
        ..........
        ..........

        This is the output board like from self.board[::-1]

        ..........
        ..........
        ..........
        .#...#....
        ######....

        look at the place for [["#",".","."],["#","#","#"]]
        the result is

        ..#
        ###

        but piece like

        #..
        ###

        can't rotate to be that

        So "mirror way" not work right here
        '''
        #return '\n'.join(''.join(line) for line in self.board[::-1])

        return '\n'.join(''.join(line) for line in self.board)

def find_best_score(board, piece):
    best_score = None
    best_rotation = None
    best_position = None
    
    for level in range(len(board.board)):
        
        #if level > 0 and board.board[level - 1].count('#') == 0:
            # Piece can't be placed here because it will fall down
            #break
        
        for _ in range(4):
            
            for offset in range(len(board.board[0]) - len(piece.piece[0]) + 1):
                if board.piece_fits(piece,(level, offset)):

                    # Surface area - level to drop
                    # TODO better score caller
                    score = piece.piece[0].count('#') - level
                    
                    if best_score is None or score > best_score:
                        
                        best_rotation = piece.piece
                        best_position = (level, offset)
                        best_score = score

            piece.rotate()
    return best_rotation, best_position     

def tetrisGame(pieces):
    board = Board()
    score = 0
    for p in pieces:
        piece = Piece(p)
        best_rot, best_pos = find_best_score(board, piece)
        board.place_piece(best_rot, best_pos)
        
        for i in board.completed_line():
            board.clear_line(i)
            score += 1

        print(board)
        
    return score

pieces = [[[".","#","."],["#","#","#"]], 
          [["#",".","."],["#","#","#"]], 
          [["#","#","."],[".","#","#"]], 
          [["#","#","#","#"]], 
          [["#","#","#","#"]], 
          [["#","#"],["#","#"]]]

print(tetrisGame(pieces))

'''
Expected output of the board after the last piece
...
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
# # . . . . . . # #
# # . . . . . . # #
. # . # . # # . # #
'''


test1 = [[[".","#","."],["#","#","#"]], 
         [["#",".","."],["#","#","#"]], 
         [["#","#","."],[".","#","#"]], 
         [["#","#","#","#"]], 
         [["#","#","#","#"]], 
         [["#","#"],["#","#"]]]
output = 1

test2 = [[["#","#"],["#","#"]], 
         [["#","#"],["#","#"]], 
         [["#","#"],["#","#"]], 
         [["#","#"],["#","#"]], 
         [["#","#"],["#","#"]], 
         [["#","#"],["#","#"]]]
output = 2

test3 = [[["#","#","#","#"]], 
 [["#","#","#","#"]], 
 [["#","#"],["#","#"]]]
output = 1

test4 = [[[".","#","#"],["#","#","."]], 
 [[".","#","."],["#","#","#"]], 
 [["#","#","."],[".","#","#"]], 
 [[".","#","."],["#","#","#"]], 
 [["#","#","#","#"]], 
 [["#",".","."],["#","#","#"]], 
 [["#","#"],["#","#"]], 
 [["#","#","#"],[".",".","#"]], 
 [[".","#","#"],["#","#","."]], 
 [[".","#","."],["#","#","#"]], 
 [["#","#","."],[".","#","#"]], 
 [[".","#","."],["#","#","#"]], 
 [["#","#","#","#"]], 
 [["#",".","."],["#","#","#"]], 
 [["#","#"],["#","#"]], 
 [["#","#","#"],[".",".","#"]]]
output = 3

test5 = [[[".","#","."],["#","#","#"]], 
 [[".",".","#"],["#","#","#"]], 
 [["#","#","."],[".","#","#"]], 
 [[".","#","."],["#","#","#"]], 
 [[".",".","#"],["#","#","#"]], 
 [["#","#","."],[".","#","#"]]]
output = 1
