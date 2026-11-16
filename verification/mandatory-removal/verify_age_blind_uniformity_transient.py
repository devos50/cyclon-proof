#!/usr/bin/env python3
"""Exact transient query-bias example; not a convergence counterexample."""
from fractions import Fraction
from itertools import combinations
from verify_thesis_cooperative_owner import ActualThree


def main():
    outcomes = 0
    for n in range(3, 9):
        c = n - 1
        V = set(range(n))
        rows = [{w: int(w == (v + 1) % n) for w in V - {v}}
                for v in range(n)]
        for length in range(1, n):
            law = {w: Fraction(0) for w in V - {0}}
            for p in range(n):
                q = (p + 1) % n
                extras = list(combinations(sorted(V - {p, q}), length - 1))
                replies = list(combinations(sorted(V - {q}), length))
                weight = Fraction(1, n * len(extras) * len(replies))
                for sent in extras:
                    for reply in replies:
                        z = ActualThree(rows, c, length)
                        z.step(p, q, sent, reply)
                        assert set(z.x[p]) == V - {p, q}
                        assert set(z.x[q]) == V - {q}
                        assert all(set(z.x[v]) == V - {v}
                                   for v in V - {p, q})
                        for w in z.x[0]:
                            law[w] += weight / len(z.x[0])
                        outcomes += 1
            assert law[1] == Fraction(1, n)
            assert all(law[w] == Fraction(n - 1, n * (n - 2))
                       for w in V - {0, 1})
            tv = sum(abs(x - Fraction(1, n - 1)) for x in law.values()) / 2
            assert tv == Fraction(1, n * (n - 1))
            # Uniform ordering lifts subset TV unchanged, since the same
            # uniform b! ordering kernel is used in both sample laws.
            for b in range(1, n - 1):
                full = list(combinations(sorted(V - {0}), b))
                reduced = list(combinations(sorted(V - {0, 1}), b))
                u = Fraction(1, len(full))
                tv_b = sum(abs((1 - Fraction(1, n)) * u
                               + (Fraction(1, n * len(reduced))
                                  if 1 not in subset else 0) - u)
                           for subset in full) / 2
                assert tv_b == Fraction(b, n * (n - 1))
    print(f'PASS {outcomes} exact packet outcomes, n=3..8, all lengths.')
    print('Uniform-query preservation fails: TV=b/(n(n-1)) for 1<=b<=n-2.')
    print('Scope: transient age-blind potential obstruction, not nonconvergence.')


if __name__ == '__main__':
    main()
