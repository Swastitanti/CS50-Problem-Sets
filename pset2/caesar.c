#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function prototype
bool only_digits(string s);
char rotate(char c, int key);

int main(int argc, string argv[])
{
    // Check for exactly one command-line argument
    if (argc != 2 || !only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert string key to int
    int key = atoi(argv[1]);

    // Get plaintext input
    string plaintext = get_string("plaintext:  ");

    // Print ciphertext header
    printf("ciphertext: ");

    // Encrypt each character
    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", rotate(plaintext[i], key));
    }

    // End with a newline
    printf("\n");
    return 0;
}

// Check if string has only digits (0–9)
bool only_digits(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

// Rotate alphabetical character by key positions
char rotate(char c, int key)
{
    if (isupper(c))
    {
        return (c - 'A' + key) % 26 + 'A';
    }
    else if (islower(c))
    {
        return (c - 'a' + key) % 26 + 'a';
    }
    else
    {
        return c; // Leave non-letters unchanged
    }
}
