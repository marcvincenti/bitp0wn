#!/usr/bin/env python

from bitcoin import fast_add, fast_multiply, G, hash_to_int, inv, N
from hashlib import sha256
from random import SystemRandom

# Generate secret key & the corresponding public key and address
d = SystemRandom().randrange(1, N)
Q = fast_multiply(G, d);

# Choose a 2 random numbers
a = SystemRandom().randrange(1, N)
b = SystemRandom().randrange(1, N)

# calculate a signature
r = fast_add(fast_multiply(G, a), fast_multiply(Q, b))[0]
s = r * inv(b, N)

# Calculate the hash corresponding to the signature (r,s)
h = a * r * inv(b, N)

# calculate the hash of the message we want to sign
z = hash_to_int(sha256('0xDEADBEEF').hexdigest())

# re-calculate s to sign z
s_p = r * s * inv(r - (z - h) * inv(d + (z * inv(r, N)), N), N)

# et voila
w = inv(s_p, N)
u1, u2 = z*w % N, r*w % N
x, y = fast_add(fast_multiply(G, u1), fast_multiply(Q, u2))
assert(r == x and (r % N) and (s_p % N))
