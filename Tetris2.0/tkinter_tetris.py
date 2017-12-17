from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from random import choice, randint


"""
I Althered the code a bit on som places, broke a few on others :p

Other then that, great work on the refractor ^^
"""

# Idk if I like this bare Classes, Too Javaish?
class Utility():
    PIECES = ([(0, 0), (1, 0), (0, 1), (1, 1)],     # Square
              [(0, 0), (1, 0), (2, 0), (3, 0)],     # Line
              [(2, 0), (0, 1), (1, 1), (2, 1)],     # Right L
              [(0, 0), (0, 1), (1, 1), (2, 1)],     # Left L
              [(0, 1), (1, 1), (1, 0), (2, 0)],     # Right Z
              [(0, 0), (1, 0), (1, 1), (2, 1)],     # Left Z
              [(1, 0), (0, 1), (1, 1), (2, 1)])     # T

    BOX_SIZE = 20

    GAME_WIDTH = 300
    GAME_HEIGHT = 500
    GAME_START_POINT = GAME_WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE


class GameCanvas(Canvas):
    def completed_lines(self, y_coords):
        cleaned_lines = 0
        all_boxes_coords = [(self.coords(box)[0], self.coords(box)[3])
                            for box in self.find_all()
                            if self.coords(box)[3] in y_coords]
        
        for y in y_coords:
            if all( (x, y) in all_boxes_coords for x in range(10, Utility.GAME_WIDTH - 10, Utility.BOX_SIZE) ):
                # Clear line
                boxes_to_delete = [box
                                   for box in self.find_all()
                                   if self.coords(box)[3] == y]
                for box in boxes_to_delete:
                    self.delete(box)

                # Drop boxes
                boxes_to_drop = [box
                                 for box in self.find_all()
                                 if self.coords(box)[3] < y]
                for box in boxes_to_drop:
                    self.move(box, 0, Utility.BOX_SIZE)

                cleaned_lines += 1
        return cleaned_lines

"""
Do these properties also need setters?

    @coords.setter
    def coords(self, value):
        self.__piece = value
"""

class Piece():
    def __init__(self):
        self.__piece = choice(Utility.PIECES)

    @property
    def coords(self):
        return self.__piece

    def rotate(self):  
        self.__piece = self.__rotate()
    
    def rotate_directions(self):
        rotated = self.__rotate()
        directions = [(rotated[i][0] - self.__piece[i][0],
                       rotated[i][1] - self.__piece[i][1]) for i in range(len(self.__piece))]

        return directions

    def __rotate(self):
        max_x = max(self.__piece, key=lambda x:x[0])[0]
        new_original = (max_x, 0)

        return [(new_original[0] - coord[1],
                 new_original[1] + coord[0]) for coord in self.__piece]


# Just a small, wtf does Square do and what does Box do? Maybe just don't get you here :p
class Box():
    def __init__(self, canvas, coord, tag = -1):
        self.__canvas = canvas
        self.__tag = tag
        if tag < 0:
            self.__tag = self.__draw_on_canvas(coord)

    @property
    def coords(self):
        return self.__canvas.coords(self.__tag)

    @property
    def tag(self):
        return self.__tag
        
    def move(self, movement):
        moved_x, moved_y = movement
        self.__canvas.move(self.__tag,
                           moved_x,
                           moved_y)

    def __draw_on_canvas(self, coord):
        x_left, y_up, x_right, y_down = coord
        return self.__canvas.create_rectangle(x_left,
                                              y_up,
                                              x_right,
                                              y_down,
                                              fill="blue")

class Square():
    def __init__(self, canvas, start_point, piece = None):
        self.piece = piece
        if not piece:
            self.piece = Piece()
        self.canvas = canvas
        self.boxes = self.__create_boxes(start_point)

    def move(self, direction):
        if all(self.__can_move(box.coords, direction) for box in self.boxes):
            x, y = direction
            for box in self.boxes:
                box.move((x * Utility.BOX_SIZE, y * Utility.BOX_SIZE))
            return True
        return False

    def rotate(self):
        directions = self.piece.rotate_directions()
        if all(self.__can_move(self.boxes[i].coords, directions[i]) for i in range(len(self.boxes))):
            self.piece.rotate()
            for i in range(len(self.boxes)):
                x, y = directions[i]
                self.boxes[i].move((x * Utility.BOX_SIZE, y * Utility.BOX_SIZE))

    def __create_boxes(self, start_point):
        boxes = []
        for coord in self.piece.coords:
            x, y = coord
            box_coord = (x * Utility.BOX_SIZE + start_point,
                         y * Utility.BOX_SIZE,
                         x * Utility.BOX_SIZE + Utility.BOX_SIZE + start_point,
                         y * Utility.BOX_SIZE + Utility.BOX_SIZE)
            boxes += [Box(self.canvas, box_coord)]

        return boxes

    def __can_move(self, box_coords, new_pos):
        x, y = new_pos
        x = x * Utility.BOX_SIZE
        y = y * Utility.BOX_SIZE
        x_left, y_up, x_right, y_down = box_coords

        overlap = set(self.canvas.find_overlapping((x_left + x_right) / 2 + x, 
                                                   (y_up + y_down) / 2 + y, 
                                                   (x_left + x_right) / 2 + x,
                                                   (y_up + y_down) / 2 + y))
        other_items = set(self.canvas.find_all()) - set([box.tag for box in self.boxes])

        if y_down + y > Utility.GAME_HEIGHT or \
           x_left + x < 0 or \
           x_right + x > Utility.GAME_WIDTH or \
           overlap & other_items:
            return False
        return True        


