#include <stdio.h>
#include <string.h>


int file_to_hex(const char *filename) {
  FILE *f = fopen(filename,"r");
  if(!f)  {
    return -1;
  }
  int i=0;
  int j;
  int m=0;
  while ((j = fgetc(f))!=EOF)  {
    printf("%02x ",j);
    i++;
    if(i==16) {
      printf("\n");
      i=0;
    }
    m++;
  }
  printf("\n");
  fclose(f);
  return m;
}
