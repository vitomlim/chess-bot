import pygame as pg
import sys

pg.init()
window = pg.display.set_mode((1000, 1000))

class board:
  def __init__(self):
    self.size = 1000
    self.squareSize = self.size / 8

    # ---------------------------------------------------------------------
    # -------------------- STARTING POSITION BITBOARDS --------------------
    # ---------------------------------------------------------------------

    self.moves = int("0" * 64, 2)
    self.wRooks = int("00000000" * 7 + "10000001", 2)
    self.bRooks = int("10000001" + "00000000" * 7, 2)
    self.wKnights = int("00000000" * 7 + "01000010", 2)
    self.bKnights = int("01000010" + "00000000" * 7, 2)
    self.wBishops = int("00000000" * 7 + "00100100", 2)
    self.bBishops = int("00100100" + "00000000" * 7, 2)
    self.wQueens = int("00000000" * 7 + "00010000", 2)
    self.bQueens = int("00010000" + "00000000" * 7, 2)
    self.wKing = int("00000000" * 7 + "00001000", 2)
    self.bKing = int("00001000" + "00000000" * 7, 2)
    self.wPawns = int("00000000" * 6 + "11111111" + "00000000", 2)
    self.bPawns = int("00000000" + "11111111" + "00000000" * 6, 2)

    self.whitePieces = self.wRooks | self.wKnights | self.wBishops | self.wQueens | self.wKing | self.wPawns
    self.blackPieces = self.bRooks | self.bKnights | self.bBishops | self.bQueens | self.bKing | self.bPawns
    self.allPieces = self.whitePieces | self.blackPieces

    # -------------------------------------------------------
    # -------------------- LOOKUP TABLES --------------------
    # -------------------------------------------------------

    # rook
    rightMoves = [0] * 64
    leftMoves = [0] * 64
    upMoves = [0] * 64
    downMoves = [0] * 64

    for square in range(64):
      x = square % 8
      y = square // 8

      for dx in range(x - 1, -1, -1):
        rightMoves[square] |= (1 << (y * 8 + dx))

      for dx in range(x + 1, 8):
        leftMoves[square] |= (1 << (y * 8 + dx))

      for dy in range(y + 1, 8):
        upMoves[square] |= (1 << (dy * 8 + x))

      for dy in range(y - 1, -1, -1):
        downMoves[square] |= (1 << (dy * 8 + x))

    self.rookMoves = [rightMoves, leftMoves, upMoves, downMoves]

    # knight
    self.knightMoves = [0] * 64
    for square in range(64):
      x = square % 8
      y = square // 8

      for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
        if (0 <= x + dx <= 7) & (0 <= y + dy <= 7):
          self.knightMoves[square] |= (1 << ((y + dy) * 8 + (x + dx)))

    # bishop
    upRightMoves = [0] * 64
    upLeftMoves = [0] * 64
    downRightMoves = [0] * 64
    downLeftMoves = [0] * 64

    for square in range(64):
      x = square % 8
      y = square // 8

      for d in range(1, min(x + 1, 8 - y)):
        upRightMoves[square] |= (1 << ((y + d) * 8 + (x - d)))

      for d in range(1, min(8 - x, 8 - y)):
        upLeftMoves[square] |= (1 << ((y + d) * 8 + (x + d)))

      for d in range(1, min(x + 1, y + 1)):
        downRightMoves[square] |= (1 << ((y - d) * 8 + (x - d)))

      for d in range(1, min(8 - x, y + 1)):
        downLeftMoves[square] |= (1 << ((y - d) * 8 + (x + d)))

    self.bishopMoves = [upRightMoves, upLeftMoves, downRightMoves, downLeftMoves]

    # queen (just merged rook and bishop)
    self.queenMoves = [rightMoves, leftMoves, upMoves, downMoves, upRightMoves, upLeftMoves, downRightMoves, downLeftMoves]

    # king
    self.kingMoves = [0] * 64
    for square in range(64):
      x = square % 8
      y = square // 8

      for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        if (0 <= x + dx <= 7) & (0 <= y + dy <= 7):
          self.kingMoves[square] |= (1 << ((y + dy) * 8 + (x + dx)))

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


  # using the lookup tables calculates collisions and returns possible moves for the given square
  # used for rooks, bishops and queens
  def calculateCollisions(self, square, movesLookupTable, isWhite):
    output = 0
    for directionRay in movesLookupTable:
      blockers = directionRay[square] & self.allPieces
      directionMoves = 0
      if blockers:

        # if the ray points in the positive direction
        if directionRay[square] > (1 << square):
          firstBlocker = blockers & -blockers
          directionMoves = directionRay[square] & ((firstBlocker - 1) | firstBlocker)

        # else (the ray points in the negative direction)
        else:
          firstBlocker = 1 << (blockers.bit_length() - 1)
          directionMoves = directionRay[square] & ~(firstBlocker - 1)
        output |= directionMoves
      else:
        output |= directionRay[square]
    if isWhite:
      output &= ~self.whitePieces
    else:
      output &= ~self.blackPieces
    return output


  def updateMoves(self, square):
    self.selectedSquare = square

    if 1 << square & self.wRooks:
      self.moves = self.calculateCollisions(square, self.rookMoves, 1)

    elif 1 << square & self.bRooks:
      self.moves = self.calculateCollisions(square, self.rookMoves, 0)

    elif 1 << square & self.wKnights:
      self.moves = self.knightMoves[square] & ~self.whitePieces

    elif 1 << square & self.bKnights:
      self.moves = self.knightMoves[square] & ~self.blackPieces

    elif 1 << square & self.wBishops:
      self.moves = self.calculateCollisions(square, self.bishopMoves, 1)

    elif 1 << square & self.bBishops:
      self.moves = self.calculateCollisions(square, self.bishopMoves, 0)

    elif 1 << square & self.wQueens:
      self.moves = self.calculateCollisions(square, self.queenMoves, 1)

    elif 1 << square & self.bQueens:
      self.moves = self.calculateCollisions(square, self.queenMoves, 0)

    elif 1 << square & self.wKing:
      self.moves = self.kingMoves[square] & ~self.whitePieces

    elif 1 << square & self.bKing:
      self.moves = self.kingMoves[square] & ~self.blackPieces

    elif 1 << square & self.wPawns:
      pass

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
      pg.draw.circle(transparentCircle, (0, 0, 0, 128), (self.squareSize / 2, self.squareSize / 2), self.squareSize / 4)
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
