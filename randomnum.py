from random import randint, normalvariate
import math
from functions import next_prime


# n Anzahl Faktoren, s1 min Stellenzahl, s2 max Stellenzahl
def randomnum(n, s1, s2):
  if n < s1:
    return 0
  exp = []
  p = []
  x = 1
  s = randint(s1, s2)
  for i in range(n - 1):
    exp.append()
  

  
  for i in range(n):
    p.append(normalvariate(10 ** exp[i]))
    x *= p[i]
  return x
