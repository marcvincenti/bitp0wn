#!/usr/bin/env python

from bitcoin import change_curve, fast_add, fast_multiply, inv
import random

# define a 16-bits curve (not secure)
P = 10177
A = 1
B = P-1
G = (1,1)
N = 10331
change_curve(P, N, A, B, G[0], G[1])

# generate private and public key
k = random.randint(1, N)
Q = fast_multiply(G, k)
print("SEARCH - {0}".format(k))

# Pollard rho
def new_xab(x, a, b):
    S = x[0] % 3
    if S == 0:
        a = (a + 1) % N
        x = fast_add(x, G)
    elif S == 1:
        a = (a * 2) % N
        b = (b * 2) % N
        x = fast_add(x, x)
    elif S == 2:
        b = (b + 1) % N
        x = fast_add(x, Q)
    return x, a, b

x=X=(0,0); a=A=0; b=B=0;
for i in range(N):
    x, a, b = new_xab(x, a, b)
    X, A, B = new_xab(X, A, B)
    X, A, B = new_xab(X, A, B)
    if x == X:
        if b == B:
            print("NOT FOUND")
        else:
            k = ((a - A) * inv(B - b, N)) % N
            print("FOUND  - {0}".format(k))
        break
