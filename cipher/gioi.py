# The G.I.O.I. encoding, by Some Random Stranger

class Gioi:
  
  def key(self, key):
    pass
  
  def encrypt(self, stream):
    is_first = True
    for symbol1 in stream:
      ascii1 = '' if is_first else ' '
      is_first = False
      ascii1 += str(ord(symbol1))
      for symbol2 in ascii1:
        ascii2 = "{0:02x}".format(ord(symbol2))
        yield from ascii2
  
  def decrypt(self, stream):
    pass
  