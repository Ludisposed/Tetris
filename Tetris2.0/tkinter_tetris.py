from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from random import choice, randint

class Box():
    def __init__(self, canvas, coords, tag = -1):
        self.canvas = canvas
        self.tag = tag
        if tag < 0:
            self.tag = self.draw_on_canvas(coords)

    @property
    def coords(self):
        return self.canvas.coords(self.tag)

    def draw_on_canvas(self, coords):
        x_left, y_up, x_right, y_down = coords
        return self.canvas.create_rectangle(x_left,
                                            y_up,
                                            x_right,
                                            y_down,
                                            fill="blue")
        
    def move(self, movement):
        moved_x, moved_y = movement
        self.canvas.move(self.tag,
                         moved_x,
                         moved_y)



class Board():
    BOX_SIZE = 20
    
    
    def __init__(self, canvas, start_point):
        self.piece = Piece()
        self.canvas = canvas
        self.boxes = self.create_boxes(start_point)

    def create_boxes(self, start_point):
        return [Box(self.canvas, self.__new_piece_coord(coord[0], coord[1], start_point)) \
                for coord in self.piece.piece]

    def move(self, direction):
        coords = [box.coords for box in self.boxes]
        movements = self.__movement(coords, [direction] * len(coords))
        if not movements is None:
            self.__move(movements)
            return True
        return False



    def rotate(self, times = 1):
        for _ in range(times % 4):
            coords = [box.coords for box in self.boxes]
            movements = self.__movement(coords, self.piece.rotate_directions())
            if movements:
                self.piece.piece = self.piece.rotate()
                self.__move(movements)

    def __new_piece_coord(self, x, y, start_point):
        return (x * self.BOX_SIZE + start_point,
                y * self.BOX_SIZE,
                x * self.BOX_SIZE + self.BOX_SIZE + start_point,
                y * self.BOX_SIZE + self.BOX_SIZE)

    def __move(self, movements):
        for i in range(len(self.boxes)): 
            self.boxes[i].move(movements[i])

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

        overlap = set(self.canvas.find_overlapping((x_left + x_right) / 2 + x, 
                                                   (y_up + y_down) / 2 + y, 
                                                   (x_left + x_right) / 2 + x,
                                                   (y_up + y_down) / 2 + y))
        other_items = set(self.canvas.find_all()) - set([box.tag for box in self.boxes])
        if overlap & other_items:
            return False
        return True
    
    
    def __movement(self, coords, directions):
        if all(self.__can_move(coords[i], directions[i]) for i in range(len(coords))):
            return [(direction[0] * self.BOX_SIZE, direction[1] * self.BOX_SIZE) for direction in directions]
        return None


