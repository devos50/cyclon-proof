#!/usr/bin/env python3
"""Exact ell=3,c>=4 empty-owner terminal gadget and callback completion.

Finite controlled checks; no stochastic time bound or convergence claim.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros, holder_count
from verify_length_three_arbitrary_capacity_callback import construct


def terminal(z, a, p, r, rng):
    assert z.ell == 3 and z.c >= 4 and not z.x[a]
    assert a in z.x[p] and r in z.x[p] and a not in z.x[r]
    assert z.x[p][a] == max(z.x[p].values())
    original = [dict(row) for row in z.x]
    initial_holders = {v for v, row in enumerate(z.x) if a in row}
    initial_zeros = zeros(z, a)
    E = set(z.x[p]) - {a}
    s = min(E, key=lambda v: (-z.x[p][v], v))
    t = r if s != r else min(E - {s}, default=None)
    first_extras = {s} | ({t} if t is not None else set())
    was_holder = a in z.x[s]
    stats = Counter()
    z.step(p, a, first_extras, set())
    assert a not in z.x[p]
    assert set(z.x[a]) == {p} | first_extras
    second_extras = set(z.x[a]) - {s}
    reply = ({a} if was_holder else set())
    reply |= set(sorted(set(z.x[s]) - reply)[:min(3, len(z.x[s])) - len(reply)])
    z.step(a, s, second_extras, reply)
    assert z.x[s][a] == 0 and p in z.x[s]
    if was_holder:
        assert r in z.x[a] and t == r
    if t is not None:
        assert t in z.x[s]
    # Frozen p still has s as an oldest residual, even when initially full.
    extras = ({t} if t is not None else set())
    available = sorted(set(z.x[p]) - {s} - extras)
    extras |= set(available[:min(2, len(z.x[p]) - 1) - len(extras)])
    incoming_s = {p} | extras
    novel = incoming_s - set(z.x[s])
    assert len(novel) <= 1
    need = max(0, len(z.x[s]) + len(novel) - z.c)
    if need:
        # p and t already reside at s; the only possible novel identity is u.
        choices = sorted(set(z.x[s]) - {a, p} - incoming_s)
        assert choices
        x = choices[0]
        reply = {a, p, x}
        victim = {x}
        stats['protected_a_replacement'] += 1
    else:
        reply = {a, p}
        reply |= set(sorted(set(z.x[s]) - reply)[:min(3, len(z.x[s])) - 2])
        victim = set()
    z.step(p, s, extras, reply, vp=set(), vq=victim)
    assert z.x[p][a] == z.x[s][a] == 0
    assert initial_zeros <= zeros(z, a)
    assert all(z.x[v] == original[v] for v in range(z.n) if v not in {a, p, s})
    restored = {v for v, row in enumerate(z.x) if a in row}
    assert restored == initial_holders | {s}
    if was_holder:
        assert r in z.x[a] and a not in z.x[r]
        stats['holder_prefix'] += 1
        while holder_count(z, a) == len(initial_holders):
            construct(z, a, r, zeros(z, a), rng, guard=z.steps + 100000)
            if holder_count(z, a) == len(initial_holders):
                assert r in z.x[a] and a not in z.x[r]
        stats['callback_completion'] += 1
    else:
        stats['nonholder_triangle'] += 1
    assert initial_holders < {v for v, row in enumerate(z.x) if a in row}
    return stats


def trial(n, c, size, seed):
    rng = Random(seed)
    a, p, r = 0, 1, 2
    ages = (0, 1, 7, 10**6)
    x = [{} for _ in range(n)]
    chosen = [r] + rng.sample(list(range(3, n)), size - 2)
    x[p] = {a: 10**6, **{v: rng.choice(ages) for v in chosen}}
    for v in range(2, n):
        x[v] = {p: rng.choice(ages)}
        if v != r and rng.randrange(2):
            x[v][a] = rng.choice(ages)
        choices = sorted(set(range(n)) - {a, v} - set(x[v]))
        maximum = min(c, len(x[v]) + len(choices))
        target = maximum if seed % 3 == 0 else rng.randint(len(x[v]), maximum)
        for u in rng.sample(choices, target - len(x[v])):
            x[v][u] = rng.choice(ages)
    z = ActualThree(x, c, 3)
    return terminal(z, a, p, r, rng), z.steps


def main():
    total = Counter()
    cases = events = longest = 0
    for n in range(5, 16):
        for c in range(4, n):
            for size in range(2, c + 1):
                for seed in range(20):
                    stats, steps = trial(n, c, size, n * 100000 + c * 1000 + size * 50 + seed)
                    total.update(stats)
                    cases += 1
                    events += steps
                    longest = max(longest, steps)
    assert total['protected_a_replacement'] > 0
    assert total['holder_prefix'] > 0 and total['nonholder_triangle'] > 0
    print('PASS ell=3,c>=4 terminal cases/events/longest:', cases, events, longest)
    print('Exact branch counts:', dict(sorted(total.items())))
    print('Scope: local gadget plus candidate callback; finite exact corroboration.')


if __name__ == '__main__':
    main()
