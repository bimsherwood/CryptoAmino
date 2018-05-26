# The Blocked Matrix Transpose cipher (Bimmo's Woof Gange puzzle)
#
# The Blocked Matrix Transpose cipher works as follows:
# 1) The key is chosen as a pair of natural numbers, R and C.
# 2) The message is padded to a multiple of R*C.
# 3) The message is broken into groups R*C long.
# 4) The groups are loaded row-major into a matrix.
# 5) The matrix is transposed.
# 6) The ciphertext is read out row-major from the matrices.

from cryptoamino import tools

class BlockedMatrixTranspose:
  
  def __init__(self, pad_1='z', pad_2='x'):
    self.pad_1 = pad_1
    self.pad_2 = pad_2
  
  # Accepts a pair of natural numbers as a key.
  def key(self, key):
    self.r, self.c = key
  
  # The first pad character is appended to the stream, and then enough second
  # pad characters are appended to the stream to make its length a multiple of
  # the block size.
  def pad(self, stream):
    
    # Echo the stream, keeping track of the length
    length = 0
    for symbol in stream:
      yield symbol
      length += 1
    
    # Echo the first padding character
    yield self.pad_1
    length += 1
    
    # Append the correct number of second padding characters
    block_size = self.r * self.c
    remaining = -length % block_size
    for i in range(remaining):
      yield self.pad_2
  
  def unpad(self, stream):
    potential_padding = []
    for symbol in stream:
      if symbol == self.pad_1:
        yield from potential_padding # Flush the old potential padding
        potential_padding.clear()
        potential_padding.append(symbol)
      elif symbol == self.pad_2: # Continue the potential padding
        potential_padding.append(symbol)
      else: # The stream continues
        yield from potential_padding # Flush the potential padding
        potential_padding.clear()
        yield symbol
  
  def encrypt(self, stream):
    block_size = self.r * self.c
    for block in tools.group(self.pad(stream), block_size):
      matrix = tools.Matrix(self.r, self.c)
      matrix.rows = [list(row) for row in tools.group(block, matrix.width)]
      matrix = matrix.transposed()
      yield from matrix
  
  def decrypt(self, stream):
    block_size = self.r * self.c
    for block in tools.group(stream, block_size):
      matrix = tools.Matrix(self.r, self.c)
      matrix.rows = [list(row) for row in tools.group(block, matrix.width)]
      matrix = matrix.transposed()
      yield from self.unpad(matrix)
