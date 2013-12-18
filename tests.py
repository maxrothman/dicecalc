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
  assertraises(TypeError, err, die, [[1,2], [3,4]])
  
  err = "die expected at most 3 int arguments, got 4"
  assertraises(TypeError, err, die, 1, 1, 1, 1)
  
  err = "die expected at most 3 int or 1 iterable arguments"
  assertraises(TypeError, err, die)
  assertraises(TypeError, err, die, 'red', 'blue')
  
  err = "die expected Fraction objects or 0<=x<=1 for values"
  assertraises(TypeError, err, die, {1:2, 3:4, 5:6})
  
  err = "total chance for all sides must sum to 1"
  assertraises(ValueError, err, die, [Fraction(1,4), Fraction(1,4)])
  assertraises(ValueError, err, die, [.25, .25])

#def test_normalize():
#  stuff = {1:3, 2:20e10, 3:1e-20}
#  assert abs(sum(_normalize(stuff).values()) - 1) <= .000001
#  assert stuff.keys() == _normalize(stuff).keys()

def test_analyses():
  pool = [die(4)]*2
  results = calculate(pool)
  assert mean(results) == 5.0
  assert median(results) == 3.0
  assert mode(results) == 5
  assert abs(std_dev(results)) - 1.58 < 1e2
  
  atleast = [None, None, 100.0, 93.75, 81.25, 62.4, 37.5, 18.75, 6.25]
  for k in results:
    assert abs(at_least(k, results) - atleast[k]) < 1e2

  atmost = [None, None, 6.25, 18.75, 37.5, 62.4, 81.25, 93.75, 100.0]
  for k in results:
    assert abs(at_most(k, results) - atmost[k]) < 1e2


def test_calculate():
  # (pool, rules, expected_result)
  pools = [
           ([die(4)]*2, None, {2:.0625, 3:.125, 4:.1875, 5:.25, 6:.1875, 7:.125, 8:.0625}),  #2d4
           ([die({0:.7, 1:.3})]*3, lambda x: x.count(1), {0:.343, 1:.441, 2:.189, 3:.027}),   #3 whitewolf d10
           ([die(8)]*4, lambda x: max(x.count(i) for i in x), {1:.4102, 2:.5332, 3:.0547, 4:.002})  #2 ORE d8
          ]
  for pool, rules, expected_result in pools:
    result = calculate(pool, rules) if rules else calculate(pool)
    result = {k:float(v) for k,v in result.items()}
    try:
      assert all(abs(result[k] - expected_result[k]) < 1e-4 for k in result)
    except AssertionError:
      print "Pool: " + str(pool)
      print "Expected: " + str(expected_result)
      print "Got:      " + str(result)
      raise

####################################################
def assertraises(exception, msg, func, *args, **kwargs):
  try:
    func(*args, **kwargs)
  except exception as e:
    if e.message == msg:
      pass
    else:
      raise AssertionError("Incorrect error message: expected '"+msg+"', got '"+e.message+"'")
  else:
    raise AssertionError("No error raised")

if __name__ == '__main__':
  #  test_normalize()
  test_calculate()
  test_die()
  test_analyses()
  print "Tests pass"
