#!/usr/bin/env python

from bitcoin import G, fast_add, fast_multiply
import random

def fast_substract(a, b):
    x1, y1 = a
    x2, y2 = b
    return fast_add((x1, y1), (x2, -y2))

# use with an even number
nbits = 16

# generate private and public key
k = random.randint(0, (2**nbits)-1)
Q = fast_multiply(G, k)
print("SEARCH - {0}".format(k))

# for x E N and x < 2^(nbits/2) , f(x) => G * x
candidates_dict = dict((fast_multiply(G, x), x) for x in range(2**(nbits/2)))

# find y where y E X and y = G + (x * 2^(nbits/2))
for candidate, factor2 in candidates_dict.iteritems() :
    candidate2 = fast_multiply(candidate, 2**(nbits/2))
    substract_res = fast_substract(candidate2, Q)
    if substract_res in candidates_dict:
        factor = candidates_dict[substract_res]
        priv = factor + (factor2 * 2**(nbits/2))
        print("FOUND  - {0}".format(priv))
        break
