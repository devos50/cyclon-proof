#!/usr/bin/env python3
"""Exact ell=2 outward-gain controller for c>=3 and n<=2c.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_half_dense.py

Every initialization has an empty owner a, only age-zero a copies, and a
chosen a-holder caching a nonholder. The controller evaluates the actual
numerical-age protected+MIN kernel, including all buffer-size, oldest-tie,
and legal-victim assertions from the sibling kernel checker. It must
increase the TOTAL number of a-holders. Gain-avoiding full-source migrations
must increase the number of full nonowner caches. The owner double callback
and underfull-tracker branches are executed directly, not assumed.

Besides random states, forced-migration initializations give the first
responder exactly the identities outside the active cache and its owner,
with age patterns 0,1,2,10^6. These include the first previously open case
n=6,c=3 and force disjoint exchanges. Optional --max-n 12 --seeds 2 gives a
quick run. Finite experiments corroborate the written arbitrary-size proof;
they do not establish it by enumeration. Assertions must be enabled.

Reproduced default result: 10,777 initializations through n=30, 36,204 exact
exchanges, maximum trajectory length20, and maximum3 migrations. Branches:
1,203 full-cache migrations, 6,920 underfull migrations, 2,364 owner double
callbacks, and 8,413 direct holder gains. The explicit n=6,c=3 chain gives
three consecutive full-cache migrations before the gain.
"""
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_anchor import Actual


def holders(z, a):
    return {p for p in range(z.n) if a in z.x[p]}


def full(z, a):
    return sum(len(z.x[p]) == z.c for p in range(z.n) if p != a)


def reply_at_holder(z, q, a, desired, rng):
    assert a in z.x[q]
    reply = [a]
    if len(z.x[q]) >= 2:
        reply.append(desired if desired in z.x[q] else rng.choice(sorted(set(z.x[q]) - {a})))
    return reply


def reply_at_nonholder(z, p, q, rng):
    assert not (set(z.x[q]) & {p, q}) - {p}
    size = min(2, len(z.x[q]))
    known = set(z.x[q]) & (set(z.x[p]) | {p})
    if known:
        first = rng.choice(sorted(known))
        return [first] + rng.sample(sorted(set(z.x[q]) - {first}), size - 1)
    return rng.sample(sorted(z.x[q]), size)


def owner_target(z, a, target, rng):
    old = holders(z, a)
    assert target in z.x[a] and target not in old
    start = z.steps
    while holders(z, a) == old:
        mx = max(z.x[a].values())
        q = rng.choice([q for q, age in z.x[a].items() if age == mx])
        pool = sorted(set(z.x[a]) - {q})
        extra = [target] if q != target else rng.sample(pool, min(1, len(pool)))
        if q in old:
            reply = reply_at_holder(z, q, a, target, rng)
        else:
            reply = rng.sample(sorted(z.x[q]), min(2, len(z.x[q])))
        z.step(a, q, extra, reply)
        assert old <= holders(z, a)
        if holders(z, a) == old:
            assert target in z.x[a]
        assert z.steps - start <= z.n + z.c
    assert len(holders(z, a)) == len(old) + 1


def owner_double(z, a, active, predecessor, rng):
    old = holders(z, a)
    assert z.x[a] == {} and predecessor not in old
    assert predecessor in z.x[active] and a in z.x[active]
    age = z.x[active][predecessor]
    z.step(active, a, [predecessor], [])
    assert z.x[a] == {active: 0, predecessor: age + 1}
    assert active not in holders(z, a)
    assert len(holders(z, a)) == len(old) - 1
    reply = rng.sample(sorted(z.x[predecessor]), min(2, len(z.x[predecessor])))
    z.step(a, predecessor, [active], reply)
    assert len(holders(z, a)) == len(old)
    assert active in z.x[a] and active not in holders(z, a)
    owner_target(z, a, active, rng)
    assert len(holders(z, a)) == len(old) + 1


