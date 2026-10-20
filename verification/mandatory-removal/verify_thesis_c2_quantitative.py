#!/usr/bin/env python3
"""Check the constructive quadratic-length c=ell=2 canonical path.

This executes the numerical-age kernel, including received-entry protection
and minimum duplicate ages. It checks each local horizon and the explicit
whole-path bound, starting with connected arbitrary-age caches. The residual
capacity-one normalizer follows cycle shortening, positive-age removal and
tree diameter constructions rather than an unrestricted preliminary sweep.
The optional exhaustive availability check verifies the two-activation full
cache construction on every connected outdegree-at-most-one state through
five peers. These finite checks support, rather than replace, the proof.
"""
from itertools import product
from math import comb
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_anchor import Actual as BaseActual, merge, tree_move
import verify_thesis_c2_saturation as sat


class Actual(BaseActual):
    def step(self, p, q, extra, reply, vp=None, vq=None):
        P0, Q0 = self.x[p], self.x[q]
        extra, reply = set(extra), set(reply)
        ties = sum(t == max(P0.values()) for t in P0.values())
        outgoing = {p} | extra
        after_remove = set(P0) - {q}
        new_p = reply - after_remove - {p}
        new_q = outgoing - set(Q0) - {q}
        dp = max(0, len(after_remove) + len(new_p) - 2)
        dq = max(0, len(Q0) + len(new_q) - 2)
        choices = (ties * comb(len(extra - reply), dp)
                   * comb(len(reply - outgoing), dq))
        # At c=ell=2 both packet subsets are deterministic. This bound
        # therefore gives each prescribed event probability >=1/(4n).
        assert choices <= 4
        super().step(p, q, extra, reply, vp, vq)


def D(m):
    return 2 * m * (m - 1)


def E(n):
    return 2 * (D(n - 1) + 1)


def C(n):
    return E(n) + 2 * D(n - 1) + 4 * (n - 2)


def L(n):
    A = 5 * n + 12
    canonical_bound = 8 * n ** 2 + 2
    result = (n - 1) * A + canonical_bound
    assert result == 13 * n ** 2 + 7 * n - 10
    assert result <= 16 * n ** 2
    return result


def connected(x):
    reached = {0}
    while True:
        more = reached | {q for p in reached for q in x[p]} | {
            p for p in range(len(x)) if set(x[p]) & reached}
        if more == reached:
            return len(reached) == len(x)
        reached = more


def all_a_zero(z, a):
    return all(a not in row or row[a] == 0 for row in z.x)


def residual_components(z, a, vertices):
    vertices = set(vertices)
    assert all(set(z.x[v]) - {a} <= vertices for v in vertices)
    unseen = set(vertices)
    answer = []
    while unseen:
        reached = {min(unseen)}
        while True:
            more = reached | {q for p in reached for q in z.x[p] if q != a} | {
                p for p in vertices if (set(z.x[p]) - {a}) & reached}
            if more == reached:
                break
            reached = more
        assert reached <= unseen
        answer.append(reached)
        unseen -= reached
    return answer


