#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;

    // Prompt user until a non-negative int is provided
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int coins = 0;

    // Greedy algorithm: Use largest coin first
    coins += cents / 25;
    cents %= 25;

    coins += cents / 10;
    cents %= 10;

    coins += cents / 5;
    cents %= 5;

    coins += cents; // Remaining 1s

    printf("%i\n", coins);
}
// This program calculates the minimum number of coins needed to make change for a given amount of
// cents. It uses a greedy algorithm, starting with the largest coin denomination (25 cents) and
// working down to the smallest (1 cent). The user is prompted to enter a non-negative integer
