#!/usr/bin/env python3
"""Exact full-shuffle three-exchange holder gain; see research note."""
from itertools import combinations, product
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree


def check(x, c, a=0, p=1, r=2):
    before = [dict(row) for row in x]
    assert not x[a] and a in x[p] and r in x[p] and a not in x[r]
    assert x[p][a] >= max(x[p].values())
    assert x[p][r] == max(age for v, age in x[p].items() if v != a)
    holders = {v for v, row in enumerate(x) if a in row}
    z = ActualThree(x, c, ell=c)
    for u, v in ((p, a), (a, r), (p, r)):
        z.step(u, v, set(z.x[u]) - {v}, set(z.x[v]))
    assert {v for v, row in enumerate(z.x) if a in row} == holders | {r}
    assert z.x[p][a] == z.x[r][a] == 0
    assert all(z.x[v] == before[v] for v in range(len(x)) if v not in (a, p, r))


def main():
    count = 0
    # Exhaust all r identity sets at c=3, both full and underfull p rows,
    # and ordered initial ages including a large finite value.
    for n in range(4, 8):
        for full in (False, True):
            for A, R, S in product((0, 1, 2, 10**6), repeat=3):
                if not A >= R >= S:
                    continue
                for k in range(4):
                    for ids in combinations([v for v in range(n) if v not in (0, 2)], k):
                        x = [{} for _ in range(n)]
                        x[1] = {0: A, 2: R, **({3: S} if full else {})}
                        x[2] = {v: 10**6 if v % 2 else 0 for v in ids}
                        for v in range(3, n):
                            x[v] = {0: v % 2}  # other holders need not be zero
                        check(x, 3)
                        count += 1
    print(f'PASS {count} exhaustive identity/ordered-age c=3 cases')
    general = 0
    for n in range(4, 15):
        for c in range(2, n):
            for size in range(2, c + 1):
                for level in (0, 1, 10**6):
                    for rsize in range(c + 1):
                        x = [{0: v % 3} if v else {} for v in range(n)]
                        x[1] = {0: level + 3, 2: level + 2}
                        x[1].update({v: level for v in range(3, size + 1)})
                        ids = [v for v in range(n) if v not in (0, 2)][:rsize]
                        x[2] = {v: level + v for v in ids}
                        check(x, c)
                        general += 1
    print(f'PASS {general} full-shuffle cases across n=4..14 and c=2..n-1')

    restored = 0
    # Remaining c=3 ordering: holder s=3 strictly outranks nonholder r=2.
    # With these labels default victim selection sacrifices p=1, not r=2,
    # whenever the owner needs one victim; assert r survives explicitly.
    for n in range(4, 9):
        for A, S, R in product((0, 1, 3, 10**6), repeat=3):
            if not A >= S > R:
                continue
            for k in range(3):
                for ids in combinations([v for v in range(n) if v not in (0, 3)], k):
                    x = [{} for _ in range(n)]
                    x[1] = {0: A, 2: R, 3: S}
                    x[3] = {0: 13, **{v: 2 * v for v in ids}}
                    for v in range(4, n):
                        x[v] = {0: v % 3}
                    before = [dict(row) for row in x]
                    holders = {v for v, row in enumerate(x) if 0 in row}
                    z = ActualThree(x, 3, ell=3)
                    for u, v in ((1, 0), (0, 3), (1, 3)):
                        z.step(u, v, set(z.x[u]) - {v}, set(z.x[v]))
                    assert {v for v, row in enumerate(z.x) if 0 in row} == holders
                    assert z.x[1][0] == z.x[3][0] == 0
                    assert 2 in z.x[0] and 0 not in z.x[2]
                    assert all(z.x[v] == before[v] for v in range(n)
                               if v not in (0, 1, 3))
                    restored += 1
    print(f'PASS {restored} holder-residual restoration prefixes; '
          'all holders restored and owner retains nonholder target')


if __name__ == '__main__':
    main()
