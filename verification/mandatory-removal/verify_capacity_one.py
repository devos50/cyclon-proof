"""Exact finite checks for the arbitrary-n mandatory-removal tree theorem."""

from collections import Counter, deque
from itertools import permutations, product
import json


def move(state, p):
    q = state[p]
    if q == -1:
        return state
    r = state[q]
    updated = list(state)
    updated[p] = -1 if r in (-1, p) else r
    updated[q] = p
    return tuple(updated)


def connected(state):
    adjacency = [set() for _ in state]
    for p, q in enumerate(state):
        if q != -1:
            adjacency[p].add(q)
            adjacency[q].add(p)
    seen = {0}
    todo = [0]
    while todo:
        for q in adjacency[todo.pop()] - seen:
            seen.add(q)
            todo.append(q)
    return len(seen) == len(state)


def cycle(state):
    trail = []
    current = 0
    while current != -1 and current not in trail:
        trail.append(current)
        current = state[current]
    return () if current == -1 else tuple(trail[trail.index(current):])


def check(n):
    choices = [tuple(q for q in range(-1, n) if q != p)
               for p in range(n)]
    states = [s for s in product(*choices) if connected(s)]
    trees = {s for s in states if -1 in s}
    assert len(trees) == n ** (n - 1)
    marked = 0
    for state in states:
        reduced = state
        steps = 0
        while (vertices := cycle(reduced)):
            previous_length = len(vertices)
            reduced = move(reduced, vertices[0])
            steps += 1
            assert len(cycle(reduced)) < previous_length
        assert reduced in trees and steps <= n - 1
        for p in range(n):
            result = move(state, p)
            assert connected(result)
            if state in trees:
                assert result in trees
                inverse = p if state[p] == -1 else state[p]
                assert move(result, inverse) == state
                marked += 1

    # Irreducibility is checked independently by graph exploration.
    star = (-1,) + (0,) * (n - 1)
    visited = {star}
    queue = deque([star])
    while queue:
        state = queue.popleft()
        for p in range(n):
            result = move(state, p)
            if result not in visited:
                visited.add(result)
                queue.append(result)
    assert visited == trees
    for observer in range(n):
        counts = Counter(state[observer] for state in trees)
        assert len(counts) == n
        assert set(counts.values()) == {len(trees) // n}

    swaps = 0
    for tail in permutations(range(1, n)):
        order = (0,) + tail
        state_list = [-1] * n
        for u, v in zip(order, order[1:]):
            state_list[u] = v
        state = tuple(state_list)
        for index in range(1, n - 1):
            x, u, v = order[index - 1:index + 2]
            result = state
            for initiator in (x, x, u, v):
                result = move(result, initiator)
            swapped = list(order)
            swapped[index], swapped[index + 1] = (
                swapped[index + 1], swapped[index])
            expected = [-1] * n
            for a, b in zip(swapped, swapped[1:]):
                expected[a] = b
            assert result == tuple(expected)
            swaps += 1
    return {
        "n": n,
        "connected_identity_states": len(states),
        "rooted_tree_states": len(trees),
        "marked_tree_transitions": marked,
        "anchored_path_swaps": swaps,
    }


if __name__ == "__main__":
    print(json.dumps({
        "status": "All exact checks passed.",
        "capacity_one_mandatory": [check(n) for n in range(2, 7)],
    }, indent=2))
