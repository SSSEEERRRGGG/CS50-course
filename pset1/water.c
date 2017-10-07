#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("Minutes: ");
    int minutes = GetInt();
   // printf("\n");
    printf("Bottles: %i\n", minutes*12);
}