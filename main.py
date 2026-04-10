from ctypes import *

engine = CDLL("./engine.so")

class Board(Structure):
    _fields_ = [
        ("bRooks", c_uint64),
        ("bKnights", c_uint64),
        ("bBishops", c_uint64),
        ("bQueens", c_uint64),
        ("bKing", c_uint64),
        ("bPawns", c_uint64),
        ("wRooks", c_uint64),
        ("wKnights", c_uint64),
        ("wBishops", c_uint64),
        ("wQueens", c_uint64),
        ("wKing", c_uint64),
        ("wPawns", c_uint64),
    ]


FENString = '4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1'
engine.initializeBoard.argtypes = [c_char_p]
engine.initializeBoard(FENString.encode('utf-8'))

engine.getBoard.restype = Board












import pygame as pg

pg.init()
windowSize = 960
squareSize = windowSize / 8
window = pg.display.set_mode((windowSize, windowSize))

# # # #
board = engine.getBoard()
# # # #

# sprite initialization
spriteDictionary = {}
for pieceName in [field for field in dir(board) if not field.startswith("_")]:
    img = pg.image.load('./assets/' + pieceName + '.png')
    img = pg.transform.smoothscale(img, (squareSize, squareSize))
    spriteDictionary[pieceName] = img

def drawBoard():
    # drawing the background
    for y in range(8):
        for x in range(8):
            if (x + y) % 2 == 0:
                color = (229, 230, 203)
            else:
                color = (112, 146, 80)

            square = pg.Rect(x * squareSize, y * squareSize, squareSize, squareSize)
            pg.draw.rect(window, color, square)

    # drawing the pieces
    for piece in [field for field in dir(board) if not field.startswith("_")]:
        bitBoard = getattr(board, piece)
        for square in range(64):
            if(bitBoard >> square) & 1:
                x = (square % 8) * squareSize
                y = (square // 8) * squareSize
                window.blit(spriteDictionary[piece], (x, y))


drawBoard()
pg.display.flip()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            drawBoard()
            pg.display.flip()



pg.quit()
