#include <stdio.h>



char *delete_comments(char *input)  {
char *arr;
int i = 0;
while(*input) {
  if(*input == '/' && *input++ == '*')  {
      while(*input != '*' || *input++ != '/')  {
        input++;
        }
      }
  if(*input == '/' && *input++ == '/')  {
    while(*input != '\n') {
      input++;
    }
  }
  i++;
  arr = realloc(arr, i * sizeof(char));
  *arr = *input;
  arr++;
  input++;
}
free(input);
return arr;
}
