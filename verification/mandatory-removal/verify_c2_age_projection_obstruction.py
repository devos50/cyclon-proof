#!/usr/bin/env python3
"""Exact four-peer obstruction to absolute-age capping plus age ranks.

For any fixed cap B, take K>B and two connected initial states differing
only in C_q's positive age K+1 versus K+2. They have identical capped ages
and identical GLOBAL age ranks/equalities, but their two-event one-ID query
laws differ by exactly TV=1/32 under the original uniform scheduler.

This disproves that particular proposed exact finite projection on all
arbitrary-age starts. It does NOT prove no finite query-sufficient
projection exists, nor that four-peer recurrent ages are unbounded.

All transition probabilities and query laws below are exact Fractions.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_anchor import Actual


def key(caches):
    return tuple(tuple(sorted(row.items())) for row in caches)


def outcomes(state):
    caches = [dict(row) for row in state]
    for initiator, active in enumerate(caches):
        if not active:
            yield state, Fraction(1, 4)
            continue
        oldest = [peer for peer in active if active[peer] == max(active.values())]
        for partner in oldest:
            passive = caches[partner]
            extras = set(active) - {partner}
            incoming = {initiator} | extras
            needed = max(0, len(passive) + len(incoming - set(passive)) - 2)
            eligible = set(passive) - incoming
            for victims in combinations(eligible, needed):
                actual = Actual(caches, 2)
                actual.step(initiator, partner, extras, passive, vq=victims)
                yield key(actual.x), Fraction(1, 4 * len(oldest) * comb(len(eligible), needed))


def two_event_query(state):
    law = {state: Fraction(1)}
    for _ in range(2):
        following = defaultdict(Fraction)
        for current, mass in law.items():
            for successor, probability in outcomes(current):
                following[successor] += mass * probability
        law = dict(following)
    query = defaultdict(Fraction)
    for current, mass in law.items():
        row = current[0]
        if not row:
            query[None] += mass
        else:
            for peer, _ in row:
                query[peer] += mass / len(row)
    assert sum(query.values()) == 1
    return dict(query)


def capped(state, bound):
    return tuple(tuple((peer, min(age, bound)) for peer, age in row) for row in state)


def ranks(state):
    order = {age: i for i, age in enumerate(sorted({age for row in state for _, age in row}))}
    return tuple(tuple((peer, order[age]) for peer, age in row) for row in state)


def main():
    for base_age in (1, 100, 10**6):
        bound = base_age - 1
        states = [
            key(({1: base_age + 4, 2: base_age}, {0: 0, 3: base_age + gap}, {}, {}))
            for gap in (1, 2)
        ]
        assert capped(states[0], bound) == capped(states[1], bound)
        assert ranks(states[0]) == ranks(states[1])
        laws = [two_event_query(state) for state in states]
        assert laws[0] == {1: Fraction(9, 32), 2: Fraction(1, 2), 3: Fraction(7, 32)}
        assert laws[1] == {1: Fraction(9, 32), 2: Fraction(17, 32), 3: Fraction(3, 16)}
        distance = sum(abs(laws[0].get(peer, 0) - laws[1].get(peer, 0)) for peer in {None, 1, 2, 3}) / 2
        assert distance == Fraction(1, 32)
        print(f'Cap={bound}, K={base_age}: same capped ages and ranks; exact query TV={distance}')
    print('PASS: specific cap-plus-rank projection fails; no general finite-projection impossibility is asserted.')


if __name__ == '__main__':
    main()
