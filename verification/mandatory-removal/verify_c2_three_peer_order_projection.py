#!/usr/bin/env python3
"""Exact three-peer local-order projection from every finite-age initial state.

At n=3,c=ell=2, project each row separately: retain zero and replace its
positive ages by their ranks starting at one. This has eleven possible
rows, and 1306 connected states. Unlike the 487-state positivity projection,
it applies at time zero, without a coupon-cover burn-in. Exact integer
powers certify conditional single-ID error below 10**-6 at every t>=56. The analytic
justification is in prop:c2threeorderprojection in paper/main.tex.

The rank map is NOT claimed exact for n>=4. Numerical lift tests corroborate,
but do not replace, the analytic proof. All transition and query calculations
use exact rational/integer arithmetic, with no truncation or simulation.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_c2_recurrent_mixing import outcomes, state_key
from verify_c2_three_peer_antisymmetric import connected, relabel


def project(state):
    result = []
    for row in state:
        positive = sorted({age for _, age in row if age > 0})
        ranks = {age: rank + 1 for rank, age in enumerate(positive)}
        result.append(tuple((peer, 0 if age == 0 else ranks[age]) for peer, age in row))
    return tuple(result)


def projection_states():
    options = []
    for peer in range(3):
        others = [other for other in range(3) if other != peer]
        rows = [{}] + [{other: age} for other in others for age in (0, 1)]
        rows += [dict(zip(others, ages)) for ages in
                 ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1))]
        assert len(rows) == 11
        options.append(rows)
    return [state_key(caches) for caches in product(*options)
            if connected(state_key(caches))]


def exact_rows(states):
    indices = {state: index for index, state in enumerate(states)}
    rows = []
    for state in states:
        row = defaultdict(Fraction)
        for successor, probability in outcomes(state):
            row[indices[project(successor)]] += probability
        assert sum(row.values()) == 1
        assert all((6 * probability).denominator == 1 for probability in row.values())
        rows.append({index: int(6 * mass) for index, mass in row.items()})
    return indices, rows


def check_lifts(states, indices, rows):
    count = 0
    for index, state in enumerate(states):
        expected = {j: Fraction(weight, 6) for j, weight in rows[index].items()}
        # Row-specific increasing maps cover unequal large ages and both
        # unit and large gaps. They preserve local ties but change cross-row
        # ranks, which are deliberately absent from this projection.
        for base, gap in ((1, 1), (10**6, 1), (17, 10**6)):
            lifted = tuple(tuple((peer, 0 if age == 0 else
                                  base + 13 * owner + gap * age)
                                 for peer, age in row)
                           for owner, row in enumerate(state))
            assert project(lifted) == state
            actual = defaultdict(Fraction)
            for successor, probability in outcomes(lifted):
                actual[indices[project(successor)]] += probability
            assert dict(actual) == expected
            count += 1
    return count


def check_independent_three_peer_kernel(states, indices, rows):
    """Compare every row with a direct three-peer-specific derivation.

    This implementation does not call outcomes or Actual. For p->q, let r
    be the remaining label. The new active row consists only of r, if
    either old row held r. The new passive row has fresh p and possibly r.
    Thus victim choices never arise here; only scheduler and oldest ties
    are random. Integer weights are six times the transition probability.
    """
    for index, state in enumerate(states):
        independently_derived = defaultdict(int)
        for p in range(3):
            active = dict(state[p])
            if not active:
                independently_derived[index] += 2
                continue
            maximum = max(active.values())
            partners = [q for q, age in active.items() if age == maximum]
            for q in partners:
                r = 3 - p - q
                passive = dict(state[q])
                new_active, new_passive = {}, {p: 0}
                if r in active:
                    new_active[r] = active[r] + 1
                if r in passive:
                    new_active[r] = min(new_active.get(r, passive[r]), passive[r])
                    new_passive[r] = passive[r]
                if r in active:
                    new_passive[r] = min(new_passive.get(r, active[r] + 1),
                                         active[r] + 1)
                successor = list(state)
                successor[p] = tuple(sorted(new_active.items()))
                successor[q] = tuple(sorted(new_passive.items()))
                independently_derived[indices[project(tuple(successor))]] += (
                    2 // len(partners))
        assert dict(independently_derived) == rows[index]
    return len(states)


def certificate():
    states = projection_states()
    assert len(states) == 1306
    assert all(project(state) == state for state in states)
    print('Connected local-order states:', len(states))
    indices, rows = exact_rows(states)
    print('Independent three-peer transition rows:',
          check_independent_three_peer_kernel(states, indices, rows))
    permutation = [indices[relabel(state)] for state in states]
    for index, row in enumerate(rows):
        assert {permutation[j]: weight for j, weight in row.items()} == rows[permutation[index]]
    print('Numerical-lift corroborations:', check_lifts(states, indices, rows))
    availability = [int(bool(state[0])) for state in states]
    imbalance = [0 if len(state[0]) != 1 else (1 if state[0][0][0] == 1 else -1)
                 for state in states]
    errors = []
    for time in range(57):
        error = max(Fraction(abs(h), 2 * a) for h, a in zip(imbalance, availability) if a)
        errors.append(error)
        if time == 2:
            assert Fraction(min(availability), 6**time) == Fraction(2, 9)
        if time >= 2:
            assert min(availability) > 0
        if time in (2, 4, 8, 55, 56):
            print(f't={time}: max conditional error={error} ({float(error):.12g}); '
                  f'min availability={Fraction(min(availability),6**time)}')
        # A pointwise bound |P^t f| <= 2 epsilon P^t g persists at all
        # later times by positivity of P, not by assumed monotonicity of
        # conditional distributions from each fixed initial state.
        availability = [sum(weight * availability[j] for j, weight in row.items()) for row in rows]
        imbalance = [sum(weight * imbalance[j] for j, weight in row.items()) for row in rows]
    assert errors[55] > Fraction(1, 10**6)
    assert errors[56] == Fraction(7848601085488402478052232343135075946,
                                7882272325236504573889078691555685474884669)
    assert errors[56] < Fraction(1, 10**6)
    assert all(error > Fraction(1, 10**6) for error in errors[:56])
    print('PASS: all connected finite-age starts, every t>=56: error < 10**-6.')
    print('Scope: n=3,c=ell=2; all connected arbitrary finite-age starts.')


if __name__ == '__main__':
    certificate()
