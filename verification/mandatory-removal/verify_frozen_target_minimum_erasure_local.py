#!/usr/bin/env python3
"""Local frozen-target minimum-age assertions for arbitrary tested L>=3.

Only p initiates; target q never initiates. In the terminal case q may
respond. These exact one-event checks do NOT establish global erasure,
class existence, or the lower-kernel first-contact/normalization inputs.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree


def copies(rows, target):
    return [row[target] for row in rows if target in row]


def case(n, c, L, k, kind, seed):
    rng = Random(seed)
    target, p = 0, 1
    partner = target if kind == 'owner_terminal' else 2
    rows = []
    for v in range(n):
        required = set()
        forbidden = {v}
        if v == p:
            required = {target, partner}
        elif v == partner and kind in ('internal_minimum', 'higher_reply'):
            required = {target}
        elif v == partner and kind == 'absent_reply':
            forbidden.add(target)
        candidates = sorted(set(range(n)) - forbidden - required)
        maximum = min(c, len(required) + len(candidates))
        size = maximum if seed % 3 == 0 else rng.randint(len(required), maximum)
        identities = required | set(rng.sample(candidates, size - len(required)))
        row = {u: rng.choice((0, 1, 7, 10**6)) for u in identities}
        if target in row:
            row[target] = k + rng.choice((0, 1, 10**6))
        rows.append(row)
    rows[p][target] = k
    if partner != target:
        oldest = max([k] + list(rows[p].values()))
        rows[p][partner] = oldest + rng.randrange(2)
        if kind == 'internal_minimum':
            rows[partner][target] = k
        elif kind == 'higher_reply':
            rows[partner][target] = k + rng.choice((1, 7, 10**6))
    else:
        for u in set(rows[p]) - {target}:
            rows[p][u] = rng.choice((0, k // 2, k))
    assert p != target and rows[p][partner] == max(rows[p].values())
    assert min(copies(rows, target)) == k
    extras = {target} if partner != target else set()
    count = min(L - 1, len(rows[p]) - 1)
    extras |= set(rng.sample(sorted(set(rows[p]) - {partner} - extras), count - len(extras)))
    reply = {target} if target in rows[partner] else set()
    count = min(L, len(rows[partner]))
    reply |= set(rng.sample(sorted(set(rows[partner]) - reply), count - len(reply)))
    resident = set(rows[p]) - {partner}
    request = {p} | extras
    dp = max(0, len(resident) + len(reply - resident - {p}) - c)
    dq = max(0, len(rows[partner]) + len(request - set(rows[partner]) - {partner}) - c)
    vp = set(rng.sample(sorted(extras - reply), dp))
    vq = set(rng.sample(sorted(reply - request), dq))
    original = [dict(row) for row in rows]
    before = copies(rows, target)
    z = ActualThree(rows, c, L)
    z.step(p, partner, extras, reply, vp=vp, vq=vq)
    after = copies(z.x, target)
    assert not after or min(after) >= k
    assert all(z.x[v] == original[v] for v in range(n) if v not in {p, partner})
    if kind == 'internal_minimum':
        assert z.x[p][target] == z.x[partner][target] == k
        assert after.count(k) == before.count(k)
    else:
        assert after.count(k) == before.count(k) - 1
        if kind == 'owner_terminal':
            assert target not in z.x[p] and target not in z.x[target]
        else:
            assert z.x[partner][target] >= k + 1
            assert target not in z.x[p] or z.x[p][target] >= k + 1
    return Counter({kind: 1, 'active_underfull': len(original[p]) < c,
                    'responder_underfull': len(original[partner]) < c,
                    'empty_responder': not original[partner],
                    'active_victims': dp, 'passive_victims': dq,
                    'minimum_fully_removed': not after or min(after) > k})


def main():
    total = Counter()
    cases = 0
    for n in range(4, 14):
        for L in range(3, n):
            for c in range(L, n):
                for k in (0, 1, 10**6):
                    for kind in ('internal_minimum', 'higher_reply', 'absent_reply', 'owner_terminal'):
                        for seed in range(4):
                            total.update(case(n,c,L,k,kind,n*100000+L*1000+c*100+seed))
                            cases += 1
    assert total['empty_responder'] and total['active_victims'] and total['passive_victims']
    print('PASS frozen-target local events:', cases)
    print('Exact branch/coverage counts:', dict(sorted(total.items())))
    print('Scope: one-event local minimum bookkeeping only; no global erasure theorem inferred.')


if __name__ == '__main__':
    main()
