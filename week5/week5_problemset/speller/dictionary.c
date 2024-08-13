// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>
#include <cs50.h>

#include "dictionary.h"

unsigned int count = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 1 << 7;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned long hash = 5381;
    int c = 0;
    char *original_word = malloc(strlen(word) + 1);
    strcpy(original_word, word);

    while ((c = *word++))
    {
        c = tolower(c);
        hash = ((hash << 5) + hash) + c;
    }

    node *item = table[hash % N];
    while (item != NULL)
    {
        if (strcasecmp((*item).word, original_word) == 0)
        {
            free(original_word);
            return true;
        }
        item = (*item).next;
    }

    free(original_word);
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int hash = 5381;
    int c;

    while ((c = *word++))
    {
        c = tolower(c);
        hash = ((hash << 5) + hash) + c;
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(input, "%s", word) != -1)
    {
        node *item = malloc(sizeof(node));
        if (item == NULL)
        {
            return false;
        }

        strcpy((*item).word, word);
        unsigned int index = hash(word);

        (*item).next = table[index];

        table[index] = item;

        count++;
    }

    fclose(input);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *item = table[i];
        while (item != NULL)
        {
            node *tmp = (*item).next;
            free(item);
            item = tmp;
        }
    }

    return true;
}
