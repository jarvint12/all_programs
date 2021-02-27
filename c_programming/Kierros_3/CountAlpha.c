#include <stdio.h>
#include <ctype.h>
#include <string.h>

int count_isalpha(const char *str)  {
  int i = 0;
  while(*str!='\0') {
    if(isalpha(*str))  {
      i++;
    }
    str++;
}
  return i;
}

int main(void)  {
char message[] = "It is going to rain tomorrow";
int i = count_isalpha(message);
printf("%d\n",i);
return 0;
}
