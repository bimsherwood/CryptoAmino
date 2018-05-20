# The G.I.O.I. 1 encoding, by Some Random Stranger
#
# The G.I.O.I. 1 encoding consists of two passes:
# 1) The symbols in the text are converted to decimal ascii, and the numbers
#    are joined with spaces.
# 2) The symbols from pass 1 are converted to hexadecimal ascii (padded to the
#    left with zeros to make two-digit numbers), and the numbers are
#    concatenated.

from cryptoamino import tools

# First pass: Decimal ascii, joined with spaces
def encodeFirstPass(stream):
  is_first = True
  for symbol in stream: # First pass
    if not is_first:
      yield ' '
    is_first = False
    yield from str(ord(symbol))

def decodeFirstPass(stream):
  decimal_num = []
  for symbol in stream:
    if symbol == ' ':
      yield chr(int(tools.concat(decimal_num)))
      decimal_num.clear()
    else:
      decimal_num.append(symbol)
  if len(decimal_num) > 0:
    yield chr(int(tools.concat(decimal_num)))

# Second pass: Fixed-width hex ascii, concatenated
def encodeSecondPass(stream):
  for symbol in stream:
    yield from "{0:02x}".format(ord(symbol))

def decodeSecondPass(stream):
  for hex_num in tools.group(stream, 2):
    yield chr(int(tools.concat(hex_num), 16))

class Gioi1:
  
  def encode(self, stream):
    return encodeSecondPass(encodeFirstPass(stream))
  
  def decode(self, stream):
    return decodeFirstPass(decodeSecondPass(stream))
  