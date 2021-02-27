#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "queue.h"

int enqueue(struct studentqueue *q, const char *name) {

  struct studentqueue *new = malloc(sizeof(struct studentqueue));

  new->name=malloc(strlen(name)+1);
  if(new->name==NULL) {
    return 0;
  }
  strcpy(new->name, name);
  new->next = NULL;
  while (q->next!=NULL) {
    q = q->next;
  }
  q->next = new;
  return 1;
}


int dequeue(struct studentqueue *q, char *buffer, unsigned int size)  {
  if(q->next==NULL) {
    return 0;
  }
  strncpy(buffer,(q->next)->name,(size-1));
  free((q->next)->name);
  struct studentqueue *temp = q->next;
  q->next=(q->next)->next;
  free(temp);
  return 1;
}

int main(void)
{
	struct studentqueue q = { NULL, NULL };

	int go_on = 1;
	char buffer[100];
	while(go_on) {
	    printf("Enter name of the student (\"-\" will end reading): ");
	    scanf("%99s", buffer);
	    buffer[99] = 0;
	    if (strlen(buffer) > 0 && strcmp(buffer, "-")) {
		    go_on = enqueue(&q, buffer);
	    } else {
		    go_on = 0;
	    }
	}

	while(dequeue(&q, buffer, 100)) {
	    printf("Fetching %s from queue\n", buffer);
	}

	return 0;
}
