from cs50 import get_string

# Get input text
text = get_string("Text: ")

# Count letters (A-Z and a-z)
letters = sum(1 for c in text if c.isalpha())

# Count words (assumes words are separated by spaces)
words = len(text.split())

# Count sentences (ends with ., ! or ?)
sentences = sum(1 for c in text if c in ['.', '!', '?'])

# Coleman-Liau index formula
L = (letters / words) * 100
S = (sentences / words) * 100
index = round(0.0588 * L - 0.296 * S - 15.8)

# Output result
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
