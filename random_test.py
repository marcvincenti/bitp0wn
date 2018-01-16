#!/usr/bin/env python

import bitcoin
import hashlib
import random

N = bitcoin.N
G = bitcoin.G

def calcul_P(x):
    P = bitcoin.P
    y = pow(int(x*x*x+7), int((P+1)//4), int(P))
    return [(x, y), (x, P-y)]

inv = bitcoin.inv
fast_multiply = bitcoin.fast_multiply
fast_add = bitcoin.fast_add
def fast_substract(a, b):
    x1, y1 = a
    x2, y2 = b
    return fast_add((x1, y1), (x2, -y2))

def get_z(msg):
    hash = hashlib.sha256(msg).hexdigest()
    return bitcoin.hash_to_int(hash)

def sign(z, k, priv):
    r, y = fast_multiply(G, k)
    s = (inv(k, N) * (z + r*bitcoin.decode_privkey(priv))) % N
    v, r, s = 27+((y % 2) ^ (0 if s * 2 < N else 1)), r, s if s * 2 < N else N - s
    return v, r, s

# Generate secret key & the corresponding public key and address
sk = bitcoin.random_key()
pk = bitcoin.privtopub(sk)
print('+ Priv key = {:s}'.format(sk))

# Sign 2 messages
d = bitcoin.decode_privkey(sk)
z1 = get_z('my_message_1')
k1 = random.SystemRandom().randrange(1, N)
v1, r1, s1 = sign(z1, k1, sk)
z2 = get_z('my_message_2')
k2 = random.SystemRandom().randrange(1, N)
v2, r2, s2 = sign(z2, k2, sk)

s1s2_candidates = [s1 + s2, s1 - s2]
r2_candidates = calcul_P(r2)
z1r2_candidates = map(lambda x: fast_multiply(x, z1), r2_candidates)
dr1r2_candidates = map(lambda x: fast_multiply(x, d*r1), r2_candidates)
r1_candidates = calcul_P(r1)
z2r1_candidates = map(lambda x: fast_multiply(x, z2), r1_candidates)
dr2r1_candidates = map(lambda x: fast_multiply(x, d*r2), r1_candidates)

dividend_candidates = [fast_substract(fast_add(z1r2, dr1r2), fast_add(z2r1, dr2r1))
                        for z1r2 in z1r2_candidates
                        for dr1r2 in dr1r2_candidates
                        for z2r1 in z2r1_candidates
                        for dr2r1 in dr2r1_candidates]

division_candidates = [fast_multiply(dividend, inv(divisor, N))
                        for dividend in dividend_candidates
                        for divisor in s1s2_candidates]

assert fast_multiply(G, k1*k2) in division_candidates
