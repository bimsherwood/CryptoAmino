# Testing of characterisation tools

from cryptoamino.analysis import characterisation

examples = [
  ("aaaaaaaa", 1.0000),
  ("whatawonderfulworld", 0.0468)
]
for text, ioc_expected in examples:
  ioc = characterisation.index_of_coincidence(text)
  print('IoC is {0:.4f} for "{1}"'.format(ioc, text))
  if abs(ioc - ioc_expected) > 1e-4:
    raise Exception("Index of Coincidence calculation failed")
