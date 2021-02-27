#include <stdio.h>
#include <math.h>

double vectorlength(double x, double y, double z)
{
  double length = sqrt(pow(x,2) + pow(y,2) + pow(z,2));
  return length;
}

int main(void)
{
  double length = vectorlength(4, 7, 200);
  printf("%lf\n", length);
  return 0;
}
