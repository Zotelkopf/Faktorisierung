from random import randint, lognormvariate
import math
from functions import nextprime_millerrabin


# n Anzahl Faktoren, s1 min Stellenzahl, s2 max Stellenzahl
def randomnum(n, s1, s2):
  if n >= s1:
    return 0
  s = randint(s1, s2)
  i1 = 1
  i2 = 2
  while i1 <= i2:
    exp = []
    p = []
    x = 1
    for i in range(n - 1):
      exp.append(randint(1, (s - 1) // (n - i)))
      s -= exp[i]  
    exp.append(s - 1)
    for i in range(n):
      p.append(nextprime_millerrabin(int(10 ** exp[i] * lognormvariate(1, 1))))
      x *= p[i]
    if (len(str(x)) < s1 or len(str(x)) > s2) and i2 <= 5:
      i2 += 1
  return x
