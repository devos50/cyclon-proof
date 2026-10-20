#!/usr/bin/env python3
"""Verify the constructive mandatory-removal CYCLON proof for shuffle length one.

Run from any directory with Python 3:
    python verification/mandatory-removal/verify_singleton_general.py

The verifier implements the actual numerical-age transition rule. It checks every
requested oldest-partner choice, clearing bound, protected-entry invariant,
connectivity assertion, zero-age block boundary, and final common atom. It tests
all connected forward-cache configurations through five peers at capacities two
and three, plus 264 reproducible random configurations through ten peers with
arbitrary initial ages. These checks corroborate the arbitrary-size written
proof; they do not replace it. Only the Python standard library is required.

Expected summary: passed; 1,102 exhaustive connected forward states; 264 random
aged initializations; largest constructed trajectory 8,472 activations.
"""

from itertools import combinations, product
import json
import random


class ControlledCyclon:
    """A legal, positive-probability controlled trajectory of the exact kernel."""

    def __init__(self, caches, capacity):
        self.caches = [dict(cache) for cache in caches]
        self.population = len(caches)
        self.active_population = self.population
        self.capacity = capacity
        self.activations = 0
        self.clearing_blocks = 0

    def all_ages_zero(self):
        return all(age == 0 for cache in self.caches for age in cache.values())

    def connected(self, vertices):
        vertices = set(vertices)
        if not vertices:
            return True
        reached = {min(vertices)}
        while True:
            enlarged = reached | {
                neighbor
                for peer in vertices
                for neighbor in self.caches[peer]
                if peer in reached and neighbor in vertices
            } | {
                peer
                for peer in vertices
                for neighbor in self.caches[peer]
                if neighbor in reached
            }
            if enlarged == reached:
                return reached == vertices
            reached = enlarged

    def activate(self, initiator, policy=None, partner=None, reply=None):
        cache = self.caches[initiator]
        assert cache
        for neighbor in cache:
            cache[neighbor] += 1
        oldest_age = max(cache.values())
        oldest = [peer for peer, age in cache.items() if age == oldest_age]
        partner = min(oldest) if partner is None else partner
        assert partner in oldest, (initiator, partner, cache)
        responder = self.caches[partner]

        if reply is not None:
            response = reply
        elif initiator in responder:
            response = initiator
        elif policy is not None:
            response = policy(initiator, partner)
        else:
            response = min(responder) if responder else None
        assert (response is None and not responder) or response in responder
        response_age = responder.get(response)

        del cache[partner]
        if response is not None and response != initiator and response not in cache:
            cache[response] = response_age
        if initiator not in responder:
            if len(responder) >= self.capacity:
                assert response is not None
                del responder[response]
            responder[initiator] = 0

        assert all(len(cache) <= self.capacity for cache in self.caches)
        self.activations += 1

    def clear(self, initiator, policy=None, first_partner=None, first_reply=None):
        count = 0
        while self.caches[initiator]:
            self.activate(
                initiator,
                policy,
                partner=first_partner if count == 0 else None,
                reply=first_reply if count == 0 else None,
            )
            count += 1
            assert count <= self.active_population + self.capacity - 1
        self.clearing_blocks += 1

    def canonicalize(self, vertices):
        """Inductively reach the greatest-label sink fan on these vertices."""
        vertices = tuple(sorted(vertices))
        population = len(vertices)
        previous_population = self.active_population
        self.active_population = population
        vertex_set = set(vertices)
        assert self.all_ages_zero() and self.connected(vertices)
        assert all(set(self.caches[peer]) <= vertex_set for peer in vertices)
        if population == 1:
            assert not self.caches[vertices[0]]
            self.active_population = previous_population
            return

        source, remainder = vertices[0], vertices[1:]
        sink = remainder[-1]

        # Separate an unknown source; the passive-source anchor merges the rest.
        self.clear(source)
        for peer in remainder:
            self.clear(peer)
        assert self.all_ages_zero() and self.connected(remainder)
        assert self.caches[source]
        assert all(source not in self.caches[peer] for peer in remainder)
        self.canonicalize(remainder)

        target_count = min(self.capacity, len(remainder))
        target = remainder[-target_count:]
        protected = target[:-1]
        other_vertices = tuple(peer for peer in remainder if peer not in target)

        # Reserve one source descriptor at the largest vertex.
        self.clear(source)
        assert self.caches[sink] == {source: 0}
        assert all(sink in self.caches[peer] for peer in remainder if peer != sink)
        assert self.connected(remainder) and self.all_ages_zero()

        def protect_sink(_initiator, responder):
            cache = self.caches[responder]
            if len(cache) >= self.capacity and sink in cache:
                return min(peer for peer in cache if peer != sink)
            return min(cache) if cache else None

        # Each of the greatest c-1 peers first receives the reserved descriptor.
        for peer in protected:
            assert sink in self.caches[peer] and self.all_ages_zero()
            self.clear(
                peer,
                protect_sink,
                first_partner=sink,
                first_reply=source,
            )
        assert set(self.caches[source]) == set(protected)
        assert set(self.caches[sink]) == {source, *protected}

        def preserve_reservoir_and_targets(_initiator, responder):
            cache = self.caches[responder]
            if responder == sink and len(cache) >= self.capacity:
                return min(peer for peer in cache if peer != source)
            if responder == source and len(cache) >= self.capacity:
                return next(peer for peer in cache if peer not in protected)
            return min(cache) if cache else None

        for peer in other_vertices:
            self.clear(peer, preserve_reservoir_and_targets)
        assert self.all_ages_zero() and source in self.caches[sink]
        assert all(source not in self.caches[peer] for peer in remainder if peer != sink)

        # The final callback inserts the sink and removes the last source copy.
        cache = self.caches[source]
        response = next(
            (peer for peer in cache if peer not in protected),
            min(cache) if cache else None,
        )
        self.clear(
            sink,
            preserve_reservoir_and_targets,
            first_partner=source,
            first_reply=response,
        )
        assert self.all_ages_zero() and self.connected(remainder)
        assert set(self.caches[source]) == set(target)
        assert all(source not in self.caches[peer] for peer in remainder)

        self.canonicalize(remainder)
        for index, peer in enumerate(vertices):
            expected = set(vertices[max(index + 1, population - self.capacity):])
            assert set(self.caches[peer]) == expected
        self.active_population = previous_population


