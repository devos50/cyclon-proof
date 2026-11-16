#!/usr/bin/env python3
"""Exact finite corroboration of the canonical clipped-capacity growth witness.

No class-invariance or arbitrary-length convergence claim is made.
Run with assertions enabled from the repository root.
"""
from verify_thesis_cooperative_owner import ActualThree


def check(n, m, c, ell):
    caches = [{j: 0 for j in range(max(i + 1, n - m), n)}
              for i in range(n)]
    q, p, r = n - m, 0, 1
    assert 0 <= p < r < q < n
    assert len(caches[q]) == m - 1
    model = ActualThree(caches, c, ell)
    for step, initiator in enumerate((p, r), 1):
        assert model.x[initiator][q] == max(model.x[initiator].values()) == 0
        extras = set(sorted(set(model.x[initiator]) - {q})[
            :min(ell - 1, len(model.x[initiator]) - 1)])
        reply = set(sorted(model.x[q])[:min(ell, len(model.x[q]))])
        model.step(initiator, q, extras, reply)
        assert len(model.x[q]) == m - 1 + step
        assert all(age == 0 for age in model.x[q].values())
    assert len(model.x[q]) == m + 1 <= c


def main():
    cases = 0
    for n in range(3, 14):
        for m in range(1, n - 1):
            for c in range(m + 1, n):
                for ell in range(1, c + 1):
                    check(n, m, c, ell)
                    cases += 1
    assert cases == 2002
    print(f"PASS: {cases} exact canonical two-event growth cases")


if __name__ == "__main__":
    main()
