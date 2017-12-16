from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from square import Square
from utility import *
from views import GameCanvas



class Tetris():

    def __init__(self):
        self._level = 1
        self._score = 0
        self._blockcount = 0

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
        elif event.char in ["s", "S", "\uf701"]:
            self.hard_drop()
        elif event.char in ["w", "W", "\uf700"]:
            self.current_square.rotate()

    def resume(self):
        self.score = 0
        self.blockcount = 0

        self.canvas.delete("all")
        self.next_canvas.delete("all")

    def start(self):
        self.resume()

        self.current_square = Square(self.canvas, GAME_START_POINT)
        self.next_square = Square(self.next_canvas, 0)

        self.canvas.update()
        self.root.after(self.speed, None)
        self.drop()
        self.root.mainloop()
        
    def drop(self):
        if not self.current_square.move((0,1)):
            self.completed_lines()

            self.current_square = Square(self.canvas, GAME_START_POINT, self.next_square.piece)
            self.next_canvas.delete("all")
            self.next_square = Square(self.next_canvas, 0)

            #reset speed from hard drop
            self.level = self.level

            if self.is_game_over():
                return 

            self.blockcount += 1
                
        self.root.after(self.speed, self.drop)
    
    def hard_drop(self):
        self.speed = 10

    def update_status(self):
        self.status_var.set(f"Level: {self.level}, Score: {self.score}")
        self.status.update()

    def is_game_over(self):
        if not self.current_square.move((0,1)):
            self.play_again_btn = Button(self.root, text="Play Again", command=self.play_again)
            self.quit_btn = Button(self.root, text="Quit", command=self.quit) 
            self.play_again_btn.place(x = GAME_WIDTH + 10, y = 200, width=100, height=25)
            self.quit_btn.place(x = GAME_WIDTH + 10, y = 300, width=100, height=25)

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
                             width = GAME_WIDTH, 
                             height = GAME_HEIGHT)
        self.canvas.pack(padx=5 , pady=10, side=LEFT)

    def __level_score_label(self):
        self.status_var = StringVar()        
        self.status = Label(self.root, 
                            textvariable=self.status_var, 
                            font=("Helvetica", 10, "bold"))
        self.status.place(x = GAME_WIDTH + 10, y = 100, width=100, height=25)

    def __next_square_canvas(self):
        self.next_canvas = Canvas(self.root,
                                 width = 60,
                                 height = 60)
        self.next_canvas.pack(padx=5 , pady=10)
    
    #set & get
    def __get_level(self):
        return self._level

    def __set_level(self, level):
        self.speed = 500 - (level - 1) * 25
        self._level = level
        self.update_status()

    def __get_score(self):
        return self._score

    def __set_score(self, score):
        self._score = score
        self.update_status()

    def __get_blockcount(self):
        return self._blockcount

    def __set_blockcount(self, blockcount):
        self.level = blockcount // 5 + 1
        self._blockcount = blockcount

    level = property(__get_level, __set_level)
    score = property(__get_score, __set_score)
    blockcount = property(__get_blockcount, __set_blockcount)


if __name__ == '__main__':
    game = Tetris()
    game.start()

