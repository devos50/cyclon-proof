#!/usr/bin/env python3
"""Bounded exact diagnostic for a constant-threshold censored lower kernel.

Only rows with maximum PRE-event age >=1 may initiate. Rows containing
only zeros (including empty rows) are frozen. Boundary-crossing transitions
are recorded, never clipped. This is not the variable-secondary embedding.
"""
from collections import deque
from itertools import combinations, product
import argparse
from random import Random


def freeze(rows):
    return tuple(tuple(sorted(row.items())) for row in rows)


def connected(state):
    reached = {0}
    while True:
        more = reached | {v for u, row in enumerate(state) if u in reached for v, _ in row}
        more |= {u for u, row in enumerate(state) if any(v in reached for v, _ in row)}
        if more == reached:
            return len(reached) == len(state)
        reached = more


def successors(state, c, ell, threshold=1):
    rows = [dict(row) for row in state]
    result = set()
    for p, row in enumerate(rows):
        if not row or max(row.values()) < threshold:
            continue
        aged = {v: age + 1 for v, age in row.items()}
        for q in row:
            if row[q] != max(row.values()):
                continue
            for extra_tuple in combinations(sorted(set(row) - {q}), min(ell - 1, len(row) - 1)):
                extra = set(extra_tuple)
                request = {p: 0, **{v: aged[v] for v in extra}}
                resident = {v: age for v, age in aged.items() if v != q}
                for reply_tuple in combinations(sorted(rows[q]), min(ell, len(rows[q]))):
                    reply = {v: rows[q][v] for v in reply_tuple}
                    validp, validq = set(reply) - {p}, set(request) - {q}
                    dp = max(0, len(resident) + len(validp - set(resident)) - c)
                    dq = max(0, len(rows[q]) + len(validq - set(rows[q])) - c)
                    ep, eq = extra & set(resident) - validp, set(reply) - validq
                    for vp in combinations(sorted(ep), dp):
                        for vq in combinations(sorted(eq), dq):
                            A = {v: age for v, age in resident.items() if v not in vp}
                            B = {v: age for v, age in rows[q].items() if v not in vq}
                            for v in validp:
                                A[v] = min(A.get(v, reply[v]), reply[v])
                            for v in validq:
                                B[v] = min(B.get(v, request[v]), request[v])
                            output = list(rows)
                            output[p], output[q] = A, B
                            result.add(freeze(output))
    return result


def run(n, c, ell, bound):
    row_options = []
    for p in range(n):
        options = []
        for size in range(c + 1):
            for ids in combinations([v for v in range(n) if v != p], size):
                for ages in product(range(bound + 1), repeat=size):
                    options.append(tuple(zip(ids, ages)))
        row_options.append(options)
    states = list(product(*row_options))
    index = {s: i for i, s in enumerate(states)}
    reverse = [[] for _ in states]
    escape = set()
    targets = []
    edges = 0
    for i, state in enumerate(states):
        if all(age == 0 for row in state for _, age in row):
            targets.append(i)
        for successor in successors(state, c, ell):
            j = index.get(successor)
            if j is None:
                escape.add(i)
            else:
                reverse[j].append(i)
            edges += 1
    distance = {i: 0 for i in targets}
    witness = {}
    queue = deque(targets)
    while queue:
        j = queue.popleft()
        for i in reverse[j]:
            if i not in distance:
                distance[i] = distance[j] + 1
                witness[i] = j
                queue.append(i)
    initial = [i for i, state in enumerate(states)
               if connected(state) and all(age <= 1 for row in state for _, age in row)]
    failures = [i for i in initial if i not in distance]
    # Greatest subset of non-target-unreachable states with no outgoing
    # transition outside the subset. Any surviving connected state is an
    # exact finite closed obstruction, not an age-truncation artifact.
    removed = set(distance) | escape
    queue = deque(removed)
    while queue:
        j = queue.popleft()
        for i in reverse[j]:
            if i not in removed:
                removed.add(i)
                queue.append(i)
    closed_bad = [i for i in range(len(states)) if i not in removed and connected(states[i])]
    longest = max((distance[i] for i in initial if i in distance), default=0)
    print(f'n={n} c={c} ell={ell} age_bound={bound}: '
          f'states={len(states)} edges={edges} boundary_sources={len(escape)} '
          f'initial_0_1_connected={len(initial)} witnessed={len(initial)-len(failures)} '
          f'max_witness_length={longest} closed_nonzero_connected={len(closed_bad)}')
    if failures:
        print('  unresolved initial (not a counterexample):', states[failures[0]])
    if closed_bad:
        print('  EXACT CLOSED NONZERO OBSTRUCTION contains:', states[closed_bad[0]])
    # Replay one longest certified path through the original, uncapped rule.
    if initial and any(i in distance for i in initial):
        i = max((i for i in initial if i in distance), key=lambda i: distance[i])
        while distance[i]:
            j = witness[i]
            assert states[j] in successors(states[i], c, ell)
            i = j
        assert all(age == 0 for row in states[i] for _, age in row)


