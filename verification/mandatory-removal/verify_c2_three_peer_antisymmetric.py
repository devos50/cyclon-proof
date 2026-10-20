#!/usr/bin/env python3
"""Exact n=3,c=ell=2 positivity-projection and antisymmetric certificate.

This certificate applies to a finite projection reached from EVERY weakly
connected three-peer initial state with arbitrary finite ages, rather than
only to the 75-state recurrent family. It proves no arbitrary-n rate.

Analytic reduction: after any exchange, the active cache has at most one
entry, while the passive cache contains a protected fresh age-zero entry.
Thus every updated cache has at most one positive-age entry. Once every
peer has initiated (failure probability <=3*(2/3)**m after m events), all
caches have that property. On this invariant family, replacing every
positive numerical age by one is an exact Markov projection: a positive
resident is the unique oldest and is removed; a forwarded extra previously
had age zero and becomes one. MIN merges preserve the zero/positive rule.

The resulting connected projection has 487 states. This standard-library
checker enumerates every transition exactly, certifies label equivariance,
certifies min(P**4 availability)=5/9, and proves

 max_x TV(P**8(x,.),P**8(sigma*x,.)) = 34447/69984 < 1/2,

where sigma fixes observer zero and swaps the other two labels. It uses
integer matrix powers because every transition denominator divides six.
No age truncation, Monte Carlo, or floating-point certificate is used.

Consequently every antisymmetric observable contracts by at least 1/2 per
eight events. From every arbitrary-age start, a sufficient conditional
single-ID mixing horizon for 0<epsilon<1 is

 ceil(log(9/epsilon)/log(3/2)) + 8*ceil(log2(3/epsilon)).

This is a computer-assisted finite proof for n=3 only. The mathematical
positivity reduction above is essential; this is not a finite truncation
of an unrestricted age process.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import ceil, log, log2
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_c2_recurrent_mixing import outcomes, state_key


def connected(state):
    reached = {0}
    while True:
        enlarged = (
            reached
            | {v for u in reached for v, _ in state[u]}
            | {u for u, row in enumerate(state) if any(v in reached for v, _ in row)}
        )
        if enlarged == reached:
            return len(reached) == 3
        reached = enlarged


def positive_projection(state):
    return tuple(tuple((peer, int(age > 0)) for peer, age in row) for row in state)


def relabel(state):
    sigma = {0: 0, 1: 2, 2: 1}
    caches = [None] * 3
    for peer, row in enumerate(state):
        caches[sigma[peer]] = {sigma[other]: age for other, age in row}
    return state_key(caches)


def projection_states():
    options = []
    for peer in range(3):
        others = [other for other in range(3) if other != peer]
        rows = [{}] + [{other: age} for other in others for age in (0, 1)]
        rows += [dict(zip(others, ages)) for ages in ((0, 0), (0, 1), (1, 0))]
        options.append(rows)
    states = [
        state_key(caches)
        for caches in product(*options)
        if connected(state_key(caches))
    ]
    assert len(states) == 487
    return states


def exact_rows(states):
    indices = {state: i for i, state in enumerate(states)}
    rows = []
    for state in states:
        row = defaultdict(Fraction)
        for successor, probability in outcomes(state):
            assert successor in indices
            row[indices[successor]] += probability
        assert sum(row.values()) == 1
        assert all((probability * 6).denominator == 1 for probability in row.values())
        rows.append({j: int(probability * 6) for j, probability in row.items()})
    return indices, rows


def check_numeric_lifts(states, indices, rows):
    """Corroborate the analytic projection with large, unequal positive ages."""
    witnesses = 0
    for index, state in enumerate(states):
        expected = {j: Fraction(weight, 6) for j, weight in rows[index].items()}
        for offset in (2, 10**6):
            caches = [
                {other: (0 if age == 0 else offset + 13 * peer + 7 * other)
                 for other, age in row}
                for peer, row in enumerate(state)
            ]
            lifted = state_key(caches)
            actual = defaultdict(Fraction)
            for successor, probability in outcomes(lifted):
                projected = positive_projection(successor)
                assert projected in indices
                actual[indices[projected]] += probability
            assert dict(actual) == expected
            witnesses += 1
    return witnesses


def eight_step_rows(rows):
    powers = []
    for index in range(len(rows)):
        distribution = {index: 1}
        for _ in range(8):
            following = defaultdict(int)
            for middle, mass in distribution.items():
                for destination, weight in rows[middle].items():
                    following[destination] += mass * weight
            distribution = dict(following)
        assert sum(distribution.values()) == 6**8
        powers.append(distribution)
    return powers


def certificate(epsilon):
    states = projection_states()
    indices, rows = exact_rows(states)
    permutation = [indices[relabel(state)] for state in states]
    for index, row in enumerate(rows):
        assert {permutation[j]: weight for j, weight in row.items()} == rows[permutation[index]]
    lifts = check_numeric_lifts(states, indices, rows)

    availability = [int(bool(state[0])) for state in states]
    for _ in range(4):
        availability = [
            sum(weight * availability[j] for j, weight in row.items())
            for row in rows
        ]
    minimum_availability = Fraction(min(availability), 6**4)
    assert minimum_availability == Fraction(5, 9)

    powers = eight_step_rows(rows)
    maximum_numerator = 0
    for index, distribution in enumerate(powers):
        other = powers[permutation[index]]
        numerator = sum(
            abs(distribution.get(j, 0) - other.get(j, 0))
            for j in distribution.keys() | other.keys()
        )
        maximum_numerator = max(maximum_numerator, numerator)
    coefficient = Fraction(maximum_numerator, 2 * 6**8)
    assert coefficient == Fraction(34447, 69984)
    assert coefficient < Fraction(1, 2)

    # This horizon is illustrative; the certificates above use exact integers.
    burn_in = ceil(log(9 / epsilon) / log(Fraction(3, 2)))
    contraction = 8 * ceil(log2(3 / epsilon))
    print('Projection states:', len(states))
    print('Large unequal-age lift checks:', lifts)
    print('Exact minimum availability after four events:', minimum_availability)
    print('Exact eight-event antisymmetric contraction:', coefficient)
    print('Integer numerator / denominator:', maximum_numerator, '/', 2 * 6**8)
    print(f'For epsilon={epsilon:g}: arbitrary-age sufficient local horizon =', burn_in + contraction)
    print('Scope: n=3,c=ell=2; arbitrary connected initial ages; one returned ID only.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epsilon', type=float, default=1e-6)
    args = parser.parse_args()
    assert 0 < args.epsilon < 1
    certificate(args.epsilon)


if __name__ == '__main__':
    main()
