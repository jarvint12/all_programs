#include <stdio.h>
#include <ctype.h>

int ascii_chart(char min, char max)
{
  int j = 1;
  for(int i=min; i<=max; i++) {
    int y = isprint(i);
    if(y==0)  {
          printf("%3d 0x%02x ?",i,i);
    }
    else  {
      printf("%3d 0x%02x %c",i,i,i);
    }
    j++;
    if(j%4==1)   {
      printf("\n");
    }
    else  {
      printf("\t");
    }
  }
  return 0;
}

int main(void)
{
  int a,b;
  scanf("%d %d",&a, &b);
  ascii_chart(a,b);
  return 0;
}
