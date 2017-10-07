#include <stdio.h>
#include <string.h>
#include <cs50.h>

int main(void)
{
    long long n;
    char m[16];
    int len, sum, j;
    do
    {
        printf("Number: ");
        n = get_long_long();
        sprintf(m, "%lld", n);
    }
    while (n<0);
    
    len = strlen(m);
    
    if (len < 13 || len > 16 || len == 14)
    {
        printf("INVALID\n");
        return 0;
    }
    int num[len];
    for (int i = 0; i < len; i++)
        num[i] = m[i]-'0';

    sum = 0;
    j = 1;
    for (int i = len - 1; i >= 0; i--)
    {
        if (j % 2 == 0)
        {
            sum += num[i] * 2 % 10;
            if (num[i]*2 >= 10)
                sum += 1; 
        } 
        else
            sum += num[i];
        j++;  
    }
    
    if (num[0] == 3 && (num[1] == 4 || num[1] == 7) && sum % 10 == 0)
        printf("AMEX\n");
    else if (num[0] == 5 && num[1] > 0 && num[1] < 6 && sum % 10 == 0)
        printf("MASTERCARD\n");
    else if (num[0] == 4 && sum % 10 == 0)
        printf("VISA\n");
    else
        printf("INVALID\n");
   
    return 0;
}   









