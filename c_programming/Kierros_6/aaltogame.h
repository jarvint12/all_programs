#ifndef AALTO_GAMEOFLIFE_H
#define	AALTO_GAMEOFLIFE_H

typedef enum {
    DEAD,
    ALIVE
} CellStatus;

typedef struct {
    unsigned int x_size, y_size;
    CellStatus **cells;
} GameArea;

GameArea *createGameArea(unsigned int x_size, unsigned int y_size);

void releaseGameArea(GameArea *a);

void initGameArea(GameArea *a, unsigned int n);

void printGameArea(const GameArea *a);

void gameTick(GameArea *a);

#endif
