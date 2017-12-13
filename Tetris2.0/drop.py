from tkinter import *
from random import randint, choice
from time import sleep
def callback(event):
    pass
def drop():
  for piece in pieces:
      board.move(piece, 0, 10)
  #check boundary and return early
  root.after(2000, drop)

root = Tk()

board = Canvas(root, width = 300, height = 500)
board.pack()


positions = ((0,0),(1,0),(1,1),(2,1))

width, height = 50, 50

pieces = []
for pos in positions:
  x,y = pos
  pieces.append(board.create_rectangle(x * width, y * height, \
               (x + 1) * width, (y + 1) *  height, fill="blue"))

root.bind('<Key>', callback)

drop()
  
mainloop()


