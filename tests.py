import dicecalc

def test_normalize():
  stuff = {1:3, 2:20e10, 3:1e-20}
  assert abs(sum(dicecalc._normalize(stuff).values()) - 1) <= .000001
  assert stuff.keys() == dicecalc._normalize(stuff).keys()

def test_calculate():
  pass

if __name__ == '__main__':
  test_normalize()
  test_calculate()
  print "Tests pass"
