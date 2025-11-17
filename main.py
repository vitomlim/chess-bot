import pygame as pg
import sys

pg.init()
window = pg.display.set_mode((1000, 1000))

class board:
  def __init__(self):
    self.size = 1000
    self.squareSize = self.size / 8


    # original position
    self.moves = int("0" * 64, 2)
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
                        "00001000"
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
                        "00010000"
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

    self.whitePieces = self.wRooks | self.wKnights | self.wBishops | self.wQueens | self.wKing | self.wPawns
    self.blackPieces = self.bRooks | self.bKnights | self.bBishops | self.bQueens | self.bKing | self.bPawns
    self.allPieces = self.whitePieces | self.blackPieces

    # rook moves lookup table generation
    rightMoves = [0] * 64
    leftMoves = [0] * 64
    upMoves = [0] * 64
    downMoves = [0] * 64

    for square in range(64):
      x = square % 8
      y = square // 8

      mask = 0
      for dx in range(x - 1, -1, -1):
        mask |= (1 << (y * 8 + dx))
      rightMoves[square] = mask

      mask = 0
      for dx in range(x + 1, 8):
        mask |= (1 << (y * 8 + dx))
      leftMoves[square] = mask

      mask = 0
      for dy in range(y + 1, 8):
        mask |= (1 << (dy * 8 + x))
      upMoves[square] = mask

      mask = 0
      for dy in range(y - 1, -1, -1):
        mask |= (1 << (dy * 8 + x))
      downMoves[square] = mask

    self.rookMoves = [rightMoves, leftMoves, upMoves, downMoves]


    # knight moves lookup table generation
    self.knightMoves = [0] * 64
    for square in range(64):
      x = square % 8
      y = square // 8

      for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
        if (0 <= x + dx <= 7) & (0 <= y + dy <= 7):
          self.knightMoves[square] |= (1 << ((y + dy) * 8 + (x + dx)))


    # bishop moves lookup table generation
    upRightMoves = [0] * 64
    upLeftMoves = [0] * 64
    downRightMoves = [0] * 64
    downLeftMoves = [0] * 64

    for square in range(64):
      x = square % 8
      y = square // 8

      mask = 0
      for d in range(1, min(x + 1, 8 - y)):
        mask |= (1 << ((y + d) * 8 + (x - d)))
      upRightMoves[square] = mask

      mask = 0
      for d in range(1, min(8 - x, 8 - y)):
        mask |= (1 << ((y + d) * 8 + (x + d)))
      upLeftMoves[square] = mask

      mask = 0
      for d in range(1, min(x + 1, y + 1)):
        mask |= (1 << ((y - d) * 8 + (x - d)))
      downRightMoves[square] = mask

      mask = 0
      for d in range(1, min(8 - x, y + 1)):
        mask |= (1 << ((y - d) * 8 + (x + d)))
      downLeftMoves[square] = mask

    self.bishopMoves = [upRightMoves, upLeftMoves, downRightMoves, downLeftMoves]


  def pieces(self):
    return {'wRooks': self.wRooks, 'bRooks': self.bRooks,
            'wKnights': self.wKnights, 'bKnights': self.bKnights,
            'wBishops': self.wBishops, 'bBishops': self.bBishops,
            'wQueens': self.wQueens, 'bQueens': self.bQueens,
            'wKing': self.wKing, 'bKing': self.bKing,
            'wPawns': self.wPawns, 'bPawns': self.bPawns}


  # position is counted from right to left and from bottom to top
  def getSquare(self, mousePosition):
    return int(63 - ((mousePosition[0] // self.squareSize) + (mousePosition[1] // self.squareSize) * 8))


  def isMovable(self, square):
    if self.moves & 1 << square:
      return True
    else:
      return False


  def move(self, destinationSquare, originalSquare):

    for pieceName, pieceState in self.pieces().items():
      if pieceState & 1 << originalSquare:
        setattr(self, pieceName, (pieceState | (1 << destinationSquare)) & ~(1 << originalSquare))
      if pieceState & 1 << destinationSquare:
        setattr(self, pieceName, pieceState & ~(1 << destinationSquare))

    self.moves = 0
    self.selectedSquare = -1

    self.whitePieces = self.wRooks | self.wKnights | self.wBishops | self.wQueens | self.wKing | self.wPawns
    self.blackPieces = self.bRooks | self.bKnights | self.bBishops | self.bQueens | self.bKing | self.bPawns
    self.allPieces = self.whitePieces | self.blackPieces


  def updateMoves(self, square):
    self.selectedSquare = square

    # rook collision analysis
    if 1 << square & self.wRooks:

      # right moves
      blockers = self.rookMoves[0][square] & self.allPieces
      rightMoves = 0
      if blockers:
        firstBlocker = 1 << (blockers.bit_length() - 1)
        rightMoves = self.rookMoves[0][square] & ~(firstBlocker - 1)
      else:
        rightMoves = self.rookMoves[0][square]

      # left moves
      blockers = self.rookMoves[1][square] & self.allPieces
      leftMoves = 0
      if blockers:
        firstBlocker = blockers & -blockers
        leftMoves = self.rookMoves[1][square] & ((firstBlocker - 1) | firstBlocker)
      else:
        leftMoves = self.rookMoves[1][square]

      # up moves
      blockers = self.rookMoves[2][square] & self.allPieces
      upMoves = 0
      if blockers:
        firstBlocker = blockers & -blockers
        upMoves = self.rookMoves[2][square] & ((firstBlocker - 1) | firstBlocker)
      else:
        upMoves = self.rookMoves[2][square]

      # down moves
      blockers = self.rookMoves[3][square] & self.allPieces
      downMoves = 0
      if blockers:
        firstBlocker = 1 << (blockers.bit_length() - 1)
        downMoves = self.rookMoves[3][square] & ~(firstBlocker - 1)

      self.moves = (rightMoves | leftMoves | upMoves | downMoves) & ~self.whitePieces

    elif 1 << square & self.bRooks:

      # right moves
      blockers = self.rookMoves[0][square] & self.allPieces
      rightMoves = 0
      if blockers:
        firstBlocker = 1 << (blockers.bit_length() - 1)
        rightMoves = self.rookMoves[0][square] & ~(firstBlocker - 1)
      else:
        rightMoves = self.rookMoves[0][square]

      # left moves
      blockers = self.rookMoves[1][square] & self.allPieces
      leftMoves = 0
      if blockers:
        firstBlocker = blockers & -blockers
        leftMoves = self.rookMoves[1][square] & ((firstBlocker - 1) | firstBlocker)
      else:
        leftMoves = self.rookMoves[1][square]

      # up moves
      blockers = self.rookMoves[2][square] & self.allPieces
      upMoves = 0
      if blockers:
        firstBlocker = blockers & -blockers
        upMoves = self.rookMoves[2][square] & ((firstBlocker - 1) | firstBlocker)
      else:
        upMoves = self.rookMoves[2][square]

      # down moves
      blockers = self.rookMoves[3][square] & self.allPieces
      downMoves = 0
      if blockers:
        firstBlocker = 1 << (blockers.bit_length() - 1)
        downMoves = self.rookMoves[3][square] & ~(firstBlocker - 1)

      self.moves = (rightMoves | leftMoves | upMoves | downMoves) & ~self.blackPieces


    # knight collision analysis except knights dont collide
    elif 1 << square & self.wKnights:
      self.moves = self.knightMoves[square] & ~self.whitePieces

    elif 1 << square & self.bKnights:
      self.moves = self.knightMoves[square] & ~self.blackPieces


    # bishop collision analysis
    elif 1 << square & self.wBishops:

      # up right moves
      blockers = self.bishopMoves[0][square] & self.allPieces
      upRightMoves = 0
      if blockers:
        firstBlocker = blockers & -blockers
        upRightMoves = self.bishopMoves[0][square] & ((firstBlocker - 1) | firstBlocker)
      else:
        upRightMoves = self.bishopMoves[0][square]

      self.moves = upRightMoves

    else:
      self.moves = 0


  def draw(self, display):
    # drawing the background
    for y in range(8):
      for x in range(8):
        if (x + y) % 2 == 0:
          color = (229, 230, 203)
        else:
          color = (112, 146, 80)

        square = pg.Rect(x * self.squareSize, y * self.squareSize, self.squareSize, self.squareSize)
        pg.draw.rect(display, color, square)
 
    # drawing pieces
    for pieceName, pieceState in self.pieces().items():
      img = pg.image.load('./assets/' + pieceName + '.png')
      img = pg.transform.scale(img, (self.squareSize, self.squareSize))

      # iterates through the ones in the bit board
      while pieceState:
        b = pieceState & -pieceState
        square = 64 - b.bit_length()
        x = (square % 8) * self.squareSize
        y = (square // 8) * self.squareSize
        display.blit(img, (x , y))
        pieceState &= pieceState - 1

    # drawing possible moves
    temp = self.moves
    while temp:
      b = temp & -temp
      square = 64 - b.bit_length()
      x = (square % 8)
      y = (square // 8)
      transparentCircle = pg.Surface((self.squareSize, self.squareSize), pg.SRCALPHA)
      pg.draw.circle(transparentCircle, (255, 255, 255, 128), (self.squareSize / 2, self.squareSize / 2), self.squareSize / 4)
      display.blit(transparentCircle, (x * self.squareSize, y * self.squareSize))
      temp &= temp - 1


gameBoard = board()

running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
    
    if event.type == pg.MOUSEBUTTONDOWN:
      square = gameBoard.getSquare(pg.mouse.get_pos())
      if gameBoard.isMovable(square):
        gameBoard.move(square, gameBoard.selectedSquare)
      else:
        gameBoard.updateMoves(square)

  gameBoard.draw(window)
  pg.display.flip()

pg.quit()
sys.exit()
