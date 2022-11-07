from random import randint, randrange
import math
from datetime import datetime


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


def ideal_reduce(idealin, d):
    idealout = idealin[:]
    while True:
        idealout[1] %= (2 * idealout[0])
        if idealout[1] > idealout[0]:
            idealout[1] -= 2 * idealout[0]
        c = (idealout[1] * idealout[1] + d) // (4 * idealout[0])
        if idealout[0] <= c:
            if idealout[0] == c and idealout[1] < 0:
                idealout[1] *= -1
            return idealout
        idealout[0] = c
        idealout[1] *= -1


def ideal_generate(a, d):
    if a <= 2:
        a = 3
    p = nextprime_deterministic(a)
    while not issquaremodm(-d, p):
        p = nextprime_deterministic(p + 1)
    b = sqrtmodm(-d, p)
    if d % 2 != b % 2:
        b = p - b
    return ideal_reduce([p, b], d)


def ideal_unit(d):
    if (d % 4) == 0:
        return [1, 0]
    else:
        return [1, 1]


def ideal_inverse(idealin, d):
    idealout = [idealin[0], idealin[1] * -1]
    return ideal_reduce(idealout, d)


def ideal_multi(idealin1, idealin2, d):
    g, u1, u2 = gcdx(idealin1[0], idealin2[0])
    if g == 1:
        idealout = [idealin1[0] * idealin2[0], idealin2[1] + u2 * 
                    idealin2[0] * (idealin1[1] - idealin2[1])]
    else:
        g, v1, v2 = gcdx(g, (idealin1[1] + idealin2[1]) // 2)
        idealout = [(idealin1[0] * idealin2[0]) // g ** 2,
                    idealin2[1] + v1 * u2 * (idealin2[0] // g) * 
                    (idealin1[1] - idealin2[1]) - v2 *
                    ((idealin2[1] * idealin2[1] + d) // (2 * g))]
    return ideal_reduce(idealout, d)


def ideal_square(idealin, d):
    g, u1, u2 = gcdx(idealin[0], idealin[1])
    idealout = [(idealin[0] // g) ** 2, idealin[1] - u2 *
                ((idealin[1] * idealin[1] + d) // (2 * g))]
    return ideal_reduce(idealout, d)


def ideal_power(idealin, n, d):
    idealout = idealin[:]
    if n == 0:
        return ideal_unit(d)
    n2 = format(n, "b")
    for i in range(1, len(n2)):
        idealout = ideal_square(idealout, d)
        print("s", end="")
        if n2[i] == "1":
            idealout = ideal_multi(idealout, idealin, d)
            print("m", end="")
    return idealout


def ideal_squaretoamb(idealin, d):
    ideal0 = ideal_unit(d)
    ideal1 = idealin[:]
    for i in range(d.bit_length() // 2):
        ideal2 = ideal_square(ideal1, d)
        print(ideal1)
        if ideal2 == ideal0:
            print("found with exponent 2^" + str(i))
            return ideal1
        ideal1 = ideal2
    return ideal1


def poexpo(a, b):
    x = 1
    for i in range(math.isqrt(a) + 1, math.isqrt(b)):
        x *= 2 * abs(i) + 1
    if (a % 2) == 1:
        a += 1
    for i in range(a + 1, b, 2):
        if isprime_deterministic(abs(i)):
            x *= i
    return x


def rwinit(idealin, bound, s, ideals, expo, d):
    for i in range(s):
        expo.append(randint(0, bound))
        ideals.append(ideal_power(idealin, expo[i], d))


def rwalk(idealin, n, d):
    ideals = []
    expo = []
    ideal1 = idealin[:]
    ideal2 = idealin[:]
    p = 8191
    s = 16
    t1 = 1
    t2 = 1
    rwinit(idealin, n * n, s, ideals, expo, d)
    for k in range(n):
        g = ((ideal1[1] * ideal1[1]) % p) % s
        t1 += expo[g]
        ideal1 = ideal_multi(ideal1, ideals[g], d)
        for j in range(2):
            g = ((ideal2[1] * ideal2[1]) % p) % s
            t2 += expo[g]
            ideal2 = ideal_multi(ideal2, ideals[g], d)
        if ideal1 == ideal2:
            return t2 - t1
    return 0


def factorizealg0(s, x, pbound):
    d = s * x
    h = poexpo(1, pbound)
    i1 = 1
    i2 = 1
    while i1 <= i2:
        i1 += 1
        print(".", end="")
        ideal1 = ideal_generate(randint(3, 64000), d)
        ideal2 = ideal_power(ideal1, h, d)
        ideal3 = ideal_squaretoamb(ideal2, d)
        if ideal3 != ideal_inverse(ideal3, d):
            print(":", end="")
            t = rwalk(ideal3, pbound, d)
            if t > 0:
                print(";", end="")
                while (t % 2) == 0:
                    t //= 2
                print("(" + str(t) + ")", end="")
                ideal2 = ideal_power(ideal2, t, d)
                ideal3 = ideal_squaretoamb(ideal2, d)
        if ideal3 == ideal_inverse(ideal3, d):
            print("!" + str(ideal3), end="")
            i2 = 8
            f = 2 * ideal3[0] - ideal3[1]
            f = gcdx(x, f)[0]
            if f > 1:
                return f
    return 0


def factorizealg(x, pbound, n):
    if (x % 2) == 0:
        return 2
    s = (x + 2) % 4
    for i in range(n):
        if s > 1 and (x % s) == 0:
            return s
        a = factorizealg0(s, x, pbound)
        if a > 1:
            return a
        s += 4
        while not isprime_deterministic(s):
            s += 4
    return 0


def factorize(x, pbound=-1, n=-1):
    tstart = datetime.now()
    switcher = {
        0: [int(12000 * math.e ** (0.05 * (len(str(x)) - 50)) +
                7000), 100],
        1: [int(10000 * math.e ** (0.025 * (len(str(x)) - 30)) +
                5000), 100],
        2: [int(20000 * math.e ** (0.05 * (len(str(x)) - 40)) +
                10000), 50],
        3: [int(10000 * math.e ** (0.025 * (len(str(x)) - 30)) +
                5000), 300],
        4: [int(20000 * math.e ** (0.05 * (len(str(x)) - 40)) +
                10000), 200],
    }
    for i in range(5):
        a = x
        b = 1
        factors = []
        count = 0
        tnow = str(datetime.now() - tstart)
        if int(tnow[0]) >= 1:
            print("!")
            break
        if pbound < 0:
            pbound = switcher.get(i)[0]
        if n < 0:
            n = switcher.get(i)[1]
        while not isprime_millerrabin(x):
            print(i + 1, "(", end="")
            factors.append(factorizealg(x, pbound, n))
            print(") ", end="")
            if factors[count] == 0:
                factors.pop(-1)
                break
            x //= factors[count]
            count += 1
        factors.append(x)
        factors.sort()
        count += 1
        for j in range(count):
            b *= factors[j]
        if a == b:
            for j in range(count):
                if isprime_millerrabin(factors[j]):
                    tnow = str(datetime.now() - tstart)
                    return "No Error", factors, tnow
    tnow = str(datetime.now() - tstart)
    return "Error #1", "factors not computable", tnow
