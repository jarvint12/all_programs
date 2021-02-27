#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "aaltoshop.h"
#include "aaltoshop.c"


int main()
{
	Product* arr = calloc(3,  sizeof(Product));
	strcpy(arr[0].name, "peanut_butter");
	arr[0].price = 5.2;
	arr[0].in_stock = 4;
	strcpy(arr[1].name, "milk");
	arr[1].price = 1.1;
	arr[1].in_stock = 42;
	arr[2].name[0] = 0;

	output_binary("testi", arr);

	Product* arr2;
	arr2 = read_binary("testi");

	output_plaintext("testi.txt", arr2);

	Product* arr3 = NULL;

	arr3 = read_plaintext("testi.txt");

	for(int i = 0; i < 3; i++)
	{
		printf("%s %f %d\n", arr3[i].name, arr3[i].price, arr3[i].in_stock);
	}
	free(arr);
	free(arr2);
	free(arr3);

	return 0;
}
