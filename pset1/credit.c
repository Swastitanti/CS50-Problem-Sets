#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Ask user to input a credit card number
    long card_number = get_long("Number: ");

    // Variables to keep track of the total sum and the number of digits
    int total_sum = 0;
    int digit_count = 0;

    // Make a copy of the card number for validation and issuer check
    long temp_number = card_number;

    // Loop through each digit of the card number from right to left
    while (temp_number > 0)
    {
        // Get the last digit
        int current_digit = temp_number % 10;

        // If this is every second digit from the right (based on position)
        if (digit_count % 2 == 1)
        {
            // Multiply the digit by 2
            int product = current_digit * 2;

            // If the result is 2 digits, add both digits (e.g., 12 → 1 + 2)
            total_sum += (product / 10) + (product % 10);
        }
        else
        {
            // If not multiplied, just add the digit directly
            total_sum += current_digit;
        }

        // Remove the last digit for the next loop
        temp_number /= 10;

        // Count how many digits the number has
        digit_count++;
    }

    // Check if the card is valid using Luhn's Algorithm (last digit of sum must be 0)
    if (total_sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0; // Exit early if invalid
    }

    // Now, determine the card type based on starting digits and length
    // First, get the first 2 digits of the card
    long starting_digits = card_number;
    while (starting_digits >= 100)
    {
        starting_digits /= 10;
    }

    // Check for AMEX: starts with 34 or 37, and length is 15
    if ((starting_digits == 34 || starting_digits == 37) && digit_count == 15)
    {
        printf("AMEX\n");
    }
    // Check for MasterCard: starts with 51 to 55, and length is 16
    else if (starting_digits >= 51 && starting_digits <= 55 && digit_count == 16)
    {
        printf("MASTERCARD\n");
    }
    // Check for Visa: starts with 4 (first digit), and length is 13 or 16
    else if ((starting_digits / 10 == 4) && (digit_count == 13 || digit_count == 16))
    {
        printf("VISA\n");
    }
    else
    {
        // If it doesn't match any known card pattern
        printf("INVALID\n");
    }
}
