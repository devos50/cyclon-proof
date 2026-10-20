#!/usr/bin/env python3
"""Exact owner-only service for proper shuffles and large zero-holder caches.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_proper_owner.py

For 3<=ell<c, every old zero-holder cache initially has at least ell+1
entries. Owner a caches nonzero-a target p. Every preterminal reply includes
a and excludes p; active victims are chosen among other sent extras to
retain p. The checker asserts exact target-age growth, passive largeness,
all old zeros, and every global virtual-age inequality at every step.
The first outside-zero-holder contact adds a fresh zero without reducing
the total a-holder count. No shared target age or shared residual IDs are
assumed. Numeric transitions use the general exact protected+MIN kernel.

Default cases: n=5,...,15, every 3<=ell<c<=n-1, three seeds, offsets0 and
1,000,000 with independently varied nonanchor gaps0,...,8. Bounded gaps
keep this check quick: arbitrary large target-age deficits can require
long owner-only trajectories, as allowed by the age-dependent proof.
These checks corroborate the conditional lemma, not its general bootstrap.

Reproduced default result: 1,716 cases, 7,734 exact exchanges, longest
trajectory 11. Branches: 6,018 preterminal internal exchanges; 1,470
protected-target replacement choices; 640 target terminals and 1,076
other nonzero terminals.
"""
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros, holder_count


def maxima(z):
    return [max(row.get(s, 0) for row in z.x) for s in range(z.n)]


def construct(z, a, p, I, counts):
    I = set(I)
    assert 3 <= z.ell < z.c and zeros(z, a) == I
    assert p in z.x[a] and p not in I | {a}
    assert all(len(z.x[v]) >= z.ell + 1 for v in I)
    A = z.x[a][p]
    H = holder_count(z, a)
    initial_maxima = maxima(z)
    budget = sum(max(0, initial_maxima[s] - A + 1) for s in I)
    selected_counts = dict.fromkeys(I, 0)
    before_outside = [row.copy() for row in z.x]
    while True:
        t = z.steps
        top = max(z.x[a].values())
        candidates = [v for v in z.x[a] if z.x[a][v] == top]
        outside = [v for v in candidates if v not in I]
        q = min(outside if outside else candidates)
        before = maxima(z)
        source = set(z.x[a])
        required = min(z.ell - 1, len(source) - 1)
        if q not in I:
            extra = sorted(source - {q})[:required]
            reply = sorted(z.x[q])[:min(z.ell, len(z.x[q]))]
            z.step(a, q, extra, reply)
            assert zeros(z, a) == I | {q} and holder_count(z, a) >= H
            assert all(z.x[v] == before_outside[v] for v in range(z.n) if v not in I | {a, q})
            counts['terminal_target' if q == p else 'terminal_other'] = counts.get('terminal_target' if q == p else 'terminal_other', 0) + 1
            break
        assert z.x[a][p] == A + t and before[q] - t >= A
        extra = [p] + sorted(source - {q, p})[:required - 1]
        assert len(extra) == required
        other = sorted(set(z.x[q]) - {a, p})
        assert len(other) >= z.ell - 1
        reply = [a] + other[:z.ell - 1]
        assert p not in reply
        remaining = source - {q}
        usable = set(reply) - remaining - {a}
        needed = max(0, len(remaining) + len(usable) - z.c)
        eligible = set(extra) - set(reply) - {p}
        assert len(eligible) >= needed
        victims = sorted(eligible)[:needed]
        if victims:
            counts['protected_target_replacements'] = counts.get('protected_target_replacements', 0) + len(victims)
        z.step(a, q, extra, reply, vp=victims)
        after = maxima(z)
        assert all(v <= u + 1 for u, v in zip(before, after))
        assert after[q] <= before[q]
        assert z.x[a][p] == A + z.steps
        assert zeros(z, a) == I and holder_count(z, a) == H
        assert all(len(z.x[v]) >= z.ell + 1 for v in I)
        selected_counts[q] += 1
        assert selected_counts[q] <= max(0, initial_maxima[q] - A + 1)
        assert z.steps <= budget
        counts['internal_events'] = counts.get('internal_events', 0) + 1
    assert z.steps <= budget + 1


def trial(n, c, ell, seed, offset, counts):
    rng = Random(seed)
    order = list(range(n))
    rng.shuffle(order)
    a, p = order[:2]
    I = set(rng.sample(order[2:], rng.randint(1, n - 2)))
    x = [{} for _ in range(n)]
    for v in range(n):
        if v in I:
            pool = sorted(set(range(n)) - {a, v})
            size = rng.randint(ell + 1, c)
            chosen = rng.sample(pool, size - 1)
            x[v] = {a: 0, **{q: offset + rng.randrange(9) for q in chosen}}
        elif v != a:
            pool = sorted(set(range(n)) - {v})
            chosen = rng.sample(pool, rng.randrange(min(c, len(pool)) + 1))
            x[v] = {q: offset + rng.randint(1 if q == a else 0, 8) for q in chosen}
    heads = rng.sample(sorted(I), min(c - 1, len(I)))
    remaining = sorted(set(range(n)) - I - {a, p})
    other_count = min(c - 1 - len(heads), len(remaining))
    other = rng.sample(remaining, other_count)
    x[a] = {p: offset, **{q: offset + rng.randint(1, 8) for q in heads}, **dict.fromkeys(other, offset)}
    z = ActualThree(x, c, ell)
    construct(z, a, p, I, counts)
    return z


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=15)
    ap.add_argument('--seeds', type=int, default=3)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled; do not use python -O')
    cases = exchanges = longest = 0
    counts = {}
    for n in range(5, args.max_n + 1):
        for c in range(4, n):
            for ell in range(3, c):
                for seed in range(args.seeds):
                    for offset in (0, 1000000):
                        z = trial(n, c, ell, 1000003*n+7919*c+101*ell+seed, offset, counts)
                        cases += 1
                        exchanges += z.steps
                        longest = max(longest, z.steps)
    print('PASS cases/exchanges/longest', (cases, exchanges, longest), 'branches', counts)


if __name__ == '__main__':
    main()
