#!/usr/bin/env python3
"""Exact affine cycle refuting universal oldest-first two-head coalescence.

The independent abstract update is checked against ActualThree at every
step of two periods, with n=7 and c=ell=3. No random sampling is used.
See docs/research/OLDEST-POINTER-CYCLE.md for the scope and argument.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree

ACTIONS = (
    1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1,
    1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1,
)
INITIAL_HEADS = (0, 1)
INITIAL_HEAD_AGES = (1, 1)
INITIAL_POINTERS = (1, 2, 3, 4, 0)
INITIAL_POINTER_AGES = (0, 0, 1, 1, 1)
SHIFT = 12


def embedded(heads, ages, pointers, pointer_ages):
    """Owner 0, secondary 1, abstract vertex v maps to peer v+2."""
    return [
        {1: 0, **{v + 2: t for v, t in zip(heads, ages)}},
        {},
        *[{0: 0, 1: 0, r + 2: t}
          for r, t in zip(pointers, pointer_ages)],
    ]


def main():
    heads, ages = list(INITIAL_HEADS), list(INITIAL_HEAD_AGES)
    pointers, pointer_ages = list(INITIAL_POINTERS), list(INITIAL_POINTER_AGES)
    z = ActualThree(embedded(heads, ages, pointers, pointer_ages), 3, ell=3)
    assert len(ACTIONS) == 72 and len(z.x) == 7
    # Connectedness is immediate from every I row containing owner 0 and
    # secondary 1. Check the actual graph too, rather than relying on prose.
    reached = {0}
    while True:
        enlarged = reached | {v for u, row in enumerate(z.x) for v in row
                              if u in reached} | {u for u, row in enumerate(z.x)
                                                   if reached.intersection(row)}
        if enlarged == reached:
            break
        reached = enlarged
    assert reached == set(range(7))

    for period in range(1, 3):
        strict = ties = 0
        for choice in ACTIONS:
            other = 1 - choice
            assert ages[choice] >= ages[other]
            strict += ages[choice] > ages[other]
            ties += ages[choice] == ages[other]
            q, s = heads[choice], heads[other]
            r, C = pointers[q], pointer_ages[q]
            assert r not in (q, s)  # neither self-pointer nor coalescence
            B = ages[other]
            # This uses the existing protected/MIN protocol implementation.
            actual_q = q + 2
            z.step(0, actual_q, set(z.x[0]) - {actual_q}, set(z.x[actual_q]))
            new = {s: B + 1, r: C}
            heads = sorted(new)
            ages = [new[v] for v in heads]
            pointers[q], pointer_ages[q] = s, B + 1
            assert z.x == embedded(heads, ages, pointers, pointer_ages)
        assert strict == 48 and ties == 24
        assert tuple(heads) == INITIAL_HEADS
        assert tuple(pointers) == INITIAL_POINTERS
        assert ages == [t + SHIFT * period for t in INITIAL_HEAD_AGES]
        assert pointer_ages == [t + SHIFT * period for t in INITIAL_POINTER_AGES]
        print(f'PASS period {period}: 72 exchanges, 48 strict oldest choices, '
              f'24 ties, all seven residual/root ages shifted by {SHIFT * period}')
    assert z.steps == 144
    print('PASS exact abstract/protected-MIN agreement at all 144 exchanges; '
          'n=7, c=ell=3, connected start')


if __name__ == '__main__':
    main()
