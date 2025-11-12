import pygame as pg
import sys

class board:
  # initial board config
  def __init__(self):
    self.moves = []
    self.selectedSquare = -1

    self.wRooks = [0, 0, 0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 1, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   1, 0, 0, 0, 0, 0, 0, 1]

    self.wKnights = [0, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 1, 0, 0, 0, 0, 1, 0]

    self.wBishops = [0, 0, 0, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 1, 0, 0, 1, 0, 0]

    self.wQueens = [0, 0, 0, 0, 0, 0, 0, 0, 
                    0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 1, 0, 0, 0, 0]


    self.wKing = [0, 0, 0, 0, 0, 0, 0, 0, 
                  0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 1, 0, 0, 0]

    self.wPawns = [0, 0, 0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   1, 1, 1, 1, 1, 1, 1, 1,
                   0, 0, 0, 0, 0, 0, 0, 0]


  # board drawing
  def drawPiece(self, piece, square, squareSize, window):
    img = pg.image.load('./assets/' + piece + '.png')
    img = pg.transform.scale(img, (squareSize, squareSize))
    window.blit(img, ((square % 8) * squareSize, (square // 8) * squareSize))

  def drawMove(self, square, squareSize, window):
    alphaSurface = pg.Surface((squareSize, squareSize), pg.SRCALPHA)
    pg.draw.circle(alphaSurface, (0, 0, 0, 128), (squareSize / 2, squareSize / 2), squareSize / 8)
    window.blit(alphaSurface, (squareSize * (square % 8), squareSize * (square // 8)))

  def draw(self, window, squareSize):
    # background
    for y in range(8):
      for x in range(8):
        if (x + y) % 2 == 0:
          color = (229, 230, 203)
        else:
          color = (112, 146, 80)

        square = pg.Rect(x * squareSize, y * squareSize, squareSize, squareSize)
        pg.draw.rect(window, color, square)

    # pieces
    for square in range(64):
      if self.wRooks[square]:
        self.drawPiece('wRook', square, squareSize, window)
      elif self.wKnights[square]:
        self.drawPiece('wKnight', square, squareSize, window)
      elif self.wBishops[square]:
        self.drawPiece('wBishop', square, squareSize, window)
      elif self.wQueens[square]:
        self.drawPiece('wQueen', square, squareSize, window)
      elif self.wKing[square]:
        self.drawPiece('wKing', square, squareSize, window)
      elif self.wPawns[square]:
        self.drawPiece('wPawn', square, squareSize, window)

      if square in self.moves:
        self.drawMove(square, squareSize, window)

  def isWhite(self, square):
    if self.wRooks[square] == 1 or self.wKnights[square] == 1 or self.wBishops[square] == 1 or self.wQueens[square] == 1 or self.wKing[square] == 1 or self.wPawns[square] == 1:
      return True
    else:
      return False

  def isBlack(self, square):
    pass

  def checkMoves(self, piece, square):
    output = []

    if piece == 'wRook':
      for dx in range(1, 8 - (square % 8)):
        if self.isWhite(square + dx):
          break
        elif self.isBlack(square + dx):
          output.append(square + dx)
          break
        else:
          output.append(square + dx)
      for dx in range(1, (square % 8) + 1):
        if self.isWhite(square - dx):
          break
        elif self.isBlack(square - dx):
          output.append(square - dx)
          break
        else:
          output.append(square - dx)
      for dy in range(8, 64 - (square // 8), 8):
        if self.isWhite(square + dy):
          break
        elif self.isBlack(square + dy):
          output.append(square + dy)
          break
        else:
          output.append(square + dy)
      for dy in range(8, square + 8, 8):
        if self.isWhite(square - dy):
          break
        elif self.isBlack(square - dy):
          output.append(square - dy)
          break
        else:
          output.append(square - dy)
    self.moves = output

  def checkEvent(self, mousePosition, squareSize):
    square = int((mousePosition[0] // squareSize) + (mousePosition[1] // squareSize) * 8)
    if square in self.moves:

    if self.wRooks[square]:
      self.checkMoves('wRook', square)
      print(self.moves)

pg.init()
screenSize = 1000
squareSize = screenSize / 8
window = pg.display.set_mode((screenSize, screenSize))
pg.display.set_caption('chess bot')
gameBoard = board()


running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
    
    if event.type == pg.MOUSEBUTTONDOWN:
      mousePosition = pg.mouse.get_pos()
      gameBoard.checkEvent(mousePosition, squareSize)

  gameBoard.draw(window, squareSize)

  pg.display.flip()

pg.quit()
sys.exit()
