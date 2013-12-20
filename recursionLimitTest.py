class c:
  x=0
  def __init__(self):
    self.rlimit = 5
  def fun(self):
    self.x+=1
    print self.x
    if self.x >= self.rlimit: return
    else: self.fun()

#variables refresh on import
lim = 5
y=0
def funn():
  print self.y
  test.y+=1
  if test.y >= test.lim: return
  else: funn()

#sets global recursion limit, not recursion limit for this function
import inspect
def funnn(maxdepth):
  zero = len(inspect.stack())
  if zero > maxdepth:
    return
  else:
    print zero
    funnn(maxdepth)

global rlim; rlim=None
global lvl; lvl=None
def hi(lim):
  global rlim, lvl
  if rlim==None: rlim = lim
  if lvl==None: lvl = 0
  print lvl
  if lvl >= rlim: 
    rlim=lvl=None
    return
  else: 
    lvl += 1
    hi(3)
