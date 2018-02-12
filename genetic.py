#!/usr/bin/env python

from bitcoin import G, N, fast_multiply
from numpy.random import choice
import random

BYTES = 16
POPULATION_SIZE = 1000
MUTABILITY = 0.05
N = min(N, 2**BYTES)

def inv_normalize(lst):
    s = sum(lst)
    lst2 = map(lambda x: 1-(float(x)/s), lst)
    s2 = sum(lst2)
    return map(lambda x: float(x)/s2, lst2)

def int2bytes(n, size):
    expr = "{0:0"+str(size)+"b}"
    return expr.format(n)

def init_random_population():
    population = [random.SystemRandom().randrange(1, N) for _ in range(POPULATION_SIZE)]
    return population

def fitness(d, r_base):
    d_x = fast_multiply(G, d)[0]
    diff = abs(d_x - r_base)
    return min(diff, N - diff)

def mutate(d):
    b = int2bytes(d, BYTES)
    res = [None] * BYTES
    for i in range(BYTES):
        if random.random() < MUTABILITY:
            res[i] = '0' if b[i] == '1' else '1'
        else:
            res[i] = b[i]
    return int(''.join(res), 2)

def crossover(d1, d2):
    b1 = int2bytes(d1, BYTES)
    b2 = int2bytes(d2, BYTES)
    res = [b1[i] if random.random()<0.5 else b2[i] for i in range(BYTES)]
    return int(''.join(res), 2)

def perform_selection(population, weights):
    probabilities = inv_normalize(weights)
    return choice(population, POPULATION_SIZE/2, p=probabilities)

def new_generation(population, weights):
    selected_candidates = perform_selection(population, weights)
    new_population = [
        crossover(random.choice(selected_candidates),random.choice(selected_candidates))
        for _ in range(POPULATION_SIZE)
    ]
    return map(mutate, new_population)

# We don't know d but we can get Q from emitted signatures
d = random.SystemRandom().randrange(1, N)
Q = fast_multiply(G, d)
print('+ Priv key = {}'.format(d))

cpt = 1
population = init_random_population()
while True:
    # We attribute a score to each candidates
    weights = map(lambda x: fitness(x, Q[0]), population)
    # We check if we have a winner over there
    if 0 in weights:
        break
    # We create a new generation
    population = new_generation(population, weights)
    cpt = cpt + 1

pk = population[weights.index(min(weights))]
print('+ Calc key = {0} after {1} generations'.format(pk, cpt))
