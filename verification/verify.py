#!/usr/bin/env python3
"""Exact finite checks for the accompanying mathematical working note.

Uses only the standard library. Enumeration corroborates the written proofs;
it does not replace the arbitrary-network-size arguments.
"""

from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, permutations, product
import json


def move(state, initiator):
    """Capacity-one retention identity update, with zero-based labels."""
    partner = state[initiator]
    reply = state[partner]
    if reply == initiator:
        return state
    updated = list(state)
    updated[initiator], updated[partner] = reply, initiator
    return tuple(updated)


def reachable(state, start, directed=False):
    adjacency = [set() for _ in state]
    for peer, neighbor in enumerate(state):
        adjacency[peer].add(neighbor)
        if not directed:
            adjacency[neighbor].add(peer)
    seen, queue = {start}, deque([start])
    while queue:
        for other in adjacency[queue.popleft()]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return seen


def check_periodic_certificate():
    state = (2, 3, 1, 0)
    initial = state
    ages = [0] * 4
    assert all(len(reachable(state, i, directed=True)) == 4 for i in range(4))
    trace = [[value + 1 for value in state]]
    triples = []
    for initiator in range(4):
        partner, reply = state[initiator], state[state[initiator]]
        assert len({initiator, partner, reply}) == 3
        triples.append([initiator + 1, partner + 1, reply + 1])
        ages[initiator] += 1
        incoming_age = ages[partner]
        state = move(state, initiator)
        ages[initiator], ages[partner] = incoming_age, 0
        assert ages == [0] * 4
        assert state[0] != 3
        trace.append([value + 1 for value in state])
    assert state == initial
    assert trace == [
        [3, 4, 2, 1], [2, 4, 1, 1], [2, 1, 1, 2],
        [3, 1, 2, 2], [3, 4, 2, 1],
    ]
    return {"trace": trace, "exchange_triples": triples,
            "round_boundary_tv": str(Fraction(2, 3))}


