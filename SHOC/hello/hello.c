#include <stdio.h>
#define NUM_ITS 3

int main() {
  int sum=0;
  int array[]={0,0,0};
  for (int i=0; i<NUM_ITS; i++) {
    array[i] = array[i] + 1;
    sum += i;
  }
  printf("hello world %d\n", sum);
  return 0;
}

