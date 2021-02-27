#ifndef AALTO_SHOP_H
#define AALTO_SHOP_H

typedef struct {
	char name[31];
	float price;
	int in_stock;
} Product;


int output_binary(const char* filename, Product* shop);

Product* read_binary(const char* filename);

int output_plaintext(const char* filename, Product* shop);

Product* read_plaintext(const char* filename);

#endif /* AALTO_SHOP_H */
