#!/usr/bin/env python

import bitcoin
import hashlib
import random

N = bitcoin.N
G = bitcoin.G
fast_add = bitcoin.fast_add
fast_multiply = bitcoin.fast_multiply
inv = bitcoin.inv

def get_z(msg):
    hash = hashlib.sha256(msg).hexdigest()
    return bitcoin.hash_to_int(hash)

# We don't know d but we can get Q from emitted signatures
d = bitcoin.decode_privkey(bitcoin.random_key())
Q = fast_multiply(G, d)

# We build up a message to sign
z = get_z('a_random_message')
Gz = fast_multiply(G, z)

cpt = 0
while True:
    cpt = cpt + 1
    s = random.SystemRandom().randrange(1, N-1)
    r = random.SystemRandom().randrange(1, N-1)
    if r == fast_multiply(fast_add(Gz, fast_multiply(Q, r)), inv(s,N))[0] :
        break

print('{}'.format((r, s)))
print('Find after {} attempts.'.format(cpt))
