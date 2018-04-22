#!/usr/bin/env python
from __future__ import print_function

from bitcoin import fast_multiply
import random

P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)

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

#assumes p prime returns cube root of a mod p
def cuberoot(a, p):
    if p == 2:
        return a
    if p == 3:
        return a
    if (p%3) == 2:
        return pow(a,(2*p - 1)/3, p)
    if (p%9) == 4:
        root = pow(a,(2*p + 1)/9, p)
        assert pow(root,3,p) == a%p
        return root
    if (p%9) == 7:
        root = pow(a,(p + 2)/9, p)
        assert pow(root,3,p) == a%p
        return root
    else:
        print("Not implemented yet. See the second paper")

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

def modular_sqrt(a, p):
    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.

        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.

        0 is returned is no square root exists for
        these a and p.

        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
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

def iroot(x,n):
    """Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    """
    high = 1
    while high ** n < x:
        high *= 2
    low = high/2
    while low < high:
        mid = int((low + high) // 2) + 1
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            assert mid**n == x
            return mid
    assert (mid+1)**n == x
    return mid + 1

def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    assert x**2 == n
    return x

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

# Double Qx and add G
Q2xp1 = (((Q2[0] * G[0]) * (Q2[0] + G[0]) - 2*Q2[1]*G[1] + 14) * inv((Q2[0] - G[0])**2, P)) % P
assert Q2xp1 == fast_multiply(G, (d*2)+1)[0]

# Eq 1.
assert x**4 % P == ((x**3 + 7) * (8*x + 4*Q2x) * inv(9, P)) % P
# Eq 2.
assert x == ((x**3 + 7) * (x - 4*Q2x) * inv(63, P)) % P
# (Eq 1.) / (Eq 2.)
assert x**3 % P == (7 * (8*x + 4*Q2x) * inv(x - 4*Q2x, P)) % P
# (Eq 1.) x (Eq 2.)
assert x**5 % P == ((x**3 + 7) * (x**3 + 7) * (8*x + 4*Q2x) * (x - 4*Q2x) * inv(567, P)) % P
# Eq 3.
assert Q2x == (x**3 - 56) * (x - 4*Q2x) * inv(252, P) % P
# Eq 4.
assert Q2x == x * (x**3 - 56) * inv(4*x**3 + 28, P) % P


# Double Qy, works only for secp256k1 curve
Q2x = (x * (y ** 2 - 63) * inv(4 * y ** 2, P)) % P
Q2y = ((y**4 + 126 * y**2 - 1323) * inv(8 * y**3, P)) % P
assert (Q2x, Q2y) == fast_multiply(G, d*2)

# Double Qy and add G
assert (3 * (G[1] - Q2y) * Q2x) % P == (x * (-3 * y**6 + 24*G[1] * y**5 - 189 * y**4 - 1512*G[1] * y**3 + 27783 * y**2 - 250047) * inv(32 * y**5, P)) % P

assert ((G[1] - Q2y)**3 * inv(G[0] - Q2x, P)**3) % P == \
(-y**12 + 24*G[1] * y**11 - (192*G[1]**2 + 378) * y**10 + (512*G[1]**3 + 6048*G[1]) * y**9 - (24192*G[1]**2 + 43659) * y**8 + 317520*G[1] * y**7 + (254016*G[1]**2 - 1000188) * y**6 - 8001504*G[1] * y**5 + 57760857 * y**4 + 42007896*G[1] * y**3 - 661624362 * y**2 + 2315685267) * \
inv((-8 * y**11 + (96*G[0]*x**2 - 384*x*G[0]**2 + 512*G[0]**3 + 1568) * y**9 + (-12096*G[0]*x**2 + 24192*x*G[0]**2 - 105840) * y**7 + (381024*G[0]*x**2 + 2667168) * y**5 - 14002632 * y**3), P) % P

Q2yp1 = (3 * (G[1] - Q2y) * Q2x * inv(G[0] - Q2x, P) - (G[1] - Q2y)**3 * inv(G[0] - Q2x, P)**3 - 2*Q2y + G[1]) % P
assert Q2yp1 == fast_multiply(G, (d*2)+1)[1]

# Build Quartic equation with the relation of Qx and 2Qx
assert (x**4 - 4 * Q2[0] * x**3 - 56 * x - 28 * Q2[0]) % P ==  0
assert ((x - 4*Q2[0]) * (x**3 + 7) * inv(63 * x, P)) % P == 1

# introduce a first root Z1 -> x
# (x - Z1) * (x**3 + G*x**2 + H*x + I) % P == 0
Z1 = x
G = (Z1 - 4*Q2[0]) % P
H = (Z1 * G) % P
I = (Z1 * H - 56) % P
assert (Z1 * I) % P == (28 * Q2[0]) % P
assert (x - Z1) * (x**3 + G*x**2 + H*x + I) % P == 0

# We now deduce the new following quartics
assert (G**4 + 12*Q2[0] * G**3 + 48*Q2[0]**2 * G**2 + (64*Q2[0]**3-56) * G - 252*Q2[0]) % P == 0
assert (I**4 + 56 * I**3 + 3136*Q2[0]**3 * I - 21952*Q2[0]**3) % P == 0

# With z1 = x, we have the resultant cubic equation for potentials other roots
assert 4 * (x**3 - 3*Q2[0]*x**2 - 14) % P == (x**3 + G*x**2 + H*x + I) % P

d0 = (9 * Q2[0]**2) % P
d1 = (-54 * Q2[0]**3 - 378) % P
d_1 = ((d1**2 - 4*d0**3) * inv(-27, P)) % P
d_2 = (-4*27*Q2[0]**3*14 - 27*14**2) % P
assert d_1 == d_2 # d_1 or d_2 is the discriminant

assert (d1**2 - 4*d0**3) % P == (40824 * Q2[0]**3 + 142884) % P

C1 = cuberoot((d1 + modular_sqrt(40824 * Q2[0]**3 + 142884, P)) * inv(2, P), P)
C2 = cuberoot((d1 - modular_sqrt(40824 * Q2[0]**3 + 142884, P)) * inv(2, P), P)

res1 = (-inv(3, P) * (-3*Q2[0] + C1 + d0*inv(C1, P))) % P
res2 = (-inv(3, P) * (-3*Q2[0] + C2 + d0*inv(C2, P))) % P

assert (res1**3 - 3*Q2[0]*res1**2 - 14) % P == 0
assert (res2**3 - 3*Q2[0]*res2**2 - 14) % P == 0

assert ((x - res1) * (x - res2)) % P == ((x**2 - (res1+res2)*x + res1*res2)) % P

# Now we look for res3
# (x**3 - (res1+res2+res3)*x**2 + (res1*res2 + res1*res3 + res2*res3)*x - res1*res2*res3)
# res1 + res2 + res3 = 3 * Q2[0]
# (res1*res2 + res1*res3 + res2*res3) = 0
# (res1 * res2 * res3) = 14
print((3 * Q2[0] - (res1 + res2)) % P)
print((-(res1 * res2) * inv(res1 + res2, P)) % P)
print(14 * inv(res1 * res2, P) % P)
# all the precendent prints have to be the same but aren't always
res3 = 14 * inv(res1 * res2, P) % P
assert (res3**3 - 3*Q2[0]*res3**2 - 14) % P == 0

assert 4 * (x**3 - (res1+res2+res3)*x**2 + (res1*res2 + res1*res3 + res2*res3)*x - res1*res2*res3) % P == (x**3 + G*x**2 + H*x + I) % P

# x = t - (b/3a) => t = x + (b/3a)
_a = 1
_b = (3*Q2[0]) % P
_c = 0
_d = (-14) % P

_t = (x + _b*inv(3*_a, P)) % P
_p = ((3*(_a)*(_c) - (_b**2)) * inv(3*(_a**2), P)) % P
_q = ((2*(_b**3) - 9*(_a)*(_b)*(_c) + 27*(_a**2)*(_d)) * inv(27*(_a**3), P)) % P

# now we have z**3 + p*z + q = 0 and thus z**4 + p*z**2 + qz = 0


# Depressed quartic version
_y = (x - Q2[0]) % P
assert (_y**4 + (-6*Q2[0]**2)*_y**2 + (-8*Q2[0]**3-56)*_y + (-3*Q2[0]**4-84*Q2[0])) % P == 0

p = (-6*Q2[0]**2)
q = (-8*Q2[0]**3-56)
r = (-3*Q2[0]**4-84*Q2[0])
assert (_y**4 + p*_y**2 + q*_y + r) % P == 0

# Resolvent cubic version with Descarte's solution
# ((U**3) + 2*p*(U**2) + ((p**2) - 4*r)*U - q**2) % P == 0

a = 1
b = 2*p % P
c = ((p**2) - 4*r) % P
d = (-(q**2)) % P

_p = ((3*(a)*(c) - (b**2)) * inv(3*(a**2), P)) % P
_q = ((2*(b**3) - 9*(a)*(b)*(c) + 27*(a**2)*(d)) * inv(27*(a**3), P)) % P
assert _p == (336 * Q2[0]) % P
assert _q == (448 * (Q2[0]**3 - 7)) % P


# Build Quartic equation with the relation of Qy and 2Qy
assert (y**4 - 8 * Q2[1] * y**3 + 126 * y**2 - 1323) % P ==  0
assert (y**2 * (y**2 - 8 * Q2[1] * y + 126) - 1323) % P ==  0

# Depressed quartic version
_x = (y - 2*Q2[1]) % P
assert (_x**4 + (126-24*Q2[1]**2)*_x**2 + (-64*Q2[1]**3+504*Q2[1])*_x + (-48*Q2[1]**4+504*Q2[1]**2-1323)) % P == 0

p = (126-24*Q2[1]**2)
q = (-64*Q2[1]**3+504*Q2[1])
r = (-48*Q2[1]**4+504*Q2[1]**2-1323)
assert (_x**4 + p*_x**2 + q*_x + r) % P == 0

# Resolvent cubic version with Ferrari's solution
# (8*(m**3) + 8*p*(m**2) + (2*(p**2) - 8*r)*m - q**2) % P == 0

a = 8
b = 8*p % P
c = (2*(p**2) - 8*r) % P
d = (-(q**2)) % P

# Resolvent depressed cubic
# t^3 + _pt + _q = 0  &  m = t + (b/(3a))

_p = ((3*(a)*(c) - (b**2)) * inv(3*(a**2), P)) % P
_q = ((2*(b**3) - 9*(a)*(b)*(c) + 27*(a**2)*(d)) * inv(27*(a**3), P)) % P

assert _p == 0
assert _q == (10584 * (Q2[1]**2 - 7)) % P

t_cube = 10584 * (Q2[1]**2 - 7)

# We know Q2[0]**3 = Q2[1]**2 - 7 mod P
# Also 10584 = 2^3 * 3^3 * 7^2
# We can conclude cbrt(49*t^3) = 6*Q2[0]

assert t_cube % P == (inv(7,P)*(42*Q2[0])**3) % P
assert t_cube % P == (49*(6*Q2[0])**3) % P

"""
t = -6 * cuberoot(49, P) * Q2[0]
assert (t**3 + _p*t + _q) % P == 0
m = t - 8*Q2[1]**2 + 42
assert (8*(m**3) + 8*p*(m**2) + (2*(p**2) - 8*r)*m - q**2) % P
"""
