class Piece():
    def __init__(self, piece):
        self.piece = piece

    def rotate(self):
        self.piece = [row for row in zip(*self.piece)][::-1]
    
    def __str__(self):
        return '\n'.join(''.join(line) for line in self.piece)

class Board():
    def __init__(self):
        self.max_height = 20
        self.max_width = 10
        self.board = [['.' for _ in range(self.max_width)] for __ in range(self.max_height)]

    def completed_line(self):
        for i, line in enumerate(self.board):
            if line.count('.') == 0:
                yield i

    def clear_line(self, index):
        del self.board[index]
        self.board.insert(0, ['.' for _ in range(10)])


    def piece_fits(self, piece, pos):
        level, offset = pos
        piece_height = len(piece.piece)
        for y, line in enumerate(piece.piece):
            for x, block in enumerate(line):
                if self.max_height + y - piece_height - level > 0 \
                    and piece.piece[y][x] == '#' \
                    and self.board[self.max_height + y - piece_height - level][offset + x] != '.':
                    return False
        return True


    def score_piece(self, piece, pos, rotate):
        # This one is funky
        # Should board be the one controlling the scoring of pieces? I don;t think so...
        # Beter move this to either a Solver class or keep it functional
        weight = [1 for _ in range(18)] + [3,100]
        level, offset = pos
        piece_height = len(piece)
        board = [b[:] for b in self.board]
        for y, line in enumerate(piece):
            for x, block in enumerate(line):
                if self.row_num + y - piece_height - level > 0 and piece[y][x] != '.':
                    board[self.max_height + y - piece_height - level][offset + x] = piece[y][x]
        
        score = sum([i * weight[i] for j in range(len(board[0])) for i in range(len(board)) if board[i][j] == "#"])
        return score


    def place_piece(self, rotation, position):        
        level, offset = position
        piece_height = len(rotation)
        for y, line in enumerate(rotation):
            for x, block in enumerate(line):
                if rotation[y][x] != '.':
                    self.board[self.max_height + y - piece_height - level][offset + x] = rotation[y][x]
        
    def __str__(self):
        return '\n'.join(''.join(line) for line in self.board)


# MAYBE?! Solver class
class Solver():
    def __init__(self, board, piece):
        pass

def find_best_score(board, piece):
    results = []

    # You don't have to calculate all the board! Only untill the next all empty line
    # Because then they drop down! (Maybe error here?)
    for level in range(len(board.board)):
        for rotate in range(4):  
            for offset in range(len(board.board[0]) - len(piece.piece[0]) + 1):
                if board.piece_fits(piece,(level, offset)):
                    score = board.score_piece(piece.piece, (level, offset), rotate)                    
                    results.append([piece.piece, (level, offset), score, len(results)])
                    
            piece.rotate()
    
    best = max(results, key = lambda x: x[2])
    return best[0], best[1]


def tetrisGame(pieces):
    board = Board()
    score = 0
    for p in pieces:
        
        piece = Piece(p)
        rotation, position = find_best_score(board, piece)
        board.place_piece(rotation, position)
        
        for i in board.completed_line():
            board.clear_line(i)
            score += 1

    return score


######
## Good code ^^
##
## [self.max_height + y - piece_height - level][offset + x]
## Do this quite alot, maybe make a class attribute?
######


if __name__ == "__main__":

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
    print("test1 -- output: {}, expected: {}".format(tetrisGame(test1), output))

    test2 = [[["#","#"],["#","#"]], 
             [["#","#"],["#","#"]], 
             [["#","#"],["#","#"]], 
             [["#","#"],["#","#"]], 
             [["#","#"],["#","#"]], 
             [["#","#"],["#","#"]]]
    output = 2
    print("test2 -- output: {}, expected: {}".format(tetrisGame(test2), output))

    test3 = [[["#","#","#","#"]], 
     [["#","#","#","#"]], 
     [["#","#"],["#","#"]]]
    output = 1
    print("test3 -- output: {}, expected: {}".format(tetrisGame(test3), output))

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
    print("test4 -- output: {}, expected: {}".format(tetrisGame(test4), output))

    test5 = [[[".","#","."],["#","#","#"]], 
     [[".",".","#"],["#","#","#"]], 
     [["#","#","."],[".","#","#"]], 
     [[".","#","."],["#","#","#"]], 
     [[".",".","#"],["#","#","#"]], 
     [["#","#","."],[".","#","#"]]]
    output = 1
    print("test5 -- output: {}, expected: {}".format(tetrisGame(test5), output))
