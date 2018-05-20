try:
  print("> Cipher tests:")
  import cryptoamino.test.ciphers
  print("> Heuristic tests:")
  import cryptoamino.test.heuristic
  print("> Characterisation tests:")
  import cryptoamino.test.characterisation
  print("> Polyalphabetic analysis tests:")
  import cryptoamino.test.polyalphabetic_analysis
  print("> All tests passed.")
except Exception as ex:
  print("> Test failed: {0}: {1}".format(type(ex), ex))
  raise
