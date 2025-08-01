#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 1; i <= height; i++)
    {
        for (int s = 0; s < height - i; s++)
        {
            printf(" ");
        }
        for (int h = 0; h < i; h++)
        {
            printf("#");
        }
        printf("\n");
    }
}
// This program prints a half-pyramid of a specified height using hashes (#).
// The height is obtained from the user and must be between 1 and 8 inclusive.
// The pyramid is right-aligned, with spaces before the hashes to create the desired shape.
// The outer loop iterates through each row, while the inner loops handle the spaces and hashes.
// The program uses the CS50 library for input handling, specifically the get_int function to ensure
// valid input. The pyramid is printed to the console, with each row containing the appropriate
// number of spaces followed
