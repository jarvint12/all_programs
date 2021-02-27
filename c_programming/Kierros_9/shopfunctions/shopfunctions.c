#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "shopfunctions.h"

/* Compare two strings lexically (ASCII value-wise, same as strcmp())
 * The string "duck" is before "rabbit" in this order but
 *  "Rabbit" is before "duck" (see an ASCII chart)
 * Returns: 0 if the two strings are equal
 * Hint: strcmp
 */
int compareAlpha(const void* a, const void* b)  {
  const Product *product_a = a;
  const Product *product_b = b;

  return strcmp(product_a->name,product_b->name);
}
/* Same as compareAlpha but compares the product *in_stock* numerically.
 * The product with higher *in_stock* -value should be first in the array.
 * If there are two or more products with same *in_stock* -value, they are compared lexically.
 */
int compareNum(const void* a, const void* b)  {
  const Product *product_a = a;
  const Product *product_b = b;
  if(product_a->in_stock > product_b->in_stock) {
    return -1;
  }
  if(product_a->in_stock == product_b->in_stock) {
    return strcmp(product_a->name,product_b->name);
  }
  else {
    return 1;
  }
}

/* Finds a product from a sorted array of products
 * Returns: Whatever bsearch returned.
 * IMPORTANT: Remember that bsearch takes a pointer to a type as first parameter, and
 * pointer to an array with same type elements as in first parameter.
 */
Product* findProduct(Product* p_array, const char* searchkey, int (*cmp)(const void*, const void*)) {
  int i=0;
  while(p_array[i].name[0]!=0) {
    i++;
  }
  return (bsearch(searchkey, p_array, (i+1), sizeof(p_array[0]),cmp));
}
