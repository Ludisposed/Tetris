from tkinter import *

def callback(event):
    board.coords(piece, (event.x, event.y, 50, 50))

root = Tk()

board = Canvas(root, width = 300, height = 500)
board.pack()

piece = board.create_rectangle(0, 0, 50, 50, fill="blue")
root.bind('<Button-1>', callback)
mainloop()

