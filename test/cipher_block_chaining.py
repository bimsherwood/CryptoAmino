
from cryptoamino.cipher.cipher_block_chaining import CipherBlockChaining
from cryptoamino.cipher.globby_block import GlobbyBlock

class NullCipher:
  
  def key(self, key):
    pass
  
  def encrypt(self, stream):
    return stream
  
  def decrypt(self, stream):
    return stream

block_size = 4
iv = bytearray(block_size)
null_cbc = CipherBlockChaining(block_size, NullCipher())

# Example encryptions

examples = [
  (bytearray([0,0,0,0,0]), bytearray([0,0,0,0,0,3,3,3])),
  (bytearray([0,0,0,0,0,0]), bytearray([0,0,0,0,0,0,2,2])),
  (bytearray([]), bytearray([4,4,4,4])),
  (bytearray([1,1,1,1]), bytearray([1,1,1,1,5,5,5,5])),
  (bytearray([1,1,1,1,1,1,1,1]), bytearray([1,1,1,1,0,0,0,0,4,4,4,4]))]

for ptxt, ctxt in examples:
  null_cbc.key((None, iv))
  ctxt_got = bytearray(null_cbc.encrypt(ptxt))
  if ctxt != ctxt_got:
    print(ptxt)
    print(ctxt)
    print(ctxt_got)
    raise Exception("Encryption failed")

# Trial decryptions

for ptxt_original, _ in examples:
  null_cbc.key((None, iv))
  ctxt = bytearray(null_cbc.encrypt(ptxt_original))
  ptxt_decrypted = bytearray(null_cbc.decrypt(ctxt))
  if ptxt_original != ptxt_decrypted:
    print(ptxt_original)
    print(ctxt)
    print(ptxt_decrypted)
    raise Exception("Decryption failed")

globby_block_cbc = CipherBlockChaining(32, GlobbyBlock())
globby_key = bytearray(32)
globby_key[10] = 1
globby_iv = bytearray(32)
for ptxt_original, _ in examples:
  globby_block_cbc.key((globby_key, globby_iv))
  ctxt = bytearray(globby_block_cbc.encrypt(ptxt_original))
  ptxt_decrypted = bytearray(globby_block_cbc.decrypt(ctxt))
  if ptxt_original != ptxt_decrypted:
    print(ptxt_original)
    print(ctxt)
    print(ptxt_decrypted)
    raise Exception("Decryption failed")
