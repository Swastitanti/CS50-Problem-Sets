#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string name = get_string("What's your name? ");
    printf("hello, %s\n", name);
}

// This program prompts the user for their name and then prints a greeting message.
// It uses the CS50 library to handle input and output.
