#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])  
{
    if (argc != 2 && !isdigit(argv[1]))
    {
        printf ("Wrong number of arguments. Please try again.\n");
        return 1;
    }

    int k = atoi(argv[1]);

    printf("plaintext: ");
    string p = GetString();
    
    printf("ciphertext: ");
    for (int i = 0, n = strlen(p); i < n; i++)
    {            
        if (isupper(p[i]))
            printf("%c", 'A' + (p[i] - 'A' + k) % 26);
        else if (islower(p[i]))
            printf("%c", 'a' + (p[i] - 'a' + k) % 26);
        else
            printf("%c", p[i]);
    }

    printf("\n");

    return 0;
}    