#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include "book.h"

int init_book(struct book *p_book, const char *p_id, const char *p_title, const char * p_author, struct date p_release) {

  strcpy(p_book->id,p_id); //Kopioidaan kirjan id

  p_book->title=malloc(strlen(p_title)+1); //Varataan otsikolle muistia
  strcpy(p_book->title,p_title); //Kopioidaan kirjan otsikko

  p_book->author=malloc(strlen(p_author)+1); //Varataan kirjailijalle muistia
  strcpy(p_book->author, p_author); //Kopioidaan kirjailia

  p_book->release_date.day = p_release.day;
  p_book->release_date.month = p_release.month;
  p_book->release_date.year = p_release.year;

  if(strcmp(p_book->id,p_id)!=0||strcmp(p_book->title,p_title)!=0||strcmp(p_book->author,p_author)!=0) {
    return 0;
  }
  return 1;
}

struct book *add_to_collection(struct book *collection, unsigned int size, struct book new_book)  {
  //new_book.title;
  struct book *new_collection = realloc(collection, sizeof(struct book)*(size+1));
  if (new_collection ==NULL)  {
    return NULL;
  }
  strcpy(new_collection[size].id, new_book.id);
  new_collection[size].title = malloc(strlen(new_book.title)+1);
  strcpy(new_collection[size].title,new_book.title);
  new_collection[size].author = malloc(strlen(new_book.title)+1);
  strcpy(new_collection[size].author, new_book.author);
  new_collection[size].release_date = new_book.release_date;
  //printf("%d",new_collection[size].release_date.day);
  //new_collection[size]=new_book;
  return new_collection;
}

void delete_collection(struct book *collection, unsigned int size)
{
    for (unsigned int i = 0; i < size; i++) {
        free(collection[i].title);
        free(collection[i].author);
    }
    free(collection);
}

int main(void)
{
    /* Feel free to modify */
    struct book a1;
    struct date a1date = {26, 6, 1997};
    if (init_book(&a1, "000000009", "Harry Potter and the Philosopher's Stone", "J. K. Rowling", a1date )) {
        printf("Initialization succeeded\n");
    } else {
        printf("Initialization failed\n");
    }

    free(a1.title);
    free(a1.author);

    struct book collection[] = {
        { "001020304", "Harry Potter and the Chamber of Secrets", "J. K. Rowling", {2,7,1998} },
        { "555566666", "Harry Potter and the Prisoner of Azkaban", "J. K. Rowling", {8,7,1999} },
        { "773466889", "Harry Potter and the Goblet of Fire", "J. K. Rowling", {8, 7, 2000} },
        { "000000000", "Something For Testing", "Testing author", {1, 2, 3456} }
    };

    struct book *array = NULL;
    unsigned int len = 0;

    for (unsigned int i = 0; i < 4; i++) {
        struct book *newarray = add_to_collection(array, len, collection[i]);
        if (!newarray) {
            printf("ERROR - New collection is NULL\n");
            return 1;
        }
        len++;
        array = newarray;
    }

    for (unsigned int i = 0; i < len; i++) {
      printf("%s: %s (%s)\n", array[i].id, array[i].title, array[i].author);
    }

    delete_collection(array, len);

    return 0;
}
