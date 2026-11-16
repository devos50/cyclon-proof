#!/usr/bin/env python3
"""Check the c=ell=3 one-I-head callback with arbitrary shared p ages.

The finite seeded cases corroborate a symbolic, age-dependent conditional
termination proof. They are not a mixing simulation or generic certificate.
"""
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros, holder_count


def construct(z, a, p, I, rng):
    I = set(I)
    anchors = {a, p}
    assert z.c == z.ell == 3 and zeros(z, a) == I
    assert p not in I | {a} and p in z.x[a]
    assert all(p in z.x[v] for v in I)
    assert len(set(z.x[a]) & I) <= 1
    u0 = z.x[a][p]
    maximum = max(z.x[v][p] for v in I | {a})
    initial_maximum = maximum
    old_holders = holder_count(z, a)
    blocks = 0
    while True:
        oldest = [v for v in z.x[a] if z.x[a][v] == max(z.x[a].values())]
        outside = [v for v in oldest if v not in I]
        q = rng.choice(outside or oldest)
        if q not in I:
            z.step(a, q, set(z.x[a]) - {q}, set(z.x[q]))
            assert zeros(z, a) == I | {q}
            assert holder_count(z, a) >= old_holders
            break
        frozen = z.x[a].copy()
        steps = 0
        while True:
            residual = set(z.x[q]) - anchors
            assert len(residual) <= 1
            if not residual:
                break
            r = next(iter(residual))
            if r not in I or z.x[q][r] < z.x[q][p]:
                break
            value = min(z.x[q][p] + 1, z.x[r][p])
            z.step(q, r, anchors, set(z.x[r]))
            steps += 1
            assert steps <= len(I)
            assert z.x[q][p] == z.x[r][p] == value
            assert z.x[a] == frozen
            assert zeros(z, a) == I
            assert max(z.x[v][p] for v in I | {a}) <= maximum
            maximum = max(z.x[v][p] for v in I | {a})
        u, v = z.x[a][p], z.x[q][p]
        inside = {r: age for r, age in z.x[q].items() if r not in anchors and r in I}
        assert all(age < v for age in inside.values())
        z.step(a, q, set(z.x[a]) - {q}, set(z.x[q]))
        assert z.x[a][p] == z.x[q][p] == min(u + 1, v)
        assert zeros(z, a) == I and holder_count(z, a) == old_holders
        assert len(set(z.x[a]) & I) <= 1
        assert max(z.x[v][p] for v in I | {a}) <= maximum
        maximum = max(z.x[v][p] for v in I | {a})
        blocks += 1
        assert blocks <= initial_maximum - u0 + 1
        oldest = {v for v in z.x[a] if z.x[a][v] == max(z.x[a].values())}
        if oldest <= I:
            assert z.x[a][p] == u + 1
    assert z.steps <= (initial_maximum - u0 + 1) * (len(I) + 1) + 1
    return blocks


def trial(n, seed, large=False):
    rng = Random(seed)
    a, p = 0, 1
    I = set(rng.sample(list(range(2, n)), rng.randint(1, n - 2)))
    row_ages = (0, 1, 2, 7, 11, 10**6) if large else (0, 1, 2, 7, 11)
    rows = []
    for v in range(n):
        pool = sorted(set(range(n)) - {v})
        row = {peer: rng.randint(1, 12) for peer in rng.sample(pool, rng.randint(0, min(3, len(pool))))}
        if v in I:
            row = {a: 0, p: rng.choice(row_ages)}
            residual = sorted(set(range(n)) - {a, p, v})
            if residual and rng.randrange(4):
                row[rng.choice(residual)] = rng.choice(row_ages)
        rows.append(row)
    rows[a] = {p: rng.choice(row_ages), rng.choice(sorted(I)): 10**6 + 2}
    other = sorted(set(range(n)) - I - {a, p})
    if other and rng.randrange(2):
        rows[a][rng.choice(other)] = rng.choice(row_ages)
    z = ActualThree(rows, 3, 3)
    return construct(z, a, p, I, rng), z.steps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=15)
    parser.add_argument('--seeds', type=int, default=100)
    args = parser.parse_args()
    if not __debug__:
        parser.error('assertions must be enabled')
    cases = exchanges = longest = most_blocks = 0
    for n in range(4, args.max_n + 1):
        for seed in range(args.seeds):
            for large in (False, True):
                blocks, steps = trial(n, n * 100000 + seed, large)
                cases += 1
                exchanges += steps
                longest = max(longest, steps)
                most_blocks = max(most_blocks, blocks)
    print('PASS cases/exchanges/longest/most-macros:', cases, exchanges, longest, most_blocks)
    print('Scope: scalar c=ell=3, at most one owner I head; initial-age-dependent bound.')


if __name__ == '__main__':
    main()
