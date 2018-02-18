#!/usr/bin/env python

from bitcoin import G, N, P, fast_multiply, inv
import random

# calculate sqrt, f: long int -> long int
def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def find_invpow(x,n):
    high = 1
    while high ** n <= x:
        high *= 2
    low = high/2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1

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
Q4x = (x * (x**3 - 56) * (x**12 - 3752 * x**9 - 65856 * x**6 - 702464 * x**3 - 1229312) * inv(16 * (x**3+7) * (x**6 + 140 * x**3 - 392)**2, P)) % P
assert Q2x == fast_multiply(G, d*2)[0]
assert Q3x == fast_multiply(G, d*3)[0]
assert Q4x == fast_multiply(G, d*4)[0]

# Build Quartic equation with the relation of Qx and 2Qx
assert (x ** 4 - 4 * Q2[0] * x ** 3 - 56 * x - 28 * Q2[0]) % P ==  0

a = 1
b = -4*Q2[0]
c = 0
d = -56
e = -28*Q2[0]

d0 = (c**2) - 3*(b)*(d) + 12*(a)*(e)
d1 = 2*(c**3) - 9*(b)*(c)*(d) + 27*(b**2)*(e) + 27*(a)*(d**2) - 72*(a)*(c)*(e)

d = 256*(a**3)*(e**3) - 192*(a**2)*(b)*(d)*(e**2) - 128*(a**2)*(c**2)*(e**2) \
    + 144*(a**2)*(c)*(d**2)*(e) - 27*(a**2)*(d**4) + 144*(a)*(b**2)*(c)*(e**2) \
    - 6*(a)*(b**2)*(d**2)*(e) - 80*(a)*(b)*(c**2)*(d)*(e) + 18*(a)*(b)*(c)*(d**3) \
    + 16*(a)*(c**4)*(e) - 4*(a)*(c**3)*(d**2) - 27*(b**4)*(e**2) + 18*(b**3)*(c)*(d)*(e) \
    - 4*(b**3)*(d**3) - 4*(b**2)*(c**3)*(e) + (b**2)*(c**2)*(d**2)

assert d1**2 - 4*d0**3 == -27*d

p = (8*(a)*(c) - 3*(b**2)) / 8*(a**2)
q = ((b**3) - 4*(a)*(b)*(c) + 8*(a**2)*(d)) / 8*(a**3)

_Q_power3 = (d1) + isqrt((d1**2) - 4*(d0**3)) / 2
_Q = find_invpow(-_Q_power3, 3) # Not a perfect cube
_S_power2 = (-2*(p)/3) + (_Q+(d0/_Q))/(3*(a))
_S = isqrt(_S_power2) / 2 # Not a perfect square

x1 = -(b)/(4*(a)) - _S - isqrt(-4*(_S_power2) - 2*(p) + (q)/(_S))/2
x2 = -(b)/(4*(a)) - _S + isqrt(-4*(_S_power2) - 2*(p) + (q)/(_S))/2
x3 = -(b)/(4*(a)) + _S - isqrt(-4*(_S_power2) - 2*(p) + (q)/(_S))/2
x4 = -(b)/(4*(a)) + _S + isqrt(-4*(_S_power2) - 2*(p) + (q)/(_S))/2