# I broke the Label with this, but this is more how properties work ^^
class Tetris():
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def blockcount(self):
        return self._blockcount

    @blockcount.setter
    def blockcount(self, blockcount):
        self._blockcount = blockcount

    def __init__(self):
        self.level = 1
        self.score = 0
        self.blockcount = 0
        self.speed = 500
        self.root = Tk()
        self.root.geometry("500x550") 
        self.root.title('Tetris')
        self.root.bind("<Key>", self.game_control)
        self.__game_canvas()
        self.__level_score_label()
        self.__next_square_canvas()

    def game_control(self, event):
        if event.char in ["a", "A", "\uf702"]:
            self.current_square.move((-1, 0))
        elif event.char in ["d", "D", "\uf703"]:
            self.current_square.move((1, 0))
        # Hard drop left for now, I wanna do it different...
        # 1. Have a mirror piece, (What the piece will look like, if you do the "hard drop")
        # 2. When "Hard Drop" is pressed, Fill the mirror piece and delete the old one. No more clunky speed things :)
        # 
        # elif event.char in ["s", "S", "\uf701"]:
        #     self.hard_drop()
        elif event.char in ["w", "W", "\uf700"]:
            self.current_square.rotate()

    # Is this after a Pause? Or a new_game?
    def new_game(self):
        self.score = 0
        self.blockcount = 0
        self.level = 1

        self.canvas.delete("all")
        self.next_canvas.delete("all")

    def start(self):
        self.new_game()

        self.current_square = Square(self.canvas, Utility.GAME_START_POINT)
        self.next_square = Square(self.next_canvas, 0)

        self.canvas.update()
        self.root.after(self.speed, None)
        self.drop()
        self.root.mainloop()
        
    def drop(self):
        if not self.current_square.move((0,1)):
            self.completed_lines()

            self.current_square = Square(self.canvas, Utility.GAME_START_POINT, self.next_square.piece)
            self.next_canvas.delete("all")
            self.next_square = Square(self.next_canvas, 0)

            if self.is_game_over():
                return 

            self.blockcount += 1
                
        self.root.after(self.speed, self.drop)

    def update_status(self):        
        self.status_var.set(f"Level: {self.level}, Score: {self.score}")
        self.status.update()

    def is_game_over(self):
        if not self.current_square.move((0,1)):
            self.play_again_btn = Button(self.root, text="Play Again", command=self.play_again)
            self.quit_btn = Button(self.root, text="Quit", command=self.quit) 
            self.play_again_btn.place(x = Utility.GAME_WIDTH + 10, y = 200, width=100, height=25)
            self.quit_btn.place(x = Utility.GAME_WIDTH + 10, y = 300, width=100, height=25)
            return True
        return False

    def play_again(self):
        self.play_again_btn.destroy()
        self.quit_btn.destroy()
        self.start()

    def quit(self):
        self.root.quit()     

    def completed_lines(self):
        y_coords = [box.coords[3] for box in self.current_square.boxes]
        self.score += self.canvas.completed_lines(y_coords)
        

    def __game_canvas(self):
        self.canvas = GameCanvas(self.root, 
                             width = Utility.GAME_WIDTH, 
                             height = Utility.GAME_HEIGHT)
        self.canvas.pack(padx=5 , pady=10, side=LEFT)

    def __level_score_label(self):
        self.status_var = StringVar()        
        self.status = Label(self.root, 
                            textvariable=self.status_var, 
                            font=("Helvetica", 10, "bold"))
        self.status.place(x = Utility.GAME_WIDTH + 10, y = 100, width=100, height=25)

    def __next_square_canvas(self):
        self.next_canvas = Canvas(self.root,
                                 width = 60,
                                 height = 60)
        self.next_canvas.pack(padx=5 , pady=10)
    


if __name__ == '__main__':
    game = Tetris()
    game.start()