def normalize(z, a, component, root):
    """Use at most D(m) actual exchanges to make a residual rooted star."""
    start = z.steps
    component = set(component)
    labels = sorted(component - {root}) + [root]
    inv = {v: i for i, v in enumerate(labels)}
    m = len(labels)
    before = [r.copy() for r in z.x]
    assert all(z.x[v].get(a) == 0 for v in component)
    assert all(set(z.x[v]) - {a} <= component for v in component)

    def state():
        return tuple(next((inv[q] for q in z.x[v] if q != a), -1)
                     for v in labels)

    def act(i):
        p = labels[i]
        q = next(q for q in z.x[p] if q != a)
        z.step(p, q, {a}, set(z.x[q]))
        assert all(z.x[v].get(a) == 0 for v in component)

    cycle_events = 0
    while True:
        s = state()
        cycle = None
        for begin in range(m):
            path = []
            v = begin
            while v != -1 and v not in path:
                path.append(v)
                v = s[v]
            if v != -1:
                cycle = path[path.index(v):]
                break
        if cycle is None:
            break
        act(min(cycle))
        cycle_events += 1
        assert cycle_events <= m - 1

    age_events = 0
    while True:
        positive = [i for i, p in enumerate(labels)
                    if any(t > 0 for q, t in z.x[p].items() if q != a)]
        if not positive:
            break
        old_positive = sum(t > 0 for p in labels for q, t in z.x[p].items()
                           if q != a)
        act(positive[0])
        assert sum(t > 0 for p in labels for q, t in z.x[p].items()
                   if q != a) == old_positive - 1
        age_events += 1
        assert age_events <= m - 1

    def insert_path(s):
        moves = []

        def path():
            order = []
            v = 0
            while v != -1:
                assert v not in order
                order.append(v)
                v = s[v]
            return order

        order = path()
        while len(order) < m:
            p = next(p for p in range(m) if p not in order and s[p] in order)
            s = tree_move(s, p)
            moves.append(p)
            order = path()
        return moves, s, order

    moves, source_path, source_order = insert_path(state())
    tree_start = z.steps
    for p in moves:
        act(p)
    assert state() == source_path
    target = tuple(-1 if i == m - 1 else m - 1 for i in range(m))
    reverse_moves, target_path, target_order = insert_path(target)
    for i in range(1, m):
        j = source_order.index(target_order[i])
        while j > i:
            x, u, v = source_order[j - 2:j + 1]
            for p in (x, x, u, v):
                act(p)
            source_order[j - 1], source_order[j] = source_order[j], source_order[j - 1]
            j -= 1
    assert state() == target_path
    inverse = []
    s = target
    for p in reverse_moves:
        inverse.append(s[p])
        s = tree_move(s, p)
    for p in reversed(inverse):
        act(p)
    assert state() == target
    assert z.steps - tree_start <= 2 * (m - 1) ** 2
    assert z.steps - start <= D(m)
    assert z.x[root] == {a: 0}
    assert all(z.x[v] == {a: 0, root: 0} for v in component - {root})
    assert all(z.x[v] == before[v] for v in range(z.n) if v not in component)
    z.embedding_steps += z.steps - start


# The incoming-boundary controller's exact case distinction is independently
# checked in its original verifier; replace only its normalizer with the
# quantitatively bounded construction above.
sat.normalize = normalize


def reachable(z, a):
    seen = {a}
    while True:
        more = seen | {q for p in seen for q in z.x[p]}
        if more == seen:
            return seen
        seen = more


def owner_service(z, a, target):
    """Restore a lost identity holder without losing existing zeros."""
    start = z.steps
    old_zeros = sat.holders(z, a)
    assert target in z.x[a] and a not in z.x[target]
    while True:
        assert target in z.x[a]
        q = max(z.x[a], key=lambda q: (z.x[a][q], -q))
        nonholder = a not in z.x[q]
        sat.exchange(z, a, q)
        assert old_zeros <= sat.holders(z, a)
        if nonholder:
            break
        assert z.steps - start <= z.n + 2
    assert z.steps - start <= z.n + 2


def positive_gain(z, a, p):
    start = z.steps
    old_zeros = sat.holders(z, a)
    old_N = sum(a in r for r in z.x)
    assert z.x[p].get(a, 0) > 0
    q = max(z.x[p], key=lambda q: (z.x[p][q], -q))
    sat.exchange(z, p, q)
    if q == a:
        assert a not in z.x[p] and p in z.x[a]
        owner_service(z, a, p)
    elif q in old_zeros:
        assert z.x[p].get(a) == 0
    else:
        assert z.x[q].get(p) == 0 and z.x[q].get(a, 0) > 0
        sat.exchange(z, q, a)
        assert a not in z.x[q] and q in z.x[a]
        owner_service(z, a, q)
    assert old_zeros < sat.holders(z, a)
    assert sum(a in r for r in z.x) >= old_N
    assert z.steps - start <= z.n + 4


def clear_owner(z, a):
    start = z.steps
    old_zeros = sat.holders(z, a)
    assert reachable(z, a) <= old_zeros | {a}
    while z.x[a]:
        R = reachable(z, a) - {a}
        q = max(z.x[a], key=lambda q: (z.x[a][q], -q))
        component = next(g for g in residual_components(z, a, R) if q in g)
        normalize(z, a, component, q)
        old_size = len(z.x[a])
        sat.exchange(z, a, q)
        assert len(z.x[a]) == old_size - 1
    assert old_zeros <= sat.holders(z, a)
    assert all_a_zero(z, a)
    assert z.steps - start <= E(z.n)


def root_clear(z, a, Q, I):
    """Clear only Q's residual pointer, stopping before an outside contact."""
    start = z.steps
    I = set(I)
    assert Q in I and all(z.x[p].get(a) == 0 for p in I)
    while set(z.x[Q]) != {a}:
        x = next(x for x in z.x[Q] if x != a)
        if x not in I:
            assert z.steps - start <= len(I)
            return x
        reply = z.x[x].copy()
        sat.exchange(z, Q, x)
        expected = {r: t for r, t in reply.items() if r != Q}
        assert z.x[Q] == expected
        assert z.x[x] == {a: 0, Q: 0}
        assert all(z.x[p].get(a) == 0 for p in I)
        assert z.steps - start <= len(I)
    return None


