from tkinter import Canvas
from utility import *

class GameCanvas(Canvas):

    def completed_lines(self, y_coords):
        cleaned_lines = 0
        all_boxes_coords = [(self.coords(box)[0], self.coords(box)[3])
                            for box in self.find_all()
                            if self.coords(box)[3] in y_coords]
        
        for y in y_coords:
            if all( (x, y) in all_boxes_coords for x in range(10, GAME_WIDTH - 10, BOX_SIZE) ):
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
                    self.move(box, 0, BOX_SIZE)

                cleaned_lines += 1
        return cleaned_lines
