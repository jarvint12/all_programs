#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *delete_comments(char *input)  {
char *arr = malloc((strlen(input)+1));
char *alku = arr;
char *inpalku = input;
int i = 0;
while(*input) {
  if(*input == '/' && *(input+1) == '*')  {
      while(*input != '*' || *(input+1) != '/')  {
        input++;
        }
        input = input+2;
      }
  if(*input == '/' && *(input+1) == '/')  {
    while(*input != '\n') {
      input++;
    }
    input++;
  }
  i++;
  *arr = *input;
  arr++;
  input++;
}
*arr = *input;
alku = realloc(alku, (i+1) * sizeof(char));
free(inpalku);
return alku;
}


char *read_file(const char *filename)
{
    FILE *f = fopen(filename, "r");
    if (!f)
        return NULL;

    char *buf = NULL;
    unsigned int count = 0;
    const unsigned int ReadBlock = 100;
    unsigned int n;
    do {
        buf = realloc(buf, count + ReadBlock + 1);
        n = fread(buf + count, 1, ReadBlock, f);
        count += n;
    } while (n == ReadBlock);

    buf[count] = 0;

    fclose(f);
    return buf;
}


int main(void)
{
    char *code = read_file("testifile.c");
    if (!code) {
        printf("No code read");
        return -1;
    }
    printf("-- Original:\n");
    fputs(code, stdout);

    code = delete_comments(code);
    printf("-- Comments removed:\n");
    fputs(code, stdout);

    free(code);

    return 0;
}
