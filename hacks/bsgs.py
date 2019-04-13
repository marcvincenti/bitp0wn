#!/usr/bin/env python

from bitcoin import fast_add, fast_multiply, G
import random

def fast_substract(a, b):
    x1, y1 = a
    x2, y2 = b
    return fast_add((x1, y1), (x2, -y2))

# use with an even number
nbits = 32

# generate private and public key
k = random.randint(0, 2**nbits)
Q = fast_multiply(G, k)
print("SEARCH - {0}".format(k))

# for x E N and x < 2^(nbits/2) , f(x) => G * x
O = (0, 0)
baby_steps = {}
for x in range(2**(nbits/2)):
    baby_steps[O] = x
    O = fast_add(O, G)

# find y where y E X and y = G + (x * 2^(nbits/2))
O = (0, 0)
O_ADDER = fast_multiply(G, 2**(nbits/2))
for factor_giant in range(2**(nbits/2)):
    substract_res = fast_substract(Q, O)
    if substract_res in baby_steps:
        factor_baby = baby_steps[substract_res]
        k = (factor_giant * 2**(nbits/2)) + factor_baby
        print("FOUND  - {0}".format(k, factor_giant, factor_baby))
        break
    O = fast_add(O, O_ADDER)
