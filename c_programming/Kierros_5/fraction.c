#include <stdlib.h>
#include "fraction.h"

/* Algorithm for determining greatest common divisor, needed in (d) */
/* The function returns gcd between the two parameters, u and v */
/* Taken from http://en.wikipedia.org/wiki/Binary_GCD_algorithm */
unsigned int gcd(unsigned int u, unsigned int v)
{
    // simple cases (termination)
    if (u == v)
        return u;

    if (u == 0)
        return v;

    if (v == 0)
        return u;

    // look for factors of 2
    if (~u & 1) // u is even
    {
        if (v & 1) // v is odd
            return gcd(u >> 1, v);
        else // both u and v are even
            return gcd(u >> 1, v >> 1) << 1;
    }

    if (~v & 1) // u is odd, v is even
        return gcd(u, v >> 1);

    // reduce larger argument
    if (u > v)
        return gcd((u - v) >> 1, v);

    return gcd((v - u) >> 1, u);
}

Fraction* setFraction(unsigned int numerator, unsigned int denominator) {
  struct fraction_st *new_fraction = malloc(sizeof(struct fraction_st));
  new_fraction->numerator = numerator;
  new_fraction->denominator = denominator;
  return new_fraction;
}

void freeFraction(Fraction* f)  {
  free(f);
}

unsigned int getNum(const Fraction *f)  {
  int numerator = f->numerator;
  return numerator;
}

unsigned int getDenom(const Fraction *f)  {
  int denominator = f->denominator;
  return denominator;
}

int compFraction(const Fraction *a, const Fraction *b)  {
  //float jako = a->numerator/a->denominator;
//  int kerto = a->numerator*b->denominator;
  //printf("%d / %d\n", a->numerator, a->denominator);
  //printf("%d", kerto);
  if((float)a->numerator/(float)a->denominator <(float)b->numerator/(float)b->denominator) {
    return -1;
  }
  else if((float)a->numerator/(float)a->denominator == (float)b->numerator/(float)b->denominator) {
    return 0;
  }
  else  {
    return 1;
  }
}

Fraction *addFraction(const Fraction *a, const Fraction *b) {
  struct fraction_st *new_fraction = malloc(sizeof(struct fraction_st));
  new_fraction->numerator = (a->numerator*b->denominator+b->numerator*a->denominator);
  new_fraction->denominator = a->denominator*b->denominator;
  return new_fraction;
}

void reduceFraction(Fraction *val)  {
  int syt = gcd(val->numerator, val->denominator);
  val->numerator = val->numerator/syt;
  val->denominator = val->denominator/syt;
}

/*void printFraction(const Fraction *a) {
  printf("%d / %d",a->numerator, a->denominator);
}*/
