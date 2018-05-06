#!/usr/bin/python3

from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from genetic_game import GeneticGame
from time import sleep

class Tetris():
    def __init__(self):
        model_path = "model/genetic"
        self.game = GeneticGame(model_path)
        self.box_size = 20
        self.game_width = self.game.board.max_width * self.box_size
        self.game_height = self.game.board.max_height * self.box_size

        self.root = Tk()
        self.root.geometry("500x550") 
        self.root.title('Tetris')
        self._game_canvas()
        self._score_label()
        self._next_piece_canvas()

    def start_ai(self):
        while 1:
            completed_lines = self.game.play()
            self.render_game_canvas()
            self.render_score_label()
            self.render_next_piece()
            
            if completed_lines < 0:
                break
            sleep(0.5)
        self.root.mainloop()
        

    def render_game_canvas(self):
        self.canvas.delete("all")
        width = self.game.board.max_width
        height = self.game.board.max_height
        coords = [(j, i) for j in range(width) for i in range(height) if self.game.board.board[i][j] == 1]
        self._create_boxes(self.canvas, coords, (0,0))

    def render_score_label(self):
        self.status_var.set(f"Score: {self.game.score}")
        self.status.update()

    def render_next_piece(self):
        self.next_canvas.delete("all")
        width = self.game.next_piece.width
        height = self.game.next_piece.height
        coords = [(j, i) for j in range(width) for i in range(height) if self.game.next_piece.piece[i][j] == 1]

        self._create_boxes(self.next_canvas, coords, (20,20))

    def _create_boxes(self, canvas, coords, start_point):
        off_x, off_y = start_point
        for coord in coords:
            x, y = coord
            canvas.create_rectangle(x * self.box_size + off_x,
                                    y * self.box_size + off_y,
                                    (x + 1) * self.box_size + off_x,
                                    (y + 1) * self.box_size + off_y,
                                    fill="blue")
            

    def _game_canvas(self):
        self.canvas = Canvas(self.root, 
                             width = self.game_width, 
                             height = self.game_height)
        self.canvas.pack(padx=5 , pady=10, side=LEFT)
    def _score_label(self):
        self.status_var = StringVar()        
        self.status = Label(self.root, 
                            textvariable=self.status_var, 
                            font=("Helvetica", 10, "bold"))
        
        self.status.pack()  

    def _next_piece_canvas(self):

        self.next_canvas = Canvas(self.root,
                                 width = 100,
                                 height = 100)
        self.next_canvas.pack(padx=5 , pady=10)

if __name__ == "__main__":
    tetris = Tetris()
    tetris.start_ai()