def owner_empty_or_gain(z, a, counts):
    start = z.steps
    I = sat.holders(z, a)
    assert all_a_zero(z, a)
    while z.x[a]:
        nonholder = next((p for p in z.x[a] if p not in I), None)
        if nonholder is not None:
            owner_service(z, a, nonholder)
            counts['direct_owner_gains'] = counts.get('direct_owner_gains', 0) + 1
            break
        Q = max(z.x[a], key=lambda q: (z.x[a][q], -q))
        x = root_clear(z, a, Q, I)
        if x is None:
            before = len(z.x[a])
            sat.exchange(z, a, Q)
            assert len(z.x[a]) == before - 1
            assert I == sat.holders(z, a)
        else:
            assert x not in I | {a}
            sat.exchange(z, Q, x)
            assert z.x[x] == {Q: 0, a: 1}
            sat.exchange(z, a, Q)
            assert z.x[Q].get(a) == 0
            assert z.x[x] == {Q: 0, a: 1}
            sat.exchange(z, x, a)
            assert a not in z.x[x] and x in z.x[a]
            owner_service(z, a, x)
            counts['owner_outward_repairs'] = counts.get('owner_outward_repairs', 0) + 1
            break
    assert I <= sat.holders(z, a)
    assert all_a_zero(z, a)
    assert z.steps - start <= 3 * z.n + 5
    gained = len(sat.holders(z, a)) > len(I)
    assert gained or not z.x[a]
    return gained


def incoming_root(z, a, P, selected):
    """Incoming-boundary macro using only a root clearing, not a star."""
    I = sat.holders(z, a)
    J = set(range(z.n)) - I - {a}
    comps = sat.components(z, a, I)
    assert z.x[a] == {} and all_a_zero(z, a)
    Q = selected if selected in I else next(q for q in z.x[P] if q in I)
    component = next(g for g in comps if Q in g)
    assert root_clear(z, a, Q, I) is None
    assert z.x[Q] == {a: 0}
    if selected in J:
        sat.exchange(z, P, selected)
        sat.exchange(z, selected, Q)
        assert z.x[selected] == {a: 0, P: 1}
        sat.outward(z, a, selected, P)
        return 'outside-oldest'
    extra = set(z.x[P]) - {Q}
    sat.exchange(z, P, Q)
    if not extra:
        assert sat.holders(z, a) == I | {P}
        return 'singleton'
    X = next(iter(extra))
    assert sat.holders(z, a) == (I - {Q}) | {P}
    if X in J:
        sat.outward(z, a, P, X)
        return 'outside-extra'
    if len(component) > 1:
        v = next(v for v in component if Q in z.x[v])
        assert z.x[v].get(a) == 0
        sat.outward(z, a, v, Q)
        return 'nontrivial-root-component'
    assert len(sat.components(z, a, sat.holders(z, a))) == len(comps) - 1
    assert z.x[a] == {} and all_a_zero(z, a)
    return 'component-decrease'


