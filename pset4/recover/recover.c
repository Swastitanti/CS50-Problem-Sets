#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Define block size
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover card.raw\n");
        return 1;
    }

    // Open memory card file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        fprintf(stderr, "Could not open file: %s\n", argv[1]);
        return 1;
    }

    // Create a buffer to store 512 bytes
    uint8_t buffer[BLOCK_SIZE];

    // Variables to manage output JPEG files
    FILE *img = NULL;
    char filename[8];
    int file_count = 0;

    // Read 512-byte blocks until the end of the file
    while (fread(buffer, 1, BLOCK_SIZE, input) == BLOCK_SIZE)
    {
        // Check for JPEG signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If an image is already open, close it
            if (img != NULL)
            {
                fclose(img);
            }

            // Create new filename for the recovered JPEG
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            file_count++;
        }

        // If currently writing a JPEG, write the buffer
        if (img != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }

    // Clean up
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(input);

    return 0;
}
