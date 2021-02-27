#include <stdio.h>

void sort(int *start, int size) {
  int i;
  int smallest;
  for (int j = 0; j<size; j++)  {
    smallest = start[j];
    i = j+1;
    while(i<size)  {
      if (start[i]<smallest)  {
        smallest = start[i];
        start[i] = start[j];
        start[j] = smallest;
      }
      //printf("Smallest: %d start[%d]: %d start[%d]: %d\n", smallest,i,start[i],j,start[j]);
      i++;
    }
  }
}

int main(void)  {
  int array[] = {65, 234, 676, 3, 98, 35, 297, 34, 12};
  int size = sizeof(array)/sizeof(int);
  sort(array, size);
  int i = 0;
  while(i<size) {
    printf("%d\n", array[i]);
    i++;
  }
  return 0;
}
