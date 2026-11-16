#!/usr/bin/env python3
"""Exact controlled outward-holder checks for c=ell=3.

Finite seeded checks corroborate the separately reviewed qualitative proof.
The resource guard is not a claimed uniform or polynomial horizon.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, holder_count
from verify_thesis_c3_learned_callback import construct, owner_step


def exchange(z, p, q, preserve=None):
    """Choose any legal active victim subset retaining preserve if possible."""
    resident = set(z.x[p]) - {q}
    reply = set(z.x[q])
    needed = max(0, len(resident) + len(reply - resident - {p}) - 3)
    eligible = resident - reply
    options = list(combinations(sorted(eligible), needed))
    assert options
    options.sort(key=lambda vv: (preserve in vv, vv))
    z.step(p, q, resident, reply, vp=set(options[0]))


def owner_terminal(z, a, p, r, rng, stats):
    """Entered before p contacts empty a; a oldest, r a nonholder."""
    before = holder_count(z, a)
    assert not z.x[a] and a not in z.x[r] and r in z.x[p]
    assert z.x[p][a] == max(z.x[p].values())
    residual = set(z.x[p]) - {a}
    high = max(z.x[p][v] for v in residual)
    candidates = [v for v in residual if z.x[p][v] == high]
    nonholders = [v for v in candidates if a not in z.x[v]]
    s = min(nonholders or candidates)
    exchange(z, p, a)
    if nonholders:
        exchange(z, a, s)
        exchange(z, p, s)
        stats['terminal_triangle'] += 1
    else:
        # s is a holder, r is the other residual and must survive at owner.
        owner_step(z, a, s, r)
        exchange(z, p, s)
        assert holder_count(z, a) == before and r in z.x[a] and a not in z.x[r]
        while holder_count(z, a) == before:
            construct(z, a, r, rng, limit=z.steps + 100000)
            if holder_count(z, a) == before:
                assert r in z.x[a] and a not in z.x[r]
        stats['terminal_holder_then_callback'] += 1
    assert holder_count(z, a) > before


def outward(z, a, p, rng, limit=100000):
    initial = holder_count(z, a)
    stats = Counter()
    while z.steps < limit:
        assert not z.x[a] and a in z.x[p]
        assert all(row.get(a, 0) == 0 for v, row in enumerate(z.x) if v != p)
        nonholders = [v for v in z.x[p] if v != a and a not in z.x[v]]
        assert nonholders
        r = min(nonholders)
        oldest = [v for v, age in z.x[p].items() if age == max(z.x[p].values())]
        q = rng.choice(oldest)
        if q == a:
            owner_terminal(z, a, p, r, rng, stats)
            break
        if a in z.x[q]:
            # The three entries a,q,r are distinct and fill p's cache.
            assert set(z.x[p]) == {a, q, r}
            exchange(z, p, q, a)
            assert z.x[p][a] == z.x[q][a] == 0
            assert set(z.x[q]) == {a, p, r}
            assert z.x[q][r] >= max(z.x[q][a], z.x[q][p])
            exchange(z, q, r, a)
            if a in z.x[q]:
                assert holder_count(z, a) > initial
                stats['zero_holder_direct_gain'] += 1
            else:
                assert set(z.x[r]) == {q, a, p}
                assert z.x[r][a] == 1 and z.x[r][p] <= 1 and z.x[r][q] == 0
                assert a not in z.x[q]
                owner_terminal(z, a, r, q, rng, stats)
                stats['zero_holder_transfer_then_terminal'] += 1
            break
        old_age = z.x[p][a]
        old_max = [max((row.get(v, 0) for row in z.x), default=0) for v in range(z.n)]
        exchange(z, p, q, a)
        if a in z.x[p]:
            assert holder_count(z, a) > initial
            stats['nonholder_direct_gain'] += 1
            break
        assert z.x[q][a] == old_age + 1 and p in z.x[q]
        new_max = [max((row.get(v, 0) for row in z.x), default=0) for v in range(z.n)]
        assert all(new_max[v] <= old_max[v] + 1 for v in range(z.n))
        assert new_max[q] <= old_max[q]  # selected identity's K drops at least one
        assert holder_count(z, a) == initial
        p = q
        stats['migrations'] += 1
    else:
        raise AssertionError('Finite resource guard reached; not a proven horizon')
    assert holder_count(z, a) > initial
    return stats


def trial(n, seed):
    rng = Random(seed)
    a, p, r = 0, 1, 2
    ages = (0, 1, 2, 7, 1000000)
    rows = [{} for _ in range(n)]
    rows[p] = {a: rng.choice(ages), r: rng.choice(ages)}
    if rng.randrange(2):
        rows[p][rng.randrange(3, n)] = rng.choice(ages)
    for v in range(2, n):
        # These links ensure the initial underlying graph is connected.
        rows[v] = {1 + v % (n - 1): rng.choice(ages)}
        if v != r and rng.randrange(2):
            rows[v][a] = 0
        candidates = sorted(set(range(n)) - {v, a} - set(rows[v]))
        for u in rng.sample(candidates, rng.randrange(min(3 - len(rows[v]), len(candidates)) + 1)):
            rows[v][u] = rng.choice(ages)
    z = ActualThree(rows, 3, 3)
    return outward(z, a, p, rng), z.steps


def main():
    # Regression: MIN lowers q's received r to zero, so q->r is a tie;
    # r also already has p^0, so the next terminal row has p-age 0, not 1.
    fixture = [
        {}, {0: 0, 3: 5, 2: 1}, {1: 0, 4: 0, 5: 0},
        {0: 0, 2: 0, 4: 3}, {0: 0}, {0: 0},
    ]
    regression = outward(ActualThree(fixture, 3, 3), 0, 1, Random(0))
    assert regression['zero_holder_transfer_then_terminal'] == 1
    print('PASS explicit MIN-lowered oldest-tie / terminal-age regression')
    total = Counter()
    cases = events = longest = 0
    for n in range(4, 21):
        for seed in range(300):
            stats, steps = trial(n, 100000 * n + seed)
            total.update(stats)
            cases += 1
            events += steps
            longest = max(longest, steps)
    print('PASS outward gain cases/exchanges/longest:', cases, events, longest)
    print('Exact branch counts:', dict(sorted(total.items())))
    print('Scope: conditional outward configuration; finite corroboration, not a generic rate.')


if __name__ == '__main__':
    main()
