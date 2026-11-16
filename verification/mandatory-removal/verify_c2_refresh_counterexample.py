#!/usr/bin/env python3
"""Exact c=ell=2 counterexamples to naive refresh/mixing arguments.

Run from the repository root:
    python3 verification/mandatory-removal/verify_c2_refresh_counterexample.py

All probabilities use fractions.Fraction, including every oldest tie and
eligible passive victim choice. Colored handles exact numeric MIN ages and
proof-only OLD/YOUNG OR marks; all initial entries are OLD. These examples
do not contradict convergence. They show that refreshing all descriptors,
or merely making the interaction graph connected, does not itself make a
sample uniform, and that old-copy count need not have negative drift.
"""
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_general_two import Colored


def fixed_initiator_outcomes(z, p):
    """Return every legal c=ell=2 transition and its conditional probability."""
    if not z.x[p]:
        return [(deepcopy(z), Fraction(1), None)]
    oldest = [q for q in z.x[p]
              if z.x[p][q] == max(z.x[p].values())]
    outcomes = []
    for q in oldest:
        extra = set(z.x[p]) - {q}
        reply = set(z.x[q])
        incoming = {p} | extra
        needed = max(0, len(z.x[q]) +
                     len(incoming - set(z.x[q]) - {q}) - 2)
        victims = list(combinations(sorted(reply - incoming), needed))
        assert victims
        for vq in victims:
            out = deepcopy(z)
            out.step(p, q, extra, reply, vq=vq)
            outcomes.append((out, Fraction(1, len(oldest) * len(victims)),
                             (p, q)))
    assert sum(prob for _, prob, _ in outcomes) == 1
    return outcomes


def old_count(z):
    return sum(map(len, z.x)) - z.F()


def check_refresh_counterexample():
    start = [{}, {0: 0}, {0: 0}]
    availability = Fraction(0)
    joint = {0: Fraction(0), 2: Fraction(0)}
    terminal_paths = 0
    total_mass = Fraction(0)
    for order in permutations(range(3)):
        paths = [(Colored(start, 2), Fraction(1, 6), set())]
        for p in order:
            paths = [
                (out, weight * prob,
                 edges | ({tuple(sorted(edge))} if edge else set()))
                for z, weight, edges in paths
                for out, prob, edge in fixed_initiator_outcomes(z, p)
            ]
        for z, weight, edges in paths:
            terminal_paths += 1
            total_mass += weight
            assert old_count(z) == 0, (order, z.x, z.young)
            reached = {0}
            for _ in range(3):
                reached |= {b for a, b in edges if a in reached}
                reached |= {a for a, b in edges if b in reached}
            assert reached == {0, 1, 2}
            if z.x[1]:
                availability += weight
                for peer in z.x[1]:
                    joint[peer] += weight / len(z.x[1])
    assert total_mass == 1
    assert availability == Fraction(7, 12)
    assert joint == {0: Fraction(1, 4), 2: Fraction(1, 3)}
    conditional = {p: mass / availability for p, mass in joint.items()}
    assert conditional == {0: Fraction(3, 7), 2: Fraction(4, 7)}
    return terminal_paths, availability, conditional


def check_old_count_positive_drift():
    z = Colored([{2: 0}, {0: 1}, {0: 0}], 2)
    # Legal positive-probability history from all-OLD initialization.
    for p, q in [(1, 0), (1, 2), (2, 1), (2, 0)]:
        z.step(p, q, set(z.x[p]) - {q}, set(z.x[q]))
    assert z.x == [{2: 0, 1: 0}, {0: 0, 2: 0}, {1: 0}]
    assert z.young == [{1, 2}, {2}, {1}]
    assert old_count(z) == 1
    drift = sum(
        prob * (old_count(out) - old_count(z)) / z.n
        for p in range(z.n)
        for out, prob, _ in fixed_initiator_outcomes(z, p)
    )
    assert drift == Fraction(1, 6)
    return drift


