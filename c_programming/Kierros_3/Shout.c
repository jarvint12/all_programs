#include <stdio.h>
#include <string.h>
#include <ctype.h>

char *my_toupper(char *dest, const char *src) {
  memset(dest, 0, 199);
  int i=0;
  int j=0;
  while(src[i]!='\0')  {
    if(src[i]=='?')  {
      dest[j] = '!';
    }
    else if(src[i]=='.'){
      dest[j] = '!';
      j++;
      dest[j] = '!';
      j++;
      dest[j] = '!';
    }
    else  {
      dest[j] = toupper(src[i]);
    }
    i++;
    j++;
  }
  return dest;
}


int main(void)
{
  char dest[200];

  /* The following helps detecting string errors, e.g. missing final nil */
  memset(dest, '#', 199);
  dest[199] = 0;

  printf("%s",
  my_toupper(dest,
    "Would you like to have a sausage? It will be two euros. Here you are.\n"));

        printf("%s",
  my_toupper(dest,
    "Madam, where are you going? The health care center is over there.\n"));

  return 0;
    }
