from tkinter import Canvas, Label, Tk, StringVar
from random import choice

class Tetris():
    WIDTH = 300
    HEIGHT = 500

    def __new__(self):
        self.level = 1
        self.score = 0
        self.speed = 500
        
        self.root = Tk()
        self.root.title('Tetris')

        self.status_var = StringVar()        
        self.status_var.set(f"Level: {self.level}, Score: {self.score}")        
        self.status = Label(self.root, 
                            textvariable=self.status_var, 
                            font=("Helvetica", 10, "bold"))
        self.status.pack()

        self.canvas = Canvas(self.root, 
                             width = Tetris.WIDTH, 
                             height = Tetris.HEIGHT)
        self.canvas.pack()

        self.root.bind("<Key>", self.handle_events)
        self.root.mainloop()

    def start_game(self):
        pass

    def handle_events(self, event):
        pass

class Piece():
    BOX_SIZE = 20
    START_POINT = Tetris.WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE
    PIECES = (((0, 0), (1, 0), (0, 1), (1, 1)),     # Square
              ((0, 0), (1, 0), (2, 0), (3, 0)),     # Line
              ((2, 0), (0, 1), (1, 1), (2, 1)),     # Right L
              ((0, 0), (0, 1), (1, 1), (2, 1)),     # Left L
              ((0, 1), (1, 1), (1, 0), (2, 0)),     # Right Z
              ((0, 0), (1, 0), (1, 1), (2, 1)),     # Left Z
              ((1, 0), (0, 1), (1, 1), (2, 1)))     # T
    
    def __init__(self, canvas):
        self.piece = choice(Piece.PIECES)
        self.canvas = canvas
        self.boxes = self.create_boxes

    def create_boxes(self):
        boxes = []
        for point in shape:
            box = canvas.create_rectangle(point[0] * Piece.BOX_SIZE + Piece.START_POINT,
                                          point[1] * Piece.BOX_SIZE,
                                          point[0] * Piece.BOX_SIZE + Piece.BOX_SIZE + Piece.START_POINT,
                                          point[1] * Piece.BOX_SIZE + Piece.BOX_SIZE,
                                          fill=self.color)
            boxes.append(box)
        return boxes

    def move(self, direction):
        pass

    def hard_drop(self):
        pass

    def drop_line(self):
        pass

    def rotate(self):
        self.piece = [row[::-1] for row in zip(*self.piece)]

if __name__ == '__main__':
    game = Tetris()    
