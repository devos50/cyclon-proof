#!/usr/bin/env python3
"""Exact colored controlled ell=3,c>=4 outward-gain checks.

The fixed young-label set Y is the complement of the owner and frozen
zero holders. F counts all stored references to Y, independently of ages.
Finite cases do not establish the generic convergence theorem or a rate.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, holder_count
from verify_length_three_owner_terminal import terminal


class Colored:
    def __init__(self, rows, c, p, r):
        self.z = ActualThree(rows, c, 3)
        frozen = {v for v, row in enumerate(rows) if 0 in row} - {p}
        self.Y = set(range(len(rows))) - frozen - {0}

    def young(self):
        return sum(len(set(row) & self.Y) for row in self.z.x)

    def step(self, p, q, extra, reply, protect=(), passive_victims=None):
        z = self.z
        extra, reply = set(extra), set(reply)
        resident = set(z.x[p]) - {q}
        outgoing = {p} | extra
        dp = max(0, len(resident) + len(reply - resident - {p}) - z.c)
        dq = max(0, len(z.x[q]) + len(outgoing - set(z.x[q]) - {q}) - z.c)
        ep = extra - reply - set(protect)
        eq = reply - outgoing
        assert dp <= len(ep) and dq <= len(eq)
        vp = set(sorted(ep)[:dp])
        vq = set(sorted(eq)[:dq]) if passive_victims is None else set(passive_victims)
        assert len(vq) == dq and vq <= eq
        z.step(p, q, extra, reply, vp=vp, vq=vq)



def run(rows, c, rng, guard=100000):
    a, p, r = 0, 1, 2
    state = Colored(rows, c, p, r)
    z = state.z
    initial = holder_count(z, a)
    stats = Counter()
    Z = {v for v, row in enumerate(rows) if a in row} - {p}
    while z.steps < guard:
        assert not z.x[a] and a in z.x[p]
        assert all(z.x[v].get(a) == 0 for v in Z)
        assert state.Y == set(range(z.n)) - Z - {a}
        assert r in z.x[p] and r in state.Y and a not in z.x[r]
        q = rng.choice([v for v, age in z.x[p].items() if age == max(z.x[p].values())])
        if q == a:
            terminal(z, a, p, r, rng)
            stats['owner_terminal'] += 1
            break
        before = (state.young(), c - len(z.x[p]))
        if q in Z:
            assert q != r
            current = set(z.x[p])
            if p in z.x[q]:
                extra = {a, r}
                if r in z.x[q]:
                    reply = {a, p, r}
                    state.step(p, q, extra, reply, protect={a, r})
                    stats['known_both_drop'] += 1
                else:
                    # If full, the one passive victim must be absent at p.
                    candidates = set(z.x[q]) - {a, p}
                    if len(z.x[q]) == c:
                        candidates -= current
                    C = min(candidates, default=None)
                    reply = {a, p} | ({C} if C is not None else set())
                    victims = {C} if len(z.x[q]) == c else set()
                    state.step(p, q, extra, reply, protect={a, r}, passive_victims=victims)
                    stats['learn_target'] += 1
            else:
                candidates = current - {a, q}
                if len(current) == c:
                    candidates -= {r}
                B = min(candidates)
                extra = {a, B}
                novel = ({p} | extra) - set(z.x[q])
                need = max(0, len(z.x[q]) + len(novel) - c)
                victims = set(sorted(set(z.x[q]) - current)[:need])
                assert len(victims) == need
                reply = {a} | victims | ({B} if B in z.x[q] else set())
                reply |= set(sorted(set(z.x[q]) - reply)[:min(3, len(z.x[q])) - len(reply)])
                state.step(p, q, extra, reply, protect={a, r}, passive_victims=victims)
                stats['learn_initiator'] += 1
            assert z.x[p][a] == 0 and holder_count(z, a) == initial
            after = (state.young(), c - len(z.x[p]))
            assert after > before, (before, after)
            continue
        assert a not in z.x[q]
        retained = set(z.x[p]) - {a, q}
        overlap = retained & set(z.x[q])
        gain_possible = len(z.x[p]) < c or len(z.x[q]) < 3 or p in z.x[q] or bool(overlap)
        if gain_possible:
            distinguished = p if p in z.x[q] else min(overlap, default=None)
            B = min(retained - ({distinguished} if distinguished is not None else set()), default=None)
            if len(z.x[p]) >= 3 and B is None:
                B = min(retained)
            extra = {a} | ({B} if B is not None else set())
            reply = ({distinguished} if distinguished is not None else set())
            reply |= set(sorted(set(z.x[q]) - reply)[:min(3, len(z.x[q])) - len(reply)])
            state.step(p, q, extra, reply, protect={a})
            assert a in z.x[p] and a in z.x[q]
            stats['direct_gain'] += 1
            break
        assert len(z.x[p]) == c and len(z.x[q]) >= 3
        B = min(retained)
        reply = set(sorted(z.x[q])[:3])
        selected_young = q in state.Y
        old_anchor = z.x[p][a]
        old_max = [max(row.get(v, 0) for row in z.x) for v in range(z.n)]
        state.step(p, q, {a, B}, reply)
        assert a not in z.x[p] and z.x[q][a] == old_anchor + 1
        assert p in z.x[q] and p in state.Y
        new_max = [max(row.get(v, 0) for row in z.x) for v in range(z.n)]
        assert all(new_max[v] <= old_max[v] + 1 for v in range(z.n))
        assert new_max[q] <= old_max[q]
        assert state.young() - before[0] >= 1 - selected_young
        r, p = p, q
        assert (state.young(), c - len(z.x[p])) >= before
        assert holder_count(z, a) == initial
        stats['migration'] += 1
    else:
        raise AssertionError('Finite resource guard reached, not a proven bound')
    assert holder_count(z, a) > initial
    return stats, z.steps


def trial(n, c, seed):
    rng = Random(seed)
    ages = (0, 1, 2, 9, 10**6)
    rows = [{} for _ in range(n)]
    rows[1] = {0: rng.choice(ages), 2: rng.choice(ages)}
    for v in rng.sample(list(range(3, n)), rng.randrange(c - 1)):
        rows[1][v] = rng.choice(ages)
    for v in range(2, n):
        rows[v] = {1 + v % (n - 1): rng.choice(ages)}
        if v != 2 and rng.randrange(2):
            rows[v][0] = 0
        candidates = sorted(set(range(n)) - {0, v} - set(rows[v]))
        maximum = min(c, len(rows[v]) + len(candidates))
        target = maximum if seed % 3 == 0 else rng.randint(len(rows[v]), maximum)
        for u in rng.sample(candidates, target - len(rows[v])):
            rows[v][u] = rng.choice(ages)
    return run(rows, c, rng)


def main():
    # Requiring B in the reply when already at q prevents an uncompensated
    # loss of its active Y-copy. Omitting B makes strict lex progress fail.
    protect_B = [{}, {0: 0, 2: 1, 3: 10, 4: 0}, {1: 0},
                 {0: 0, 4: 0, 5: 0, 6: 0}, {1: 0}, {1: 0}, {1: 0}]
    metrics, _ = run(protect_B, 4, Random(0))
    assert metrics['learn_initiator'] == 1 and metrics['direct_gain'] == 1
    # A full current migrates into an underfull, disjoint responder.
    partial = [{} for _ in range(12)]
    partial[1] = {0: 10**6, 2: 10**6 + 1, **{v: 0 for v in range(3, 8)}}
    partial[2] = {8: 0, 9: 0, 10: 0}
    for v in range(3, 12):
        partial[v] = {1: 0}
    metrics, _ = run(partial, 7, Random(0))
    assert metrics['migration'] == 1 and metrics['owner_terminal'] == 1
    print('PASS explicit B-protection and disjoint-underfull migration regressions')
    total = Counter()
    cases = events = longest = 0
    for n in range(5, 19):
        for c in range(4, n):
            for seed in range(100):
                stats, steps = trial(n, c, n * 100000 + c * 1000 + seed)
                total.update(stats)
                cases += 1
                events += steps
                longest = max(longest, steps)
    print('PASS colored outward cases/events/longest:', cases, events, longest)
    print('Exact branch counts:', dict(sorted(total.items())))
    print('Scope: finite candidate-controller corroboration; no generic rate.')


if __name__ == '__main__':
    main()
