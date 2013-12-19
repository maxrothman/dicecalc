dicecalc
========

####Python module for simulating dice mechanics

Requirements
-----
* Python 2.7

Use
-----
There are several use examples in EXAMPLES.py. Generally, you define a "rules" function that maps an iterable of dice faces to a result, create dice via dicecalc.die(), then pass those as arguments to dicecalc.calculate(). You can then use functions such as mean, std\_dev, and at\_least to analyze the result.
