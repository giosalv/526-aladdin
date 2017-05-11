#include "simple.h"


int main(int argc, char **argv)
{
    srand(0);

    const int size = (rand() % RANGE_SIZE) + RANGE_BEGIN;

    init_all(PARAMS);

    if_else(PARAMS);
    loop(PARAMS);
    loop_if_else(PARAMS);
    nested_loop(PARAMS);
    nested_loop_if_else(PARAMS);

    printf("Done.\n");

    return 0;
}


void init_all(FORMALS)
{
    for (int i = 0; i < size; ++i)
        a[i] = rand() % MAX_INT;

    for (int i = 0; i < size; ++i)
        b[i] = rand() % MAX_INT;

    for (int i = 0; i < size; ++i)
        c[i] = rand() % MAX_INT;
}


void if_else(FORMALS)
{
    int result = -1;

    if (rand() % 2) {
        const int a_idx = get_rand_idx();
        const int b_idx = get_rand_idx();
        const int c_idx = get_rand_idx();
        result = a[a_idx] + b[b_idx] + c[c_idx] + s;
    } else {
        result = a[0] + b[0] + c[0] + s;
    }

    printf("result: %d\n", result);
}


void loop(FORMALS)
{
    for (int i = 0; i < size; ++i)
        c[i] = s * a[i] + b[i];

    for (int i = 0; i < size; ++i)
        printf("c[%d]: %d\n", i, c[i]);
}


void loop_if_else(FORMALS)
{
    for (int i = 0; i < size; ++i) {
        if (rand() % 2) {
            const int a_idx = get_rand_idx();
            const int b_idx = get_rand_idx();
            c[i] = s * a[a_idx] + b[b_idx];
        } else {
            c[i] = s * a[i] + b[i];
        }
    }

    for (int i = 0; i < size; ++i)
        printf("c[%d]: %d\n", i, c[i]);
}


void nested_loop(FORMALS)
{
    for (int i = 0; i < size; ++i) {
        const int a_val = a[i];
        int result = 0;

        for (int j = 0; j < size; ++j)
            result += a_val + s * b[j];

        c[i] = result;
    }

    for (int i = 0; i < size; ++i)
        printf("c[%d]: %d\n", i, c[i]);
}


void nested_loop_if_else(FORMALS)
{
    for (int i = 0; i < size; ++i) {
        const int a_val = a[i];
        int result = 0;

        for (int j = 0; j < size; ++j) {
            if (rand() % 2) {
                const int b_idx = get_rand_idx();
                result += a_val + s * b[b_idx];
            } else {
                result += a_val + s * b[j];
            }
        }

        c[i] = result;
    }

    for (int i = 0; i < size; ++i)
        printf("c[%d]: %d\n", i, c[i]);
}
