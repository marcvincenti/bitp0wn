#!/usr/bin/env python

from bitcoin import G, N, P, fast_multiply, inv
import random

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
