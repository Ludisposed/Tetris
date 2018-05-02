# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2018-05-02 08:24:09
# @Last Modified by:   Li Qin
# @Last Modified time: 2018-05-02 08:49:11

from .tetris_game import Piece, Board
from .genetic import GeneticAI

class GeneticGame():
    def __init__(self, model_path):
        self.board = Board()
        self.ai_player = GeneticAI(model_path)
        self.score = 0
        self.next_piece = Piece()

    def play(self):
        self.current_piece = Piece(self.next_piece.piece)
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