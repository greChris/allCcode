#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
//GREECE
int checks(string key);

int main(int argc, string argv[])
{
    if(!argv[1])
    {
        printf("Please enter a string after running the programm (./substitution <key>)");
        return 1;
    }else if(checks(argv[1]) == 1)
    {
        return 1;
    }
    char key[27];
    for (int i = 0; i < 26; i++)
    {
        key[i] = argv[1][i];
    }
    key[26] = '\0';
    string text = get_string("plaintext: ");
    char encrypted[strlen(text) + 1];
    for (int i = 0; i < strlen(text); i++)
    {
        if (!isalpha(text[i]))
        {
            encrypted[i] = text[i];
        }
        else if (islower(text[i]))
        {
            encrypted[i] = tolower(key[toupper(text[i]) - 'A']);
        }
        else
        {
            encrypted[i] = toupper(key[text[i] - 'A']);
        }
    }
        encrypted[strlen(text)] = '\0';

    printf("ciphertext: %s\n", encrypted);

}



int checks(string key)
{
    if (strlen(key) != 26)
    {
        printf("Key must be exactly 26 characters!\n");
        return 1;
    }

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Only letters are allowed!\n");
            return 1;
        }

        for (int j = i + 1; j < 26; j++)
        {
            if (tolower(key[i]) == tolower(key[j]))
            {
                printf("No duplicates allowed!\n");
                return 1;
            }
        }
    }

    return 0;


}
