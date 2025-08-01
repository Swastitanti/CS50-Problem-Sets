from cs50 import get_string

# Get card number as a string to preserve leading zeros
card = get_string("Number: ")

# Check if card is numeric
if not card.isdigit():
    print("INVALID")
    exit(0)

# Luhn's Algorithm to validate the card
total = 0
reverse = card[::-1]

for i in range(len(reverse)):
    digit = int(reverse[i])
    if i % 2 == 1:
        doubled = digit * 2
        total += doubled if doubled < 10 else (doubled - 9)
    else:
        total += digit

# Checksum result
if total % 10 != 0:
    print("INVALID")
    exit(0)

# Determine card type by length and starting digits
length = len(card)

if length == 15 and card.startswith(("34", "37")):
    print("AMEX")
elif length == 16 and card.startswith(("51", "52", "53", "54", "55")):
    print("MASTERCARD")
elif length in [13, 16] and card.startswith("4"):
    print("VISA")
else:
    print("INVALID")
