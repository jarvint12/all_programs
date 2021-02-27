#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include "aaltogame.h"

int main(void)
{
    /* Feel free to modify this function to test different things */

    // re-seed random number generator
    srand((unsigned)time(NULL));

    GameArea *a = createGameArea(50,20);
    initGameArea(a, 150);

    // how many iterations we want
    int rounds = 80;

    // loop iterations, cancel with ctrl-c
    for(int i=0; i<rounds; i++) {
        printf("\nGeneration: %d\n", i+1);
        printGameArea(a);
        // slow down iterations
        sleep(1);
        gameTick(a);
    }
    releaseGameArea(a);
    return 0;
}
