"""Exact recurrent-class n=3,c=ell=2 local-sampling benchmark.

This is not a theorem for arbitrary n or arbitrary initial ages. All rows of
the recurrent transition matrix are enumerated, and reported local errors
are exact rational numbers, with no Monte Carlo or age truncation.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb
import sys

sys.path.insert(0, '/Users/martijndevos/Documents/decentralized-learning-simulator/docs/peer-sampling-convergence/mandatory-removal')
from verify_thesis_anchor import Actual

def key(x):
    return tuple(tuple(sorted(row.items())) for row in x)

def outcomes(st):
    x = [dict(row) for row in st]
    for p, P in enumerate(x):
        if not P:
            yield st, Fraction(1, 3)
            continue
        oldest = [q for q in P if P[q] == max(P.values())]
        for q in oldest:
            Q = x[q]
            S = set(P) - {q}
            out = {p} | S
            needed = max(0, len(Q) + len(out - set(Q)) - 2)
            eligible = set(Q) - out
            for victims in combinations(eligible, needed):
                z = Actual(x, 2)
                z.step(p, q, S, Q, vq=victims)
                yield key(z.x), Fraction(1, 3 * len(oldest) * comb(len(eligible), needed))

start = key(({1: 0, 2: 0}, {2: 0}, {}))
states = [start]
indices = {start: 0}
for st in states:
    for nxt, probability in outcomes(st):
        if nxt not in indices:
            indices[nxt] = len(states)
            states.append(nxt)
assert len(states) == 75
assert max(age for st in states for row in st for _, age in row) == 1

rows = []
for st in states:
    row = defaultdict(Fraction)
    for nxt, probability in outcomes(st):
        row[indices[nxt]] += probability
    assert sum(row.values()) == 1
    # All transition denominators divide six in the c=ell=2,n=3 chain.
    assert all((probability * 6).denominator == 1 for probability in row.values())
    rows.append({j: int(probability * 6) for j, probability in row.items()})

# At observer 0, a=availability, h=2*(mass(output=1)-availability/2).
# The propagated integer vectors are scaled by the common factor 6**t,
# which cancels exactly in conditional TV=abs(h)/(2*a).
a = [int(bool(st[0])) for st in states]
h = [0 if len(st[0]) != 1 else (1 if st[0][0][0] == 1 else -1) for st in states]
targets = [Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000), Fraction(1, 10**6)]
first = {}
for t in range(51):
    error = max(Fraction(abs(hh), 2 * aa) for hh, aa in zip(h, a) if aa)
    for target in targets:
        if error <= target:
            first.setdefault(str(target), t)
    if t in (0, 1, 2, 3, 4, 5, 8, 10, 12, 20, 25, 30, 50):
        print(f't={t:2d}: worst conditional error={float(error):.12g}; exact={error}')
    a = [sum(weight * a[j] for j, weight in row.items()) for row in rows]
    h = [sum(weight * h[j] for j, weight in row.items()) for row in rows]
print('States:', len(states), 'first threshold times:', first)
