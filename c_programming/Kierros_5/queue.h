#ifndef AALTO_C_QUEUE_H
#define AALTO_C_QUEUE_H

struct studentqueue {
    char *name;  // Name of queue member (dynamically allocated)
    struct studentqueue *next;  // (pointer to next queue member)
};

int enqueue(struct studentqueue *q, const char *name);

int dequeue(struct studentqueue *q, char *buffer, unsigned int size);

#endif
