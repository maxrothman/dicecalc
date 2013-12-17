"""A module for simulating dice mechanics.
Dependancies: python >=2.7"""

__author__ = 'Max Rothman'
__email__ = 'whereswalden90@gmail.com'
__version__ = '1.0'
__license__ = 'GPL v2'

from collections import Counter, Iterable
from itertools import product
from fractions import Fraction, gcd

def calculate(pool, rules=sum):
  """Calculates results of a pool given a ruleset.
  Input: pool  - an iterable of dicecalc.die objects
         rules - a function that will be applied to every result.
                 Uses sum by default.
  """
  #TODO: check validity of rules function
  rules = memoized(rules)     # Memoize rules func for performance
  results = Counter()
  for i in itertools.product(*pool):
    results[rules(i)] += 1
  return _normalize(results)

def _normalize(stuff):
  "Given a dict mapping items to counts, returns a normalized dict mapping items to decimal percentages"
  total = float(sum(stuff.values()))
  return dict([(k, v/total) for k,v in stuff.items()])

def die(*args):
  """Converts to internal representation for a die.
  Can take several different types of input:
    - Number of sides
    - Smallest side, largest side [, step]
    - Iterable of sides
    - Iterable of chances where all chances sum to 1
      Chance can be an instance of fractions.Fraction or 0<=chance<=1
      Can be either simple iterable or dict of sides -> chances
  In all cases, sides must be hashable.
  """
  #TODO: verify that sides are hashable
  #TODO: verify chances add up to 100%
  if all(isinstance(i, int) for i in args):
    if len(args)==1:
      therange = range(1, args[0]+1)     # num sides
    elif len(args) in (2, 3):
      args = list(args)
      args[1] += 1
      therange = range(*args)         # start, stop [, step]
    else:
      pass
      #TODO: throw error
     
    return {i: Fraction(1, len(therange)) for i in therange}
  
  elif len(args)==1 and isinstance(args[0], Iterable):
    thedice = args[0]
    
    if not isinstance(thedice, dict):
      thedice = dict(enumerate(thedice, 1))
    
    if all(isinstance(i, Fraction) for i in thedice.values()): 
      pass                                              # {side:Fraction, ...}
    elif all(0<=i<=1 for i in thedice.values()):
      for k,v in thedice.items():
        thedice[k] = Fraction(v).limit_denominator()    # {side: 0<x<1, ...}
    else:
      try:
        thedice = {v: Fraction(1, len(thedice)) for v in thedice.values()}    # [side, side, ...]
      except TypeError:
        pass
        #TODO: throw error
  
    return thedice

  else:
    pass
    #TODO: throw error



class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   Borrowed from <https://wiki.python.org/moin/PythonDecoratorLibrary>
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
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
