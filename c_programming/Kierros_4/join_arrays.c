#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int *join_arrays(unsigned int count1, int *a1,
  unsigned int count2, int *a2, unsigned int count3, int *a3) {
    int *newarray = malloc((count1+count2+count3)*sizeof(int));
    //int *array2 = newarray;
    memcpy(newarray, a1, count1*sizeof(int));
    memcpy(&newarray[count1], a2, count2*sizeof(int));
    memcpy(&newarray[count1+count2], a3, count3*sizeof(int));
    return newarray;
  }


  int main(void)
{
    /* testing exercise. Feel free to modify */
    int a1[] = { 1, 2, 3, 4, 5 };
    int a2[] = { 10, 11, 12, 13, 14, 15, 16, 17 };
    int a3[] = { 20, 21, 22 };

    int *joined = join_arrays(5, a1, 8, a2, 3, a3);

    for (int i = 0; i < 5 + 8 + 3; i++) {
        printf("%d  ", joined[i]);
    }
    printf("\n");

    return 0;
}
