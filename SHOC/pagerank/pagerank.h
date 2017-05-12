#include <stdio.h>
#include <stdlib.h>

// NNZ: number of non-zero values (and columns)
//   N: number of rows in the matrix

#define NNZ 20
#define N   1024

#define TYPE float
#define MIN  1
#define MAX  128


void pagerank1(TYPE *data, int *rows, int *cols, TYPE *x, TYPE *y);
void pagerank2(TYPE *data, int *rows, int *cols, TYPE *x, TYPE *y);
