// Implements a dictionary's functionality

#include <cstddef>
#include <cstdio>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

bool first = true;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 + 26 + 26 + 26;
int location;
// Hash table
node *table[N];
char * ptr;
int counter = 0;
// Returns true if word is in dictionary, else false

bool check(const char *word)
{
    char temp[LENGTH + 1];
    int n = strlen(word);

    // Convert word to lowercase for case-insensitive comparison
    for (int i = 0; i < n; i++)
    {
        temp[i] = tolower(word[i]);
    }
    temp[n] = '\0';

    // Hash word to obtain hash value
    int index = hash(temp);

    // Access linked list at that index
    node *cursor = table[index];

    // Traverse linked list to find the word
    while (cursor != NULL)
    {
        if (strcmp(cursor->word, temp) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}



// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long hash = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash = (hash << 2) ^ word[i];
    }
    return hash % N;
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }
        strcpy(new_node->word, word);

        int index = hash(word);

        // Insert node at the beginning of the linked list
        new_node->next = table[index];
        table[index] = new_node;
    }
    fclose(file);
    return true;
}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (counter == 0 )
    {
        return 0;
    }
    return word_count;  // Assuming `word_count` is updated during `load`


}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
