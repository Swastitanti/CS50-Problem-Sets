from cs50 import get_int

# Prompt for height between 1 and 8
while True:
    height = get_int("Height: ")
    if 1 <= height <= 8:
        break

# Build the pyramid
for row in range(1, height + 1):
    spaces = height - row
    hashes = row
    print(" " * spaces + "#" * hashes)
