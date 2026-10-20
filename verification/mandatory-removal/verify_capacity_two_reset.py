#!/usr/bin/env python3
"""Check the uniform finite-age reset for mandatory CYCLON with c = ell = 2.

Run from the repository root:
    python3 verification/mandatory-removal/verify_capacity_two_reset.py

The default check covers n=3,...,30, initial age bounds 0, 1, 100, and
1,000,000, and seeds 0,...,19. Caches may be empty, underfull, or full;
connectivity is unrestricted. The reproduced run passes 2,240 initial
states and exercises 16,238 forced descriptor migrations. Its longest
execution has 88 exchanges (n=30, age bound=0, seed=12).

The constructive proof uses at most n exchanges per routing or callback
block and at most 2*n*n*(n-1) exchanges overall, regardless of initial
ages. The checks below assert these uniform bounds. The finite checks
support the controller; the arbitrary-size theorem relies on the proof.

Requires only Python and the sibling verify_lineage_erasure.py. Keep
assertions enabled: do not run Python with -O.
"""

import argparse

from verify_lineage_erasure import Chain


def erase(chain):
    n = chain.n
    for identity in range(n):
        immune = {
            peer
            for peer in range(n)
            if identity in chain.x[peer] and not chain.x[peer][identity][1]
        }
        iterations = 0
        while any(identity in cache and cache[identity][1] for cache in chain.x):
            iterations += 1
            assert iterations <= n - 1
            holder = next(
                peer
                for peer in range(n)
                if identity in chain.x[peer] and chain.x[peer][identity][1]
            )
            count = 0
            while True:
                partner, forced = chain.step(
                    holder,
                    identity,
                    immune,
                    identity,
                    callback=True,
                    canonical_pairs=True,
                )
                count += 1
                assert count <= n
                if partner == identity:
                    break
                if forced:
                    holder = partner
                    other = next(other for other in chain.x[holder] if other != identity)
                    assert chain.x[holder][identity][0] > chain.x[holder][other][0]
            callback_peer = holder
            assert identity not in chain.x[callback_peer]
            assert callback_peer in chain.x[identity]

            count = 0
            while True:
                knew_identity = [identity in cache for cache in chain.x]
                partner, forced = chain.step(
                    identity,
                    callback_peer,
                    immune,
                    identity,
                    canonical_pairs=True,
                )
                count += 1
                assert count <= n
                if not knew_identity[partner]:
                    assert identity in chain.x[partner]
                    assert not chain.x[partner][identity][1]
                    assert partner not in immune
                    immune.add(partner)
                    break
                assert not forced
        assert all(
            identity not in cache or not cache[identity][1] for cache in chain.x
        )
    assert not any(old for cache in chain.x for _, old in cache.values())
    assert chain.moves <= 2 * n * n * (n - 1)
    assert max([age for cache in chain.x for age, _ in cache.values()] + [0]) <= chain.moves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=30)
    parser.add_argument("--seeds", type=int, default=20)
    parser.add_argument("--ages", type=int, nargs="+", default=[0, 1, 100, 1000000])
    args = parser.parse_args()
    if args.max_n < 3 or args.seeds < 1 or min(args.ages) < 0:
        parser.error("require --max-n >= 3, --seeds >= 1, and nonnegative --ages")
    if not __debug__:
        parser.error("assertions must be enabled; do not use python -O")

    total = 0
    worst = 0
    worst_case = None
    migrations = 0
    for n in range(3, args.max_n + 1):
        for max_age in args.ages:
            for seed in range(args.seeds):
                chain = Chain(n, 2, 2, seed, max_age)
                erase(chain)
                total += 1
                migrations += chain.migrations
                if chain.moves > worst:
                    worst = chain.moves
                    worst_case = (n, max_age, seed)
    print(
        f"Passed {total} initial states. Forced migrations {migrations}; "
        f"maximum exchanges {worst}; case {worst_case}."
    )


if __name__ == "__main__":
    main()
