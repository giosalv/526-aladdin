#include "pagerank.h"

void pagerank1(TYPE *data, int *rows, int *cols, TYPE *x, TYPE *y)
{
    int i, j;
    int begin, end;
    TYPE sum, Si;

    p1nodes: for (i = 0; i < N; i++) {
        sum = 0;
        Si = 0;
        begin = rows[i];
        end = rows[i + 1];

        p1edges: for (j = begin; j < end; j++) {
            Si = data[j] * x[cols[j]];
            sum += Si;
        }

        y[i] = sum;
    }
}


void pagerank2(TYPE *data, int *rows, int *cols, TYPE *x, TYPE *y)
{
    int i;

    p2nodes: for (i = 0; i < N; i++) {
        x[i] = 0.15f / ((float)N) + 0.85f * y[i];
        y[i] = 0.0f;
    }
}


int main()
{
    TYPE *data;
    TYPE *x;
    TYPE *y;

    int *rows;
    int *cols;
    int *col_cnt;

    int i, j;
    int elements_per_row, extra_elements;

    const int min = MIN;
    const int max = MAX;

    srand(0);

    data = (TYPE *) malloc(sizeof(TYPE) * NNZ);
    x = (TYPE *) malloc(sizeof(TYPE) * N);
    y = (TYPE *) malloc(sizeof(TYPE) * N);

    rows = (int *) malloc(sizeof(int) * (N + 1));
    cols = (int *) malloc(sizeof(int) * NNZ);
    col_cnt = (int *) malloc(sizeof(int) * N);

    // values can be random and so can their columns
    for (i = 0; i < NNZ; i++) {
        data[i] = (TYPE) (min + rand() * 1.0f * (max - min) / RAND_MAX);
        cols[i]   = (int)  (rand() * 1.0f * (N - 1) / RAND_MAX);
    }

    // y needs to be all zeroes
    for (i = 0; i < N; i++) {
        x[i] = 1.0f / ((float)N);
        y[i] = 0.0f;
    }

    elements_per_row = NNZ / N;
    extra_elements = NNZ % N;
    rows[0] = 0;
    rows[N] = NNZ;

    // evenly divide elements among the rows
    for (i = 1; i < N; i++) {
        rows[i] = rows[i - 1] + elements_per_row;

        if (i <= extra_elements)
            rows[i]++;
    }

    // initialize x
    for (i = 0; i < N; i++) {
        int begin = rows[i];
        int end = rows[i + 1];
        col_cnt[i] = end - begin;
    }

    for (i = 0; i < N; i++) {
        int begin = rows[i];
        int end = rows[i + 1];

        for (j = begin; j < end; j++) {
            int nodeid = cols[j];
            x[j] = 1.0f / ((float)col_cnt[nodeid]);
        }
    }

    pagerank1(&data[0], &rows[0], &cols[0], &x[0], &y[0]);
    pagerank2(&data[0], &rows[0], &cols[0], &x[0], &y[0]);

    /*
    for (i = 0; i < NNZ; i++) {
        printf("values[%d] = %f\n", i, values[i]);
    }

    for (i = 0; i < N; i++) {
        printf("rows[%d] = %d\n", i, rows[i]);
    }
    printf("row[%d] = %d\n", N, rows[N]);

    for (i = 0; i < NNZ; i++) {
        printf("cols[%d] = %d\n", i, cols[i]);
    }

    for (i = 0; i < N; i++) {
        printf("vector[%d] = %f\n", i, vector[i]);
    }

    for (i = 0; i < N; i++) {
        printf("result[%d] = %f\n", i, result[i]);
    }
    */

    return 0;
}

