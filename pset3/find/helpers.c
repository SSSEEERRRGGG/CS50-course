#include <cs50.h>
#include <stdio.h>
#include "helpers.h"

bool search(int value, int values[], int n)
{
    if (n == 1)
    {
        if (value != values[0])
            return false;
    }
    if (n == 2)
    {
        if (value == values[0] || value == values[1])
            return true;
        else
            return false;
    }

    int middle = n/2;
    const int MAX = 65536;
    int new_array[MAX];
    if (value > values[middle])
    {
        int new_size = n - middle;
        
        for (int i = 0, m = middle; i < new_size; i++, m++)
             new_array[i] = values[m];

        return search(value, new_array, new_size);
    }
    else if (value < values[middle])
    {
        int new_size = n - middle;
        for (int i = 0, m = 0; i < middle; i++, m++)
             new_array[i] = values[m];
        return search(value, new_array, new_size);
    }
    else if (value == values[middle])
        return true;

    return false;
}

void sort(int values[], int n)
{
    for (int i = 1; i<(n-1); i++)
    {
        int element = values[i];
        int j = i;
        while (j>0 && values[j-1]>element)
        {
            values[j] =values[j-1];
            j = j - 1;
        }
        values[j] = element;
        //printf("%d\n", values[i]);
    }
}
