#!/usr/bin/env python

from bitcoin import fast_add, fast_multiply, G, hash_to_int, inv, N
from hashlib import sha256
from random import SystemRandom

def ecdsa_sign_k(z, d, k):
    r, y = fast_multiply(G, k)
    s = inv(k, N) * (z + r*d) % N
    v, r, s = 27+((y % 2) ^ (0 if s * 2 < N else 1)), r, s if s * 2 < N else N - s
    return v, r, s

# Generate secret key & the corresponding public key and address
d = SystemRandom().randrange(1, N)
Q = fast_multiply(G, d);

# Sign a message with k
k = SystemRandom().randrange(1, N)
z1 = hash_to_int(sha256('0xDEADBEEF').hexdigest())
z2 = hash_to_int(sha256('try forge this').hexdigest())
v1, r1, s1 = ecdsa_sign_k(z1, d, k)
v2, r2, s2 = ecdsa_sign_k(z2, d, k)

# Basic verifications
assert r1 == r2
a1 = z1 * inv(s1, N) % N
b1 = r1 * inv(s1, N) % N
assert k == (a1 + d * b1) % N \
    or N - k == (a1 + d * b1) % N
assert z1 == r1 * a1 * inv(b1, N) % N

# now we multiply z by n
n = z2 * inv(z1, N) % N
assert z2 == r1 * (a1 * n * inv(b1, N)) % N

a2 = z2 * inv(s2, N) % N
b2 = r2 * inv(s2, N) % N

assert (a1 + d * b1) % N == (a2 + d * b2) % N \
    or N - (a1 + d * b1) % N == (a2 + d * b2) % N
assert (a1 * n * inv(b1, N)) % N == (a2 * inv(b2, N)) % N

# a' = a * (m + d*r) / (m + d*r/n)
assert a2 == a1 * (z1 + d * r1) * inv(z1 + d * r1 * inv(n, N), N) % N

# b' = b * (d + m/r) /  (d + n*m/r)
assert b2 == b1 * (d + z1 * inv(r1, N)) * inv(d + z2 * inv(r1, N), N) % N

# a' = b' * n * m / r
assert a2 == b2 * z2 * inv(r1, N) % N

print "b' = " + str(b1) + " * (d + " + str(z1 * inv(r1, N) % N) + ") / (d + " + str(z2 * inv(r1, N) % N) + ")"
print "a' = " + str(a1) + " * (" + str(z1) + " + d * " + str(r1) + ") / (" + str(z1) + " + d * " + str(r1 * inv(n, N) % N) + ")"
print "a' = b' * " + str(z2 * inv(r1, N) % N)
