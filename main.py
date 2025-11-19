import pygame as pg
import sys

pg.init()
window = pg.display.set_mode((960, 960))

class board:
  def __init__(self):
    self.size = 960
    self.squareSize = self.size / 8

    # ---------------------------------------------------------------------
    # -------------------- STARTING POSITION BITBOARDS --------------------
    # ---------------------------------------------------------------------

    self.moves = int("0" * 64, 2)
    self.lastMove = int("0" * 64, 2)

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

    self.wBigCastleRights = True
    self.wSmallCastleRights = True
    self.bBigCastleRights = True
    self.bSmallCastleRights = True

    self.isWhiteTurn = True

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

    # adding castling
    self.wKingSmallCastleMove = 1 << 1
    self.wKingBigCastleMove = 1 << 5
    self.bKingSmallCastleMove = 1 << 57
    self.bKingBigCastleMove = 1 << 61

    self.wSmallCastleBlockers = 1 << 1 | 1 << 2
    self.wBigCastleBlockers = 1 << 4 | 1 << 5 | 1 << 6
    self.bSmallCastleBlockers = 1 << 57 | 1 << 58
    self.bBigCastleBlockers = 1 << 60 | 1 << 61 | 1 << 62

    # pawn
    self.wPawnMoves = [0] * 64
    for square in range(64):
      y = square // 8

      if y != 7:
        self.wPawnMoves[square] |= (1 << square + 8)
        if y == 1:
          self.wPawnMoves[square] |= (1 << square + 16)

    self.wPawnCaptures = [0] * 64
    for square in range(64):
      x = square % 8
      y = square // 8

      if y != 7:
        if x > 0:
          self.wPawnCaptures[square] |= (1 << square + 7)
        if x < 7:
          self.wPawnCaptures[square] |= (1 << square + 9)

    self.bPawnMoves = [0] * 64
    for square in range(64):
      y = square // 8

      if y != 0:
        self.bPawnMoves[square] |= (1 << square - 8)
        if y == 6:
          self.bPawnMoves[square] |= (1 << square - 16)

    self.bPawnCaptures = [0] * 64
    for square in range(64):
      x = square % 8
      y = square // 8

      if y != 0:
        if x > 0:
          self.bPawnCaptures[square] |= (1 << square - 9)
        if x < 7:
          self.bPawnCaptures[square] |= (1 << square - 7)

  # -----------------------------------------------------------
  # -------------------- UTILITY FUNCTIONS --------------------
  # -----------------------------------------------------------

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
    return self.moves & 1 << square

  # ----------------------------------------------------------
  # -------------------- MOVING FUNCTIONS --------------------
  # ----------------------------------------------------------

  def castleMoveHandling(self, pieceName, destinationSquare, originalSquare):

    if self.wSmallCastleRights:
      # removing castling rights and handling rook castle movement
      if pieceName == 'wKing':
        self.wSmallCastleRights = False
        # if is small castling (wKing from original square to square 1)
        if destinationSquare == 1:
          self.wRooks |= 1 << 2
          self.wRooks &= ~1

      # removing castling rights for right rook movement/losing
      if originalSquare == 0 or destinationSquare == 0:
        self.wSmallCastleRights = False

    if self.wBigCastleRights:
      # removing castling rights and handling rook castle movement
      if pieceName == 'wKing':
        self.wBigCastleRights = False
        # if is big castling (wKing from original square to square 5)
        if destinationSquare == 5:
          self.wRooks |= 1 << 4
          self.wRooks &= ~(1 << 7)

      # removing castling rights for left rook movement/losing
      if originalSquare == 7 or destinationSquare == 7:
        self.wBigCastleRights = False

    if self.bSmallCastleRights:
      # removing castling rights and handling rook castle movement
      if pieceName == 'bKing':
        self.bSmallCastleRights = False
        # if is small castling (bKing from original square to square 57)
        if destinationSquare == 57:
          self.bRooks |= 1 << 58
          self.bRooks &= ~(1 << 56)

      # removing castling rights for right rook movement/losing
      if originalSquare == 56 or destinationSquare == 56:
        self.bSmallCastleRights = False

    if self.bBigCastleRights:
      # removing castling rights and handling rook castle movement
      if pieceName == 'bKing':
        self.bBigCastleRights = False
        # if is big castling (wKing from original square to square 5)
        if destinationSquare == 61:
          self.bRooks |= 1 << 60
          self.bRooks &= ~(1 << 63)

      # removing castling rights for left rook movement/losing
      if originalSquare == 63 or destinationSquare == 63:
        self.bBigCastleRights = False


  def enpassantMoveHandling(self, pieceName, destinationSquare, originalSquare):
    if pieceName == 'wPawns' and self.wPawnCaptures[originalSquare] & 1 << destinationSquare and not (1 << destinationSquare & self.blackPieces):
      self.bPawns &= ~(1 << destinationSquare - 8)

    elif pieceName == 'bPawns' and self.bPawnCaptures[originalSquare] & 1 << destinationSquare and not (1 << destinationSquare & self.whitePieces):
      self.wPawns &= ~(1 << destinationSquare + 8)


  def promotionMoveHandling(self, pieceName, destinationSquare, originalSquare):
    if pieceName == 'wPawns' and destinationSquare // 8 == 7:
      promotedPiece = input()
      setattr(self, promotedPiece, getattr(self, promotedPiece) | 1 << destinationSquare)
      self.wPawns &= ~(1 << destinationSquare)


  def move(self, destinationSquare, originalSquare):

    for pieceName, pieceState in self.pieces().items():
      # piece that will move
      if pieceState & 1 << originalSquare:

        setattr(self, pieceName, (pieceState | (1 << destinationSquare)) & ~(1 << originalSquare))

        self.castleMoveHandling(pieceName, destinationSquare, originalSquare)
        self.enpassantMoveHandling(pieceName, destinationSquare, originalSquare)
        self.promotionMoveHandling(pieceName, destinationSquare, originalSquare)

      # piece that will be captured (if there is one)
      if pieceState & 1 << destinationSquare:

        pieceState &= ~(1 << destinationSquare)
        setattr(self, pieceName, pieceState)

    self.moves = 0
    self.selectedSquare = -1
    self.lastMove = 1 << originalSquare | 1 << destinationSquare
    self.isWhiteTurn = not self.isWhiteTurn

    self.whitePieces = self.wRooks | self.wKnights | self.wBishops | self.wQueens | self.wKing | self.wPawns
    self.blackPieces = self.bRooks | self.bKnights | self.bBishops | self.bQueens | self.bKing | self.bPawns
    self.allPieces = self.whitePieces | self.blackPieces

  # ---------------------------------------------------------------------
  # -------------------- CALCULATING MOVES FUNCTIONS --------------------
  # ---------------------------------------------------------------------

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
    squareBitBoard = 1 << square

    if self.isWhiteTurn:
      # not special pieces
      if squareBitBoard & self.wRooks:
        self.moves = self.calculateCollisions(square, self.rookMoves, 1)
      elif squareBitBoard & self.wKnights:
        self.moves = self.knightMoves[square] & ~self.whitePieces
      elif squareBitBoard & self.wBishops:
        self.moves = self.calculateCollisions(square, self.bishopMoves, 1)
      elif squareBitBoard & self.wQueens:
        self.moves = self.calculateCollisions(square, self.queenMoves, 1)

      # king update has to handle castling
      elif squareBitBoard & self.wKing:
        # normal moves
        self.moves = self.kingMoves[square] & ~self.whitePieces

        if self.wSmallCastleRights:
          # no pieces in the way
          if not (self.wSmallCastleBlockers & self.allPieces):
            self.moves |= self.wKingSmallCastleMove
          # no checks in the way?

        if self.wBigCastleRights:
          # no pieces in the way
          if not (self.wBigCastleBlockers & self.allPieces):
            self.moves |= self.wKingBigCastleMove
          # no checks in the way?

      # pawn update has to handle enpassant and unique collision
      elif squareBitBoard & self.wPawns:

        # collision check
        if (squareBitBoard << 8) & self.allPieces:
          self.moves = self.wPawnCaptures[square] & self.blackPieces
        else:
          self.moves = self.wPawnMoves[square] & ~self.allPieces | (self.wPawnCaptures[square] & self.blackPieces)

        # enpassant check
        # if in the fith rank and
        # last move was from enemy pawn and
        # was neighbor double advancing
        if square // 8 == 4 and self.lastMove & self.bPawns and ((self.lastMove & self.wPawnCaptures[square] << 8) and (self.lastMove & self.wPawnCaptures[square] >> 8)):
          self.moves |= (self.lastMove & -self.lastMove) << 8

      # no piece was selected:
      elif squareBitBoard & ~self.whitePieces:
        self.moves = 0

    else:
      # not special pieces
      if squareBitBoard & self.bRooks:
        self.moves = self.calculateCollisions(square, self.rookMoves, 0)
      elif squareBitBoard & self.bKnights:
        self.moves = self.knightMoves[square] & ~self.blackPieces
      elif squareBitBoard & self.bBishops:
        self.moves = self.calculateCollisions(square, self.bishopMoves, 0)
      elif squareBitBoard & self.bQueens:
        self.moves = self.calculateCollisions(square, self.queenMoves, 0)

      # king update has to handle castling
      elif squareBitBoard & self.bKing:
        # normal moves
        self.moves = self.kingMoves[square] & ~self.blackPieces

        if self.bSmallCastleRights:
          # no pieces in the way
          if not (self.bSmallCastleBlockers & self.allPieces):
            self.moves |= self.bKingSmallCastleMove

        if self.bBigCastleRights:
          # no pieces in the way
          if not (self.bBigCastleBlockers & self.allPieces):
            self.moves |= self.bKingBigCastleMove

      # pawn update has to handle enpassant and unique collision
      elif squareBitBoard & self.bPawns:

        # collision check
        if (squareBitBoard >> 8) & self.allPieces:
          self.moves = self.bPawnCaptures[square] & self.whitePieces
        else:
          self.moves = (self.bPawnMoves[square] & ~self.allPieces) | (self.bPawnCaptures[square] & self.whitePieces)

        # enpassant check
        # if in the fourth rank and
        # last move was from enemy pawn and
        # was neighbor double advancing
        if square // 8 == 3 and self.lastMove & self.wPawns and ((self.lastMove & self.bPawnCaptures[square] << 8) and (self.lastMove & self.bPawnCaptures[square] >> 8)):
          self.moves |= (self.lastMove & -self.lastMove) << 8

      # no piece was selected:
      elif squareBitBoard & ~self.blackPieces:
        self.moves = 0

  # -------------------------------------------------
  # -------------------- DRAWING --------------------
  # -------------------------------------------------

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

    # drawing the last move different colored squares
    lastMoveBitBoard = self.lastMove
    while lastMoveBitBoard:
      b = lastMoveBitBoard & -lastMoveBitBoard
      square = 64 - b.bit_length()
      x = (square % 8)
      y = (square // 8)

      if (x + y) % 2 == 0:
        color = (245, 246, 130)
      else:
        color = (185, 202, 67)

      square = pg.Rect(x * self.squareSize, y * self.squareSize, self.squareSize, self.squareSize)
      pg.draw.rect(display, color, square)

      lastMoveBitBoard &= lastMoveBitBoard - 1
 
    # drawing pieces
    for pieceName, pieceState in self.pieces().items():
      img = pg.image.load('./assets/' + pieceName + '.png')
      img = pg.transform.smoothscale(img, (self.squareSize, self.squareSize))

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
      transparentCircle = pg.Surface((self.squareSize * 4, self.squareSize * 4), pg.SRCALPHA)
      pg.draw.circle(transparentCircle, (0, 0, 0, 128), (self.squareSize * 2, self.squareSize * 2), self.squareSize / 2)
      transparentCircle = pg.transform.smoothscale(transparentCircle, (self.squareSize, self.squareSize))
      display.blit(transparentCircle, (x * self.squareSize, y * self.squareSize))
      temp &= temp - 1

# ---------------------------------------------------
# -------------------- GAME LOOP --------------------
# ---------------------------------------------------

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
