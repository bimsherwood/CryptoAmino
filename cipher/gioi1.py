# The G.I.O.I. 1 encoding, by Some Random Stranger
from cryptoamino import tools

# The G.I.O.I. 1 encoding consists of two passes:
# 1) The symbols in the text are converted to decimal ascii, and the numbers
#    are joined with spaces.
# 2) The symbols from pass 1 are converted to hexadecimal ascii (padded to the
#    left with zeros to make two-digit numbers), and the numbers are
#    concatenated.
class Gioi1:
  
  def key(self, key):
    pass
  
  def encrypt(self, stream):
    is_first = True
    for symbol1 in stream: # First pass
      ascii1 = '' if is_first else ' '
      is_first = False
      ascii1 += str(ord(symbol1))
      for symbol2 in ascii1: # Second pass
        ascii2 = "{0:02x}".format(ord(symbol2))
        yield from ascii2
  
  def decrypt(self, stream):
    
    def decodeSecondPass(stream2):
      for hex_num in tools.group(stream2, 2):
        yield chr(int(tools.concat(hex_num), 16))
        
    def decodeFirstPass(stream1):
      dec_num = []
      for symbol in stream1:
        if symbol == ' ':
          yield chr(int(tools.concat(dec_num)))
          dec_num.clear()
        else:
          dec_num.append(symbol)
      if len(dec_num) > 0:
        yield chr(int(tools.concat(dec_num)))
        
    return decodeFirstPass(decodeSecondPass(stream))
  