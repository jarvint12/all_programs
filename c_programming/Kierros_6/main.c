#include <stdio.h>
#include <stdlib.h>
#include "stringarray.h"

int main(void)
{
    char **string_array = init_string_array();
    
    string_array = insert_string(string_array, "oNe");
    string_array = insert_string(string_array, "TWO");
    string_array = insert_string(string_array, "three");
    string_array = insert_string(string_array, "Four");

    print_string_array(string_array);

    //make_lower(string_array);
    sort_string_array(string_array);

    print_string_array(string_array);
    release_string_array(string_array);

    return EXIT_SUCCESS;
}
