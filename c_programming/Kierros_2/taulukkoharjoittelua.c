#include <stdio.h>

int array_sum(int *array, int count)
{
int sum = 0;
for(int i=0; i<count; i++)  {
  sum = sum + array[i];
  }
  return sum;
}

int array_reader(int *vals, int n)  {
  int m = 0;
  int d;
  int ret = scanf("%d", &d);
  if (ret != 1) {
    return m;
  }
  else  {
    vals[m] = d;
    for (m=1;m<n;m++)  {
      ret = scanf("%d", &d);
      if (ret == 1) {
        vals[m] = d;
      }
      else  {
        return m;
      }
    }
  }
  return m;
}


int main(void)  {
int valarray[] = { 10, 100, 1000 };
int ret = array_sum(valarray, 3);
printf("%d\n", ret);

int array[10];
int n = array_reader(array, 10);
printf("%d numbers read\n", n);
int i;
for (i = 0; i < n; i++) {
    printf("%d ", array[i]);
}

return 0;
}
