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
                if self.row_num + y - piece_height - level > 0 and piece.piece[y][x] == '#' and self.board[self.row_num + y - piece_height - level][offset + x] != '.':
                    
                    return False
        return True
    def try_place(self, piece, pos, rotate):
        weight = [1 for _ in range(18)] + [3,100]
        level, offset = pos
        piece_height = len(piece)
        board = [b[:] for b in self.board]
        for y, line in enumerate(piece):
            for x, block in enumerate(line):
                if self.row_num + y - piece_height - level > 0 and piece[y][x] != '.':
                    board[self.row_num + y - piece_height - level][offset + x] = piece[y][x]
        
        score = sum([i * weight[i] for j in range(len(board[0])) for i in range(len(board)) if board[i][j] == "#"])
        return score

    def place_piece(self, best_rot, best_pos):
        
        level, offset = best_pos
        piece_height = len(best_rot)
        for y, line in enumerate(best_rot):
            for x, block in enumerate(line):
                if best_rot[y][x] != '.':
                    self.board[self.row_num + y - piece_height - level][offset + x] = best_rot[y][x]
        
    
    def __str__(self):

        return '\n'.join(''.join(line) for line in self.board)

def find_best_score(board, piece):
    results = []
    for level in range(len(board.board)):
        for rotate in range(4):  
            for offset in range(len(board.board[0]) - len(piece.piece[0]) + 1):
                if board.piece_fits(piece,(level, offset)):
                    
                    score = board.try_place(piece.piece, (level, offset), rotate)
                    
                    results.append([piece.piece, (level, offset), score, len(results)])
            piece.rotate()
    
    best = max(results, key = lambda x: x[2])
    # print("--------")
    # print("[*] best")
    # print(best)
    # print("--------")    
    return best[0], best[1]

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

        #print(board)
        
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
