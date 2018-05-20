# Test the polyalphabetic analysis module

from cryptoamino import tools
from cryptoamino.analysis import characterisation
from cryptoamino.analysis import polyalphabetic
from cryptoamino.cipher.vigenere import Vigenere

  #
  # Test the likely substitution periods detector
  #

# Any periodic polyalphabetic cipher
cipher = Vigenere(tools.add, tools.subtract)

# Test case
plaintext = (
    "assdassddadsdasdasddddsadasdsdasdsdasdsassssdaasdsd"
  + "asdddsasasdsdsdsssasdasdadssssdasdaasdasdassssdadad"
  + "asssdsddsadasdsdaaddsaddsdssdsasdadsssdsdasdsdsddsd")
key = "udgnshb"
correct_period = len(key)
cipher.key(key)
ciphertext = tools.concat(cipher.encrypt(plaintext))

# Run the detector
detected = polyalphabetic.likely_substitution_periods(ciphertext, 2, 16)
print("Periods detected:", detected)
if detected[0] != correct_period:
  raise Exception("Likely substitution period detector failed.")
