#!/usr/bin/env python

from bitcoin import G, N, P, fast_multiply, inv
import random

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
        print "Not implemented yet. See the second paper"

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

t = -6 * cuberoot(49, P) * Q2[0]
assert (t**3 + _p*t + _q) % P == 0
m = t - 8*Q2[1]**2 + 42
assert (8*(m**3) + 8*p*(m**2) + (2*(p**2) - 8*r)*m - q**2) % P
