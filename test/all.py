try:
  print("> Cipher tests:")
  import cryptoamino.test.ciphers
  print("> Encoding tests:")
  import cryptoamino.test.encoding
  print("> Heuristic tests:")
  import cryptoamino.test.heuristic
  print("> Characterisation tests:")
  import cryptoamino.test.characterisation
  print("> Polyalphabetic analysis tests:")
  import cryptoamino.test.polyalphabetic_analysis
  print("> Cipher Block Chaining tests:")
  import cryptoamino.test.cipher_block_chaining
  print("> All tests passed.")
except Exception as ex:
  print("> Test failed: {0}: {1}".format(type(ex), ex))
  raise
