#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

#include "types.h"
#include "moves.h"

uint64_t pieceMaps[6][64];
uint64_t board[12];
bool isWhiteTurn;
bool castlingRights[4];

// getting board state from FEN code
void initializeBoard(char* FENString) {

  initializePieceMaps(pieceMaps);

  // first field: pieces position
  int x = 0, y = 0;
  while(*FENString && *FENString != ' ') {
    char currentChar = *FENString++;

    if('1' <= currentChar && currentChar <= '8') {
      x += currentChar - '0';
      continue;
    }

    if(currentChar == '/') {
      y++;
      x = 0;
      continue;
    }

    int currentSquare = x + 8*y;
    uint64_t currentBit = (uint64_t)1 << currentSquare;
    switch(currentChar) {
      case 'r': board[bRooks] |= currentBit; break;
      case 'n': board[bKnights] |= currentBit; break;
      case 'b': board[bBishops] |= currentBit; break;
      case 'q': board[bQueens] |= currentBit; break;
      case 'k': board[bKing] |= currentBit; break;
      case 'p': board[bPawns] |= currentBit; break;
      case 'R': board[wRooks] |= currentBit; break;
      case 'N': board[wKnights] |= currentBit; break;
      case 'B': board[wBishops] |= currentBit; break;
      case 'Q': board[wQueens] |= currentBit; break;
      case 'K': board[wKing] |= currentBit; break;
      case 'P': board[wPawns] |= currentBit; break;
    }
    x++;
  }

  FENString++;
  // second field: current turn
  isWhiteTurn = (*FENString++ == 'w');

}

uint64_t* getBoard() {
  return board;
}

void move(int fromSquare, int toSquare) {
  uint64_t fromBit = (uint64_t)1 << fromSquare;
  uint64_t toBit = (uint64_t)1 << toSquare;

  for(int pieceType = 0; pieceType < 12; pieceType++) {
    if((board[pieceType] >> toSquare) & 1) {
      board[pieceType] &= ~toBit;
      break;
    }
  }
  for(int pieceType = 0; pieceType < 12; pieceType++) {
    if((board[pieceType] >> fromSquare) & 1) {
      board[pieceType] &= ~fromBit;
      board[pieceType] |= toBit;
      break;
    }
  }
  isWhiteTurn = !isWhiteTurn;
}

// board array uses board enum
// pieceMaps array uses pieceTypes enum
// check types.h
uint64_t getMoves(int square) {

  int color = isWhiteTurn ? 6 : 0;
  for(int boardPiece = color; boardPiece < 6 + color; boardPiece++) {
    if((board[boardPiece] >> square) & 1ULL) {
      return pieceMaps[boardPiece - color][square];
    }
  }
  return 0;
}

uint64_t filterCollisions(int pieceType, int square) {

}