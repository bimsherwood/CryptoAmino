# Test some heuristics

import itertools

from cryptoamino.analysis import heuristic
from cryptoamino.analysis import characterisation
from cryptoamino.analysis import distribution
from cryptoamino.cipher.vigenere import *
from cryptoamino import tools

print("Heuristic tests:")

  #
  # Brute Force test, using a cipher
  #

# Test case
cipher = Vigenere(tools.add, tools.subtract)
plaintext = tools.normalise_text(
  "abbabaabababbabbbabbababababababbbbabaaabababbabbbabababbaabababbbab")
correct_key = "ht"
cipher.key(correct_key)
ciphertext = tools.concat(cipher.encrypt(plaintext))

# Prepare the attack
keys = itertools.product(tools.letters, repeat=2)
quadgram_freq = distribution.freq(characterisation.quads(plaintext))
text_fitness = characterisation.quadgram_scorer(quadgram_freq)
def key_fitness(key):
  cipher.key(key)
  return text_fitness(cipher.decrypt(ciphertext))

# Perform the attack
recovered_key = tools.concat(
  heuristic.brute_force(keys=keys, fitness=key_fitness))

print('Used key "{0}", recovered "{1}"'.format(correct_key, recovered_key))

if correct_key != recovered_key:
  raise Exception("Brute force failed")
