#include <stdio.h>

int simple_multiply (void)
{
  int a;
  int b;
  scanf("%d %d", &a, &b);
  int c = a * b;
  printf("%d * %d = %d\n",a,b,c);
  return 0;
}

int simple_math(void)
{
  float a;
  char b = 0;
  float c;

  scanf("%f %s %f", &a, &b, &c);
  switch(b) {
    case '+':
    printf("%.1f\n",(a+c));
    break;

    case '-':
    printf("%.1f\n",a-c);
    break;

    case '*':
    printf("%.1f\n",a*c);
    break;

    case '/':
    printf("%.1f\n",a/c);
    break;

    default:
    printf("ERR\n");
    break;
  }
  return 0;
}

int main(void)
{
  simple_multiply();
  simple_math();
  return 0;
}
