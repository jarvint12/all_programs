#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "aaltoshop.h"


int output_binary(const char* filename, Product* shop)  {
  FILE *f = fopen(filename, "wb");
  if(!f)  {
    return 1;
  }

  int i=0;
  while((shop[i].name[0])!=0) {
    if((fwrite(&shop[i],sizeof(shop[0]),1,f))!=1) {
      return 1;
    }
    i++;
  }
  fclose(f);
  return 0;
}


Product* read_binary(const char* filename)  {
  FILE *f = fopen(filename, "rb");
  if(!f)  {
    return NULL;
  }

  int i=0;
  Product* products = malloc(sizeof(Product));
  while(!feof(f)) {
    products = realloc(products,((i+2)*sizeof(Product)));
    fread(&products[i],sizeof(Product),1,f);
    i++;
  }
  products[i-1].name[0]=0;
  fclose(f);
  return products;
}


int output_plaintext(const char* filename, Product* shop) {
  FILE *f = fopen(filename, "w");
  if(!f)  {
    return 1;
  }

  int i=0;
  while(shop[i].name[0]!=0)  {
    fprintf(f, "%s", shop[i].name);
    fputc(' ',f);
    fprintf(f, "%f", shop[i].price);
    fputc(' ',f);
    fprintf(f, "%d", shop[i].in_stock);
    fputc('\n',f);
    i++;
  }
  fclose(f);
  return 0;
}

Product* read_plaintext(const char* filename) {
  FILE *f = fopen(filename, "r");
  if(!f)  {
    return NULL;
  }

  Product* products = malloc(sizeof(Product));
  int i=0;

  while(!feof(f)) {
    products = realloc(products,((i+2)*sizeof(Product)));
    fscanf(f,"%s", products[i].name);
    fscanf(f, "%f", &products[i].price);
    fscanf(f, "%d", &products[i].in_stock);
    i++;
    }
    products[i-1].name[0]=0;
    fclose(f);
    return products;
  }
