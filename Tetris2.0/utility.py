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

