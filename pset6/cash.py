from cs50 import get_float

# Prompt user until valid (non-negative) input
while True:
    dollars = get_float("Change owed: ")
    if dollars >= 0:
        break

# Convert dollars to cents and round to avoid floating-point issues
cents = round(dollars * 100)

# Coin denominations in cents
coins = 0
for coin in [25, 10, 5, 1]:
    coins += cents // coin
    cents %= coin

# Output minimum number of coins
print(coins)
