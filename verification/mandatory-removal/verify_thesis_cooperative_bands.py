#!/usr/bin/env python3
"""Exact controlled-path checks for unit-width full-shuffle callback bands.

Every old zero holder shares c-2 secondary identities, each in its own
adjacent-age pair {m_p,m_p+1}; the owner's secondary ages are >=m_p.
This checks a conditional lemma, not accessibility of its hypotheses.
Seeded starts and all arithmetic/transitions are exact, not a Monte Carlo
estimate of ordinary execution probabilities. See the linked research note.
"""
from collections import Counter
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros, holder_count


def construct(z, a, secondary, zero_holders, lower, rng):
    P, I = set(secondary), set(zero_holders)
    anchors = P | {a}
    assert z.ell == z.c >= 3 and len(P) == z.c - 2
    assert set(lower) == P and all(m >= 0 for m in lower.values())
    assert P.isdisjoint(I | {a}) and zeros(z, a) == I
    assert all(z.x[a].get(p, -1) >= lower[p] for p in P)
    original = [row.copy() for row in z.x]
    initial_holders = holder_count(z, a)
    blocks = 0

    def invariants():
        assert zeros(z, a) == I
        assert holder_count(z, a) == initial_holders
        assert all(z.x[v].get(p) in (lower[p], lower[p] + 1) for v in I for p in P)
        assert all(z.x[a].get(p, -1) >= lower[p] for p in P)

    invariants()
    while True:
        oldest = [v for v in z.x[a] if z.x[a][v] == max(z.x[a].values())]
        outside = [v for v in oldest if v not in I]
        q = rng.choice(outside or oldest)
        if q not in I:
            z.step(a, q, set(z.x[a]) - {q}, set(z.x[q]))
            z.owner_steps += 1
            assert zeros(z, a) == I | {q}
            assert holder_count(z, a) >= initial_holders
            assert all(z.x[v] == original[v] for v in range(z.n) if v not in I | {a, q})
            break

        frozen_owner = z.x[a].copy()
        preparation_steps = 0
        while True:
            residual = set(z.x[q]) - anchors
            assert len(residual) <= 1
            if not residual:
                break
            r = next(iter(residual))
            if r not in I or z.x[q][r] < max(z.x[q][p] for p in P):
                break
            before = [row.copy() for row in z.x]
            # Full requests/replies are forced. Independent residual update:
            expected_q = {p: min(before[q][p] + 1, before[r][p]) for p in anchors}
            expected_r = dict(expected_q)
            for peer, age in before[r].items():
                if peer not in anchors and peer != q:
                    expected_q[peer] = age
            expected_r[q] = 0
            z.step(q, r, anchors, set(before[r]))
            assert z.x[q] == expected_q and z.x[r] == expected_r
            preparation_steps += 1
            z.residual_steps += 1
            assert preparation_steps <= len(I)
            assert z.x[a] == frozen_owner
            invariants()

        new_inside = {v: age for v, age in z.x[q].items() if v not in anchors and v in I}
        reply_vector = {p: z.x[q][p] for p in P}
        old_heads = set(z.x[a]) - {q}
        z.step(a, q, old_heads, set(z.x[q]))
        z.owner_steps += 1
        assert all(z.x[a][p] == z.x[q][p] == reply_vector[p] for p in P)
        assert old_heads <= set(z.x[a])  # Mandatory deletion is the only active removal.
        for v, age in new_inside.items():
            # A duplicate may already be cached; MIN can only lower its age.
            assert z.x[a][v] <= age < max(z.x[a][p] for p in P)
        blocks += 1
        assert blocks <= 3
        invariants()

    assert z.owner_steps == blocks + 1
    assert z.steps <= 3 * (len(I) + 1) + 1
    return blocks


def trial(n, c, seed):
    rng = Random(seed)
    order = list(range(n))
    rng.shuffle(order)
    a = order[0]
    P = set(order[1:c - 1])
    remaining = order[c - 1:]
    I = set(rng.sample(remaining, rng.randint(1, len(remaining))))
    lower = {p: rng.choice((0, 1, 2, 5, 10**6)) for p in sorted(P)}
    M = max(lower.values())
    anchors = P | {a}
    rows = []
    for v in range(n):
        pool = sorted(set(range(n)) - {v})
        row = {peer: rng.randint(1, 9) for peer in rng.sample(pool, rng.randint(0, min(c, len(pool))))}
        if v in I:
            row = {a: 0, **{p: lower[p] + rng.randrange(2) for p in sorted(P)}}
            residual_pool = sorted(set(range(n)) - anchors - {v})
            if residual_pool and rng.randrange(4):
                row[rng.choice(residual_pool)] = rng.choice((0, max(0, M - 1), M, M + 1, M + 10**6))
        rows.append(row)
    rows[a] = {p: lower[p] + rng.randint(0, 2) for p in sorted(P)}
    for q in rng.sample(sorted(I), min(2, len(I))):
        rows[a][q] = M + rng.randint(1, 10)
    z = ActualThree(rows, c, c)
    return construct(z, a, P, I, lower, rng), z


def regression():
    rows = [{1: 1, 2: 3, 3: 3}, {}, {0: 0, 1: 2, 4: 1},
            {0: 0, 1: 1, 5: 0}, {0: 0, 1: 1}, {0: 0, 1: 1}]
    class FirstChoice:
        @staticmethod
        def choice(items):
            return min(items)
    z = ActualThree(rows, 3, 3)
    assert construct(z, 0, {1}, {2, 3, 4, 5}, {1: 1}, FirstChoice()) == 3
    assert z.steps == 4 and z.residual_steps == 0
    # No second residual does NOT imply immediate termination: the first
    # returned head aged once while the owner secondary reset downward.
    rows[3] = {0: 0, 1: 1}
    z = ActualThree(rows, 3, 3)
    assert construct(z, 0, {1}, {2, 3, 4, 5}, {1: 1}, FirstChoice()) == 3
    assert z.steps == 4 and z.residual_steps == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=14)
    parser.add_argument('--seeds', type=int, default=100)
    args = parser.parse_args()
    if not __debug__:
        parser.error('assertions must be enabled')
    regression()
    histogram = Counter()
    exchanges = preparations = longest = 0
    for n in range(4, args.max_n + 1):
        for c in range(3, n):
            for seed in range(args.seeds):
                blocks, z = trial(n, c, n * 100000 + c * 1000 + seed)
                histogram[blocks] += 1
                exchanges += z.steps
                preparations += z.residual_steps
                longest = max(longest, z.steps)
    print('PASS two explicit three-macro regressions')
    print('PASS cases/exchanges/preparation/longest:',
          sum(histogram.values()), exchanges, preparations, longest)
    print('Nonfinishing macro histogram:', dict(sorted(histogram.items())))
    print('Scope: finite corroboration of a conditional symbolic lemma, not generic convergence.')


if __name__ == '__main__':
    main()
