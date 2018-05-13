# Polyalphabetic cipher analysis

from cryptoamino.analysis import characterisation

# For substitutions that change periodically: Sort the periods from most to
# least likely; most likely being those periods which produce the least uniform
# symbol distribution.
def likely_substitution_periods(sequence, min_period, max_period):
  symbols = list(sequence)
  period_scores = {} # Period vs. score dict
  for period in range(min_period, max_period + 1):
    subsequences = [symbols[offset::period] for offset in range(period)]
    scores = [
      characterisation.index_of_coincidence(seq)
      for seq in subsequences]
    score = sum(scores)/len(scores)
    period_scores[period] = score
  likely_period_scores = sorted(period_scores.items(), key=lambda ps : -ps[1])
  likely_periods = [period for period, score in likely_period_scores]
  return likely_periods
  