from tkinter import Canvas, Label, Tk, StringVar
from random import choice, randint


class Board():
    pass


class Tetris():
    WIDTH = 300
    HEIGHT = 500

    def __init__(self):
        self.level = 1
        self.score = 0
        self.speed = 500
        self.fast_speed = 100
        
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

    def start(self):
        self.current_piece = Piece(self.canvas)
        self.canvas.update()
        self.root.after(500,None)
        self.drop()
        self.root.mainloop()

    def hard_drop(self):
        pass

    def drop(self):
        if not self.current_piece.move((0,1)):
            self.current_piece = Piece(self.canvas)
        self.root.after(500, self.drop)

    def call_back(self, event):
        if event.char in ["a", "\uf702"]:
            self.current_piece.move((-1, 0))
        elif event.char in ["d", "\uf703"]:
            self.current_piece.move((1, 0))
        elif event.char in ["s", "\uf701"]:
            self.current_piece.rotate()

class Piece():
    BOX_SIZE = 20
    START_POINT = Tetris.WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE
    PIECES = ([(0, 0), (1, 0), (0, 1), (1, 1)],     # Square
              [(0, 0), (1, 0), (2, 0), (3, 0)],     # Line
              [(2, 0), (0, 1), (1, 1), (2, 1)],     # Right L
              [(0, 0), (0, 1), (1, 1), (2, 1)],     # Left L
              [(0, 1), (1, 1), (1, 0), (2, 0)],     # Right Z
              [(0, 0), (1, 0), (1, 1), (2, 1)],     # Left Z
              [(1, 0), (0, 1), (1, 1), (2, 1)])     # T
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.boxes = self.create_boxes()
        self.rotate(randint(0,3))

    def create_boxes(self):
        boxes = []
        coords = choice(Piece.PIECES)
        for coord in coords:
            x, y = coord
            x_left, y_up, x_right, y_down = self.__new_piece_coord(x,y)
            box = self.canvas.create_rectangle(x_left,
                                               y_up,
                                               x_right,
                                               y_down,
                                               fill="blue")
            boxes.append(box)
        return boxes

    def move(self, direction):

        coords = [self.canvas.coords(box) for box in self.boxes]
        movements = self.__movement(coords, [direction] * len(coords))
        if movements:
            self.__move(movements)
            return True
        return False

    def rotate(self, times = 1):
        for _ in range(times % 4):
            coords = [self.canvas.coords(box) for box in self.boxes]
            movements = self.__rotate_movement(coords)
            if movements:
                self.__move(movements)

    def __move(self, movements):
        for i in range(len(self.boxes)): 
            moved_x, moved_y = movements[i]
            self.canvas.move(self.boxes[i],
                             moved_x,
                             moved_y)

    def __can_move(self, box_coords, new_pos):
        x, y = new_pos
        x = x * self.BOX_SIZE
        y = y * self.BOX_SIZE
        x_left, y_up, x_right, y_down = box_coords

        if y_down + y > Tetris.HEIGHT:
            return False
        if x_left + x < 0:
            return False
        if x_right + x > Tetris.WIDTH:
            return False
        if len(self.canvas.find_overlapping(x_left + x, y_up + y, x_right + x, y_down + y)) > 4:
            return False
        return True

    
    def __new_piece_coord(self, x, y):
        return (x * self.BOX_SIZE + self.START_POINT,
                y * self.BOX_SIZE,
                x * self.BOX_SIZE + self.BOX_SIZE + self.START_POINT,
                y * self.BOX_SIZE + self.BOX_SIZE)


    
    def __movement(self, coords, directions):
        if all(self.__can_move(coords[i], directions[i]) for i in range(len(coords))):
            return [(direction[0] * self.BOX_SIZE, direction[1] * self.BOX_SIZE) for direction in directions]
        
        return None

    
    def __rotate_movement(self, coords):
        coords_x = [coord[0] for coord in coords]
        coords_y = [coord[1] for coord in coords]
        mid_x = (max(coords_x) + min(coords_x)) / 2
        mid_y = (max(coords_y) + min(coords_y)) / 2

        def pivot_box(coord):
            x_diff = coord[0] - mid_x
            y_diff = coord[1] - mid_y
            x_pivot = (-x_diff - y_diff) / self.BOX_SIZE
            y_pivot = (x_diff - y_diff) / self.BOX_SIZE
            return (x_pivot, y_pivot)

        directions = [pivot_box(coord) for coord in coords]
        return self.__movement(coords, directions)

    
        

if __name__ == '__main__':
    game = Tetris()
    game.start()

