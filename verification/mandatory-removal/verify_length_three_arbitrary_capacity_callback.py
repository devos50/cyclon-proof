#!/usr/bin/env python3
"""Exact controlled tests of the candidate ell=3 arbitrary-capacity callback.

Finite tests only; not a convergence certificate or a proven numeric horizon.
Hypothetical clearing plans do not alter the actual state unless accepted.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros, holder_count


def retain_step(z, a, q, p, extras, reply):
    resident = set(z.x[a]) - {q}
    needed = max(0, len(resident) + len(set(reply) - resident - {a}) - z.c)
    eligible = set(extras) - set(reply) - {p}
    assert needed <= len(eligible)
    z.step(a, q, extras, reply, vp=set(sorted(eligible)[:needed]))
    assert p in z.x[a]


def plan(z, Q, a, p, learned, partial):
    if Q not in learned:
        return None
    trial = ActualThree(z.x, z.c, 3)
    moves = []
    bound = (len(learned) + 1) * (z.c - 2)
    for _ in range(bound + 1):
        residual = set(trial.x[Q]) - {a, p}
        if not residual:
            return moves
        maximum = max(trial.x[Q][v] for v in residual)
        if maximum < trial.x[Q][p]:
            return moves if partial else None
        r = min(v for v in residual if trial.x[Q][v] == maximum)
        if r not in learned:
            return None
        other = set(trial.x[r]) - {a, p}
        C = Q if Q in other else min(other, default=None)
        reply = {a, p} | ({C} if C is not None else set())
        before = [dict(row) for row in trial.x]
        trial.step(Q, r, {a, p}, reply)
        # Independent singleton residual update at both endpoints.
        eq = {v: t + 1 for v, t in before[Q].items() if v not in {a, p, r}}
        if C is not None and C != Q:
            eq[C] = min(eq.get(C, before[r][C]), before[r][C])
        er = {v: t for v, t in before[r].items() if v not in {a, p}}
        if Q not in er and len(er) == z.c - 2:
            del er[C]
        er[Q] = 0
        assert {v: t for v, t in trial.x[Q].items() if v not in {a, p}} == eq
        assert {v: t for v, t in trial.x[r].items() if v not in {a, p}} == er
        assert trial.x[Q][a] == trial.x[r][a] == 0
        assert trial.x[Q][p] == trial.x[r][p] == min(before[Q][p] + 1, before[r][p])
        moves.append((r, reply))
    raise AssertionError('Singleton clearing exceeded finite first-visit/repeat bound')


def construct(z, a, p, H, rng, guard=100000):
    H = set(H)
    original = [dict(row) for row in z.x]
    old_zeros, old_count = zeros(z, a), holder_count(z, a)
    assert H <= old_zeros and p in z.x[a] and p not in H | {a}
    learned = {v for v in H if p in z.x[v]}
    sent, replied = {}, {}
    stats = Counter()
    while z.steps < guard:
        t = z.steps
        heads = set(z.x[a]) - {p}
        sent = {v: sent.get(v, t) for v in heads}
        oldest = [v for v, age in z.x[a].items() if age == max(z.x[a].values())]
        boundary = sorted(set(oldest) - H)
        q = rng.choice(boundary or oldest)
        rest = set(z.x[a]) - {q, p}
        B = min(rest, key=lambda v: (sent.get(v, t), v)) if rest else None
        extras = ({p} if q != p else set()) | ({B} if B is not None else set())
        if q == p:
            extras = set(sorted(set(z.x[a]) - {q})[:2])
        if B is not None:
            sent[B] = t
        if q not in H:
            reply = ({a} if a in z.x[q] else set())
            reply |= set(sorted(set(z.x[q]) - reply)[:min(3, len(z.x[q])) - len(reply)])
            if q != p and a in reply:
                retain_step(z, a, q, p, extras, reply)
            else:
                z.step(a, q, extras, reply)
            assert old_zeros <= zeros(z, a) and holder_count(z, a) >= old_count
            assert all(z.x[v] == original[v] for v in range(z.n) if v not in H | {a, q})
            stats['boundary'] += 1
            return stats
        k = len(heads)
        moves = plan(z, q, a, p, learned, partial=(k == 1))
        if moves is not None:
            owner_frozen = dict(z.x[a])
            for r, reply in moves:
                z.step(q, r, {a, p}, reply)
                assert z.x[a] == owner_frozen and zeros(z, a) == old_zeros
                assert holder_count(z, a) == old_count
            stats['accepted_plans'] += 1
            stats['preparation_events'] += len(moves)
            if not (set(z.x[q]) - {a, p}):
                stats['full_clears'] += 1
            else:
                assert k == 1 and max(z.x[q][v] for v in set(z.x[q]) - {a, p}) < z.x[q][p]
                stats['partial_stops'] += 1
        old_learned = learned.copy()
        if q in learned:
            residual = set(z.x[q]) - {a, p}
            overlap = residual & (set(z.x[a]) - {p, q})
            if overlap:
                C = min(overlap)
                stats['overlap_replies'] += 1
            elif residual:
                if k == 1:
                    if moves is not None:
                        C = max(residual, key=lambda v: (z.x[q][v], v))
                    else:
                        C = min(residual, key=lambda v: (replied.get((q, v), -1), v))
                else:
                    C = min(residual, key=lambda v: (z.x[q][v], v))
            else:
                C = None
            reply = {a, p} | ({C} if C is not None else set())
            if C is not None:
                replied[q, C] = t
        else:
            reply = {a} | set(sorted(set(z.x[q]) - {a})[:min(3, len(z.x[q])) - 1])
        before_u = z.x[a][p]
        retain_step(z, a, q, p, extras, reply)
        assert zeros(z, a) == old_zeros and holder_count(z, a) == old_count
        learned = {v for v in H if p in z.x[v]}
        assert old_learned <= learned and q in learned
        newk = len(z.x[a]) - 1
        if q in old_learned:
            assert newk <= k
        if moves is not None:
            if k >= 2:
                assert newk < k
            elif newk and z.x[a][p] < max(z.x[a].values()):
                assert z.x[a][p] == before_u + 1
        stats['owner_events'] += 1
        stats['new_learnings'] += len(learned - old_learned)
    raise AssertionError('Finite resource guard reached, not a proved horizon')


def trial(n, c, seed):
    rng = Random(seed)
    a, p = 0, 1
    ages = (0, 1, 2, 7, 10**6)
    rows = [{} for _ in range(n)]
    for v in range(1, n):
        rows[v] = {a: 0 if rng.randrange(3) else rng.choice((1, 7, 10**6))}
        candidates = sorted(set(range(n)) - {a, v})
        for u in rng.sample(candidates, rng.randrange(min(c - 1, len(candidates)) + 1)):
            rows[v][u] = rng.choice(ages)
    rows[a] = {p: rng.choice(ages)}
    for u in rng.sample(list(range(2, n)), rng.randrange(c)):
        rows[a][u] = rng.choice(ages)
    if seed % 3 == 0:
        # Force a long internal phase: p is the only boundary identity.
        for v in range(2, n):
            rows[v][a] = 0
        rows[a][p] = 0
        for v in set(rows[a]) - {p}:
            rows[a][v] = 10**6
    H = {v for v in range(2, n) if rows[v].get(a) == 0}
    if seed % 2 and seed % 3:
        H = set(rng.sample(sorted(H), rng.randrange(len(H) + 1)))
    z = ActualThree(rows, c, 3)
    return construct(z, a, p, H, rng), z.steps


def main():
    multi = Counter()
    for c in range(4, 11):
        n = c + 5
        H = set(range(2, n))
        rows = [{1: 0, **{v: 1000 for v in range(2, c + 1)}}, {0: 0}]
        for q in range(2, n):
            others = [2 + ((q - 2 + offset) % (n - 2)) for offset in range(1, n - 2)]
            rows.append({0: 0, 1: 1, **{v: 100 for v in others[:c - 2]}})
        z = ActualThree(rows, c, 3)
        moves = plan(z, 2, 0, 1, H, False)
        assert moves is not None and len(moves) >= c - 2
        multi.update(construct(z, 0, 1, H, Random(c)))
    assert multi['full_clears'] >= 7 and multi['preparation_events'] > 7
    print('PASS seven multi-residual known-anchor regressions:', dict(sorted(multi.items())))
    total = Counter()
    cases = events = longest = 0
    for n in range(4, 19):
        for c in range(3, n):
            for seed in range(50):
                stats, steps = trial(n, c, n * 100000 + c * 1000 + seed)
                total.update(stats)
                cases += 1
                events += steps
                longest = max(longest, steps)
    print('PASS ell=3 arbitrary-capacity cases/events/longest:', cases, events, longest)
    print('Exact structural counts:', dict(sorted(total.items())))
    print('Scope: finite candidate-controller corroboration, not general convergence.')


if __name__ == '__main__':
    main()