def twin_caches(n, capacity):
    assert n % 2 == 0 and 2 <= capacity <= n - 2
    caches = []
    for pair in range(n // 2):
        first, second = 2 * pair, 2 * pair + 1
        next_first = (first + 2) % n
        candidates = [next_first] + [
            peer for peer in range(n)
            if peer not in {first, second, next_first}
        ]
        common = candidates[:capacity - 1]
        caches.extend([
            {second: 1, **{peer: 0 for peer in common}},
            {first: 1, **{peer: 0 for peer in common}},
        ])
    return caches


def strongly_connected_caches(caches):
    for start in range(len(caches)):
        seen, queue = {start}, deque([start])
        while queue:
            for other in caches[queue.popleft()]:
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        if len(seen) != len(caches):
            return False
    return True


def check_frozen_twins():
    caches = twin_caches(4, 2)
    assert strongly_connected_caches(caches)
    checked = 0
    for length in (1, 2):
        for initiator in range(4):
            partner = max(caches[initiator], key=caches[initiator].get)
            others = set(caches[initiator]) - {partner}
            for extra in combinations(others, length - 1):
                outgoing = {initiator, *extra}
                for response in combinations(caches[partner], length):
                    accepted_by_partner = (
                        outgoing - {partner} - set(caches[partner])
                    )
                    accepted_by_initiator = (
                        set(response) - {initiator} - set(caches[initiator])
                    )
                    assert not accepted_by_partner
                    assert not accepted_by_initiator
                    checked += 1
    # Different local activation counts preserve every strict age gap.
    for step in range(100):
        initiator = (step * step + 3 * step + 1) % 4
        caches[initiator] = {
            peer: age + 1 for peer, age in caches[initiator].items()
        }
        assert max(caches[initiator], key=caches[initiator].get) == (initiator ^ 1)
    general = []
    for n, capacity in ((4, 2), (6, 2), (10, 3), (24, 20)):
        family = twin_caches(n, capacity)
        assert strongly_connected_caches(family)
        for p, cache in enumerate(family):
            q = p ^ 1
            assert set(cache) - {q} == set(family[q]) - {p}
            assert len(cache) == capacity
            assert max(cache, key=cache.get) == q
        general.append({"n": n, "capacity": capacity,
                        "singleton_tv": str(1 - Fraction(capacity, n - 1))})
    return {"all_small_subset_choices_checked": checked, "families": general}


def check_zero_age_absorption():
    caches = [
        {1: 0, 3: 0}, {2: 0, 3: 0}, {0: 0, 1: 0}, {0: 0, 1: 0}
    ]
    assert strongly_connected_caches(caches)
    triples = [(1, 3, 0), (0, 3, 1), (2, 0, 1),
               (2, 0, 3), (3, 1, 0), (3, 1, 2)]
    probability = Fraction(1)
    for initiator, partner, reply in triples:
        caches[initiator] = {
            peer: age + 1 for peer, age in caches[initiator].items()
        }
        oldest_age = max(caches[initiator].values())
        oldest = [
            peer for peer, age in caches[initiator].items()
            if age == oldest_age
        ]
        assert partner in oldest and len(oldest) == 2
        assert reply in caches[partner] and len(caches[partner]) == 2
        probability *= Fraction(1, 4 * len(oldest) * len(caches[partner]))
        reply_age = caches[partner][reply]
        if reply != initiator and reply not in caches[initiator]:
            del caches[initiator][partner]
            caches[initiator][reply] = reply_age
        if initiator not in caches[partner]:
            del caches[partner][reply]
            caches[partner][initiator] = 0
    expected = [{3: 1, 2: 0}, {2: 1, 3: 0}, {1: 2, 3: 1}, {0: 2, 2: 1}]
    assert caches == expected
    assert probability == Fraction(1, 2**24)
    for initiator, cache in enumerate(caches):
        partner = max(cache, key=cache.get)
        assert max(caches[partner], key=caches[partner].get) == initiator
        assert set(cache) - {partner} == set(caches[partner]) - {initiator}
    return {"prefix_probability": str(probability),
            "triples": [[v + 1 for v in triple] for triple in triples]}


def check_availability():
    checked = 0
    for n in range(3, 7):
        initiator, partner = 0, 1
        possible_initiator = [v for v in range(n) if v != initiator]
        possible_responder = [v for v in range(n) if v != partner]
        for bits in product((False, True), repeat=n - 1):
            cache = {v for v, chosen in zip(possible_initiator, bits) if chosen}
            if partner not in cache:
                continue
            for reply_bits in product((False, True), repeat=n - 1):
                reply = {
                    v for v, chosen in zip(possible_responder, reply_bits)
                    if chosen
                }
                # Every response subset also lacks the responder's identity.
                possible_post_removal = (cache - {partner}) | (reply - {initiator})
                assert partner not in possible_post_removal
                assert len(possible_post_removal) <= n - 2
                checked += 1
    return {"cache_pairs_checked": checked}


def check_identity_chain(n):
    possibilities = [tuple(v for v in range(n) if v != p) for p in range(n)]
    states = {
        state for state in product(*possibilities)
        if len(reachable(state, 0)) == n
    }
    transitions = {}
    for state in states:
        counts = Counter(move(state, p) for p in range(n))
        transitions[state] = counts
        for p in range(n):
            following = move(state, p)
            assert following in states
            if following != state:
                assert move(following, state[p]) == state
    for state, counts in transitions.items():
        for following, count in counts.items():
            assert transitions[following][state] == count

    unseen = set(states)
    components = []
    while unseen:
        first = next(iter(unseen))
        component, queue = {first}, deque([first])
        unseen.remove(first)
        while queue:
            for following in transitions[queue.popleft()]:
                if following in unseen:
                    unseen.remove(following)
                    component.add(following)
                    queue.append(following)
        for observer in range(n):
            local = Counter(state[observer] for state in component)
            assert set(local) == set(range(n)) - {observer}
            assert len(set(local.values())) == 1
        components.append(component)
    expected = {2: [1], 3: [4, 4], 4: [78], 5: [944], 6: [13800]}
    sizes = sorted(map(len, components))
    assert sizes == expected[n]

    swap_checks = 0
    if n >= 4:
        # Every directed Hamiltonian cycle with vertex zero as anchor.
        for order in permutations(range(1, n)):
            cycle = (0,) + order
            state = [None] * n
            for index, peer in enumerate(cycle):
                state[peer] = cycle[(index + 1) % n]
            state = tuple(state)
            for position in range(1, n - 1):
                x, a, b = cycle[position - 1:position + 2]
                result = state
                for p in (x, x, a, b):
                    result = move(result, p)
                target_order = list(cycle)
                target_order[position:position + 2] = (b, a)
                expected_state = [None] * n
                for index, peer in enumerate(target_order):
                    expected_state[peer] = target_order[(index + 1) % n]
                assert result == tuple(expected_state)
                swap_checks += 1
    return {"n": n, "connected_states": len(states),
            "communicating_class_sizes": sizes,
            "hamiltonian_swap_words_checked": swap_checks,
            "marked_transitions_checked": n * len(states)}


def main():
    report = {
        "periodic_counterexample": check_periodic_certificate(),
        "frozen_twins": check_frozen_twins(),
        "zero_age_absorption": check_zero_age_absorption(),
        "mandatory_removal_availability": check_availability(),
        "capacity_one": [check_identity_chain(n) for n in range(2, 7)],
        "status": "All exact finite checks passed.",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
