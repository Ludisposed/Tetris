# The total number of blocks in the rows this piece will occupy after falling down is maximized
# I think over this sentence, and finally get it
# It means, after place the piece, those rows it in, add the block number, should be maximized
class Piece():
    def __init__(self, piece):
        self.piece = piece
    def width(self):
        return len(self.piece[0])
    def height(self):
        return len(self.piece)

    def rotate(self, times = 1):
        for i in range(times):
            # About rotate, I checked the text about challenge you send me before
            # It said `clockwise`, there once before I remember 
            # We seem have difference in `clockwise`(that time I ask if you are left hand)
            # I think clockwise is like
            '''
            ---->
            ^   |
            |   |
            |   v
            <----
            '''

            #sooo I think
            '''
             #
            ###

            rotate once will be

            #
            ##
            #
            '''
            self.piece = [row[::-1] for row in zip(*self.piece)]
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

    def drop(self, piece, offset):

        last_level = self.max_height - piece.height() + 1
        for level in range(last_level):
            for i in range(piece.height()):
                for j in range(piece.width()):
                    
                    if self.board[level+i][offset+j] == "#" and piece.piece[i][j] == "#":

                        return level - 1
        return last_level - 1
    def place_piece(self, piece, pos):
        level, offset = pos
        for i in range(piece.height()):
            for j in range(piece.width()):
                if piece.piece[i][j] == "#":
                    self.board[level+i][offset+j] = piece.piece[i][j]


    def __str__(self):
        return '\n'.join(''.join(line) for line in self.board)
def find_best_position(board, piece):
    result = []
    for rotate in range(4):

        for offset in range(board.max_width - piece.width() + 1):
        
            level = board.drop(piece,offset)
            blocks = sum([b.count('#') for b in board.board[level:level+piece.height()]])
            result.append([blocks, rotate, offset, level + piece.height() - 1])
        piece.rotate()
    #sorry still using `filter` what you hate xD
    result = list(filter(lambda x: x[0] == max(result, key = lambda x: x[0])[0], result))
    result = list(filter(lambda x: x[1] == min(result, key = lambda x: x[1])[1], result))
    result = list(filter(lambda x: x[2] == min(result, key = lambda x: x[2])[2], result))[0]
    return result


def tetrisGame(pieces):
    board = Board()
    score = 0
    for p in pieces:
        piece = Piece(p)
        _, rotate, offset, level = find_best_position(board, piece)
        
        piece.rotate(rotate)
        board.place_piece(piece ,(level - piece.height() + 1, offset))
        #print(board)
        #print()
        for i in board.completed_line():
            board.clear_line(i)
            score += 1

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
    