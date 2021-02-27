#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>

int line_count(const char *filename)  {
  FILE *f = fopen(filename, "r");
  if(!f)  {
    return -1;
  }
  int i=0;
  char j;
  char m;
  if((j=fgetc(f))==EOF) {
    return 0;
  }
  if (j=='\n') {
    i++;
  }
  while((j=fgetc(f))!=EOF) {
    m=j;
    if(j=='\n')  {
      i++;
    }
  }
  if(m!='\n') {
    i++;
  }
  return i;
}


int word_count(const char *filename)  {
  FILE *f = fopen(filename, "r");
  if (!f) {
    return -1;
  }

  int i=0;
  char j;
  while((j = fgetc(f))!=EOF) {

    if(isspace(j))  { //Mikäli whitespace-merkki, siirrytään seuraavaan
      continue;
    }

    else if(isalpha(j))  { //Jos kyseessä kirjain, lisätään summaan yksi sana
      i++;
      while ((j = fgetc(f))!=EOF) { //Siirrytään eteenpäin kunnes tullaan sanan loppuun
        if(isspace(j)) { //Sanan loppuessa siirrytään isoon while-looppiin
          break;
        }
      }
    }
  }
  return i;
}
