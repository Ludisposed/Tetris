from tkinter import Canvas, Label, Tk, StringVar
from random import choice

class Board():
    pass

class Tetris():
    WIDTH = 300
    HEIGHT = 500

    def __init__(self):
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
        
        self.root.bind("<Key>", self.call_back)
        self.canvas.pack()
        self.root.mainloop()

    def start(self):
        self.current_piece = Piece(self.canvas)
        self.canvas.update()

    def call_back(self, event):
        if event.char in ["a", "\uf702"]:
            pass
        elif event.char in ["d", "\uf703"]:
            pass
        elif event.char in ["s", "\uf701"]:
            self.current_piece.rotate()

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
        self.boxes = self.create_boxes()

    def create_boxes(self):
        boxes = []
        for point in self.piece:
            x, y = point
            box = self.canvas.create_rectangle(x * Piece.BOX_SIZE + Piece.START_POINT,
                                               y * Piece.BOX_SIZE,
                                               x * Piece.BOX_SIZE + Piece.BOX_SIZE + Piece.START_POINT,
                                               y * Piece.BOX_SIZE + Piece.BOX_SIZE,
                                               fill="blue")
            boxes.append(box)
        return boxes

    def move(self, direction):
        pass

    def hard_drop(self):
        pass

    def drop_line(self):
        pass

    def can_move(self, position):
        '''Check if box can move (x, y) boxes.'''
        x, y = position
        x = x * Piece.BOX_SIZE
        y = y * Piece.BOX_SIZE
        x_left, y_up, x_right, y_down = self.canvas.coords(box)

        if y_down + y > Tetris.HEIGHT:
            return False
        if x_left + x < 0:
            return False
        if x_right + x > Tetris.WIDTH:
            return False

        return True

    def rotate(self):
        boxes = self.boxes[:]
        pivot = boxes.pop(2)

        def pivot_box(box):
            '''Return (x, y) boxes needed to rotate a box around the pivot.'''
            box_coords = self.canvas.coords(box)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            x_pivot = (- x_diff - y_diff) / self.BOX_SIZE
            y_pivot = (x_diff - y_diff) / self.BOX_SIZE
            return (x_pivot, y_pivot)

        if all(self.can_move(box, pivot_box(box)) for box in boxes):
            for box in boxes:
                x_move, y_move = get_move_coords(box)
                self.canvas.move(box, 
                                 x_move * self.BOX_SIZE, 
                                 y_move * self.BOX_SIZE)

        return True
        

if __name__ == '__main__':
    game = Tetris()
    game.start()
