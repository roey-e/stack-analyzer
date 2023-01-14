#include <stdio.h>

int factorial(int n) {
    int k = 1;
    if(n == 0) { return 1; }
    else {
        k = n * factorial(n - 1);
    }
    return k;
}

int main() {
    int k = factorial(6);
    printf("%d\n", k);
}
