#include <stdio.h>
#include <string.h>

int num_substr(const char *str, const char *sub)  {
  int sum = 0;
  while(*str!='\0')  {
    if(strstr(str, sub) != NULL)  {
      str=strstr(str, sub);
      sum++;
    }
    str++;
  }
  return sum;
}

int main(void)  {
  int i = num_substr("one two one twotwo three", "two");
  printf("%d\n", i);
  return 0;
}
