from random import randrange
import math


# https://www.techiedelight.com/de/extended-euclidean-algorithm-
# implementation/
def gcdx(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = gcdx(b % a, a)
        return g, y - (b // a) * x, x


def isprime_deterministic(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    for i in range(5, math.isqrt(n) + 1, 6):
        if n % i == 0:
            return False
        if n % (i + 2) == 0:
            return False
    return True


# https://gist.github.com/Ayrx/5884790
def isprime_millerrabin(n, k=40):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def nextprime_deterministic(n):
    while True:
        n += 1
        if isprime_deterministic(n):
            return n


def nextprime_millerrabin(n):
    while True:
        n += 1
        if isprime_millerrabin(n, 20):
            return n


def issquaremodm(a, m):
    for i in range(1, m // 2):
        if (i * i) % m == a % m:
            return True
    return False


def sqrtmodm(a, m):
    for i in range(1, m // 2):
        if (i * i) % m == a % m:
            return i
    return None
