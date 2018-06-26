# Perform a Padding Oracle Attack given some ciphertext.

from cryptoamino import tools

# The following diagram illustrates one round of CBC decryption, given a carry
# block (possibly the IV) and ciphertext block.
#
# carry  ciphertext
#   |        |
#   |    +-------+
#   |    |decrypt|
#   |    +-------+
#   |        |
#   |   pre-plaintext
#   |        |
#   +-------[+]
#            |
#        plaintext

# Perform Padding Oracle against the CBC mode of operation and the PKCS#7
# padding scheme, given:
#   iv:         A byte array containing a block of Initialisation Vector
#   ciphertext: A byte array containing at least one block of ciphertext.
#   block_size: The number of bytes in a block of text.
#   oracle:     A function which returns True when a ciphertext is padded
#               in PKCS#7 correctly after decryption, given an IV and
#               some ciphertext.
def cbc_pkcs7(iv, ciphertext, block_size, oracle):
  
  # Given some possible preplaintext (a block of bytes), and the amount of
  # progress already made on it (the number of rightmost bytes which are
  # assumed correct), yield a set of possible preplaintexts which have one more
  # byte of progress.
  def break_next_byte(known_carry, known_ciphertext, preplaintext, progress):
    
    # The position of the byte being cracked, measured from the right.
    target_progress = progress + 1
    # The value of the padding bytes when the padding is correct AND expected.
    target_padding_byte = target_progress
    
    # Prepare a trial carry block which, when combined with the preplaintext,
    # produces most of the expected padding.
    trial_carry = bytearray(block_size)
    for i in range(progress):
      trial_carry[-i] = preplaintext[-i] ^ target_padding_byte
    
    # Run through some trial carry blocks, finding the ones which lead to
    # correct paddings. One of the results will correspond with the expected
    # padding, which is `target_progress` bytes long.
    trial_carries_passing = []
    for trial_carry_byte in range(255):
      trial_carry[-target_progress] = trial_carry_byte
      if oracle(trial_carry, known_ciphertext):
        trial_carries_passing.append(bytearray(trial_carry))
    
    # One of the trial carries will XOR with the expected plaintext to produce
    # a preplaintext with one extra correct byte.
    for trial_carry_passing in trial_carries_passing:
      next_preplaintext = bytearray(block_size)
      for i in range(block_size):
        next_preplaintext[i] = trial_carry_passing[i] ^ target_padding_byte
      yield next_preplaintext
  
  # Break a block of ciphertext byte by byte, collecting all possible
  # plaintexts.
  def break_block(known_carry, known_ciphertext):
    
    # Collect and improve preplaintext possibilities
    last_preplaintexts = []
    for progress in range(block_size):
      next_preplaintexts = []
      for last_preplaintext in last_preplaintexts:
        next_preplaintexts.append(break_next_byte(
          known_carry,
          known_ciphertext,
          last_preplaintext,
          progress))
      last_preplaintexts = next_preplaintexts
    
    # Convert known preplaintexts into plaintexts
    for preplaintext in last_preplaintexts:
      plaintext = bytearray(block_size)
      for i in range(block_size):
        plaintext[i] = preplaintext[i] ^ known_carry[i]
      yield plaintext
  
  # Break all blocks
  ciphertext_blocks = list(tools.group(ciphertext, block_size))
  blocks = [iv] + ciphertext_blocks
  plaintext_blocks = []
  for i in range(len(ciphertext_blocks)):
    block = blocks[-i]
    carry = blocks[-i-1]
    plaintext_blocks = break_block(carry, block)
    assert len(plaintext_blocks) = 1
    yield from plaintext_blocks
  