def induction_bound(population, capacity):
    bound = 0
    for active_count in range(2, population + 1):
        bound = 2 * active_count * (active_count + capacity - 1) + 2 * bound
    return bound


def connected_forward_states(population, capacity):
    choices = [
        [
            subset
            for count in range(min(capacity, population - peer - 1) + 1)
            for subset in combinations(range(peer + 1, population), count)
        ]
        for peer in range(population)
    ]
    for state in product(*choices):
        caches = [{neighbor: 0 for neighbor in cache} for cache in state]
        process = ControlledCyclon(caches, capacity)
        if process.connected(range(population)):
            yield process


def main():
    exhaustive_count = 0
    random_count = 0
    largest_trajectory = 0

    for population in range(2, 6):
        for capacity in (2, 3):
            for process in connected_forward_states(population, capacity):
                process.canonicalize(range(population))
                assert process.activations <= induction_bound(population, capacity)
                exhaustive_count += 1
                largest_trajectory = max(largest_trajectory, process.activations)

    generator = random.Random(734)
    for population in range(2, 11):
        for capacity in range(2, min(population + 2, 6)):
            for _sample in range(8):
                caches = []
                for peer in range(population):
                    neighbors = [peer + 1] if peer < population - 1 else []
                    candidates = [
                        other for other in range(population)
                        if other != peer and other not in neighbors
                    ]
                    generator.shuffle(candidates)
                    extra_count = generator.randrange(
                        min(capacity - len(neighbors), len(candidates)) + 1
                    )
                    neighbors += candidates[:extra_count]
                    caches.append({other: generator.randrange(30) for other in neighbors})

                process = ControlledCyclon(caches, capacity)
                for peer in range(population):
                    process.clear(peer)
                assert process.all_ages_zero() and process.connected(range(population))
                process.canonicalize(range(population))
                age_reset_bound = population * (population + capacity - 1)
                assert process.activations <= (
                    age_reset_bound + induction_bound(population, capacity)
                )
                random_count += 1
                largest_trajectory = max(largest_trajectory, process.activations)

    print(json.dumps({
        "status": "passed",
        "exhaustive_connected_forward_states": exhaustive_count,
        "random_aged_initializations": random_count,
        "largest_trajectory_activations": largest_trajectory,
    }, indent=2))


if __name__ == "__main__":
    main()
