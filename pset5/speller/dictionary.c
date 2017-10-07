#include <ctype.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "dictionary.h"

int hash(const char* word);     // prototype

typedef struct node         // define node structure
{
    char *word; 
    struct node* next;
} node;

int count = 0;          // define main variables
char word[LENGTH + 1];

#define HASHTABLE 27                // define hashtable
node *hashtable[HASHTABLE];
/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char* word)
{
    node* checker = malloc(sizeof(node));       // allocate memory to our checker
    int bucket = hash(word);                    // determine in which bucket is the word
    checker = hashtable[bucket];            // situation of the word in our checker

    while (checker != NULL)
    {
        if (strcasecmp(checker->word, word) == 0)       // use strcasecmp to be case insensitive
            return true;
        checker = checker->next;
    }
    return false;
}
/**
 * Loads dictionary into memory.  Returns true if successful else false.
 */
bool load(const char* dictionary)
{
    FILE* dico = fopen(dictionary, "r");            // open the dictionnary file (reading)
    if (dico == NULL)                           // check if the dictionnary opens correctly
        return false;
    
    while (fscanf(dico, "%s\n", word) != EOF)   // iterate through the dictionnary
    {
        node *new = malloc(sizeof(node));           // initialize new node
        new->word = malloc(strlen(word) + 1);       // initiate first pointer
        strcpy(new->word, word);                // copy word into pointer
        int hashed = hash(word);                // hash the word

        if (hashtable[hashed] == NULL)    // if new belongs at head, prepend
        {
            hashtable[hashed] = new;
            new->next = NULL;
        }
        else                               // if belongs in middle or end
        {
            new->next = hashtable[hashed];
            hashtable[hashed] = new;
        }
        count++;                              // count words
    }
    fclose(dico);                           // close dictionnary
    return true;                         // return
}

int hash(const char* word)
{
    int index = 0;                  // initialize index to 0
    for (int i = 0; word[i] != '\0'; i++)   // sum ascii values
        index += tolower(word[i]);       // search for lower cases words

    return index % HASHTABLE;            // mod by size to stay w/in bound of table
}
/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // TODO
    return count;
}
/**
 * Unloads dictionary from memory.  Returns true if successful else false.
 */
bool unload(void)
{
    // TODO
    for (int i = 0; i < HASHTABLE; i++)
    {
        node *cursor;               // initiate a cursor
        cursor = hashtable[i];          // place cursor inside the hashtable

        while (cursor)
        {
            node* tmp = cursor;
            cursor = cursor->next;
            free(tmp);
            return true;
        }
        hashtable[i] = NULL;            // clean hashtable
    }
    return false;
}