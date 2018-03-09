#!/usr/bin/env python

from bitcoin import G, N, P, fast_multiply, inv
import random

def modular_sqrt(a, p):
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) / 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
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


def legendre_symbol(a, p):
    """ Compute the Legendre symbol a|p using
        Euler's criterion. p is a prime, a is
        relatively prime to p (if p divides
        a, then a|p = 0)

        Returns 1 if a has a square root modulo
        p, -1 otherwise.
    """
    ls = pow(a, (p - 1) / 2, p)
    return -1 if ls == p - 1 else ls

# Generate secret key & the corresponding public key and address
d = random.SystemRandom().randrange(1, N)
(x, y) = fast_multiply(G, d)

# Double Q, works only when A = 0 in ECDSA curve
Q2 = (
    (9 * x ** 4 * inv(4 * y ** 2, P) - (2 * x)) % P,
    (9 * x ** 3 * inv(2 * y, P) - (27 * x ** 6) * inv(8 * y ** 3, P) - y) % P
)
assert Q2 == fast_multiply(G, d*2)

# Double and triple Qx, works only for secp256k1 curve
Q2x = ((x**4 - 56 * x) * inv(4 * x**3 + 28, P)) % P
Q3x = ((x**9 - 672 * x**6 + 2352 * x**3 + 21952) * inv(9 * x**2 * (x**3 + 28)**2, P)) % P
assert Q2x == fast_multiply(G, d*2)[0]
assert Q3x == fast_multiply(G, d*3)[0]

# Double Qy, works only for secp256k1 curve
Q2y = ((y**4 + 126 * y**2 - 1323) * inv(8 * y**3, P)) % P
assert Q2y == fast_multiply(G, d*2)[1]

# Build Quartic equation with the relation of Qx and 2Qx
assert (x**4 - 4 * Q2[0] * x**3 - 56 * x - 28 * Q2[0]) % P ==  0
assert ((x - 4*Q2[0]) * (x**3 + 7) * inv(63 * x, P)) % P == 1

# Depressed quartic version
_y = (x - Q2[0]) % P
assert (_y**4 - 6*Q2[0]**2*_y**2 + (-8*Q2[0]**3-56)*_y - 3*Q2[0]**4-84*Q2[0]) % P == 0

# Build Quartic equation with the relation of Qy and 2Qy
assert (y**4 - 8 * Q2[1] * y**3 + 126 * y**2 - 1323) % P ==  0
assert (y**2 * (y**2 - 8 * Q2[1] * y + 126) - 1323) % P ==  0

# Depressed quartic version
_x = (y - 2*Q2[1]) % P
assert (_x**4 + (126-24*Q2[1]**2)*_x**2 + (-64*Q2[1]**3+504*Q2[1])*_x - 48*Q2[1]**4+504*Q2[1]**2-1323) % P == 0
