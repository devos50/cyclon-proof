#!/usr/bin/env python3
"""Check the constructive initial-lineage erasure proof for mandatory CYCLON.

Run from the repository root:
    python3 verification/mandatory-removal/verify_lineage_erasure.py

The defaults cover all 1 <= shuffle length <= capacity <= n - 1 for
n = 2, ..., 10, with seeds 0, ..., 19. Initial cache sizes are random,
including empty and underfull caches; ages are integers in [0, 100].
Connectivity is unrestricted. Every initial descriptor is marked old,
copies inherit their mark, and fresh self descriptors are marked fresh.

The reproduced default run checks 3,300 initial states, exercises 307
forced descriptor migrations, and takes at most 2,237 exchanges in one
case (n=9, capacity=8, shuffle length=8, seed=4). This checks the concrete
controller and its invariants; the arbitrary-size result relies on the
symbolic proof in main.tex.

No external packages are required. The assertions check legal buffers
and victims, preservation of immune peers, the numerical routing bounds,
fresh insertion at each callback, extinction of all initial lineages,
and the final age bound. They must remain enabled (do not use python -O).
"""

import argparse
from random import Random


class Chain:
    def __init__(self, n, capacity, shuffle_length, seed, max_age=100):
        self.n = n
        self.c = capacity
        self.l = shuffle_length
        self.rng = Random(seed)
        self.t = 0
        self.x = []
        for peer in range(n):
            identities = [other for other in range(n) if other != peer]
            self.rng.shuffle(identities)
            size = self.rng.randint(0, min(capacity, n - 1))
            self.x.append(
                {
                    other: (self.rng.randrange(max_age + 1), True)
                    for other in identities[:size]
                }
            )
        self.initial_max = max(
            [age for cache in self.x for age, _ in cache.values()] + [0]
        )
        self.moves = 0
        self.migrations = 0

    def choose(self, identities, size, exclude=None):
        candidates = [other for other in identities if other != exclude]
        assert len(candidates) >= size
        self.rng.shuffle(candidates)
        return candidates[:size]

    def global_ages(self):
        return [
            max([cache[identity][0] for cache in self.x if identity in cache] + [0])
            for identity in range(self.n)
        ]

    def step(
        self, initiator, target, immune, identity, callback=False, canonical_pairs=False
    ):
        """Make one legal controlled exchange, preserving the designated entries."""
        p = initiator
        cache_p = self.x[p]
        size_p = len(cache_p)
        assert target in cache_p
        oldest_age = max(value[0] for value in cache_p.values())
        oldest = [other for other in cache_p if cache_p[other][0] == oldest_age]
        q = self.rng.choice(oldest)
        cache_q = self.x[q]
        size_q = len(cache_q)
        extra_size = min(self.l - 1, size_p - 1)
        reply_size = min(self.l, size_q)
        eligible_extra = [other for other in cache_p if other != q]
        excluded = (
            target if target != q and len(eligible_extra) > extra_size else None
        )
        extra = self.choose(eligible_extra, extra_size, excluded)

        protected_q = identity if q in immune else None
        if callback and q == identity:
            protected_q = p if p in cache_q else None
        excluded_q = protected_q if size_q > reply_size else None
        reply = self.choose(cache_q, reply_size, excluded_q)

        remaining_p = {
            other: (value[0] + 1, value[1])
            for other, value in cache_p.items()
            if other != q
        }
        outgoing = {p: (0, False), **{other: remaining_p[other] for other in extra}}
        incoming_p = {
            other: cache_q[other]
            for other in reply
            if other != p and other not in remaining_p
        }
        incoming_q = {
            other: value
            for other, value in outgoing.items()
            if other != q and other not in cache_q
        }
        replacements_p = max(0, len(remaining_p) + len(incoming_p) - self.c)
        replacements_q = max(0, size_q + len(incoming_q) - self.c)

        victims_p = [other for other in extra if other != target]
        self.rng.shuffle(victims_p)
        forced = replacements_p > len(victims_p)
        if forced:
            victims_p.append(target)
        victims_p = victims_p[:replacements_p]
        if canonical_pairs and q != target:
            assert self.c == self.l == 2
            victims_q = [other for other in reply if other not in (p, target)]
            assert len(victims_q) == replacements_q
        else:
            victims_q = [other for other in reply if other != protected_q]
            assert replacements_q <= len(victims_q)
            self.rng.shuffle(victims_q)
            victims_q = victims_q[:replacements_q]

        if forced:
            assert self.l == self.c
            assert len(incoming_p) == self.c and size_q == self.c
            assert not set(cache_q) & (set(cache_p) | {p})
            assert target in incoming_q
            self.migrations += 1

        self.x[p] = {
            other: value
            for other, value in remaining_p.items()
            if other not in victims_p
        } | incoming_p
        self.x[q] = {
            other: value
            for other, value in cache_q.items()
            if other not in victims_q
        } | incoming_q
        for peer in immune:
            assert identity in self.x[peer] and not self.x[peer][identity][1]
        self.t += 1
        self.moves += 1
        return q, forced

    def erase(self):
        """Execute the proof's routing and immunity construction for every identity."""
        for identity in range(self.n):
            immune = {
                peer
                for peer in range(self.n)
                if identity in self.x[peer] and not self.x[peer][identity][1]
            }
            iterations = 0
            while any(identity in cache and cache[identity][1] for cache in self.x):
                iterations += 1
                assert iterations <= self.n - 1
                holder = next(
                    peer
                    for peer in range(self.n)
                    if identity in self.x[peer] and self.x[peer][identity][1]
                )
                target_age = self.x[holder][identity][0]
                maxima = self.global_ages()
                limit = 1 + sum(
                    max(0, maxima[other] - target_age + 1)
                    for other in range(self.n)
                    if other != identity
                )
                count = 0
                while True:
                    partner, forced = self.step(
                        holder, identity, immune, identity, callback=True
                    )
                    count += 1
                    assert count <= limit
                    if partner == identity:
                        break
                    if forced:
                        holder = partner
                    assert identity in self.x[holder] and self.x[holder][identity][1]

                callback_peer = holder
                assert identity not in self.x[callback_peer]
                assert callback_peer in self.x[identity]
                target_age = self.x[identity][callback_peer][0]
                maxima = self.global_ages()
                limit = 1 + sum(
                    max(0, maxima[other] - target_age + 1)
                    for other in range(self.n)
                    if other not in (identity, callback_peer)
                )
                count = 0
                while True:
                    partner, forced = self.step(
                        identity, callback_peer, immune, identity
                    )
                    count += 1
                    assert count <= limit
                    if partner == callback_peer or forced:
                        assert identity in self.x[partner]
                        assert not self.x[partner][identity][1]
                        assert partner not in immune
                        immune.add(partner)
                        break
            assert all(
                identity not in cache or not cache[identity][1] for cache in self.x
            )
        assert not any(old for cache in self.x for _, old in cache.values())
        assert max([age for cache in self.x for age, _ in cache.values()] + [0]) <= self.moves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=10)
    parser.add_argument("--seeds", type=int, default=20)
    parser.add_argument("--max-age", type=int, default=100)
    args = parser.parse_args()
    if args.max_n < 2 or args.seeds < 1 or args.max_age < 0:
        parser.error("require --max-n >= 2, --seeds >= 1, and --max-age >= 0")
    if not __debug__:
        parser.error("assertions must be enabled; do not use python -O")

    total = 0
    migrations = 0
    worst = 0
    worst_case = None
    for n in range(2, args.max_n + 1):
        for capacity in range(1, n):
            for shuffle_length in range(1, capacity + 1):
                for seed in range(args.seeds):
                    chain = Chain(n, capacity, shuffle_length, seed, args.max_age)
                    chain.erase()
                    total += 1
                    migrations += chain.migrations
                    if chain.moves > worst:
                        worst = chain.moves
                        worst_case = (n, capacity, shuffle_length, seed)
    print(
        f"Passed {total} initial states. Forced migrations {migrations}; "
        f"maximum exchanges {worst}; case {worst_case}."
    )


if __name__ == "__main__":
    main()
