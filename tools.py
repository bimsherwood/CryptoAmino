# A collection of tools for performing routine operations. Intended to make
# personal scripts and interactive Python sessions briefer.

  #
  # Letters/number Conversion and Arithmetic
  #

letters = "abcdefghijklmnopqrstuvwxyz"
assert len(letters) == 26
tabulaRecta = {letters[x]: x for x in range(0, 26)}

# For adding both letters and numbers to letters, using a Tabula Recta and
# letter index.
# The Tabula Recta is a dictionary for mapping (lowercase) letters to numbers,
# and the letter index is a dictionary (or array) for mapping numbers to
# letters.
def add(a, b, tabulaRecta=tabulaRecta, letters=letters):
  aNum = tabulaRecta[a.lower()] if type(a) is str else a
  bNum = tabulaRecta[b.lower()] if type(b) is str else b
  return letters[(aNum + bNum)%26]

def subtract(a, b, tabulaRecta=tabulaRecta, letters=letters):
  aNum = tabulaRecta[a.lower()] if type(a) is str else a
  bNum = tabulaRecta[b.lower()] if type(b) is str else b
  return letters[(aNum - bNum) % 26]

  #
  # Operations with Sequences
  #

# For applying a function to the corresponding entries of lists
def zipWith(f, *streams):
  inputs = list(map(collections.deque, streams))
  results = collections.deque()
  while True:
    heads = []
    for inputQueue in inputs:
      if len(inputQueue) == 0:
        return results
      heads.append(inputQueue.popleft())
    results.append(f(*heads))

# For breaking a sequence into fixed-size groups
def group(stream, size):
  group = []
  for symbol in stream:
    group.append(symbol)
    if len(group) >= size:
      yield group
      group = []
  if len(group) > 0:
    yield group

# Maintains ordering, unlike list(set(...))
def nub(lst):
  result = []
  for entry in lst:
    if not entry in result:
      result.append(entry)
  return result

def concat(strs):
  return ''.join(strs)

def flatten(lst):
  return [elem for sublist in lst for elem in sublist]

# A rectangular array of symbols
class Matrix:
  
  def __init__(self, rows, cols):
    self.row_count = rows
    self.col_count = cols
    self.height = rows
    self.width = cols
    self.rows = [
      [(row, col)
       for col in range(cols)]
        for row in range(rows)]
  
  def __getitem__(self, index):
    return self.rows[index[0]][index[1]];
  
  def __setitem__(self, index, value):
    self.rows[index[0]][index[1]] = value;
    
  # Sequence is Row Major
  def __iter__(self):
    elems = []
    for row in self.rows:
      elems.extend(row)
    return elems.__iter__()
  
  def __eq__(self, other):
    return self.row_count == other.row_count and list(self) == list(other)
  
  def __repr__(self):
    return repr(self.rows)
  
  def __str__(self):
    cell_size = max(map(lambda cell : len(str(cell)), self))
    def cell_str(elem): # Stringifies and pads a value
      return "{message: >{cell_size}}".format(
        message=str(elem),
        cell_size=cell_size)
    elems_str = [[cell_str(cell) for cell in row] for row in self.rows]
    return "\n".join(
      [", ".join(row_str) for row_str in elems_str])
  
  def fmap(self, f):
    for row in range(self.rows):
      for col in range(self.cols):
        self.rows[row][col] = f(self.rows[row][col])
  
  def transposed(self):
    m = Matrix(self.col_count, self.row_count)
    for x in range(self.width):
      for y in range(self.height):
        m.rows[x][y] = self.rows[y][x]
    return m
  
  def columns(self):
    columns = []
    for c in range(self.col_count):
      column = []
      for r in range(self.row_count):
        column.append(self.rows[r][c])
      columns.append(column)
    return columns

  #
  # Notations
  #

def fromBin(x):
  return int(x, 2)

def fromOct(x):
  return int(x, 2)

def fromHex(x):
  return int(x, 16)

def concat(lines):
  return ''.join(lines)

def normalise_text(x):
  return concat(filter(lambda char : char in letters, x.lower()))

def printlist(x):
  print(list(x))
  
  #
  # Other
  #

def indexer(indexed):
  return lambda i : indexed[i]

def substitutor(substitution):
  return (lambda x :
    substitution[x] if x in substitution else x)
