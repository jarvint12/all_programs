#include <stdio.h>
#include <string.h>
#include "hexread.h"
#include "hex.c"


int main(void)
{
    if (file_to_hex("main.c") == -1) {
         fprintf(stderr, "Could not open main.c\n");
    }
}
