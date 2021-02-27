#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int *create_dyn_array(unsigned int n) {
  int *table = malloc(n*sizeof(int));
  unsigned int i = 0;
  while (i<n) {
    if (scanf("%d", &table[i])==1){
      i++;
    }
  }
  return table;
}

int *add_dyn_array(int *arr, unsigned int num, int newval)  {
  arr = realloc(arr, (num+1)*sizeof(int));
  arr[num] = newval;
  return arr;
}

int main(void)  {
  int *str;
  str = create_dyn_array(7);
  for(int i=0; i<7; i++) {
  printf("%d", str[i]);
}
  printf("\n");
  int *dst = (int *)calloc(4,sizeof(int));
  dst = add_dyn_array(dst, 4, 10);
  dst = add_dyn_array(dst, 5, 11);
  dst = add_dyn_array(dst, 6, 12);
  for(int i=0;i<7;i++) {
  printf("%d\n", dst[i]);
}
  return 0;
}
