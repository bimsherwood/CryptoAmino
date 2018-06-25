# The Cipher Block Chaining mode of operation
#
# CipherBlockChaining wraps a block cipher with a given block size. It is a
# stream cipher, and employs the PKCS#7 padding scheme.

import itertools
from cryptoamino import tools

# Block size is in bytes
def pad_pkcs7(stream, block_size):
  block_length = 0
  for byte in stream:
    block_length += 1
    block_length %= block_size
    yield byte
  remaining = block_size - block_length
  for i in range(0,remaining):
    yield remaining

class PaddingError(Exception):
    pass

# Throws a PaddingError when the padding is incorrect
def unpad_pkcs7(stream, block_size):
  
  blocks = tools.group(stream, block_size)
  
  # Cache the first block
  try:
    cache = next(blocks)
  except StopIteration:
    raise PaddingError()
  
  # Move all blocks through the cache, keeping the last one
  for block in blocks:
    yield from cache
    cache = block
  
  # Validate the padding in the last block
  if len(cache) != block_size:
    raise PaddingError()
  pad_byte = cache[-1]
  if not 0 < pad_byte <= block_size:
    raise PaddingError()
  for i in range(0, pad_byte):
    if cache[-1-i] != pad_byte:
      raise PaddingError()
  
  # Depad the last block
  yield from cache[:block_size - pad_byte]

class CipherBlockChaining:
  
  # Block size is in bytes.
  def __init__(self, block_size, cipher):
    self.cipher = cipher
    self.block_size = block_size
  
  def key(self, key_iv):
    key, iv = key_iv
    self.cipher.key(key)
    self.iv = bytearray(iv)
  
  def encrypt(self, stream):
    padded = pad_pkcs7(stream, self.block_size)
    state = bytearray(self.iv)
    while True:
      # Extract a block of plaintext
      plaintext_block = bytearray(itertools.islice(padded, self.block_size))
      if len(plaintext_block) == 0:
        break;
      # Combine the chained input
      for i in range(0, self.block_size):
        state[i] = state[i] ^ plaintext_block[i]
      # Encrypt the block
      state = self.cipher.encrypt(state)
      yield from state
  
  # Returns a byte stream.
  # The stream ends in None if the padding was bad.
  def decrypt(self, stream):
    
    ciphertext_blocks = tools.group(stream, self.block_size)
    
    def plaintext_blocks():
      carry = bytearray(self.iv)
      for ciphertext_block in ciphertext_blocks:
        difference = self.cipher.decrypt(ciphertext_block)
        plaintext_block = bytearray(self.block_size)
        for i in range(self.block_size):
          plaintext_block[i] = carry[i] ^ difference[i]
        carry = ciphertext_block
        yield plaintext_block
    
    plaintext = (byte for block in plaintext_blocks() for byte in block)
    return unpad_pkcs7(plaintext, self.block_size)
