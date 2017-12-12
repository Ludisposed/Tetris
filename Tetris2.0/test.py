from tkinter import *



def callback(event):
    global start_x
    print(event.char)
    if event.char in ["a", "\uf702"]:
      print("go left")
      start_x -= 10
      if start_x < 0:
        start_x = 0
    elif event.char in ["d", "\uf703"]:
      print("go right")
      start_x += 10
      if start_x > 200:
        start_x = 200
    elif event.char in ["s", "\uf701"]:
      print("rotate")
      
    
    
    board.coords(pieces[0], (start_x, start_y, start_x + 100, start_y + 50))
    board.coords(pieces[1], (start_x + 50, start_y + 50, start_x + 150, start_y + 100))

root = Tk()
start_x, start_y = 0, 0
board = Canvas(root, width = 300, height = 500)
board.pack()


piece1 = board.create_rectangle(0, 0, 100, 50, fill="blue")
piece2 = board.create_rectangle(50, 50, 150, 100, fill="blue")

pieces = [piece1, piece2]
root.bind('<Key>', callback)
mainloop()