def sampled_search(n, c, ell, count=12, depth_bound=8, state_limit=10000):
    results = []
    for seed in range(count):
        rng = Random(10000 * n + 100 * ell + seed)
        rows = []
        for v in range(n):
            row = {(v + 1) % n: rng.choice((0, 1, 2, 7))}
            available = sorted(set(range(n)) - {v} - set(row))
            for w in rng.sample(available, rng.randrange(min(c - 1, len(available)) + 1)):
                row[w] = rng.choice((0, 1, 2, 7))
            rows.append(row)
        start = freeze(rows)
        assert connected(start)
        queue, seen = deque([(start, 0)]), {start}
        distance = None
        maximum_age = max(age for row in start for _, age in row)
        exhausted = False
        while queue:
            state, depth = queue.popleft()
            if all(age == 0 for row in state for _, age in row):
                distance = depth
                break
            if depth == depth_bound:
                continue
            for successor in sorted(successors(state, c, ell)):
                maximum_age = max(maximum_age, max((age for row in successor for _, age in row), default=0))
                if successor in seen:
                    continue
                if len(seen) >= state_limit:
                    exhausted = True
                    break
                seen.add(successor)
                queue.append((successor, depth + 1))
            if exhausted:
                break
        results.append((distance, len(seen), maximum_age, exhausted))
    found = [d for d, _, _, _ in results if d is not None]
    print(f'SAMPLED n={n} c={c} ell={ell}: starts={count} '
          f'witnessed={len(found)} max_witness={max(found, default=0)} '
          f'depth_limit={depth_bound} state_limit={state_limit} '
          f'max_seen={max(r[1] for r in results)} max_age_seen={max(r[2] for r in results)} '
          f'state_limit_stops={sum(r[3] for r in results)}')
    return results


def check_singleton_threshold():
    transitions = 0
    for n in range(2, 7):
        for threshold in (1, 2, 7, 10**6):
            for seed in range(20):
                rng = Random(n * 10000 + threshold + seed)
                rows = []
                for v in range(n):
                    row = {}
                    if rng.randrange(4):
                        q = rng.choice(sorted(set(range(n)) - {v}))
                        row[q] = rng.choice((0, threshold - 1, threshold, threshold + 1, 10**6))
                    rows.append(row)
                state = freeze(rows)
                high = sum(age >= threshold for row in state for _, age in row)
                for after in successors(state, 1, 1, threshold):
                    assert sum(age >= threshold for row in after for _, age in row) <= high - 1
                    transitions += 1
    print('PASS singleton arbitrary-threshold high-count checks:', transitions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--age-bound', type=int, default=2)
    parser.add_argument('--sample-only', action='store_true')
    args = parser.parse_args()
    assert args.age_bound >= 1
    check_singleton_threshold()
    if args.sample_only:
        for n, c, ell in ((4, 2, 1), (4, 2, 2), (5, 3, 3)):
            sampled_search(n, c, ell)
    else:
        for n, c, ell in ((2, 1, 1), (3, 1, 1), (3, 2, 1), (3, 2, 2), (4, 1, 1)):
            run(n, c, ell, args.age_bound)
    print('Diagnostic only: explicit finite search limits; no generic reachability conclusion.')


if __name__ == '__main__':
    main()
