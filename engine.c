#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

// Board struct defines entirely and unambiagualy a board state using bit boards
typedef struct {
  uint64_t bRooks;
  uint64_t bKnights;
  uint64_t bBishops;
  uint64_t bQueens;
  uint64_t bKing;
  uint64_t bPawns;
  uint64_t wRooks;
  uint64_t wKnights;
  uint64_t wBishops;
  uint64_t wQueens;
  uint64_t wKing;
  uint64_t wPawns;
} Board;

Board board = {0};
bool isWhiteTurn;

Board getBoard() {
  return board;
}

// getting board state from FEN code
void initializeBoard(char* FENString) {

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
      case 'r': board.bRooks |= currentBit; break;
      case 'n': board.bKnights |= currentBit; break;
      case 'b': board.bBishops |= currentBit; break;
      case 'q': board.bQueens |= currentBit; break;
      case 'k': board.bKing |= currentBit; break;
      case 'p': board.bPawns |= currentBit; break;
      case 'R': board.wRooks |= currentBit; break;
      case 'N': board.wKnights |= currentBit; break;
      case 'B': board.wBishops |= currentBit; break;
      case 'Q': board.wQueens |= currentBit; break;
      case 'K': board.wKing |= currentBit; break;
      case 'P': board.wPawns |= currentBit; break;
    }
    x++;
  }

  FENString++;
  // second field: current turn
  isWhiteTurn = (*FENString++ == 'w');

}