def construct(z, a, counts):
    normalization_start = z.steps
    initial_positive_blocks = counts['positive_blocks']
    while any(z.x[p].get(a, 0) > 0 for p in range(z.n)):
        p = next(p for p in range(z.n) if z.x[p].get(a, 0) > 0)
        positive_gain(z, a, p)
        counts['positive_blocks'] += 1
    positive_stages = counts['positive_blocks'] - initial_positive_blocks
    assert z.steps - normalization_start <= (z.n - 1) * (z.n + 4)
    assert all_a_zero(z, a)

    gain_stages = 0
    while len(sat.holders(z, a)) < z.n - 1:
        start = z.steps
        k = len(sat.holders(z, a))
        I = sat.holders(z, a)
        if owner_empty_or_gain(z, a, counts):
            counts['source_gains'] += 1
        else:
            I = sat.holders(z, a)
            assert len(I) == k
            J = set(range(z.n)) - I - {a}
            outward_edges = [(p, q) for p in I for q in z.x[p] if q in J]
            if outward_edges:
                sat.outward(z, a, *outward_edges[0])
                counts['outward_gains'] += 1
            else:
                assert k > 0
                macros = 0
                d = len(sat.components(z, a, I))
                while len(sat.holders(z, a)) == k:
                    I = sat.holders(z, a)
                    J = set(range(z.n)) - I - {a}
                    P = next(p for p in J if set(z.x[p]) & I)
                    q = max(z.x[P], key=lambda q: (z.x[P][q], -q))
                    before = z.steps
                    branch = incoming_root(z, a, P, q)
                    counts[branch] = counts.get(branch, 0) + 1
                    assert z.steps - before <= z.n + 6
                    macros += 1
                    if branch == 'component-decrease':
                        assert z.steps - before == 1
                        new_d = len(sat.components(z, a, sat.holders(z, a)))
                        assert new_d == d - 1
                        d = new_d
                    assert macros <= k
        assert len(sat.holders(z, a)) > k
        assert all_a_zero(z, a)
        assert z.steps - start <= 5 * z.n + 12
        gain_stages += 1

    finish_start = z.steps
    clear_owner(z, a)
    comps = residual_components(z, a, set(range(z.n)) - {a})
    roots = []
    for comp in comps:
        root = max(comp)
        normalize(z, a, comp, root)
        roots.append(root)
    for v in roots[1:]:
        merge(z, a, roots[0], v)
    normalize(z, a, set(range(z.n)) - {a}, max(set(range(z.n)) - {a}))
    assert z.steps - finish_start <= C(z.n)
    assert positive_stages + gain_stages <= z.n - 1
    assert z.steps <= L(z.n)
    order = sorted(set(range(z.n)) - {a}) + [a]
    for i, p in enumerate(order):
        assert z.x[p] == {q: 0 for q in order[max(i + 1, z.n - 2):]}


def availability_exhaustive(max_n):
    counts = {'already_full': 0, 'three_path': 0, 'star': 0}
    checked = 0
    for n in range(3, max_n + 1):
        options = [[-1] + [q for q in range(n) if q != p] for p in range(n)]
        for f in product(*options):
            x = [{} if q == -1 else {q: 0} for q in f]
            if not connected(x):
                continue
            z = Actual(x, 2)
            paths = [(u, v, f[v]) for u, v in enumerate(f)
                     if v != -1 and f[v] not in {-1, u}]
            if paths:
                u, v, w = paths[0]
                sat.exchange(z, u, v)
                assert len(z.x[v]) == 2
                p = next(p for p in range(n) if p != v)
                if z.x[p]:
                    q = next(q for q in z.x[p] if z.x[p][q] == max(z.x[p].values()))
                    sat.exchange(z, p, q)
                counts['three_path'] += 1
            else:
                roots = [p for p, q in enumerate(f) if q == -1]
                assert len(roots) == 1
                r = roots[0]
                leaves = [p for p in range(n) if p != r]
                assert all(f[p] == r for p in leaves)
                sat.exchange(z, leaves[0], r)
                sat.exchange(z, leaves[1], r)
                counts['star'] += 1
            assert any(len(row) == 2 for row in z.x)
            checked += 1
    return checked, counts


def random_checks(max_n, seeds):
    counts = dict(positive_blocks=0, source_gains=0, outward_gains=0)
    trials = events = 0
    worst = (0, None)
    for n in range(3, max_n + 1):
        for seed in range(seeds):
            for age_bound in (0, 1, 1000000):
                rng = Random(1000003 * n + 7919 * seed + age_bound)
                order = list(range(n))
                rng.shuffle(order)
                x = [{} for _ in range(n)]
                for j, p in enumerate(order[1:], 1):
                    q = rng.choice(order[:j])
                    x[p][q] = rng.randint(0, age_bound)
                for p in range(n):
                    pool = [q for q in range(n) if q != p and q not in x[p]]
                    rng.shuffle(pool)
                    for q in pool[:rng.randrange(3 - len(x[p]))]:
                        x[p][q] = rng.randint(0, age_bound)
                assert connected(x)
                a = rng.randrange(n)
                z = Actual(x, 2)
                construct(z, a, counts)
                trials += 1
                events += z.steps
                worst = max(worst, (z.steps, (n, seed, age_bound, L(n))))
    return trials, events, worst, counts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=30)
    ap.add_argument('--seeds', type=int, default=12)
    ap.add_argument('--availability-n', type=int, default=5)
    args = ap.parse_args()
    if args.max_n < 3 or args.seeds < 1 or args.availability_n < 3:
        ap.error('require max-n>=3, seeds>=1, availability-n>=3')
    if not __debug__:
        ap.error('assertions must be enabled')
    print('PASS complete_paths', random_checks(args.max_n, args.seeds))
    print('PASS availability_functional_states', availability_exhaustive(args.availability_n))


if __name__ == '__main__':
    main()
