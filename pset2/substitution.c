#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Function prototypes
bool is_valid_key(string key);
char substitute(char c, string key);

int main(int argc, string argv[])
{
    // Check for exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Store the key from argument
    string key = argv[1];

    // Validate the key
    if (!is_valid_key(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    // Get plaintext input from user
    string plaintext = get_string("plaintext:  ");

    // Print ciphertext header
    printf("ciphertext: ");

    // Loop through each character in the plaintext
    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", substitute(plaintext[i], key));
    }

    printf("\n");
    return 0;
}

// Function to validate the key
bool is_valid_key(string key)
{
    if (strlen(key) != 26)
    {
        return false;
    }

    bool seen[26] = {false};

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        int index = toupper(key[i]) - 'A';
        if (seen[index])
        {
            return false;
        }
        seen[index] = true;
    }
    return true;
}

// Function to substitute a character using the key
char substitute(char c, string key)
{
    if (isupper(c))
    {
        int pos = c - 'A';
        return toupper(key[pos]);
    }
    else if (islower(c))
    {
        int pos = c - 'a';
        return tolower(key[pos]);
    }
    else
    {
        return c;
    }
}
