#!/usr/bin/env python

import bitcoin
import hashlib
import random

N = bitcoin.N
G = bitcoin.G
fast_add = bitcoin.fast_add
fast_multiply = bitcoin.fast_multiply
def fast_substract(a, b):
    x1, y1 = a
    x2, y2 = b
    return fast_add((x1, y1), (x2, -y2))
inv = bitcoin.inv

# We don't know d but we can get Q from emitted signatures
d = bitcoin.decode_privkey(bitcoin.random_key())
Q = fast_multiply(G, d)

# We build up a message to sign
msghash = hashlib.sha256('a_random_message').hexdigest()
z = bitcoin.hash_to_int(msghash)

cpt = 0
while True:
    cpt = cpt + 1
    r = random.SystemRandom().randrange(1, N)
    s = random.SystemRandom().randrange(1, N/2)
    if r == fast_add(fast_multiply(G, z*inv(s,N)), fast_multiply(Q, r*inv(s,N)))[0] :
        break

assert bitcoin.ecdsa_raw_verify(msghash, (27, r, s), Q)
print('v={0}\nr={1}\ns={2}'.format(27, r, s))
print('Find after {} attempts.'.format(cpt))
