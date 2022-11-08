from random import randint
import math


# n Anzahl Faktoren, s1 min Stellenzahl, s2 max Stellenzahl
def randomnum(n, s1, s2):
  exp = []
  exp.append(randint(s1, s2))
  for i in range(n - 1):
    exp.append()
  
