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

        self.canvas = Canvas(
                self.root, 
                width = Tetris.WIDTH, 
                height = Tetris.HEIGHT
        )
        self.canvas.pack()

        self.root.bind("<Key>", self.handle_events)
        self.timer()
        self.root.mainloop()

    def timer(self):
        pass

    def handle_events(self, event):
        pass

game = Tetris()
    
