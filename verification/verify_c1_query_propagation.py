#!/usr/bin/env python3
"""Exact finite checks; not a substitute for the all-n mathematical proof."""
from collections import defaultdict
from fractions import Fraction
from itertools import product


def distance(i, j, n):
    return min(abs(i-j), n-abs(i-j))


def length(state):
    n = len(state)
    return sum(distance(i, j, n) for i, j in enumerate(state) if j >= 0)


def connected(state):
    n = len(state)
    adjacency = [set() for _ in state]
    for i, j in enumerate(state):
        if j >= 0:
            adjacency[i].add(j)
            adjacency[j].add(i)
    seen = {0}
    todo = [0]
    for i in todo:
        for j in adjacency[i]-seen:
            seen.add(j)
            todo.append(j)
    return len(seen) == n


def step(state, p):
    q = state[p]
    if q < 0:
        return state
    r = state[q]
    new = list(state)
    new[q] = p
    new[p] = -1 if r == p else r
    return tuple(new)


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    states = transitions = laws = 0
    for n in range(2, 6):
        choices = [tuple([-1]+[j for j in range(n) if j != i]) for i in range(n)]
        for state in product(*choices):
            if not connected(state):
                continue
            states += 1
            assert state.count(-1) <= 1
            old = length(state)
            total = 0
            for p in range(n):
                new = step(state, p)
                assert connected(new)
                active_length = 0 if state[p] < 0 else distance(p, state[p], n)
                assert length(new)-old <= active_length
                total += length(new)
                transitions += 1
            assert total <= (n+1)*old
    for n in range(2, 7):
        initial = tuple((i+1) % n for i in range(n))
        law = {initial: Fraction(1)}
        for t in range(5):
            bound = n * Fraction(n+1, n)**t
            energy = sum(mass*length(state) for state, mass in law.items())
            assert energy <= bound
            availabilities = []
            means = []
            for i in range(n):
                query = defaultdict(Fraction)
                for state, mass in law.items():
                    if state[i] >= 0:
                        query[state[i]] += mass
                availability = sum(query.values())
                assert availability >= Fraction(n-1, n)
                mean = sum(mass*distance(i, j, n) for j, mass in query.items()) / availability
                assert mean == energy / (n*availability)
                availabilities.append(availability)
                means.append(mean)
                tv = sum(abs(query.get(j, 0)/availability-Fraction(1, n-1))
                         for j in range(n) if j != i)/2
                for twice_radius in range(1, 2*n+1):
                    radius = Fraction(twice_radius, 2)
                    lower = 1-bound/((n-1)*radius)-2*radius/(n-1)
                    assert tv >= max(0, lower)
                # Optimized radical bound, checked without rounding or floats.
                assert (1-tv)**2 * (n-1)**2 <= 8*n*Fraction(n+1, n)**t
            assert len(set(availabilities)) == len(set(means)) == 1
            laws += 1
            if t == 4:
                break
            following = defaultdict(Fraction)
            for state, mass in law.items():
                for p in range(n):
                    following[step(state, p)] += mass/n
            law = following
            assert sum(law.values()) == 1
    print(f'PASS {states} connected states, {transitions} transitions, {laws} exact cycle laws.')


if __name__ == '__main__':
    main()
