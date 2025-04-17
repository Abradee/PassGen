import os
import random
import string
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# --- Constants and Word Lists ---
HISTORY_FILE = "password_history.enc"
KEY_FILE = "secret.key"

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

# --- Encryption ---
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

def encrypt_data(data, key):
    return Fernet(key).encrypt(data.encode())

def decrypt_data(data, key):
    return Fernet(key).decrypt(data).decode()

# --- Password Generation ---
def apply_substitution(word):
    return ''.join(random.choice(substitutions[c.lower()]) if c.lower() in substitutions and random.random() < 0.5 else c for c in word)

def generate_password(num_adjectives, num_nouns, num_numbers, num_punctuations, scramble, custom_words):
    words = random.choices(adjectives, k=num_adjectives) + random.choices(nouns, k=num_nouns) + custom_words
    result_words, has_upper, has_lower = [], False, False

    for word in words:
        word = apply_substitution(word)
        word = list(word)
        if not has_upper:
            word[0] = word[0].upper()
            has_upper = True
        elif not has_lower:
            word[0] = word[0].lower()
            has_lower = True
        else:
            word[0] = word[0].upper() if random.choice([True, False]) else word[0].lower()
        result_words.append(''.join(word))

    numbers = [str(random.randint(0, 9)) for _ in range(num_numbers)]
    punctuation = random.choices(string.punctuation, k=num_punctuations)
    all_parts = result_words + numbers + punctuation

    if scramble:
        random.shuffle(all_parts)

    password = ''.join(all_parts)
    if not any(c.isupper() for c in password): password += 'A'
    if not any(c.islower() for c in password): password += 'a'
    return password

# --- GUI Application ---
class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.key = load_key()
        self.history = []

        tk.Label(root, text="Adjectives:").grid(row=0, column=0)
        tk.Label(root, text="Nouns:").grid(row=1, column=0)
        tk.Label(root, text="Numbers:").grid(row=2, column=0)
        tk.Label(root, text="Punctuations:").grid(row=3, column=0)
        tk.Label(root, text="How many passwords:").grid(row=4, column=0)
        tk.Label(root, text="Custom words (space-separated):").grid(row=5, column=0)

        self.adj_entry = tk.Entry(root); self.adj_entry.grid(row=0, column=1)
        self.noun_entry = tk.Entry(root); self.noun_entry.grid(row=1, column=1)
        self.num_entry = tk.Entry(root); self.num_entry.grid(row=2, column=1)
        self.punc_entry = tk.Entry(root); self.punc_entry.grid(row=3, column=1)
        self.count_entry = tk.Entry(root); self.count_entry.grid(row=4, column=1)
        self.custom_entry = tk.Entry(root); self.custom_entry.grid(row=5, column=1)

        self.scramble_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Scramble", variable=self.scramble_var).grid(row=6, column=0, columnspan=2)

        tk.Button(root, text="Generate", command=self.generate_passwords).grid(row=7, column=0)
        tk.Button(root, text="Show History", command=self.show_history).grid(row=7, column=1)

        self.output = scrolledtext.ScrolledText(root, width=40, height=10)
        self.output.grid(row=8, column=0, columnspan=2, pady=10)

    def generate_passwords(self):
        try:
            num_adjectives = int(self.adj_entry.get())
            num_nouns = int(self.noun_entry.get())
            num_numbers = int(self.num_entry.get())
            num_punctuations = int(self.punc_entry.get())
            how_many = int(self.count_entry.get())
            custom_words = self.custom_entry.get().split()
            scramble = self.scramble_var.get()

            passwords = []
            for _ in range(how_many):
                pwd = generate_password(num_adjectives, num_nouns, num_numbers, num_punctuations, scramble, custom_words)
                passwords.append(pwd)
                self.history.append(pwd)

            self.output.delete('1.0', tk.END)
            self.output.insert(tk.END, "\n".join(passwords))

            self.save_to_file(passwords)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")

    def save_to_file(self, passwords):
        data = "\n".join(passwords) + "\n"
        encrypted = encrypt_data(data, self.key)
        with open(HISTORY_FILE, 'ab') as f:
            f.write(encrypted + b'\n')

    def show_history(self):
        if not os.path.exists(HISTORY_FILE):
            messagebox.showinfo("No History", "No history file found.")
            return
        try:
            with open(HISTORY_FILE, 'rb') as f:
                lines = f.readlines()
            decrypted = [decrypt_data(line.strip(), self.key) for line in lines]
            history = "\n".join(decrypted)
            self.output.delete('1.0', tk.END)
            self.output.insert(tk.END, "History:\n" + history)
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()

