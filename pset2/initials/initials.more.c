#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string name = GetString();
    
    if (!isalpha(name[0]))
    {
        printf("%c", toupper(name[0]));
    }
    
    int n = strlen(name);
    for (int i = 1; i < n; i++)
    {
        if (isblank(name[i]) && isblank(name[i+1]))
        {
            i+=2;
            
        }
        if ( isalpha(name[i]) && isalpha(name[i+1]) && isblank(name[i-1]))
        {
            printf("%c", toupper(name[i]));
        }
             
    }
    printf("\n"); 
}