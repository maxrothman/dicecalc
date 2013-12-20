# Examples for dicecalc.py

import dicecalc

# 4d6
four_d6 = dicecalc.calculate( [dicecalc.die(6)]*4 )


# 2d8 + 1d6
two_d8_one_d6 = dicecalc.calculate( [dicecalc.die(8)]*2 + [dicecalc.die(6)] )


# White Wolf 4d10 (success >= 8)

# You could do it like this:
def rules_whitewolf(pool):
  return len([i for i in pool if i>=8])

whitewolf_try1 = dicecalc.calculate( [dicecalc.die(10)]*4 , rules_whitewolf )

# But this would run much faster:
whitewolf_try2 = dicecalc.calculate( [dicecalc.die({0: 0.7, 1: 0.3})]*4 )

# If you wanted to analyze the same rules for d6, you'd have to do this:
from fractions import Fraction
other_success_based_system = dicecalc.calculate( [dicecalc.die([Fraction(2,6), Fraction(4,6)])] )
# Otherwise, you'll get a ValueError("total chance for all sides must sum to 1")
# because of floating point accuracy issues

# Fudge dice:
fudge = dicecalc.calculate( [dicecalc.die([-1, -1, 0, 0, 1, 1])]*4 )


# One Roll Engine 4d6
def rules_ore(pool):
  return max(pool.count(i) for i in set(pool))

ore = dicecalc.calculate( [dicecalc.die(6)]*4, rules_ore )


# Zombie Dice
green = dicecalc.die(['brain']*3 + ['shotgun'] + ['runner']*2)
yellow = dicecalc.die(['brain']*2 + ['shotgun']*2 + ['runner']*2)
red = dicecalc.die(['brain']*1 + ['shotgun']*3 + ['runner']*2)
def zombie_dice_rules(pool):
  return pool.count('brain') if 'shotgun' not in pool else 0

zombie_dice = dicecalc.calculate([red, yellow, green], zombie_dice_rules)


# Analysis (on White Wolf 4d10)
mean = dicecalc.mean(whitewolf_try2)
standard_deviation = dicecalc.std_dev(whitewolf_try2)
at_least_1_success = dicecalc.at_least(1, whitewolf_try2)
at_most_0_successes = dicecalc.at_most(0, whitewolf_try2)


#def graph(results):
#  for k in sorted(results.keys()):
#    print k, "#"*(int(round(results[k]*100)))
#
#print "\n  4d6"
#graph(four_d6)
#print "\n  2d8+1d6"
#graph(two_d8_one_d6)
#print "\n  4d10 whitewolf try1"
#graph(whitewolf_try1)
#print "\n  4d10 whitewolf try2"
#graph(whitewolf_try2)
#print "\n  fudge"
#graph(fudge)
#print "\n  ore"
#graph(ore)
#print "\n  zombie"
#graph(zombie_dice)
