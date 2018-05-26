from cryptoamino import tools
from cryptoamino.encoding import *

  #
  # Text-based encodings
  #

text_encodings = [
  
  (gioi1.Gioi1(), "Some ascii text will do it!")
  
]

for codec, sample in text_encodings:
  encoded = list(codec.encode(sample))
  print("{0} -> {1}".format(sample, tools.concat(encoded)))
  sample2 = tools.concat(codec.decode(encoded))
  if list(sample2) != list(sample):
    raise Exception(
      "Encoding failed: sample {0} was decoded to {1}".format(
        sample,
        sample2))

  #
  # The FileSystem encoding
  #

files = [b'File 1!', b'File2', None, b'File3'] + [None]*12
fs = filesystem.FileSystem()
image = fs.encode(files)
print("Testing filesystem encoding...")
decoded = list(fs.decode(image))
if decoded != files:
    raise Exception(
      "Encoding failed: sample {0} was decoded to {1}".format(
        files,
        list(map(str, decoded))))
