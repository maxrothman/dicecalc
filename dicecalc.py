"""A module for simulating dice mechanics.
Dependancies: python >=2.7"""

__author__ = 'Max Rothman'
__email__ = 'whereswalden90@gmail.com'
__version__ = '1.0'
__license__ = 'GPL v2'

from collections import Counter, defaultdict, Iterable, Sequence, Hashable
from fractions import Fraction
import itertools
import operator
import math


def calculate(pool, rules=sum, fractions=False):
  """Calculates results of a pool given a ruleset.
  Input: pool      - an iterable of the die representation returned by dicecalc.die()
         rules     - a function that takes as input an iterable of side names and returns 
                     some result. Will be applied to every combination of sides.
                     Uses sum by default.
         fractions - if True, returns fractions.Fraction objects instead of floats.
                     False by default.
  """
  #TODO: check validity of rules function
  rules = _memoized(rules)     # Memoize rules func for performance
  #results = Counter()
  results = defaultdict(lambda: 0)
  for comb in itertools.product(*pool):
    results[rules(comb)] += reduce(operator.mul, (pool[i][comb[i]] for i in range(len(comb))))
  if not fractions: results = {k:float(v) for k,v in results.items()}
  return dict(results)


#def _normalize(stuff):
#  # NOT USED
#  "Given a dict mapping items to counts, returns a normalized dict mapping items to decimal percentages"
#  total = float(sum(stuff.values()))
#  return dict([(k, v/total) for k,v in stuff.items()])


def die(*args):
  """Converts input to internal representation for a die.
  Can take several different types of input:
    - Number of sides
    - Smallest side, largest side [, step]
    - Iterable of sides
    - Iterable of chances where all chances sum to 1
      Chance can be an instance of fractions.Fraction or 0<=chance<=1
      Can be either simple iterable or dict of sides -> chances
  In all cases, sides must be hashable.
  """
  if args and all(isinstance(i, int) for i in args):    # all() returns true if there are no args
    if len(args)==1:
      therange = range(1, args[0]+1)     # num sides
    elif len(args) in (2, 3):
      args = list(args)
      args[1] += 1
      therange = range(*args)         # start, stop [, step]
    else:
      raise TypeError("die expected at most 3 int arguments, got " + str(len(args)))
     
    return {i: Fraction(1, len(therange)) for i in therange}
  
  elif len(args)==1 and isinstance(args[0], Iterable):
    thedice = args[0]
    
    if isinstance(thedice, Sequence):
      if all(isinstance(i, Fraction) for i in thedice) or all(0<=i<=1 for i in thedice):
        thedice = dict(enumerate(thedice, 1))   # sequence of chances, prep for dict block
      else:                                     # sequence of side names
        try:
          thedice = Counter(args[0])
          return {k: Fraction(v, len(args[0])) for k,v in thedice.items()}
        except TypeError as e:
          raise TypeError("side names must be hashable, " + e.message)

    if isinstance(thedice, dict):
      if all(isinstance(i, Fraction) for i in thedice.values()):   # {side:Fraction, ...}
        pass
      elif all(0<=i<=1 for i in thedice.values()):                 # {side: 0<x<1, ...}
        for k,v in thedice.items():
          thedice[k] = Fraction(v).limit_denominator()
      else:
        raise TypeError("die expected Fraction objects or 0<=x<=1 for values")

      if sum(thedice.values()) != 1:
        raise ValueError("total chance for all sides must sum to 1")

      return thedice
  
  else:
    raise TypeError("die expected at most 3 int or 1 iterable arguments")


def median(results):
  "Return the median of the given distribution"
  return (max(results) - min(results))/2.0

def mean(results):
  "Return the mean of the given distribution"
  return float(sum(k*v for k,v in results.items()))

def mode(results):
  "Return the mode of the given distribution"
  return max(results, key=lambda x: results[x])

def std_dev(results):
  "Return the standard deviation of the given distribution"
  u = mean(results)
  return math.sqrt(sum((k-u)**2 * v for k,v in results.items()))

def at_least(x, results):
  "Return the probability of getting at least the result x"
  return float(sum(v for k,v in results.items() if k>=x))

def at_most(x, results):
  "Return the probability of getting at most the result x"
  return float(sum(v for k,v in results.items() if k<=x))


class _memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   Borrowed from <https://wiki.python.org/moin/PythonDecoratorLibrary>
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)
