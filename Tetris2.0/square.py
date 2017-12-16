from tkinter import Canvas
from random import choice, randint
from utility import *

class Piece():
    
    def __init__(self):
        self.__piece = choice(PIECES)

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
                box.move((x * BOX_SIZE, y * BOX_SIZE))
            return True
        return False

    def rotate(self):
        directions = self.piece.rotate_directions()
        if all(self.__can_move(self.boxes[i].coords, directions[i]) for i in range(len(self.boxes))):
            self.piece.rotate()
            for i in range(len(self.boxes)):
                x, y = directions[i]
                self.boxes[i].move((x * BOX_SIZE, y * BOX_SIZE))

    def __create_boxes(self, start_point):
        boxes = []
        for coord in self.piece.coords:
            x, y = coord
            box_coord = (x * BOX_SIZE + start_point,
                         y * BOX_SIZE,
                         x * BOX_SIZE + BOX_SIZE + start_point,
                         y * BOX_SIZE + BOX_SIZE)
            boxes += [Box(self.canvas, box_coord)]

        return boxes

    def __can_move(self, box_coords, new_pos):
        x, y = new_pos
        x = x * BOX_SIZE
        y = y * BOX_SIZE
        x_left, y_up, x_right, y_down = box_coords

        overlap = set(self.canvas.find_overlapping((x_left + x_right) / 2 + x, 
                                                   (y_up + y_down) / 2 + y, 
                                                   (x_left + x_right) / 2 + x,
                                                   (y_up + y_down) / 2 + y))
        other_items = set(self.canvas.find_all()) - set([box.tag for box in self.boxes])

        if y_down + y > GAME_HEIGHT or \
           x_left + x < 0 or \
           x_right + x > GAME_WIDTH or \
           overlap & other_items:
            return False
        return True