# Testing of ciphers

import random

from cryptoamino.cipher import *
from cryptoamino import tools

# Get a random letter substitution
shuffled_letters = list(tools.letters).copy()
random.shuffle(shuffled_letters)
random_substitution = {a: b for a, b in zip(tools.letters, shuffled_letters)}

ciphers = [
  
  # Simple substitution over lowercase letters, ignoring other symbols.
  (simple_substitution.SimpleSubstitution(),
    random_substitution,
    "plaintext plaintext plaintext"),
  
  # Vigenere over lowercase letters only.
  (vigenere.Vigenere(tools.add, tools.subtract),
    "key",
    "plaintextplaintextglorp")
  
]

# Run all ciphers in encrypt then decrypt mode to ensure they completely undo
# themselves.
for cipher, key, plaintext in ciphers:
  cipher.key(key)
  ciphertext = tools.concat(cipher.encrypt(plaintext))
  print("{0} -> {1}".format(plaintext, tools.concat(ciphertext)))
  plaintext2 = tools.concat(cipher.decrypt(ciphertext))
  if plaintext2 != plaintext:
    raise Exception(
      "Cipher failed: plaintext {0} was decrypted to {1}".format(
        plaintext,
        plaintext2))
