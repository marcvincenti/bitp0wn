#!/usr/bin/env python

import bitcoin
import hashlib
import random
import numpy as np

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

# Express d
d_candidates = [
    (z1*s2*_k2 - z2*s1*_k1) * inv(r1*z2 - r2*z1, N) % N
    for _k1 in [k1, N - k1]
    for _k2 in [k2, N - k2]
]
assert d in d_candidates

# Express k1 with k2 and k2 with k1
f1_candidates = [
    (_k1 * (s1*r2*inv(s2*r1, N)) - _k2) % N
    for _k1 in [k1, N - k1]
    for _k2 in [k2, N - k2]
]
assert (z2*r1 - z1*r2) * inv(s2*r1, N) % N in f1_candidates
f2_candidates = [
    (_k2 * (s2*r1*inv(s1*r2, N)) - _k1)  % N
    for _k1 in [k1, N - k1]
    for _k2 in [k2, N - k2]
]
assert (r2*z1 - r1*z2) * inv(s1*r2, N) % N in f2_candidates

# Express k1 & k2 with d
_a = r1*inv(s1,N) % N
_b = z1*inv(s1, N) % N
assert ( d*_a + _b) % N == k1 or ( d*_a + _b) % N == N-k1
_c = r2*inv(s2,N) % N
_d = z2*inv(s2, N) % N
assert ( d*_c + _d) % N == k2 or ( d*_c + _d) % N == N-k2
