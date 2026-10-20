#!/usr/bin/env python3
"""Exact local-case checks for ordinary c=ell=2 ready-copy drift.

Run from repository root:
    python3 verification/mandatory-removal/verify_c2_ready_drift.py

A full cache {r^A,s^B}, A>=B, is READY for target r. The target is not
either endpoint. Every numeric age, oldest choice, full request/reply,
protected victim outcome, and MIN merge is executed by the independent
Actual kernel. Other cache rows cannot affect this local claim.

The enumerated endpoint pairs on 3..6 labels and ages 0..3 represent every
possible equality/inequality and overlap pattern required by the proof.
Finite checks corroborate the structural case argument; they are not an
arbitrary-size proof. No random sampling, simulations, or third-party
packages are used.
"""
from itertools import combinations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_anchor import Actual


def rows(ids):
    for k in range(3):
        for chosen in combinations(ids, k):
            for aa in product(range(4), repeat=k):
                yield dict(zip(chosen, aa))


def ready(row, target):
    return (len(row) == 2 and target in row
            and row[target] == max(row.values()))


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled; do not use python -O.")
    cases = deaths = creations = transports = 0
    target, p, q = 0, 1, 2
    for n in range(3, 7):
        for P in rows([v for v in range(n) if v != p]):
            if q not in P or P[q] != max(P.values()):
                continue
            for Q in rows([v for v in range(n) if v != q]):
                extra, reply = set(P) - {q}, set(Q)
                incoming = {p} | extra
                needed = max(0, len(Q) +
                             len(incoming - set(Q) - {q}) - 2)
                for victims in combinations(sorted(reply - incoming), needed):
                    x = [{} for _ in range(n)]
                    x[p], x[q] = P.copy(), Q.copy()
                    z = Actual(x, 2)
                    bp, bq = ready(P, target), ready(Q, target)
                    old_R = int(bp) + int(bq)
                    old_N = sum(target in row for row in x)
                    z.step(p, q, extra, reply, vq=victims)
                    ap, aq = ready(z.x[p], target), ready(z.x[q], target)
                    new_R = int(ap) + int(aq)
                    assert sum(target in row for row in z.x) >= old_N
                    assert new_R >= old_R - 1, (P, Q, victims, z.x)
                    if new_R < old_R:
                        deaths += 1
                        assert bp or (bq and p in Q and p != target), (
                            P, Q, victims, z.x)
                    if target in P:
                        # The active endpoint is not the target's owner.
                        # Sending the target extra always creates a ready
                        # responder, even if its old duplicate age is zero.
                        assert aq
                        creations += 1
                    if bq and not bp and target not in incoming and p not in Q:
                        # A nonexceptional passive readiness loss must be
                        # compensated by a ready reply location.
                        assert ap
                        transports += 1
                    cases += 1
    print("PASS endpoint cases", cases, "ready deaths", deaths,
          "ready creations", creations, "generic reply transports", transports)


if __name__ == "__main__":
    main()

