# Used in the main program's search function
# Protects user search queries from tracking
# Adds random words to queries before sending to Google API

import random

def obfuscate_query(query):
    # Enhanced list of padding words
    padding_words = [
        ' extra',
        ' search',
        ' query',
        ' find',
        ' lookup',
        ' explore'
    ]
    # Select a random padding word
    padding = random.choice(padding_words)
    return f"{query}{padding}"

if __name__ == "__main__":
    user_input = input("Enter your search query: ")
    obfuscated = obfuscate_query(user_input)
    print(f"\nOriginal query: {user_input}")
    print(f"Obfuscated query: {obfuscated}")
