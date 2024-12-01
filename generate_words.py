import enchant
import itertools
import string

english_dict = enchant.Dict("en_US")
valid_words = []
alphabet = string.ascii_lowercase
word_length = 5

for letters in itertools.product(alphabet, repeat=word_length):
    word = ''.join(letters)
    if english_dict.check(word):
        valid_words.append(word)

with open("words.txt", "w") as file:
    for word in valid_words:
        file.write(word + "\n")

print(f"Generated {len(valid_words)} valid 5-letter words.")
