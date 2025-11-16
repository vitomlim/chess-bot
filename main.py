import pygame as pg
import sys

pg.init()
window = pg.display.set_mode((1000, 1000))

class board:
  def __init__(self):
    self.size = 1000
    self.squareSize = self.size / 8

    self.moves = int("00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000", 2)

    self.wRooks = int("00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "10000001", 2)

    self.bRooks = int("10000001"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000", 2)

    self.wKnights = int("00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "01000010", 2)

    self.bKnights = int("01000010"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000", 2)

    self.wBishops = int("00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00100100", 2)

    self.bBishops = int("00100100"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000"
                        "00000000", 2)

    self.wQueens = int("00000000"
                       "00000000"
                       "00000000"
                       "00000000"
                       "00000000"
                       "00000000"
                       "00000000"
                       "00010000", 2)

    self.bQueens = int("00010000"
                       "00000000"
                       "00000000"
                       "00000000"
                       "00000000"
                       "00000000"
                       "00000000"
                       "00000000", 2)

    self.wKing = int("00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00001000", 2)

    self.bKing = int("00001000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000"
                     "00000000", 2)

    self.wPawns = int("00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "11111111"
                      "00000000", 2)

    self.bPawns = int("00000000"
                      "11111111"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000"
                      "00000000", 2)

  def pieces(self):
    return {'wRook': self.wRooks, 'bRook': self.bRooks,
            'wKnight': self.wKnights, 'bKnight': self.bKnights,
            'wBishop': self.wBishops, 'bBishop': self.bBishops,
            'wQueen': self.wQueens, 'bQueen': self.bQueens,
            'wKing': self.wKing, 'bKing': self.bKing,
            'wPawn': self.wPawns, 'bPawn': self.bPawns}

  # bitboards for each color, used for calculating moves
  def whitePieces(self):
    return self.wRooks | self.wKnights | self.wBishops | self.wQueens | self.wKing | self.wPawns

  def blackPieces(self):
    return self.bRooks | self.bKnights | self.bBishops | self.bQueens | self.bKing | self.bPawns


  # position is counted from right to left and from bottom to top
  def getSquare(self, mousePosition):
    return int(63 - ((mousePosition[0] // self.squareSize) + (mousePosition[1] // self.squareSize) * 8))


  # only executed on input, not insanely optimized
  def getPiece(self, square):
    for pieceName, pieceState in self.pieces().items():
      pieceState >>= square
      if pieceState & 1:
        return pieceName
    return 'empty'


  # could use bitboards for every piece in every square, but thats too monkey
  def updateMoves(self, square, pieceName):
    if pieceName == 'empty':
      self.moves = 0
    else:
      pieceColor = pieceName[0]
      if pieceName[1:] == 'Rook':
        pass


  # drawing functions
  def drawBackground(self, display):
    for y in range(8):
      for x in range(8):
        if (x + y) % 2 == 0:
          color = (229, 230, 203)
        else:
          color = (112, 146, 80)

        square = pg.Rect(x * self.squareSize, y * self.squareSize, self.squareSize, self.squareSize)
        pg.draw.rect(display, color, square)

  def drawPieces(self, display):
    for pieceName, pieceState in self.pieces().items():
      img = pg.image.load('./assets/' + pieceName + '.png')
      img = pg.transform.scale(img, (self.squareSize, self.squareSize))

      # kernighan algorithm
      while pieceState:
        b = pieceState & -pieceState
        square = 64 - b.bit_length()
        x = (square % 8) * self.squareSize
        y = (square // 8) * self.squareSize
        display.blit(img, (x , y))
        pieceState &= pieceState - 1

  def drawMoves(self, display):
    pass

  def draw(self, display):
    self.drawBackground(display)
    self.drawPieces(display)
    self.drawMoves(display)


gameBoard = board()

running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
    
    if event.type == pg.MOUSEBUTTONDOWN:
      square = gameBoard.getSquare(pg.mouse.get_pos())
      gameBoard.updateMoves(square, gameBoard.getPiece(square))

  gameBoard.draw(window)
  pg.display.flip()

pg.quit()
sys.exit()
