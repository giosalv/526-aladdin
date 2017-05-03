#include "hello.h"

int main() {
  int sum=0;
  for (int i=0; i<6; i++) {
    sum += i;
  }
  printf("hello world %d\n", sum);
  return 0;
}

