#!/usr/bin/env python3
"""Exact n=3, c=ell=2 RECURRENT-START sampling benchmark.

Enumerate the entire state family reachable from the canonical atom H.
There are exactly 75 states and their maximum numerical age is one; ages
are never truncated. The existing recurrence theorem identifies this as
the recurrent class. These calculations cover every initial state IN THIS
CLASS, not arbitrary finite-age initial states and not arbitrary n.

Transitions and single-identifier conditional errors use exact rational /
integer arithmetic. No simulation is used. Optional NumPy calculations
provide floating-point full-state matrix powers and eigenvalues; these
numerical quantities are diagnostic, not certified interval bounds.

Run with the standard library:
    python3 -B verification/mandatory-removal/verify_c2_recurrent_mixing.py

Optional numerical diagnostics, in an environment with NumPy:
    python3 -B verification/mandatory-removal/verify_c2_recurrent_mixing.py --numerical
"""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_anchor import Actual


def state_key(caches):
    return tuple(tuple(sorted(row.items())) for row in caches)


def outcomes(state):
    """All exact outcomes, including duplicate-state outcomes separately."""
    caches = [dict(row) for row in state]
    for initiator, active in enumerate(caches):
        if not active:
            yield state, Fraction(1, 3)
            continue
        oldest = [peer for peer in active if active[peer] == max(active.values())]
        for partner in oldest:
            passive = caches[partner]
            extras = set(active) - {partner}
            outgoing = {initiator} | extras
            needed = max(0, len(passive) + len(outgoing - set(passive)) - 2)
            eligible = set(passive) - outgoing
            victim_count = comb(len(eligible), needed)
            for victims in combinations(eligible, needed):
                actual = Actual(caches, 2)
                actual.step(initiator, partner, extras, passive, vq=victims)
                yield state_key(actual.x), Fraction(1, 3 * len(oldest) * victim_count)


def enumerate_class():
    initial = state_key(({1: 0, 2: 0}, {2: 0}, {}))
    states = [initial]
    indices = {initial: 0}
    for state in states:
        for successor, _ in outcomes(state):
            if successor not in indices:
                indices[successor] = len(states)
                states.append(successor)
    assert len(states) == 75
    assert max(age for state in states for row in state for _, age in row) == 1
    rows = []
    for state in states:
        row = defaultdict(Fraction)
        for successor, probability in outcomes(state):
            row[indices[successor]] += probability
        assert sum(row.values()) == 1
        assert all((probability * 6).denominator == 1 for probability in row.values())
        rows.append({j: int(probability * 6) for j, probability in row.items()})
    return states, rows


def exact_local(states, rows, steps):
    # Observer 0; h=2*(mass(output=1)-availability/2).
    # A common factor 6**t cancels in conditional TV=abs(h)/(2*a).
    availability = [int(bool(state[0])) for state in states]
    imbalance = [
        0 if len(state[0]) != 1 else (1 if state[0][0][0] == 1 else -1)
        for state in states
    ]
    targets = [Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000), Fraction(1, 10**6)]
    first = {}
    errors = []
    for time in range(steps + 1):
        error = max(
            Fraction(abs(h), 2 * a)
            for h, a in zip(imbalance, availability) if a
        )
        errors.append(error)
        for target in targets:
            if error <= target:
                first.setdefault(str(target), time)
        if time in (0, 1, 2, 3, 4, 5, 8, 10, 12, 20, 25, 30, 50):
            print(f't={time:2d}: worst conditional error={float(error):.12g}; exact={error}')
        availability = [
            sum(weight * availability[j] for j, weight in row.items())
            for row in rows
        ]
        imbalance = [
            sum(weight * imbalance[j] for j, weight in row.items())
            for row in rows
        ]
    if steps >= 8:
        assert errors[8] == Fraction(9483, 1420660)
    if steps >= 25:
        assert errors[25] == Fraction(18359438816999, 23769834206568612112)
    print('Exact first threshold times over the inspected horizon:', first)


def numerical_diagnostics(states, rows, steps):
    try:
        import numpy as np
    except ImportError as error:
        raise SystemExit('--numerical requires NumPy; omit it for exact standard-library checks.') from error
    size = len(states)
    transition = np.zeros((size, size))
    for i, row in enumerate(rows):
        for j, weight in row.items():
            transition[i, j] = weight / 6
    equation = transition.T - np.eye(size)
    equation[-1, :] = 1
    rhs = np.zeros(size)
    rhs[-1] = 1
    stationary = np.linalg.solve(equation, rhs)
    assert np.min(stationary) > 0
    assert np.max(abs(stationary @ transition - stationary)) < 1e-12
    eigenvalues = np.linalg.eigvals(transition)
    second_modulus = sorted(abs(value) for value in eigenvalues)[-2]
    stationary_availability = sum(
        stationary[i] for i, state in enumerate(states) if state[0]
    )
    print('NUMERICAL second eigenvalue modulus:', second_modulus)
    print('NUMERICAL stationary nonempty probability:', stationary_availability)
    power = np.eye(size)
    targets = (0.1, 0.01, 0.001, 1e-6)
    first = {}
    for time in range(steps + 1):
        error = np.max(np.sum(abs(power - stationary), axis=1) / 2)
        for target in targets:
            if error <= target:
                first.setdefault(target, time)
        if time in (0, 1, 2, 3, 5, 10, 15, 20, 30, 50):
            print(f't={time:2d}: NUMERICAL worst recurrent-start full-state TV={error:.12g}')
        power = power @ transition
    print('NUMERICAL full-state first threshold times over inspected horizon:', first)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--steps', type=int, default=50)
    parser.add_argument('--numerical', action='store_true')
    args = parser.parse_args()
    assert args.steps >= 0
    states, rows = enumerate_class()
    print('Enumerated recurrent class:', len(states), 'states; n=3, c=ell=2 only.')
    print('All initial states below are RESTRICTED TO THIS RECURRENT CLASS.')
    exact_local(states, rows, args.steps)
    if args.numerical:
        numerical_diagnostics(states, rows, args.steps)


if __name__ == '__main__':
    main()
