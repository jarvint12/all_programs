#ifndef AALTO_BITS_H
#define AALTO_BITS_H

int op_bit_get(const unsigned char* data, int i);
void op_bit_set(unsigned char* data, int i);
void op_bit_unset(unsigned char* data, int i);
unsigned char op_bit_get_sequence(const unsigned char* data, int i, int how_many);
void op_print_byte(unsigned char b);

#endif
