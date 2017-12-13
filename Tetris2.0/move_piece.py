from tkinter import *
from random import randint, choice

def callback(event):
    offset = 0

    #without check boundary here
    #but I will add later in rotate maybe
    print(event.char)
    if event.char in ["a", "\uf702"]:
      print("go left")
      offset = -10
    elif event.char in ["d", "\uf703"]:
      print("go right")
      offset = 10
    elif event.char in ["s", "\uf701"]:
      print("rotate")
    

    '''
    move the pieces
    '''
    for piece in pieces:
      board.move(piece, offset, 0)



root = Tk()

board = Canvas(root, width = 300, height = 500)
board.pack()

'''
This will be a piece like this

 ##
  ##

positons are the cords of this four blocks
'''
positions = ((0,0),(1,0),(1,1),(2,1))

'''
draw this piece on board(Canvas)

board.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill=<color>)

so for

x, y = pos

board.create_rectangle(x * width, y * height, (x + 1) * width, (y + 1) *  height, fill=<color>)

'''
width, height = 50, 50

pieces = []
for pos in positions:
  x,y = pos
  pieces.append(board.create_rectangle(x * width, y * height, (x + 1) * width, (y + 1) *  height, fill="blue"))

'''
bind event call back function
'''
root.bind('<Key>', callback)
mainloop()


