#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "filebasics.h"
#include "filebasics.c"


int main(void)
{
    printf("--- Printing file:\n");
    int t = print_file_and_count("testifile.c");
    if(t<0)
        printf("Opening failed!\n");

    printf("--- Printed %d characters\n", t);

    char* diff = difference("testifile.c", "testifile2.c");
    printf("\n--- Difference:\n");
    printf("%s", diff);

    free(diff);

    return 0;
}
