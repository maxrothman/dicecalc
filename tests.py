from dicecalc import *
from dicecalc import _normalize
from fractions import Fraction

def test_die():
  # Should pass
  assert die(6) == {i:Fraction(1,6) for i in range(1,7)}
  assert die(3, 6) == {i:Fraction(1,4) for i in range(3, 7)}
  assert die(2, 10, 2) == {i:Fraction(1,5) for i in range(2,11,2)}
  assert die(['red', 'blue', 'green']) == {i:Fraction(1,3) for i in ['red', 'blue', 'green']}
  assert die(['red', 'red', 'blue']) == {'red':Fraction(2,3), 'blue':Fraction(1,3)}
  assert die([.25, .25, .5]) == {1:Fraction(1,4), 2:Fraction(1,4), 3:Fraction(1,2)}
  assert die([Fraction(1,3), Fraction(2,3)]) == {1:Fraction(1,3), 2:Fraction(2,3)}
  assert die({'red':.25, 'blue':.75}) == {'red':Fraction(1,4), 'blue':Fraction(3,4)}
  
  # Should fail
  err = "side names must be hashable, unhashable type: 'list'"
  assertraises(TypeError(err), die, [[1,2], [3,4]])
  
  err = "die expected at most 3 int arguments, got 4"
  assertraises(TypeError(err), die, 1, 1, 1, 1)
  
  err = "die expected at most 3 int or 1 iterable arguments"
  assertraises(TypeError(err), die)
  assertraises(TypeError(err), die, 'red', 'blue')
  
  err = "die expected Fraction objects or 0<=x<=1 for values"
  assertraises(TypeError(err), die, {1:2, 3:4, 5:6})
  
  #Not yet implimented
  assertraises(ValueError, die, [Fraction(1,4), Fraction(1,4)])
  assertraises(ValueError, die, [.25, .25])

def test_normalize():
  stuff = {1:3, 2:20e10, 3:1e-20}
  assert abs(sum(_normalize(stuff).values()) - 1) <= .000001
  assert stuff.keys() == _normalize(stuff).keys()

def test_calculate():
  pass

def assertraises(exception, func, *args, **kwargs):
  try:
    func(*args, **kwargs)
  except exception:
    pass
  else:
    raise AssertionError

if __name__ == '__main__':
  test_normalize()
  test_calculate()
  test_die()
  print "Tests pass"
