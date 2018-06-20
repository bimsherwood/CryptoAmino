# The GlobbyBlock cipher
#
# A 16-round block cipher which operates on 32-byte blocks and keys, using
# multiplication and addition.

class GlobbyBlock:
  
  def __init__(self, rounds=16):
    self.rounds = 16
  
  # The key must be a byte array, 32 bytes long.
  def key(self, key):
    key_int = int.from_bytes(key, byteorder="big")
    self.key_schedule = []
    state = key_int
    for r in range(0,self.rounds):
      state = (65533*state + 3) % (2**256)
      self.key_schedule.append(state.to_bytes(32, byteorder="big"))
  
  # The block must be a byte array, 32 bytes long.
  def encrypt(self, block):
    cipher_state = bytearray(32)
    cipher_state[:] = block
    for r in range(0,self.rounds): # Round
      cipher_state = cipher_state[::-1]
      for i in range(0, 32): # Byte
        cipher_state[i] = (
          (cipher_state[i] + self.key_schedule[r][i])
          % (2**8))
    return cipher_state
  
  # The block must be a byte array, 32 bytes long.
  def decrypt(self, block):
    cipher_state = bytearray(32)
    cipher_state[:] = block
    for r in reversed(range(0,self.rounds)): # Round
      for i in range(0, 32): # Byte
        cipher_state[i] = (
          (cipher_state[i] - self.key_schedule[r][i])
          % (2**8))
      cipher_state = cipher_state[::-1]
    return cipher_state
