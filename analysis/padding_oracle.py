# Perform a Padding Oracle Attack given some ciphertext.

from cryptoamino import tools

# The following diagram illustrates one round of CBC decryption, given an IV
# block (or carry-in from the previous ciphertext block) and ciphertext block.
#
# IV  ciphertext
# |       |
# |   +-------+
# |   |decrypt|
# |   +-------+
# |       |
# | pre-plaintext
# |       |
# +------[+]
#         |
#     plaintext

# Perform Padding Oracle against the CBC mode of operation and the PKCS#7
# padding scheme, given:
#   iv:         A byte array containing a block of Initialisation Vector
#   ciphertext: A byte array containing at least one block of ciphertext.
#   block_size: The number of bytes in a block of text.
#   oracle:     A function which returns True when a ciphertext is padded
#               in PKCS#7 correctly after decryption, given an IV and
#               some ciphertext.
def cbc_pkcs7(iv, ciphertext, block_size, oracle):
  
  blocks = [iv] + list(tools.group(ciphertext, block_size))
  carry_block = blocks[-2]
  target_block = blocks[-1]
  
  # Break the last byte
  trial_carry_block = bytearray(block_size)
  predicted_padding = 0x01
  pre_plaintext_possibilities = []
  for i in range(0,256):
    trial_carry_block[-1] = i # Try a new byte in the last position
    if oracle(trial_carry_block, ciphertext):
      # Predicted padding = trial IV + pre-plaintext
      # Pre-plaintext = predicted padding + tril IV
      pre_plaintext_possibilities.append(i ^ predicted_padding)
  
  # Plaintext possibilities
  # Plaintext = pre-plaintext + actual IV
  plaintext_possibilities = [pre_plaintext ^ carry_block[-1]
    for pre_plaintext
    in pre_plaintext_possibilities]
  
  print(plaintext_possibilities)
