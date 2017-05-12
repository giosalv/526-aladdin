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


int if_else(FORMALS)
{
    int result = -1;

    if (s % 2) {//rand() % 2) {
        //const int a_idx = get_rand_idx();
        //const int b_idx = get_rand_idx();
        //const int c_idx = get_rand_idx();
        result = a[idx] + b[idx] + c[idx] + s;
    } else {
        result = a[idx] + b[idx+1] + c[idx+1] + s;
    }

    return result;
}


int loop(FORMALS)
{
    int result;
    for (int i = 0; i < size; ++i) {
        result = s * a[i] + b[i];
        c[i] = result;
    }
    return result;
    //for (int i = 0; i < size; ++i)
    //    printf("c[%d]: %d\n", i, c[i]);
}


int loop_if_else(FORMALS)
{
    int result;
    for (int i = 0; i < size; ++i) {
        if (s % 2) {//rand() % 2) {
            //const int a_idx = get_rand_idx();
            //const int b_idx = get_rand_idx();
            result = s * a[idx] + b[idx];
            c[idx] = result;
        } else {
            result = s * a[i] + b[i];
            c[i] = result;
        }
    }
    return result;
    //for (int i = 0; i < size; ++i)
    //    printf("c[%d]: %d\n", i, c[i]);
}


int nested_loop(FORMALS)
{
    int result=0;
    for (int i = 0; i < size; ++i) {
        const int a_val = a[i];

        for (int j = 0; j < size; ++j)
            result += a_val + s * b[j];

        c[i] = result;
    }
    return result;

    //for (int i = 0; i < size; ++i)
    //    printf("c[%d]: %d\n", i, c[i]);
}


int nested_loop_if_else(FORMALS)
{
    int result = 0;
    for (int i = 0; i < size; ++i) {
        const int a_val = a[i];

        for (int j = 0; j < size; ++j) {
            if (rand() % 2) {
                //const int b_idx = get_rand_idx();
                result += a_val + s * b[idx];
            } else {
                result += a_val + s * b[j];
            }
        }

        c[i] = result;
    }
    return result;

    //for (int i = 0; i < size; ++i)
    //    printf("c[%d]: %d\n", i, c[i]);
}
