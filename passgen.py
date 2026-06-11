import os
import random
import string


substitutions = {
    'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'],
    's': ['$', '5'], 'l': ['1'], 't': ['7']
}

adjectives = [
    "quick", "bright", "silent", "brave", "happy", "wild", "gentle", "bold", "clever", "fuzzy",
    "glowing", "icy", "jolly", "kind", "lucky", "mighty", "neat", "odd", "proud", "quiet",
    "rapid", "shiny", "tiny", "vast", "witty", "zany", "young", "ancient", "chilly", "dusty",
    "eager", "fierce", "graceful", "honest", "intense", "jazzy", "keen", "loyal", "modern", "nifty",
    "orange", "playful", "quirky", "rusty", "sharp", "tough", "upbeat", "vivid", "warm", "zealous"
]

nouns = [
    "fox", "river", "mountain", "storm", "ocean", "tree", "cloud", "wolf", "sun", "moon",
    "star", "stone", "leaf", "wind", "flame", "shadow", "echo", "forest", "valley", "canyon",
    "breeze", "island", "snow", "rain", "meadow", "rock", "beach", "sand", "ice", "lake",
    "peak", "fog", "wave", "hill", "thunder", "lightning", "desert", "glacier", "tide", "grove",
    "creek", "field", "plain", "cliff", "earth", "sky", "comet", "crater", "volcano", "marsh"
]
def generate_password():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = str(random.randint(10, 99))
    password = adjective + noun + number

    for char in password:
        if char in substitutions and random.random() < 0.5:
            password = password.replace(char, random.choice(substitutions[char]), 1)
    return password

print("Welcome to PassGen")
print("generating password..")
passwords = input("how many passwords do you want? (enter a number): \n")
passwordsint = int(passwords)
for i in range(passwordsint):  
    password = generate_password()
    print("password generated!\n" + str(password))

print("\npress enter to exit")
input()