#include <stdio.h>

char *mystrcat(char *dest, const char *src) {
  int i=0;
  int j=0;
  while(dest[i]!='\0')  {
    i++;
  }
  dest[i]=' ';
  i++;
  while(src[j]!='\0') {
    dest[i]=src[j];
    i++;
    j++;
  }
  printf("%s\n",dest);
  return dest;
}


unsigned int pickmax(unsigned int *numbers) {
  int i=0;
  int max=0;
  while(numbers[i]!='\0') {
    if(numbers[i]>max) {
      max=numbers[i];
    }
  }
  return max;
}


int main(void)  {
  char string1[20]="Hello";
  char string2[20]="world";
  //unsigned int string3[20]="123459765";
  mystrcat(string1,string2);
  int max = pickmax("1239584754");
  printf("Maksimi: %d", max);
  return 0;
}
