#!/usr/bin/env python

from bitcoin import fast_add, fast_multiply, G, inv, N
from random import SystemRandom

# Generate random public key
Q = fast_multiply(G, SystemRandom().randrange(1, N))

# Choose a 2 random numbers
a = SystemRandom().randrange(1, N)
b = SystemRandom().randrange(1, N)

# calculate a signature
r = fast_add(fast_multiply(G, a), fast_multiply(Q, b))[0]
s = r * inv(b, N)

# and now calculate the non hashed message from the result
m = a * r * inv(b, N)

# et voila
w = inv(s, N)
u1, u2 = m*w % N, r*w % N
x, y = fast_add(fast_multiply(G, u1), fast_multiply(Q, u2))
assert(r == x and (r % N) and (s % N))
