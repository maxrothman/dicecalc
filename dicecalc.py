"""A module for simulating dice mechanics"""
__author__ = 'Max Rothman'
__version__ = '1.0'
__email__ = 'max.r.rothman@gmail.com'
__license__ = 'GPL v2'

from collections import Counter
from itertools import product

def calculate(pool, rules=rules):
  """Calculates results of a pool given a ruleset.
  Input: pool - an iterable of dicecalc.die objects
         rules - an option function that will be applied to every result
  """
  #TODO: check validity of rules function
  if not rules: rules = lambda x: x
  results = Counter()
  for i in itertools.product(*pool):
    results[i] += rules(i)
  return dict(results)
