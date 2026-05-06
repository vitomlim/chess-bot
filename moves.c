#include <stdint.h>
#include <stdbool.h>

#include "types.h"
#include "moves.h"

void initializePieceMaps(uint64_t pieceMaps[6][64]) {
  for(int i = 0; i < 64; i++) {
    uint64_t currentBit = (uint64_t)1 << i;
    uint64_t currentRookMap = 0;

    for(int j = i + 1; j % 8 != 0; j++) {
      currentRookMap |= (uint64_t)1 << j;
    }
    for(int j = i - 1; j % 8 != 7 && j >= 0; j--) {
      currentRookMap |= (uint64_t)1 << j;
    }
    for(int j = i + 8; j < 64; j += 8) {
      currentRookMap |= (uint64_t)1 << j;
    }
    for(int j = i - 8; j >= 0; j -= 8) {
      currentRookMap |= (uint64_t)1 << j;
    }

    pieceMaps[rook][i] = currentRookMap;
  }

  for(int i = 0; i < 64; i++) {
    uint64_t currentBit = (uint64_t)1 << i;
    uint64_t currentKnightMap = 0;

    if(i % 8 < 7 && i / 8 < 6) currentKnightMap |= (uint64_t)1 << (i + 17);
    if(i % 8 < 7 && i / 8 > 1) currentKnightMap |= (uint64_t)1 << (i - 15);
    if(i % 8 > 0 && i / 8 < 6) currentKnightMap |= (uint64_t)1 << (i + 15);
    if(i % 8 > 0 && i / 8 > 1) currentKnightMap |= (uint64_t)1 << (i - 17);
    if(i % 8 < 6 && i / 8 < 7) currentKnightMap |= (uint64_t)1 << (i + 10);
    if(i % 8 > 1 && i / 8 < 7) currentKnightMap |= (uint64_t)1 << (i + 6);
    if(i % 8 < 6 && i / 8 > 0) currentKnightMap |= (uint64_t)1 << (i - 6);
    if(i % 8 > 1 && i / 8 > 0) currentKnightMap |= (uint64_t)1 << (i - 10);

    pieceMaps[knight][i] = currentKnightMap;
  }

  for(int i = 0; i < 64; i++) {
    uint64_t currentBit = (uint64_t)1 << i;
    uint64_t currentBishopMap = 0;

    for(int j = i - 7; j >= 0 && j % 8 != 0; j -= 7) {
      currentBishopMap |= (uint64_t)1 << j;
    }
    for(int j = i - 9; j >= 0 && j % 8 != 7; j -= 9) {
      currentBishopMap |= (uint64_t)1 << j;
    }
    for(int j = i + 9; j < 64 && j % 8 != 0; j += 9) {
      currentBishopMap |= (uint64_t)1 << j;
    }
    for(int j = i + 7; j < 64 && j % 8 != 7; j += 7) {
      currentBishopMap |= (uint64_t)1 << j;
    }

    pieceMaps[bishop][i] = currentBishopMap;
  }

  for(int i = 0; i < 64; i++) {
    pieceMaps[queen][i] = pieceMaps[rook][i] | pieceMaps[bishop][i];
  }

  for(int i = 0; i < 64; i++) {
    uint64_t currentBit = (uint64_t)1 << i;
    uint64_t currentKingMap = 0;

    if(i % 8 < 7) currentKingMap |= (uint64_t)1 << (i + 1);
    if(i % 8 > 0) currentKingMap |= (uint64_t)1 << (i - 1);
    if(i / 8 < 7) currentKingMap |= (uint64_t)1 << (i + 8);
    if(i / 8 > 0) currentKingMap |= (uint64_t)1 << (i - 8);
    if(i % 8 < 7 && i / 8 < 7) currentKingMap |= (uint64_t)1 << (i + 9);
    if(i % 8 > 0 && i / 8 < 7) currentKingMap |= (uint64_t)1 << (i + 7);
    if(i % 8 < 7 && i / 8 > 0) currentKingMap |= (uint64_t)1 << (i - 7);
    if(i % 8 > 0 && i / 8 > 0) currentKingMap |= (uint64_t)1 << (i - 9);

    pieceMaps[king][i] = currentKingMap;
  }
}

