#ifndef AALTO_SHOP_FUNCTIONS_H
#define AALTO_SHOP_FUNCTIONS_H

typedef struct {
	char name[31];
	float price;
	int in_stock;
} Product;


/* Compare two strings lexically (ASCII value-wise, same as strcmp())
 * The string "duck" is before "rabbit" in this order but
 *  "Rabbit" is before "duck" (see an ASCII chart)
 * Returns: 0 if the two strings are equal
 * Hint: strcmp
 */
int compareAlpha(const void* a, const void* b);

/* Same as compareAlpha but compares the product *in_stock* numerically.
 * The product with higher *in_stock* -value should be first in the array.
 * If there are two or more products with same *in_stock* -value, they are compared lexically.
 */
int compareNum(const void* a, const void* b);

/* Finds a product from a sorted array of products
 * Returns: Whatever bsearch returned.
 * IMPORTANT: Remember that bsearch takes a pointer to a type as first parameter, and 
 * pointer to an array with same type elements as in first parameter.
 */
Product* findProduct(Product* p_array, const char* searchkey, int (*cmp)(const void*, const void*));


#endif /* AALTO_SHOP_FUNCTIONS_H */
