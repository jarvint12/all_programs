#ifndef AALTO_STRINGARRAY_H
#define AALTO_STRINGARRAY_H

char **init_string_array(void);
void release_string_array(char **arr);
char **insert_string(char **arr, const char *str);
void make_lower(char **arr);
void sort_string_array(char **arr);
void print_string_array(char **arr);

#endif
