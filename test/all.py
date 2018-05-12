try:
  import cryptoamino.test.ciphers
  import cryptoamino.test.heuristic
  print("All tests passed.")
except Exception as ex:
  print("Test failed: {0}: {1}".format(type(ex), ex))
  raise