def control(z, a, active, rng, stats):
    assert z.c >= 3 and z.n <= 2 * z.c and z.x[a] == {}
    H = len(holders(z, a))
    assert all(z.x[p][a] == 0 for p in holders(z, a))
    assert set(z.x[active]) - holders(z, a) - {a}
    predecessor = None
    migrations = 0
    service = 0
    while len(holders(z, a)) == H:
        assert a in z.x[active]
        assert all(p == active or z.x[p][a] == 0 for p in holders(z, a))
        if predecessor is not None:
            assert predecessor in z.x[active] and predecessor not in holders(z, a)
        if z.x[active][a] == 0:
            nonanchors = set(z.x[active]) - {a}
            assert nonanchors
            mx = max(z.x[active][v] for v in nonanchors)
            assert mx == max(z.x[active].values())
            q = rng.choice([v for v in nonanchors if z.x[active][v] == mx])
            service += 1
            assert service <= z.n + z.c
        else:
            mx = max(z.x[active].values())
            q = rng.choice([v for v in z.x[active] if z.x[active][v] == mx])
        if q == a:
            assert predecessor is not None
            owner_double(z, a, active, predecessor, rng)
            stats['owner_double'] = stats.get('owner_double', 0) + 1
            break
        old = holders(z, a)
        before_full = full(z, a)
        active_size = len(z.x[active])
        if q in old:
            reply = reply_at_holder(z, q, a, active, rng)
            z.step(active, q, [a], reply)
            assert holders(z, a) == old
            assert z.x[active][a] == 0
            assert len(z.x[active]) <= active_size
            if len(z.x[active]) == z.c:
                assert full(z, a) >= before_full
            else:
                stats['underfull_holder'] = stats.get('underfull_holder', 0) + 1
        else:
            before_Q = set(z.x[q])
            known = before_Q & (set(z.x[active]) | {active})
            reply = reply_at_nonholder(z, active, q, rng)
            needed = max(0, len(before_Q) + len({active, a} - before_Q) - z.c)
            eligible = set(reply) - {active, a}
            victims = sorted(eligible, key=lambda v: (z.x[q][v], v))[:needed]
            z.step(active, q, [a], reply, vq=victims)
            if len(holders(z, a)) == H + 1:
                stats['direct_gain'] = stats.get('direct_gain', 0) + 1
                break
            assert not known and active_size == z.c
            assert len(before_Q) <= z.n - z.c - 1 <= z.c - 1
            assert holders(z, a) == old - {active} | {q}
            assert len(z.x[active]) == z.c and q not in z.x[active]
            assert z.x[q][active] == 0 and z.x[q][a] > 0
            assert len(z.x[q]) == min(z.c, len(before_Q) + 2)
            if len(z.x[q]) == z.c:
                assert full(z, a) >= before_full + 1
                stats['full_migration'] = stats.get('full_migration', 0) + 1
            else:
                stats['underfull_migration'] = stats.get('underfull_migration', 0) + 1
            predecessor, active = active, q
            migrations += 1
            service = 0
            assert migrations <= z.n - 1
        assert z.steps <= (z.n + 1) * (z.n + z.c + 1)
    assert len(holders(z, a)) == H + 1
    assert z.steps <= (z.n + 1) * (z.n + z.c + 1)
    return migrations


def make_case(n, c, seed, forced, age_pattern):
    rng = Random(seed)
    labels = list(range(n))
    rng.shuffle(labels)
    a, p, q = labels[:3]
    k = rng.randint(1, n - 2)
    pool = labels[3:]
    rng.shuffle(pool)
    I = {p} | set(pool[:k - 1])
    J = set(range(n)) - I - {a}
    x = [{} for _ in range(n)]
    for v in range(n):
        if v == a:
            continue
        peers = sorted(set(range(n)) - {a, v})
        reserve = {a: 0} if v in I else {}
        count = rng.randint(0, min(c - len(reserve), len(peers)))
        x[v] = {**reserve, **{u: rng.choice((0, 1, 2, 1000000)) for u in rng.sample(peers, count)}}
    if forced:
        chosen = [q] + rng.sample(sorted(set(range(n)) - {a, p, q}), c - 2)
        x[p] = {a: 0, **{v: rng.randint(0, 10) for v in chosen}}
        x[p][q] = max(x[p].values()) + 1
        complement = sorted(set(range(n)) - set(x[p]) - {p})
        assert len(complement) >= 2
        x[q] = {v: age_pattern for v in complement}
    else:
        if q not in x[p]:
            if len(x[p]) == c:
                del x[p][rng.choice(sorted(set(x[p]) - {a}))]
            x[p][q] = rng.randint(0, 1000000)
    return Actual(x, c), a, p, rng


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=30)
    ap.add_argument('--seeds', type=int, default=12)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled; do not use python -O')
    cases = steps = worst = max_migrations = 0
    stats = {}
    # A designed n=6,c=3 chain forces three full-source migrations,
    # successively 1->2->4->3, before full old source 1 accepts a again.
    # Distinct high/low ages choose the intended next partner and victim.
    chain = Actual([{}, {0: 0, 2: 1000000, 3: 0}, {4: 1000000, 5: 0},
                    {1: 1000000, 5: 0}, {3: 1000000, 5: 0}, {}], 3)
    mm = control(chain, 0, 1, Random(1), stats)
    assert mm == 3 and len(holders(chain, 0)) == 2
    cases += 1
    steps += chain.steps
    worst = chain.steps
    max_migrations = mm
    for n in range(4, args.max_n + 1):
        for c in range(max(3, (n + 1) // 2), n):
            for seed in range(args.seeds):
                modes = [(False, 0)]
                if n - c - 1 >= 2:
                    modes += [(True, age) for age in (0, 1, 2, 1000000)]
                for forced, age in modes:
                    z, a, p, rng = make_case(n, c, 1000003*n+7919*c+seed, forced, age)
                    migrations = control(z, a, p, rng, stats)
                    cases += 1
                    steps += z.steps
                    worst = max(worst, z.steps)
                    max_migrations = max(max_migrations, migrations)
    print('PASS cases/exchanges/worst/migrations', (cases, steps, worst, max_migrations), 'branches', stats)


if __name__ == '__main__':
    main()
