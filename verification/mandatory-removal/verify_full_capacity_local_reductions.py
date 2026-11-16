#!/usr/bin/env python3
"""Focused local checks for the full-capacity all-lengths candidate.

Checks only q-free embedding, source-to-canonical universal-zero creation,
and a cross-component edge insertion. No source erasure, normalization
path, closed-class existence, or induction theorem is proved by this file.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree
from verify_shared_zero_secondary_embedding import lower_step


def edges(rows):
    return {tuple(sorted((v, u))) for v, row in enumerate(rows) for u in row}


def canonical(vertices, root):
    order = sorted(set(vertices) - {root}) + [root]
    return {v: dict.fromkeys(order[i + 1:], 0) for i, v in enumerate(order)}


def qfree_embedding(n, L, seed):
    rng = Random(seed)
    m = n - 1
    lower = []
    for v in range(m):
        candidates = sorted(set(range(m)) - {v})
        lower.append({u: rng.choice((0, 1, 9, 10**6))
                      for u in rng.sample(candidates, rng.randrange(m))})
    frozen = {u: rng.choice((0, 1, 10**6))
              for u in rng.sample(list(range(1, n)), rng.randrange(n))}
    z = ActualThree([frozen] + [{u + 1: age for u, age in row.items()} for row in lower], n - 1, L)
    stats = Counter({'qfree_starts': 1, 'effective_length_clipped': L > n - 2})
    for _ in range(12):
        transition = lower_step(lower, n - 2, min(L, n - 2), rng)
        if transition is None:
            assert all(not row for row in z.x[1:])
            break
        lower, p, q, extra, reply, vp, vq, metrics = transition
        assert not vp and not vq
        before_edges = edges(z.x)
        z.step(p + 1, q + 1, {u + 1 for u in extra}, {u + 1 for u in reply}, vp=set(), vq=set())
        assert z.x[0] == frozen
        assert z.x[1:] == [{u + 1: age for u, age in row.items()} for row in lower]
        assert all(0 not in row for row in z.x[1:])
        assert before_edges <= edges(z.x)
        stats['qfree_events'] += 1
        stats['qfree_MIN_refreshes'] += metrics['minimum_refreshes']
        stats['qfree_empty_responders'] += metrics['empty_responder']
    return stats


def source_universal(n, L, seed):
    assert L >= 2
    rng = Random(seed)
    q = 0
    W = set(range(1, n))
    source = {u: rng.choice((0, 1, 9, 10**6))
              for u in rng.sample(sorted(W), rng.randint(1, n - 1))}
    u = min(source, key=lambda v: (-source[v], v))
    r = rng.choice(sorted(W - {u}))
    core = canonical(W, r)
    rows = [source] + [core[v] for v in range(1, n)]
    original = [dict(row) for row in rows]
    extra = set(rng.sample(sorted(set(source) - {u}), min(L - 1, len(source) - 1)))
    reply = {r}
    reply |= set(rng.sample(sorted(set(rows[u]) - {r}), min(L, len(rows[u])) - 1))
    z = ActualThree(rows, n - 1, L)
    z.step(q, u, extra, reply, vp=set(), vq=set())
    assert all(z.x[v].get(r) == 0 for v in range(n) if v != r)
    assert z.x[r] == {}
    assert all(z.x[v] == original[v] for v in W - {u})
    assert edges(original) <= edges(z.x)
    return Counter({'source_universal_events': 1,
                    'source_underfull': len(source) < n - 1,
                    'source_singleton': len(source) == 1})


def bridge(n, L, seed):
    assert L >= 2
    rng = Random(seed)
    q = 0
    W = list(range(1, n))
    component_count = rng.randint(2, min(4, len(W)))
    groups = [set(W[j::component_count]) for j in range(component_count)]
    belonging = {v: j for j, group in enumerate(groups) for v in group}
    source_ids = {rng.choice(sorted(group)) for group in groups}
    available = sorted(set(W) - source_ids)
    source_ids |= set(rng.sample(available, rng.randrange(len(available) + 1)))
    source = {v: rng.choice((0, 1, 9, 10**6)) for v in source_ids}
    u = min(source, key=lambda v: (-source[v], v))
    v = rng.choice(sorted(w for w in source if belonging[w] != belonging[u]))
    core = {}
    for group in groups:
        core.update(canonical(group, max(group)))
    rows = [source] + [core[w] for w in W]
    original = [dict(row) for row in rows]
    extra = {v}
    extra |= set(rng.sample(sorted(set(source) - {u, v}), min(L - 1, len(source) - 1) - 1))
    reply = set(rng.sample(sorted(rows[u]), min(L, len(rows[u]))))
    assert tuple(sorted((u, v))) not in edges(rows)
    z = ActualThree(rows, n - 1, L)
    z.step(q, u, extra, reply, vp=set(), vq=set())
    assert v in z.x[u]
    assert tuple(sorted((u, v))) in edges(z.x)
    assert edges(original) <= edges(z.x)
    assert all(z.x[w] == original[w] for w in W if w != u)
    return Counter({'component_bridge_events': 1, 'bridge_empty_responder': not original[u],
                    'bridge_underfull_source': len(source) < n - 1})


def main():
    stats = Counter()
    for n in range(3, 17):
        for L in range(1, n):
            for seed in range(8):
                key = n * 10000 + L * 100 + seed
                stats.update(qfree_embedding(n, L, key))
                if L >= 2:
                    stats.update(source_universal(n, L, key))
                    stats.update(bridge(n, L, key))
    # At n=2 the q-free complement is a single empty row: omit its no-op.
    singleton = ActualThree([{1: 10**6}, {}], 1, 1)
    assert singleton.x[1] == {} and singleton.steps == 0
    assert stats['source_singleton'] and stats['bridge_empty_responder']
    print('PASS full-capacity local reductions:', dict(sorted(stats.items())))
    print('Scope: local events only; no source-erasure, normalization, or induction assertion.')


if __name__ == '__main__':
    main()
