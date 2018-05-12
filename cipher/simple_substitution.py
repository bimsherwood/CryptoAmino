class SimpleSubstitution:
  
  # Accepts a dictionary as a key.
  # The dictionary is reversed, for the sake of decryption.
  def key(self, key):
    self.key = key
    self._decryption_key = {c:p for (p, c) in key.items()}
  
  # Encrypt the entire enumerable stream.
  # Returns an enumerable stream.
  def encrypt(self, stream):
    for symbol in stream:
      if symbol in self.key:
        yield self.key[symbol]
      else:
        yield symbol
  
  # Encrypt the entire enumerable stream.
  # Returns an enumerable stream.
  def decrypt(self, stream):
    for symbol in stream:
      if symbol in self._decryption_key:
        yield self._decryption_key[symbol]
      else:
        yield symbol
