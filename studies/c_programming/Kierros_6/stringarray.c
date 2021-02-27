#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stringarray.h"

/* Exercise a: Initializes the string array to contain the initial
 * NULL pointer, but nothing else.
 * Returns: pointer to the array of strings that has one element
 *      (that contains NULL)
 */
char **init_string_array(void)
{
  char **arr = malloc(sizeof(char *));
  *arr= NULL;
  return arr;
}

/* Releases the memory used by the strings.
 */
void release_string_array(char **arr)
{
  int i=0;
  while(arr[i]!=NULL)  {
    free(arr[i]);
    i++;
  }
  free(arr);
}

/* Exercise b: Add <string> to the end of array <array>.
 * Returns: pointer to the array after the string has been added.
 */
char **insert_string(char **arr, const char *str)
{
  int i=0;
  //Mitataan arrayn koko
  while(*arr!=NULL) {
    arr++;
    i++;
  }
  arr -= i; //Palautetaan osoitin alkuun
  arr = realloc(arr, (i+2)*sizeof(char *)); //Kasvatetaan arrayn muistia
  arr[i] = malloc(strlen(str)+1); //tila uudelle merkkijoholle+lopetusmerkille
  strcpy(arr[i],str); //Liitetään uusi merkkijono sille varattuun muistipaikkaan
  arr[i+1] = NULL; //Lisätään loppuun nolla
  return arr;
}


/* Exercise c: reorder strings in <array> to lexicographical order */
void sort_string_array(char **arr)
{
  unsigned int size = 0;
  char *smallest;
  //Mitataan merkkijonon koko
  while(*arr!=NULL) {
    arr++;
    size++;
  }
  arr -=size; //Palautetaan merkkijono alkuun
  int i=0;
  for (int j = 0; j<size; j++)  {
    i = j+1;
    while(arr[i])  { //Pyöritetään koko merkkijono läpi
      if (strcmp(arr[i], arr[j])<0)  { //Jos uusi merkkijono on aakkosjärjestyksessä ensin
        smallest = arr[i]; //Tallennetaan uusi merkkijono talteen
        arr[i] = arr[j]; //Laitetaan vanha merkkijono uuden paikalle
        arr[j] = smallest; //Tallennetaan uusi merkkijono vanhan paikalle
      }
      i++; //Jatketaan merkkijonon pyörittämistä
    }
  } //Aloitetaan merkkijonon toisesta kohdasta
}

/* You can use this function to check what your array looks like.
 */
void print_string_array(char **arr)
{
    if (!arr)
        return;
    while (*arr) {
        printf("%s  ", *arr);
        arr++;
    }
    printf("\n");
}


int main(void)
{
    char **string_array = init_string_array();

    string_array = insert_string(string_array, "oNe");
    string_array = insert_string(string_array, "TWO");
    string_array = insert_string(string_array, "three");
    string_array = insert_string(string_array, "Four");
    print_string_array(string_array);

  //  make_lower(string_array);
    sort_string_array(string_array);
    print_string_array(string_array);
    release_string_array(string_array);

    return EXIT_SUCCESS;
}
