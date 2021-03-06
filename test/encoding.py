from cryptoamino import tools
from cryptoamino.encoding import *

encodings = [
  
  # G.I.O.I. 1 encoding
  (gioi1.Gioi1(), "Some ascii text will do it!")
  
]

for codec, sample in encodings:
  encoded = list(codec.encode(sample))
  print("{0} -> {1}".format(sample, tools.concat(encoded)))
  sample2 = tools.concat(codec.decode(encoded))
  if list(sample2) != list(sample):
    raise Exception(
      "Encoding failed: sample {0} was decoded to {1}".format(
        sample,
        sample2))
