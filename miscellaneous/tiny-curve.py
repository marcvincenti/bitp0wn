#!/usr/bin/env python

import random

""" modular inverse """
def inv(a, n):
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high//low
        nm, new = hm-lm*r, high-low*r
        lm, low, hm, high = nm, new, lm, low
    return lm % n

""" Jacobian """
def to_jacobian(p):
    o = (p[0], p[1], 1)
    return o

def from_jacobian(p, P):
    z = inv(p[2], P)
    return ((p[0] * z**2) % P, (p[1] * z**3) % P)

def jacobian_double(p, P):
    if not p[1]:
        return (0, 0, 0)
    ysq = (p[1] ** 2) % P
    S = (4 * p[0] * ysq) % P
    M = (3 * p[0] ** 2 + A * p[2] ** 4) % P
    nx = (M**2 - 2 * S) % P
    ny = (M * (S - nx) - 8 * ysq ** 2) % P
    nz = (2 * p[1] * p[2]) % P
    return (nx, ny, nz)

def jacobian_add(p, q, P):
    if not p[1]:
        return q
    if not q[1]:
        return p
    U1 = (p[0] * q[2] ** 2) % P
    U2 = (q[0] * p[2] ** 2) % P
    S1 = (p[1] * q[2] ** 3) % P
    S2 = (q[1] * p[2] ** 3) % P
    if U1 == U2:
        if S1 != S2:
            return (0, 0, 1)
        return jacobian_double(p, P)
    H = U2 - U1
    R = S2 - S1
    H2 = (H * H) % P
    H3 = (H * H2) % P
    U1H2 = (U1 * H2) % P
    nx = (R ** 2 - H3 - 2 * U1H2) % P
    ny = (R * (U1H2 - nx) - S1 * H3) % P
    nz = (H * p[2] * q[2]) % P
    return (nx, ny, nz)

def jacobian_multiply(a, n, P):
    if a[1] == 0 or n == 0:
        return (0, 0, 1)
    if n == 1:
        return a
    if (n % 2) == 0:
        return jacobian_double(jacobian_multiply(a, n//2, P), P)
    if (n % 2) == 1:
        return jacobian_add(jacobian_double(jacobian_multiply(a, n//2, P), P), a, P)

""" Elliptic curve functions """
def fast_add(a, b, P):
    return from_jacobian(jacobian_add(to_jacobian(a), to_jacobian(b), P), P)

def fast_substract((x1, y1), (x2, y2), P):
    return fast_add((x1, y1), (x2, -y2), P)

def fast_multiply(a, n, P):
    return from_jacobian(jacobian_multiply(to_jacobian(a), n, P), P)

""" Legendre symbol
Compute Legendre symbol (a|p) using Euler's criterion.
p is a prime, a is relatively prime to p (if p divides a, then a|p = 0)
Returns 1 if a has a square root modulo p, -1 otherwise.
"""
def legendre_symbol(a, p):
    ls = pow(a, (p - 1) / 2, p)
    return -1 if ls == p - 1 else ls

""" Tonelli-Shanks algorithm
Find a square root of n modulo p.
Solve for r in a congruence of the form r^2 = n (mod p), where p is a prime
"""
def tonnelli_shanks(a, p):
    # Partition p-1 to s * 2^e for an odd s (i.e. reduce all the powers of 2 from p-1)
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1
    # Find some 'n' with a legendre symbol n|p = -1.
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    # x is a guess of the square root that gets better with each iteration.
    # b is the "fudge factor" - by how much we're off with the guess.
    # The invariant x^2 = ab (mod p) is maintained throughout the loop.
    # g is used for successive powers of n to update both a and b
    # r is the exponent - decreases with each update
    x = pow(a, (s + 1) / 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    while True:
        t = b
        m = 0
        for m in xrange(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

""" Newton's method to compute sqrt """
def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

""" Deterministic variant of the Miller-Rabin primality test
See http://miller-rabin.appspot.com/ for more informations
"""
def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True # n  is definitely composite

def is_prime(n, _precision_for_huge_n=40):
    if n in _known_primes:
        return True
    if any((n % p) == 0 for p in _known_primes) or n in (0, 1):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653:
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467:
        if n == 3215031751:
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s) for a in _known_primes[:_precision_for_huge_n])

_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if is_prime(x)]

""" Prime generation """
def generate_prime(nbits=1024):
    p = random.getrandbits(nbits)
    while p < 2**(nbits-1) or not is_prime(p, 20):
        p = random.getrandbits(nbits)
    return p

""" Curve generation
Generate a curve defined over a Weierstrass function
"""

# Generate P
P = generate_prime(32)
print("P = {0}".format(P))
# Generate A & B
while True:
    A = random.randint(0, P)
    B = random.randint(0, P)
    if (4*A*A*A + 27*B*B) % P != 0:
        break;
print("A = {0}, B = {1}".format(A, B))
while True:
    # Generate G, a random point on the curve
    while True:
        x = random.randint(0, P)
        xcubedaxb = (x*x*x+A*x+B) % P
        if legendre_symbol(xcubedaxb, P) == 1:
            if P % 4 == 3:
                y = int(pow(xcubedaxb, (P+1)//4, P))
            else:
                y = int(tonnelli_shanks(xcubedaxb, P))
            assert (y**2 - xcubedaxb) % P == 0
            G = (x, y)
            break;
    # Calculate order N from Hasse theorem and bsgs algorithm
    sqrt_p = isqrt(P)
    min_m, max_m = P + 1 - 2 * sqrt_p, P + 1 + 2 * sqrt_p
    steps = isqrt(max_m - min_m)
    m_candidates = []
    O = (0, 0)
    baby_steps = {}
    for x in range(steps):
        baby_steps[O] = x
        O = fast_add(O, G, P)
    O = fast_multiply(G, min_m, P)
    O_ADDER = fast_multiply(G, steps, P)
    for factor_giant in range(steps):
        substract_res = fast_substract((0,0), O, P)
        if substract_res in baby_steps:
            factor_baby = baby_steps[substract_res]
            m_candidates.append((factor_giant * steps) + factor_baby + min_m)
        O = fast_add(O, O_ADDER, P)
    if len(m_candidates) == 1:
        print("G = {0}".format(G))
        print("N = {0}".format(m_candidates[0]))
        break;
