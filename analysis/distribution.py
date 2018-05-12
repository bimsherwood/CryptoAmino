# Find the frequency distribution of the elements in a sequence.
def freq(sequence):
  frequencies = {}
  for element in sequence:
    if element in frequencies:
      frequencies[element] += 1
    else:
      frequencies[element] = 1
  return frequencies

# Find the probability distribution for a frequency distribution.
def dist(freq):
  sample_size = sum(f for f in freq.values())
  return {element: f/sample_size
    for (element, f)
    in freq.items()}

# Find the best substitution (a dictionary, mapping input symbols to output
# symbols) for changing sequences with the source distribution into sequences
# with the target distribution.
# Programmed with frequency distributions in mind, but probability
# distributions should work just as well.
def distribution_switch(source_dist, target_dist):
  
  source_sorted_freqs = sorted(
    source_dist.items(),
    key = lambda frequency: frequency[1])
  source_order_by_freq = [element
    for (element, frequency) in source_sorted_freqs]
  
  target_sorted_freqs = sorted(
    target_dist.items(),
    key = lambda frequency: frequency[1])
  target_order_by_freq = [element
    for (element, frequency) in target_sorted_freqs]
  
  return {i_elem: t_elem for (i_elem, t_elem) in zip(
    source_order_by_freq,
    target_order_by_freq)}