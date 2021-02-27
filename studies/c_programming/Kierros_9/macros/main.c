#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include "macros.h"

int main(void)
{
#ifdef EQ3
    printf("Testing EQ3:\n");
    printf("EQ3(3,3,3) returned %d, should have been 1.\n", EQ3(3,3,3));
    printf("EQ3(1,2,3) returned %d, should have been 0.\n", EQ3(1,2,3));
#else
    printf("Implement EQ3 first");
#endif
    
#ifdef MIN3 
    printf("\nTesting MIN3:\n");
    printf("MIN3(1,2,3) returned %d, should have been 1.\n", MIN3(1,2,3));
#else
    printf("Implement MIN3 first");
#endif    

    return 0;
}
