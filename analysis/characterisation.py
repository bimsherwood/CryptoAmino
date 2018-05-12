import math

# Compute the Chi-Squared statistic for the source frequency distribution (a
# symbol vs. frequency dictionary) against the reference probability
# distribution (a symbol vs. probability dictionary).
def chi_squared(src_freq, ref_dist):
  sample_size = sum(src_freq.values())
  assert sample_size > 0
  acc = 0
  for element in nub(ref_dist.keys()):
    expected_dist = ref_dist[element]
    expected_freq = expected_dist * sample_size
    assert expected_freq > 0
    actual_freq = src_freq[element] if element in src_freq else 0
    freq_difference = (actual_freq - expected_freq)
    acc += (freq_difference*freq_difference) / expected_freq
  return acc
  
# Return the quadgrams in a sequence
def quads(sequence):
  sequence = iter(sequence)
  a = next(sequence)
  b = next(sequence)
  c = next(sequence)
  while True:
    x = next(sequence)
    yield (a,b,c,x)
    a, b, c = (b, c, x)

# Accepts a quadram frequency distribution (a quadruple vs. frequency
# dictionary).
# Returns a "scorer" function, which scores sequences of symbols. Higher scores
# are given to sequences which contain more popular quadgrams.
def quadgram_scorer(quadgram_freqs):
  
  def quad_freq(quad):
    return quadgram_freqs[quad] if quad in quadgram_freqs else 1
  
  sample_size = sum(quadgram_freqs.values())
  log_sample_size = math.log(sample_size)
  def scorer(sequence):
    quad_count = 0
    sum_log_freq = 0
    for quad in quads(sequence):
      sum_log_freq += math.log(quad_freq(quad))
      quad_count += 1
    sequence_prob = sum_log_freq - log_sample_size*quad_count
    return sequence_prob/quad_count
  
  return scorer
