#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "shopfunctions.h"
#include "shopfunctions.c"


void printProducts(Product* array)
{
	int i = 0;
	while(array[i].name[0] != 0)
	{
		printf("product: %s price: %f in stock: %d\n", array[i].name, array[i].price, array[i].in_stock);
		i++;
	}
}

int main()
{
	Product array[6] = {
	{"peanut butter", 1.2, 	5},
	{"cookies", 	 12.3, 23},
	{"cereals", 	  3.2, 12},
	{"bread",	  2.7, 12},
	{"butter", 	  4.2,  5},
	{"\0",		0.0, 0}
	};

	qsort(array, 5, sizeof(Product), compareAlpha);
	printf("sorted lexically:\n");
	printProducts(array);

	Product* search = findProduct(array, "cookies", compareAlpha);
	if(search)
	{
		printf("Found product:\n");
		printf("%s\n", search->name);
	}
	search = findProduct(array, "nonexistent", compareAlpha);
	if(search)
	{
		printf("Found product:\n");
		printf("%s\n", search->name);
	}
	else printf("Product not found!\n");

	qsort(array, 5, sizeof(Product), compareNum);
	printf("sorted by in stock:\n");
	printProducts(array);

	return 0;
}