def check_iid_two_event_refresh_counterexample():
    """Actual iid scheduler, deterministic horizon, then condition on refreshing.

    This is not the separate random-permutation experiment. Enumerate all
    ordinary two-event paths before imposing the freshness event.
    """
    paths = [(Colored([{}, {0: 0}, {0: 0}], 2), Fraction(1), (), set())]
    for _ in range(2):
        paths = [
            (out, weight * probability / 3, history + (initiator,),
             edges | ({tuple(sorted(edge))} if edge else set()))
            for state, weight, history, edges in paths
            for initiator in range(3)
            for out, probability, edge in fixed_initiator_outcomes(state, initiator)
        ]
    assert sum(weight for _, weight, _, _ in paths) == 1
    fresh = [(state, weight, history, edges)
             for state, weight, history, edges in paths if old_count(state) == 0]
    assert {history for _, _, history, _ in fresh} == {(1, 2), (2, 1)}
    assert all(edges == {(0, 1), (0, 2)} for _, _, _, edges in fresh)
    event_mass = sum(weight for _, weight, _, _ in fresh)
    availability_mass = sum(weight for state, weight, _, _ in fresh if state.x[1])
    joint = {
        peer: sum(weight / len(state.x[1]) for state, weight, _, _ in fresh
                  if peer in state.x[1])
        for peer in (0, 2)
    }
    assert event_mass == Fraction(2, 9)
    assert availability_mass == Fraction(1, 9)
    assert joint == {0: 0, 2: Fraction(1, 9)}
    conditional = {peer: mass / availability_mass for peer, mass in joint.items()}
    assert conditional == {0: 0, 2: 1}
    return event_mass, availability_mass / event_mass, conditional


def check_successful_source_cover_counterexample():
    """Condition on all three initiations actually emitting fresh selves."""
    start = [{}, {0: 0}, {0: 0}]
    event_mass = availability_mass = Fraction(0)
    joint = {0: Fraction(0), 2: Fraction(0)}
    for order in permutations(range(3)):
        paths = [(Colored(start, 2), Fraction(1, 6), set())]
        for p in order:
            paths = [
                (out, weight * prob,
                 successful | ({p} if z.x[p] else set()))
                for z, weight, successful in paths
                for out, prob, _ in fixed_initiator_outcomes(z, p)
            ]
        for z, weight, successful in paths:
            assert old_count(z) == 0
            if successful != {0, 1, 2}:
                continue
            event_mass += weight
            if z.x[1]:
                availability_mass += weight
                for peer in z.x[1]:
                    joint[peer] += weight / len(z.x[1])
    assert event_mass == Fraction(2, 3)
    assert availability_mass == Fraction(5, 12)
    assert joint == {0: Fraction(1, 4), 2: Fraction(1, 6)}
    availability = availability_mass / event_mass
    conditional = {p: mass / availability_mass for p, mass in joint.items()}
    assert availability == Fraction(5, 8)
    assert conditional == {0: Fraction(3, 5), 2: Fraction(2, 5)}
    return event_mass, availability, conditional


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled; do not use python -O.")
    paths, availability, conditional = check_refresh_counterexample()
    drift = check_old_count_positive_drift()
    cover_mass, cover_availability, cover_sample = (
        check_successful_source_cover_counterexample())
    iid_mass, iid_availability, iid_sample = check_iid_two_event_refresh_counterexample()
    print("PASS exact permutation terminal paths", paths,
          "availability", availability,
          "conditional sample", conditional,
          "all entries YOUNG and interaction graph connected in every outcome;",
          "reachable OLD-count expected drift", drift)
    print("PASS successful-source-cover conditioning event mass", cover_mass,
          "availability", cover_availability,
          "conditional sample", cover_sample)
    print("PASS iid two-event refreshing event mass", iid_mass,
          "conditional availability", iid_availability,
          "conditional sample", iid_sample, "TV error", Fraction(1, 2))


if __name__ == "__main__":
    main()

