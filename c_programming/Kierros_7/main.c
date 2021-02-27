#include <stdio.h>
#include "tcpheader.h"
#include "tcpheader.c"

int main()
{
    /* Feel free to modify this function to test different things */

    unsigned char bytes[] = {
        0x12,0x34,0x45,0x67,0xaa,0xbb,0xcc,0xdd,
        0xee,0xff,0xaa,0xbb,0xb1,0x5c,0x08,0x00,
        0x12,0x34,0x00,0x00 };

    printf("Source port: %d\n", getSourcePort(bytes));
    printf("Destination port: %d\n", getDestinationPort(bytes));
    printf("ACK flag: %d\n", getAckFlag(bytes));
    printf("Data Offset: %d\n", getDataOffset(bytes));
}
