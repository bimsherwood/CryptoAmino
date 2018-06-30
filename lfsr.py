# Linear Feedback Shift Register stream
#
# This library is used to create and evaluate Linear Feedback Shift Registers.

class FeedbackShiftRegister:
  
  # Construction of an LFSR requires a seed state (an array of booleans) and a
  # linear function f taking a state into a bit (boolean). If the function is
  # not linear (i.e. the function is not the xor sum of some fixed subset of
  # state bits, or the inverse thereof) then the feedback register is not
  # linear after all.
  def __init__(self, seed, f):
    self.state = list(seed)
    self.feedback_function = f
  
  # Shift the state, yield the rightmost value, and prepend the next feedback
  # bit.
  def __iter__(self):
    while True:
      feedback = self.feedback_function(self.state)
      output = self.state.pop()
      self.state.insert(0,feedback)
      yield output

# Returns a function which takes an LFSR state (boolean array) and returns a
# feedback bit (boolean) which is the xor sum of some bits of the state. Those
# bits are called Taps. The Taps are indexed from the left, starting at *ONE*.
# 'tap_indices' is an array of indices of taps to use, and may also contain the
# zero index to negate the result of the xor sum.
def tap(tap_indices):
  
  def feedback_function(state):
    xor_sum = False
    for tap_index in tap_indices:
      if tap_index == 0:
        xor_sum ^= True
      else:
        xor_sum ^= state[tap_index - 1]
    return xor_sum
  
  return feedback_function
