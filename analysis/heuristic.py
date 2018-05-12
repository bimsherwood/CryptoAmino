# Perform a hill climb, given:
#   fitness:    A function to calculate a state's fitness
#   mutate:     A function which randomly selects a mutation of the state
#   state:      The intial state
#   steps:      The number of steps to simulate
def hill_climb(**kwargs):
  
  fitness = kwargs['fitness']
  mutate = kwargs['mutate']
  state = kwargs['state']
  steps = kwargs['steps']
  
  state_fitness = fitness(state)
  for i in range(steps):
    attempt = mutate(state)
    attempt_fitness = fitness(attempt)
    if attempt_fitness > state_fitness:
      state = attempt
      state_fitness = attempt_fitness
  
  return state

# Perform simulated annealing (using a linear cooling schedule), given:
#   cooling:    The rate at which temperature falls
#   energy:     A function to calculate the energy of a state
#   neighbour:  A function which randomly selects a state's neighbour
#   state:      The initial state
#   steps:      The number of steps for which to simulate
#   temp:       The initial temperature
def anneal(**kwargs):
  
  cooling = kwargs['cooling']
  energy = kwargs['energy']
  neighbour = kwargs['neighbour']
  state = kwargs['state']
  steps = kwargs['steps']
  temp = kwargs['temp']
  
  def probability(energy, ref_energy):
    if temp <= 0:
      return 0
    elif energy > ref_energy:
      return math.exp((ref_energy - energy) / temp)
    else:
      return 1
  
  state_energy = energy(state)
  for i in range(steps):
    new_state = neighbour(state)
    new_state_energy = energy(new_state)
    transition_prob = probability(new_state_energy, state_energy)
    if transition_prob > random.uniform(0,1):
      state = new_state
      state_energy = new_state_energy
    temp -= cooling
  
  return state

# Perform a brute force attack, given:
#   keys:     A sequence (generator) of keys to try.
#   fitness:  A way to score a key.
def brute_force(**kwargs):
  
  keys = kwargs["keys"]
  fitness = kwargs["fitness"]
  
  best = None
  best_score = None
  for key in keys:
    score = fitness(key)
    if best_score == None or score > best_score:
      best = key
      best_score = score
  
  return best

# TODO
# Perform evolution, given:
#   proto:        The initial population
#   breed:        A function for combining members of the population
#   fitness:      A function to calculate a state's fitness
#   survival:     The number of specimens who survive each generation
#   generations:  The number of generations to run
def evolve(**kwargs):
  pass
