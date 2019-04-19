#!/usr/bin/env python

from bitcoin import inv, N, P
from random import randint, sample

def make_random_shares(secret, minimum_shares, total_shares):
    # generate a polynomial of degree 'minimum_shares-1' with constant = secret
    polynomial_coefficients = [secret] + [randint(0, P) for _ in range(minimum_shares - 1)]
    # lambda wich take a polynomial and some x and return the corresponding y
    eval = lambda coeffs, x : reduce(lambda acc, coeff: (x*acc)+coeff % P, reversed(coeffs))
    # generate points on the polynomial with x != 0 (this point hold the secret)
    x_s = set()
    while len(x_s) < total_shares:
        x_s.add(randint(1, P))
    return [(x, eval(polynomial_coefficients, x)) for x in x_s]

def recover_secret(shares):
    p_count = len(shares)
    x_s, y_s = zip(*shares)
    # Use lagrange interpolation
    product = lambda vals: reduce(lambda x, y: x*y, vals)
    nums = []; dens = [];
    for i in range(p_count):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(product(0 - o for o in others))
        dens.append(product(cur - o for o in others))
    den = product(dens)
    num = sum([nums[i] * den * y_s[i] * inv(dens[i], P) % P for i in range(p_count)])
    return num * inv(den, P) % P


k = randint(0, P)
shares = make_random_shares(k, 6, 12)
print("SPLIT - {0}".format(k))

rec1 = recover_secret(sample(shares, 6))
print("FOUND - {0}".format(rec1))

rec2 = recover_secret(sample(shares, 6))
print("FOUND - {0}".format(rec2))

assert rec1 == rec2 == k
