#!/usr/bin/env python3
"""Corroborate the all-size finite-horizon initial-age compression lemma.

Compress successive GLOBAL initial-age gaps, anchored at zero, to T+1.
This is not repeated age truncation and not a time-homogeneous projection.
The proof covers arbitrary n, capacity, length, and integer ages; finite
checks below corroborate its arithmetic and coupled transition argument.
A common injective map of all reachable numerical ages is checked across
every enumerated history, corroborating the full-state TV strengthening.
All branch probabilities use exact Fractions. No Monte Carlo is used.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_c2_age_projection_obstruction import outcomes as four_peer_outcomes


def key(caches):
    return tuple(tuple(sorted(row.items())) for row in caches)


def compress(state, horizon):
    levels = sorted({0} | {age for row in state for _, age in row})
    mapping = {0: 0}
    for before, after in zip(levels, levels[1:]):
        mapping[after] = mapping[before] + min(after - before, horizon + 1)
    return tuple(tuple((peer, mapping[age]) for peer, age in row) for row in state)


def reachable_age_map(state, horizon):
    """One injective numerical-age map shared by every history through T."""
    levels = sorted({0} | {age for row in state for _, age in row})
    representative = (tuple(enumerate(levels)),)
    compressed = [age for _, age in compress(representative, horizon)[0]]
    mapping = {}
    for age, small in zip(levels, compressed):
        for offset in range(horizon + 1):
            old_value, new_value = age + offset, small + offset
            if old_value in mapping:
                assert mapping[old_value] == new_value
            mapping[old_value] = new_value
    assert len(set(mapping.values())) == len(mapping)
    return mapping


def map_state_ages(state, mapping):
    return tuple(tuple((peer, mapping[age]) for peer, age in row) for row in state)


def choices(items, count):
    return combinations(sorted(items), count)


def merge(owner, resident, received, eligible, capacity):
    valid = {peer: age for peer, age in received.items() if peer != owner}
    novel = set(valid) - set(resident)
    needed = max(0, len(novel) - (capacity - len(resident)))
    victims = set(eligible) & set(resident) - set(valid)
    assert needed <= len(victims)
    for removed in choices(victims, needed):
        row = {peer: age for peer, age in resident.items() if peer not in removed}
        for peer, age in valid.items():
            row[peer] = min(row.get(peer, age), age)
        yield removed, row, Fraction(1, comb(len(victims), needed))


def branches(state, capacity, length):
    """Independent exact implementation of the adopted full protocol."""
    caches = [dict(row) for row in state]
    n = len(caches)
    for p, old_active in enumerate(caches):
        if not old_active:
            yield (p,), state, Fraction(1, n)
            continue
        active = {peer: age + 1 for peer, age in old_active.items()}
        oldest = [peer for peer, age in active.items() if age == max(active.values())]
        for q in oldest:
            passive = caches[q]
            k = min(length - 1, len(active) - 1)
            m = min(length, len(passive))
            denominator = n * len(oldest) * comb(len(active) - 1, k) * comb(len(passive), m)
            for extra in choices(set(active) - {q}, k):
                request = {p: 0, **{peer: active[peer] for peer in extra}}
                for reply_ids in choices(passive, m):
                    reply = {peer: passive[peer] for peer in reply_ids}
                    resident = {peer: age for peer, age in active.items() if peer != q}
                    for vp, new_p, wp in merge(p, resident, reply, extra, capacity):
                        for vq, new_q, wq in merge(q, passive, request, reply_ids, capacity):
                            result = caches.copy()
                            result[p], result[q] = new_p, new_q
                            yield (p, q, extra, reply_ids, vp, vq), key(result), wp * wq / denominator


def sign(value):
    return (value > 0) - (value < 0)


def arithmetic_checks():
    comparisons = 0
    for horizon in range(5):
        for gaps in product((1, 2, horizon + 1, horizon + 2, 10**6), repeat=3):
            levels = [0]
            for gap in gaps:
                levels.append(levels[-1] + gap)
            state = (tuple(enumerate(levels)),)
            small = [age for _, age in compress(state, horizon)[0]]
            assert max(small) <= 3 * (horizon + 1)
            for i, j, offset_i, offset_j in product(range(4), range(4), range(horizon + 1), range(horizon + 1)):
                assert sign(levels[i] + offset_i - levels[j] - offset_j) == sign(small[i] + offset_i - small[j] - offset_j)
                comparisons += 1
    return comparisons


def trajectory_checks():
    starts = pairs = branch_count = 0
    for n in range(2, 6):
        for capacity in range(1, min(3, n - 1) + 1):
            for length in range(1, capacity + 1):
                horizon = 3 if n <= 4 else 2
                for mode in range(3):
                    ages = ((0,), (0, 1, 10**6, 10**6 + 1), (10**6, 10**6 + 2, 2 * 10**6))[mode]
                    caches = []
                    for p in range(n):
                        size = capacity if mode != 2 else (0 if p == n - 1 else 1 + p % capacity)
                        caches.append({(p + j + 1) % n: ages[(p * capacity + j) % len(ages)] for j in range(size)})
                    initial = key(caches)
                    small = compress(initial, horizon)
                    age_map = reachable_age_map(initial, horizon)
                    assert map_state_ages(initial, age_map) == small
                    assert max((age for row in small for _, age in row), default=0) <= n * capacity * (horizon + 1)
                    frontier = {(initial, small)}
                    starts += 1
                    for _ in range(horizon):
                        following = set()
                        for original, compressed in frontier:
                            left = list(branches(original, capacity, length))
                            right = list(branches(compressed, capacity, length))
                            assert sum(w for _, _, w in left) == sum(w for _, _, w in right) == 1
                            assert len(left) == len(right)
                            for (choice, successor, probability), (other_choice, other_successor, other_probability) in zip(left, right):
                                assert choice == other_choice and probability == other_probability
                                assert tuple(tuple(peer for peer, _ in row) for row in successor) == tuple(tuple(peer for peer, _ in row) for row in other_successor)
                                assert map_state_ages(successor, age_map) == other_successor
                                following.add((successor, other_successor))
                                branch_count += 1
                            pairs += 1
                        frontier = following
    return starts, pairs, branch_count


def independent_kernel_check():
    for gap in (1, 2):
        state = key(({1: 10**6 + 4, 2: 10**6}, {0: 0, 3: 10**6 + gap}, {}, {}))
        expected = defaultdict(Fraction)
        actual = defaultdict(Fraction)
        for successor, weight in four_peer_outcomes(state):
            expected[successor] += weight
        for _, successor, weight in branches(state, 2, 2):
            actual[successor] += weight
        assert dict(expected) == dict(actual)
        # The critical unit-vs-two gap remains distinct at horizon two.
        assert compress(state, 2)[1][1][1] == 3 + gap


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    independent_kernel_check()
    print('PASS arithmetic offset comparisons:', arithmetic_checks())
    print('PASS coupled starts / state pairs / branches:', trajectory_checks())
    print('Scope: finite corroboration of the symbolic arbitrary-size, fixed-horizon lemma; no mixing-rate certificate.')


if __name__ == '__main__':
    main()
