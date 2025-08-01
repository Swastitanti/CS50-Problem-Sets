#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Point values for each letter of the alphabet (A=0, B=1, ..., Z=25)
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

// Function prototype
int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Compute the scores for both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Compare scores and declare the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

// Function to compute score of a word
int compute_score(string word)
{
    int score = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        char c = word[i];

        // Only score alphabet letters
        if (isalpha(c))
        {
            // Convert character to uppercase to simplify
            c = toupper(c);

            // Subtract 'A' to get index between 0-25
            int index = c - 'A';

            // Add that letter's point value to total score
            score += POINTS[index];
        }
    }

    return score;
}
