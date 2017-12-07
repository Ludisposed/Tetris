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
        self.blocks = [0 for _ in range(self.max_height)]
        self.board = [['.' for _ in range(self.max_width)] for __ in range(self.max_height)]

    def update_blocks(self):
        return [b.count('#') for b in self.board]


    def completed_line(self):
        for i, line in enumerate(self.board):
            if line.count('.') == 0:
                yield i

    def clear_line(self, index):
        del self.board[index]
        self.board.insert(0, ['.' for _ in range(10)])

    def can_not_drop(self, piece, pos):
        level, offset = pos
        for i in range(0, level):
            if self.board[i][offset] == '#':
               return True
        return False

    def piece_fits(self, piece, pos):
        level, offset = pos
        piece_height = len(piece.piece)
        for y, line in enumerate(piece.piece):
            for x, block in enumerate(line):
                if (piece.piece[y][x] == '#' and self.board[self.max_height + y - piece_height - level][offset + x] == '#') \
                   or self.can_not_drop(piece, (self.max_height + y - piece_height - level, offset + x)):
                    return False
        return True

    def place_piece(self, rotation, position):        
        level, offset = position
        piece_height = len(rotation)
        for y, line in enumerate(rotation):
            for x, block in enumerate(line):
                if rotation[y][x] != '.':
                    self.board[self.max_height + y - piece_height - level][offset + x] = rotation[y][x]
        
    def __str__(self):
        return '\n'.join(''.join(line) for line in self.board)

class Solver():
    def __init__(self, board):
        self.board = board


    def find_best_score(self, piece):
        self.board.update_blocks()
        results = []
        for level in range(len(self.board.board)):
            if level > 0 and self.board.board[self.board.max_height - level - 1].count('#') == 0:
                # Will not change but just drop to a below level, so break
                break
            
            for rotate in range(4):  
                for offset in range(len(self.board.board[0]) - len(piece.piece[0]) + 1):
                    if self.board.piece_fits(piece, (level, offset)):
                        
                        score = self.score_piece(piece, (level, offset), rotate)                    
                        results.append([piece.piece, (level, offset), score, len(results)])
                        
                piece.rotate()
        
        rot, pos, *_ = max(results, key = lambda x: x[2])
        return rot, pos

    def score_piece(self, piece, pos, rotate):
        level, offset = pos
        blocks = self.board.blocks[:]
        #scores = [sum(range(i+1)) for i in range(10)] + [1000]

        #simple score way works better
        scores = [1 for _ in range(10)] + [1000]
        
        for i in range(len(piece.piece)):
            blocks[self.board.max_height + i - len(piece.piece) - level] += piece.piece[i].count("#")
        
        score = sum([scores[b] for b in blocks])
        #add this work worse
        #score = level - rotate + 20 - offset
        return score


        

def tetrisGame(pieces):
    board = Board()
    solver = Solver(board)
    score = 0
    
    for p in pieces:
        piece = Piece(p)
        print(piece)
        rotation, position = solver.find_best_score(piece)
        board.place_piece(rotation, position)
        
        for i in board.completed_line():
            board.clear_line(i)
            score += 1

        #print(board)
        #print()
        
    return score


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
    '''
    '''

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

    '''
    '''
    test5 = [[[".","#","."],["#","#","#"]], 
     [[".",".","#"],["#","#","#"]], 
     [["#","#","."],[".","#","#"]], 
     [[".","#","."],["#","#","#"]], 
     [[".",".","#"],["#","#","#"]], 
     [["#","#","."],[".","#","#"]]]
    output = 1
    print("test5 -- output: {}, expected: {}".format(tetrisGame(test5), output))
    
