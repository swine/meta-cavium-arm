#include <stdio.h>

int main () {
    void *p;
    printf("Hello World!!! INT=%d LONG=%d POINTER=%d \n",
	sizeof(int), sizeof(long), sizeof(p));
    return 0;
}
