#include <stdio.h>
#include <math.h>
#include "cs50.h"

int main(void)
{
    float n;
    int count = 0;
    int amount;

    do
    {
        printf("How much change is owed?\n");
        n = get_float();
    }
    while (n < 0);

    n *= 100.0;
    amount = (int) round(n);

    while (amount >= 25)
    {
        count++;
        amount -= 25;
    }
    while (amount >= 10)
    {
        count++;
        amount -= 10;
    }
    while (amount >= 5)
    {
        count++;
        amount -= 5;
    }
    while (amount >= 1)
    {
        count++;
        amount -= 1;
    }

    printf("%d\n", count);
    return 0;
}