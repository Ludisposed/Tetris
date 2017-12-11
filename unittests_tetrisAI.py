import unittest

class CodeFightsTest(unittest.TestCase):
    def test_lowest_line(self):
        '''
        Board:
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .

        Piece:
        . . #
        # # #

        =>
        . . . . . . . . . .
        . . # . . . . . . .
        # # # . . . . . . .        
        '''
        pass

    def test_i_fits(self):
        '''
        Board:
        . . . . . . . . . .
        . # # . . . . . . .
        # # . . . . . . . .

        Piece:
        . # .
        # # #

        =>
        . . . . . . . . . .
        . # # # . . . . . .
        # # # # # . . . . .        
        '''
        pass

    def test_next_piece(self):
        '''
        Board:
        . . . . . . . . . .
        . # # . . . . . . .
        # # . . . . . . . .

        Piece:
        . # .
        # # #

        =>
        . . . . . . . . . .
        . # # # . . . . . .
        # # # # # . . . . .        
        '''
        pass
    
