#!/usr/bin/env python

from bitcoin import G, fast_multiply
import random

# use with an even number
nbits = 16

# generate private and public key
k = random.randint(0, 2**nbits - 2**(nbits/2))
q = fast_multiply(G, k)[0]
print("SEARCH - {0}".format(k))

for n in range(2**nbits - 2**(nbits/2)) :
    candidate = fast_multiply(G, n)
    if candidate[0] == q:
        print("FOUND  - {0}".format(n))
        break
