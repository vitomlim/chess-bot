import pygame as pg
import sys

class board:
  def __init__(self):
    self.wRooks = [0, 0, 0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0,
                   1, 0, 0, 0, 0, 0, 0, 1]

  def drawPiece(self, piece, square, squareSize):
    img = pg.image.load('./assets/' + piece + '.png')
    img = pg.transform.scale(img, (squareSize, squareSize))
    window.blit(img, ((square % 8) * squareSize, (square // 8) * squareSize))

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
        self.drawPiece('wRook', square, squareSize)

  def checkEvent(self, mousePosition, squareSize):
    square = (mousePosition[0] // squareSize) + (mousePosition[1] // squareSize) * 8
    
    if self.wRooks[square]:
      wRooks.checkMoves


pg.init()
screenSize = 400
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
