#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>


#define MAX_INT			65536
#define RANGE_BEGIN		1
#define RANGE_END		4
#define RANGE_SIZE		((RANGE_END) - (RANGE_BEGIN) + 1)
#define get_rand_idx()	((rand()) % (RANGE_SIZE))

#define FORMALS   const int size, \
				  int * const a, \
				  int * const b, \
				  int * const c, \
				  const int idx, \
				  const int s

#define PARAMS    size, \
				  _a, \
				  _b, \
				  _c, \
				  _idx, \
				  _s


int _a[RANGE_SIZE];
int _b[RANGE_SIZE];
int _c[RANGE_SIZE];
const int _idx = 2;
const int _s = 35;


void init_all(FORMALS);

int if_else(FORMALS);
int loop(FORMALS);
int loop_if_else(FORMALS);
int nested_loop(FORMALS);
int nested_loop_if_else(FORMALS);
