#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int print_file_and_count(const char *filename)  {
  FILE *f = fopen(filename, "r");
  if(!f)  {
    return -1;
  }
  int i=0;
  char j;
  while ((j = fgetc(f))!=EOF) {
    printf("%c",j);
    i++;
  }
  return i;
}


char *difference(const char* file1, const char* file2)  {
  FILE *f1 = fopen(file1, "r");
  FILE *f2 = fopen(file2, "r");

  char buffer1[100];
  char buffer2[100];
  while((feof(f1)==0) && (feof(f2) == 0)) {
    fgets(buffer1, sizeof(buffer1), f1);
    fgets(buffer2, sizeof(buffer2), f2);
    if(strcmp(buffer1, buffer2)!=0)  {
      char *diff = malloc(300);
      strcpy(diff,buffer1);
      strcat(diff,"----\n");
      strcat(diff, buffer2);
      return diff;
    }
  }
  return NULL;
}
