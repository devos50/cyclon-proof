#!/usr/bin/env python3
"""Finite exact controlled checks of the learned-anchor c=ell=3 callback.

Owner a caches p outside a chosen subset I of its zero-holder set. Other zero holders need
not cache p, and all numerical ages are arbitrary. A clearing plan is
simulated on a copy and executed only if every step is legal and it clears.
Failed hypothetical preparations do not change the actual trajectory.
These seeded cases corroborate a symbolic qualitative termination argument;
they are not an exhaustive proof, random mixing experiment, or generic
convergence certificate. The mathematical proof is qualitative and has been independently reviewed.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros, holder_count


def clearing_plan(z, q, a, p, learned):
    if q not in learned:
        return None
    trial = ActualThree(z.x, 3, 3)
    partners = []
    for _ in range(len(learned) + 1):
        residual = set(trial.x[q]) - {a, p}
        assert len(residual) <= 1
        if not residual:
            return partners
        r = next(iter(residual))
        if r not in learned or trial.x[q][r] < trial.x[q][p]:
            return None
        trial.step(q, r, {a, p}, set(trial.x[r]))
        partners.append(r)
    raise AssertionError('Legal Q-only path did not clear within finite learned set')


def owner_step(z, a, q, p):
    resident = set(z.x[a]) - {q}
    reply = set(z.x[q])
    new = reply - resident - {a}
    needed = max(0, len(resident) + len(new) - 3)
    eligible = resident - reply - {p}
    assert needed <= len(eligible), (z.x, a, q, p, needed, eligible)
    z.step(a, q, resident, reply, vp=set(sorted(eligible)[:needed]))
    assert p in z.x[a]


def construct(z, a, p, rng, limit=20000, boundary_set=None):
    original_zeros = zeros(z, a)
    I = original_zeros if boundary_set is None else set(boundary_set)
    assert I <= original_zeros
    assert z.c == z.ell == 3 and p in z.x[a] and p not in I | {a}
    original = [row.copy() for row in z.x]
    initial_holders = holder_count(z, a)
    learned = {q for q in I if p in z.x[q]}
    metrics = Counter()
    while z.steps < limit:
        oldest = [q for q, age in z.x[a].items() if age == max(z.x[a].values())]
        outside = [q for q in oldest if q not in I]
        q = rng.choice(outside or oldest)
        if q not in I:
            if q != p and a in z.x[q]:
                owner_step(z, a, q, p)
            else:
                z.step(a, q, set(z.x[a]) - {q}, set(z.x[q]))
            assert zeros(z, a) == original_zeros | {q}
            assert holder_count(z, a) >= initial_holders
            assert all(z.x[v] == original[v] for v in range(z.n) if v not in I | {a, q})
            metrics['final'] += 1
            return metrics
        plan = clearing_plan(z, q, a, p, learned)
        old_head_count = len(set(z.x[a]) & I)
        old_learned = learned.copy()
        if plan is not None:
            frozen = z.x[a].copy()
            for r in plan:
                z.step(q, r, {a, p}, set(z.x[r]))
                assert z.x[a] == frozen and zeros(z, a) == original_zeros
                assert all(p in z.x[v] for v in learned)
                assert holder_count(z, a) == initial_holders
            assert set(z.x[q]) == {a, p}
            metrics['clearings'] += 1
            metrics['preparation_steps'] += len(plan)
        owner_step(z, a, q, p)
        metrics['owner_steps'] += 1
        assert zeros(z, a) == original_zeros and holder_count(z, a) == initial_holders
        learned = {v for v in I if p in z.x[v]}
        assert old_learned <= learned and q in learned
        new_head_count = len(set(z.x[a]) & I)
        if new_head_count > old_head_count:
            assert q not in old_learned and learned > old_learned
            metrics['charged_head_increases'] += 1
        if plan is not None:
            assert new_head_count == old_head_count - 1
        metrics['learned_new'] += len(learned - old_learned)
    raise AssertionError('Finite test resource guard reached; not a proven horizon')


def trial(n, seed):
    rng = Random(seed)
    a, p = 0, 1
    I = set(rng.sample(list(range(2, n)), rng.randint(0, n - 2)))
    ages = (0, 1, 2, 5, 11, 10**6)
    rows = []
    for v in range(n):
        if v == a:
            rows.append({})
            continue
        if v in I:
            row = {a: 0}
        elif v == p or rng.randrange(2):
            row = {a: rng.choice((1, 2, 10**6))}
        else:
            # Genuine nonholder, connected through p's positive a-copy.
            row = {p: rng.choice(ages)}
        candidates = sorted(set(range(n)) - {a, v} - set(row))
        for peer in rng.sample(candidates, rng.randint(0, min(2, len(candidates)))):
            row[peer] = rng.choice(ages)
        rows.append(row)
    rows[a] = {p: rng.choice(ages)}
    for peer in rng.sample(list(range(2, n)), rng.randint(0, min(2, n - 2))):
        rows[a][peer] = rng.choice(ages)
    if seed % 3 == 0:
        rows[p][a] = 0
        I.add(p)
    z = ActualThree(rows, 3, 3)
    assert zeros(z, a) == I
    eligible_boundary = I - {p}
    boundary = set(rng.sample(sorted(eligible_boundary), rng.randint(0, len(eligible_boundary)))) if seed % 2 else eligible_boundary
    return construct(z, a, p, rng, boundary_set=boundary), z.steps


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    total = Counter()
    cases = exchanges = longest = 0
    for n in range(4, 21):
        for seed in range(300):
            metrics, steps = trial(n, 100000 * n + seed)
            total.update(metrics)
            cases += 1
            exchanges += steps
            longest = max(longest, steps)
    print('PASS learned callback cases/exchanges/longest:', cases, exchanges, longest)
    print('Exact structural assertions:', dict(sorted(total.items())))
    print('Scope: finite corroboration only; owner-cached target outside the chosen zero-holder boundary is assumed.')


if __name__ == '__main__':
    main()
