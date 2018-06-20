import itertools

class Vigenere:
  
  # The add function must take a plaintext symbol and key symbol, and produce
  # a ciphertext symbol.
  # The subtract function must take a ciphertext symbol and key symbol, and
  # produce a plaintext symbol.
  # It should hold that, for all plaintext, ciphertext, and key symbols
  # p, c, and k:
  #   subtract(add(p, k), k) == p
  #   add(subtract(c, k), k) == c
  def __init__(self, add, subtract):
    self.add = add
    self.subtract = subtract
  
  # Accepts a symbol stream as a key.
  # The symbol stream is buffered up during encryption, in case it needs to
  # repeat.
  def key(self, key):
    
    def key_stream(key):
      key_buffer = []
      for k in key:
        key_buffer.append(k)
        yield k
      while True:
        for k in key_buffer:
          yield k
    
    key = list(key)
    self._encryption_key_stream = key_stream(list(key))
    self._decryption_key_stream = key_stream(list(key))
  
  def encrypt(self, stream):
    for symbol in stream:
      yield self.add(symbol, next(self._encryption_key_stream))
  
  def decrypt(self, stream):
    for symbol in stream:
      yield self.subtract(symbol, next(self._decryption_key_stream))
  