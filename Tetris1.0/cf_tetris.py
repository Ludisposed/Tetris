import unittest

class Piece():
    def __init__(self, piece):
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

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    # Debugging purposes
    def __str__(self):
       return '\n'.join(''.join(line) for line in self.piece)

class Board():
    def __init__(self, width, height):
        self.max_height = height
        self.max_width = width
        self.board = [['.']*width for __ in range(height)]

    def completed_line(self):
        for i, line in enumerate(self.board):
            if line.count('.') == 0:
                yield i

    def clear_line(self, index):
        del self.board[index]
        self.board.insert(0, ['.' for _ in range(self.max_width)])

    def drop(self, piece, offset):
        last_level = self.max_height - piece.height + 1
        for level in range(last_level):
            for i in range(piece.height):
                for j in range(piece.width):
                    if self.board[level+i][offset+j] == "#" and piece.piece[i][j] == "#":
                        return level - 1
        return last_level - 1

    def place_piece(self, piece, pos):
        level, offset = pos
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.piece[i][j] == "#":
                    self.board[level+i][offset+j] = piece.piece[i][j]

    # Debugging purposes
    def __str__(self):
       return '-' * self.max_width  + '\n' + \
              '\n'.join(''.join(line) for line in self.board) + '\n' + \
              '-' * self.max_width + '\n' + \
              ''.join([str(i) for i in range(self.max_width)]) + '\n' + \
              '-' * self.max_width


def find_best_position(board, piece):
    result = []
    for rotation in range(4):
        for offset in range(board.max_width - piece.width + 1):
            level = board.drop(piece, offset)
            blocks = sum(b.count('#') for b in board.board[level:level + piece.height])
            result.append([blocks, rotation, offset, level])
        piece.rotate()

    for i, fn in enumerate([max, min, min]):
        key = fn(result, key=lambda x: x[i])[i]
        result = [x for x in result if x[i] == key]
    return result[0]

def tetrisGame(pieces):
    board = Board(10, 20)
    score = 0
    for p in pieces:
        piece = Piece(p)
        _, rotate, offset, level = find_best_position(board, piece)

        piece.rotate(rotate)
        board.place_piece(piece ,(level, offset))

        for i in board.completed_line():
            board.clear_line(i)
            score += 1

    return score

class CodeFightsTest(unittest.TestCase):
    def test_1(self):
        pieces = [[[".","#","."],["#","#","#"]], 
                  [["#",".","."],["#","#","#"]], 
                  [["#","#","."],[".","#","#"]], 
                  [["#","#","#","#"]], 
                  [["#","#","#","#"]], 
                  [["#","#"],["#","#"]]]
        self.assertEqual(tetrisGame(pieces), 1)

    def test_2(self):
        pieces = [[["#","#"],["#","#"]], 
                  [["#","#"],["#","#"]], 
                  [["#","#"],["#","#"]], 
                  [["#","#"],["#","#"]], 
                  [["#","#"],["#","#"]], 
                  [["#","#"],["#","#"]]]
        self.assertEqual(tetrisGame(pieces), 2)

    def test_3(self):
        pieces = [[["#","#","#","#"]], 
                  [["#","#","#","#"]], 
                  [["#","#"],["#","#"]]]
        self.assertEqual(tetrisGame(pieces), 1)

    def test_4(self):
        pieces = [[[".","#","#"],["#","#","."]], 
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
        self.assertEqual(tetrisGame(pieces), 3)

    def test_5(self):
        pieces = [[[".","#","."],["#","#","#"]], 
                  [[".",".","#"],["#","#","#"]], 
                  [["#","#","."],[".","#","#"]], 
                  [[".","#","."],["#","#","#"]], 
                  [[".",".","#"],["#","#","#"]], 
                  [["#","#","."],[".","#","#"]]]
        self.assertEqual(tetrisGame(pieces), 1)

    
if __name__ == "__main__":
    unittest.main()
