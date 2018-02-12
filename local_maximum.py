#!/usr/bin/env python

from bitcoin import G, N, fast_multiply
import random

BYTES = 16

def bytes2int(vector):
    return int(''.join(map(str, vector)), 2)

def gen_random(size):
    return [random.randrange(0, 2) for _ in range(size)]

def fitness(x, y):
    diff = abs(abs(x[0]) - abs(y[0]))
    return min(diff, N-diff)

def best_neighbor(vector, base, level):
    if level > 0:
        best_fitness = fitness(fast_multiply(G, bytes2int(vector)), base)
        best_candidate = vector
        for i in range(BYTES):
            temp_vector = vector[:]
            temp_vector[i] = 0 if temp_vector[i] == 1 else 1
            temp_vector = best_neighbor(temp_vector, base, level-1)
            temp_fitness = fitness(fast_multiply(G, bytes2int(temp_vector)), base)
            if temp_fitness < best_fitness:
                best_fitness = temp_fitness
                best_candidate = temp_vector
        return best_candidate
    else:
        return vector

# We don't know d but we can get Q from emitted signatures
d = random.SystemRandom().randrange(1, 2**BYTES)
Q = fast_multiply(G, d)
print(('+ Priv key = {0:0'+str(BYTES)+'b}').format(d))

results = [0] * BYTES
for _ in range(100):
    calculated = gen_random(BYTES)
    while True:
        temp = best_neighbor(calculated, Q, 3)
        if temp == calculated:
            break
        calculated = temp
    for i in range(BYTES):
        if calculated[i] == 1:
            results[i] += 1

print('+ Calc key = {0}'.format(''.join(map(lambda x: '1' if x > 50 else '0', results))))
