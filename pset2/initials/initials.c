#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string name = GetString();

    printf("%c", toupper(name[0]));
   
    for (int i = 0, n = strlen(name); i < n; i++)
    {
        if ( name[i] == ' ' && name[i + 1] != '\0') 
            printf("%c", toupper(name[i + 1])); 
    }
    printf("\n"); 
}