class Tetris():
    WIDTH = 300
    HEIGHT = 500
    START_POINT = WIDTH / 2 / Board.BOX_SIZE * Board.BOX_SIZE - Board.BOX_SIZE
    def __init__(self):
        self.level = 1
        self.score = 0

        self.root = Tk()
        self.root.geometry("500x550") 
        self.root.title('Tetris')

        

        self.canvas = Canvas(self.root, 
                             width = Tetris.WIDTH, 
                             height = Tetris.HEIGHT)

        self.next_piece = Canvas(self.root,
                                 width = 60,
                                 height = 60)
        self.root.bind("<Key>", self.call_back)
        self.canvas.pack(padx=5 , pady=0, side=LEFT)
        self.next_piece.pack(padx=5 , pady=20)

        self.status_var = StringVar()        
        self.status_var.set(f"Level: {self.level}, Score: {self.score}")        
        self.status = Label(self.root, 
                            textvariable=self.status_var, 
                            font=("Helvetica", 10, "bold"))
        self.status.place(x = self.WIDTH + 10, y = 100, width=100, height=25)

        self.play_again_btn = None
        self.quit_btn = None

    def start(self):
        self.next_piece.create_rectangle(0,
                                       0,
                                       40,
                                       40,
                                       fill="red")
        self.level = 1
        self.score = 0
        self.speed = 500
        self.block_count = 0

        self.current_piece = Board(self.canvas, self.START_POINT)
        self.canvas.update()
        self.root.after(self.speed, None)
        self.drop()
        self.root.mainloop()

    def hard_drop(self):
        pass

    def update_status(self):
        self.status_var.set(f"Level: {self.level}, Score: {self.score}")
        self.status.update()

    def next_level(self):
        self.speed -= 25
        self.level += 1
        self.update_status()

    def drop(self):
        if not self.current_piece.move((0,1)):
            # Check for completed lines
            self.completed_lines()

            # Create a new piece
            self.current_piece = Board(self.canvas, self.START_POINT)

            # Check for game over(if new piece cannot be dropped)
            if not self.current_piece.move((0,1)):
                self.game_over()
                return 

            # Next level logic
            self.block_count += 1
            if self.block_count % 5 == 0:
                self.next_level()
                
        self.root.after(self.speed, self.drop)

    def call_back(self, event):
        if event.char in ["a", "\uf702"]:
            self.current_piece.move((-1, 0))
        elif event.char in ["d", "\uf703"]:
            self.current_piece.move((1, 0))
        elif event.char in ["s", "\uf701"]:
            self.current_piece.rotate()

    def play_again(self):
        for box in self.canvas.find_all():
            self.canvas.delete(box)
        self.play_again_btn.destroy()
        self.quit_btn.destroy()

        self.start()

    def quit(self):
        self.root.quit()

    def game_over(self):
        self.play_again_btn = Button(self.root, text="Play Again", command=self.play_again)
        self.quit_btn = Button(self.root, text="Quit", command=self.quit) 
        self.play_again_btn.place(x = self.WIDTH + 10, y = 200, width=100, height=25)
        self.quit_btn.place(x = self.WIDTH + 10, y = 300, width=100, height=25)

    def completed_lines(self):
        y_coords_piece = [box.coords[3] for box in self.current_piece.boxes]
        all_boxes_coords = [(self.canvas.coords(box)[0], self.canvas.coords(box)[3])
                            for box in self.canvas.find_all()
                            if self.canvas.coords(box)[3] in y_coords_piece]
        
        for y in y_coords_piece:
            if all( (x, y) in all_boxes_coords for x in range(10, self.WIDTH - 10, Board.BOX_SIZE) ):
                # Clear line
                boxes_to_delete = [box
                                   for box in self.canvas.find_all()
                                   if self.canvas.coords(box)[3] == y]
                for box in boxes_to_delete:
                    self.canvas.delete(box)

                # Drop boxes
                boxes_to_drop = [box
                                 for box in self.canvas.find_all()
                                 if self.canvas.coords(box)[3] < y]
                for box in boxes_to_drop:
                    self.canvas.move(box, 0, Board.BOX_SIZE)

                self.score += 1
                self.update_status()


class Piece():
    PIECES = ([(0, 0), (1, 0), (0, 1), (1, 1)],     # Square
              [(0, 0), (1, 0), (2, 0), (3, 0)],     # Line
              [(2, 0), (0, 1), (1, 1), (2, 1)],     # Right L
              [(0, 0), (0, 1), (1, 1), (2, 1)],     # Left L
              [(0, 1), (1, 1), (1, 0), (2, 0)],     # Right Z
              [(0, 0), (1, 0), (1, 1), (2, 1)],     # Left Z
              [(1, 0), (0, 1), (1, 1), (2, 1)])     # T
    
    def __init__(self):
        self.piece = choice(self.PIECES)


    def rotate(self):  
        max_x = max(self.piece, key=lambda x:x[0])[0]
        new_original = (max_x, 0)

        return [(new_original[0] - coord[1],
                 new_original[1] + coord[0]) for coord in self.piece]
    
    def rotate_directions(self):
        rotated = self.rotate()
        directions = [(rotated[i][0] - self.piece[i][0],
                       rotated[i][1] - self.piece[i][1]) for i in range(len(self.piece))]

        return directions


if __name__ == '__main__':
    game = Tetris()
    game.start()

