from cs50 import get_int

# Prompt user for height
while True:
    height = get_int("Height: ")
    if 1 <= height <= 8:
        break

# Print the double half-pyramid
for i in range(1, height + 1):
    spaces = height - i
    blocks = i
    print(" " * spaces + "#" * blocks + "  " + "#" * blocks)
