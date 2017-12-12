from tkinter import *

def callback(event):
    
    board.coords(pieces[0], (event.x, event.y, event.x + 100, event.y + 50))
    board.coords(pieces[1], (event.x + 50, event.y + 50, event.x + 150, event.y + 100))

root = Tk()

board = Canvas(root, width = 300, height = 500)
board.pack()


piece1 = board.create_rectangle(0, 0, 100, 50, fill="blue")
piece2 = board.create_rectangle(50, 50, 150, 100, fill="blue")

pieces = [piece1, piece2]
root.bind('<Button-1>', callback)
mainloop()

