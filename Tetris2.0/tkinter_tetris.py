from tkinter import Canvas, Label, Tk, StringVar
from random import choice, randint


class Board():
    WIDTH = 300
    HEIGHT = 500
    BOX_SIZE = 20
    START_POINT = WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE

    @classmethod
    def can_move(self, box_coords, new_pos, coords_occupied):
        x, y = new_pos
        x = x * Board.BOX_SIZE
        y = y * Board.BOX_SIZE
        x_left, y_up, x_right, y_down = box_coords

        if y_down + y > Board.HEIGHT:
            return False
        if x_left + x < 0:
            return False
        if x_right + x > Board.WIDTH:
            return False
        if (x_left + x, y_up + y) in coords_occupied:
            return False
        return True

    @classmethod
    def new_piece_coord(self, x, y):
        return (x * Board.BOX_SIZE + Board.START_POINT,
                y * Board.BOX_SIZE,
                x * Board.BOX_SIZE + Board.BOX_SIZE + Board.START_POINT,
                y * Board.BOX_SIZE + Board.BOX_SIZE)

    @classmethod
    def movement(self, x, y):
        return (x * Board.BOX_SIZE,
                y * Board.BOX_SIZE)

    @classmethod
    def rotate(self, coords, times = 1):
        points = Board.coords_to_points(coords)
        for _ in range(times % 4):
            print(points)
            rotated_points = []
            max_y = max(points, key=lambda a:a[1])[1]
            min_y = min(points, key=lambda a:a[1])[1]
            for point in points:
                x,y = point
                tmp = y
                y = x
                x = max_y - tmp + min_y
                rotated_points.append((x,y))

            points = rotated_points
            print(points)
        return Board.points_to_coords(points)

    @classmethod
    def coords_to_points(self, coords):
        return [(coord[0] // Board.BOX_SIZE, coord[1] // Board.BOX_SIZE) for coord in coords]

    @classmethod
    def points_to_coords(self, points):
        return [(point[0] * Board.BOX_SIZE, point[1] * Board.BOX_SIZE) for point in points]





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
        if self.current_piece.move((0,1)):
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

    def create_boxes(self):
        boxes = []
        coords = choice(Piece.PIECES)
        for coord in coords:
            x, y = coord
            x_left, y_up, x_right, y_down = Board.new_piece_coord(x,y)
            box = self.canvas.create_rectangle(x_left,
                                               y_up,
                                               x_right,
                                               y_down,
                                               fill="blue")
            boxes.append(box)
        return boxes

    def move(self, direction):
        x, y = direction
        if all(Board.can_move(self.canvas.coords(box), direction, []) for box in self.boxes):
            for box in self.boxes: 
                moved_x, moved_y = Board.movement(x,y)
                self.canvas.move(box,
                                 moved_x,
                                 moved_y)
            return True
        return False
    
    def rotate(self):
        print([self.canvas.coords(box)[:2] for box in self.boxes])
        coords = Board.rotate([self.canvas.coords(box)[:2] for box in self.boxes])
        print(coords)
        directions = [((coords[i][0] - self.canvas.coords(self.boxes[i])[0]) // Board.BOX_SIZE, \
                       (coords[i][1] - self.canvas.coords(self.boxes[i])[1]) // Board.BOX_SIZE) \
                      for i in range(len(self.boxes))]
        print(directions)
        if all(Board.can_move(self.canvas.coords(self.boxes[i]), directions[i], []) \
               for i in range(len(self.boxes))):
            
            for i in range(len(self.boxes)):
                x_move, y_move = directions[i]
                self.canvas.move(self.boxes[i], 
                                 x_move * self.BOX_SIZE, 
                                 y_move * self.BOX_SIZE)





    # def rotate(self):
    #     boxes = self.boxes[:]
    #     pivot = boxes.pop(2)

    #     def pivot_box(box):
    #         box_coords = self.canvas.coords(box)
    #         pivot_coords = self.canvas.coords(pivot)
    #         x_diff = box_coords[0] - pivot_coords[0]
    #         y_diff = box_coords[1] - pivot_coords[1]
    #         x_pivot = (-x_diff - y_diff) / self.BOX_SIZE
    #         y_pivot = (x_diff - y_diff) / self.BOX_SIZE
    #         return (x_pivot, y_pivot)

    #     if all(self.can_move(box, pivot_box(box)) for box in boxes):
    #         for box in boxes:
    #             x_move, y_move = pivot_box(box)
    #             self.canvas.move(box, 
    #                              x_move * self.BOX_SIZE, 
    #                              y_move * self.BOX_SIZE)
        

if __name__ == '__main__':
    game = Tetris()
    game.start()

