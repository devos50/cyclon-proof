from itertools import combinations
from fractions import Fraction


def successors(state, p):
    n = len(state)
    if not state[p]:
        return [(state, Fraction(1))]
    P0 = state[p]
    oldest = [q for q in P0 if P0[q][0] == max(t[0] for t in P0.values())]
    answer = []
    for q in oldest:
        P = {r: (t + 1, old) for r, (t, old) in P0.items()}
        Q = state[q].copy()
        extra = set(P) - {q}
        out = {p: (0, False), **{r: P[r] for r in extra}}
        incoming = Q.copy()
        del P[q]
        dp = max(0, len(P) + len(set(incoming) - set(P) - {p}) - 2)
        dq = max(0, len(Q) + len(set(out) - set(Q) - {q}) - 2)
        pv = list(combinations(extra - set(incoming), dp))
        qv = list(combinations(set(Q) - set(out), dq))
        for vp in pv:
            for vq in qv:
                A = {r: t for r, t in P.items() if r not in vp}
                B = {r: t for r, t in Q.items() if r not in vq}
                for dest, packet, own in ((A, incoming, p), (B, out, q)):
                    for r, value in packet.items():
                        if r == own:
                            continue
                        if r in dest:
                            t, old = dest[r]
                            dest[r] = (min(t, value[0]), old and value[1])
                        else:
                            dest[r] = value
                new = [r.copy() for r in state]
                new[p], new[q] = A, B
                answer.append((new, Fraction(1, len(oldest) * len(pv) * len(qv))))
    assert sum(prob for _, prob in answer) == 1
    return answer


def prescribed(state, p, q):
    assert q in state[p]
    assert state[p][q][0] == max(t[0] for t in state[p].values())
    ss = successors(state, p)
    assert len(ss) == 1
    return ss[0][0]


def minimum_count(state, m):
    return sum(old and t == m for row in state for t, old in row.values())


def trial(n, m=2):
    q, r, s, h, x = range(5)
    ordinary = list(range(5, n))
    initial = [{} for _ in range(n)]
    initial[h] = {r: (m, True), s: (m, True)}
    initial[x] = {q: (10 * m, True), h: (m - 1, True)}
    for p in [r, s] + ordinary:
        initial[p] = {q: (0, True)}
    state = initial
    for p in [r, s] + ordinary:
        state = prescribed(state, p, q)
        state = prescribed(state, q, p)
    state = prescribed(state, x, q)
    state = prescribed(state, q, h)
    assert state[q] == {r: (m, True), s: (m, True)}
    assert state[h] == {q: (0, False), x: (1, False)}
    assert state[x] == {h: (m, True)}
    for p in [r, s] + ordinary:
        assert state[p] == {q: (0, False)}
    assert minimum_count(state, m) == 3
    assert min(t for row in state for t, old in row.values() if old) == m
    assert max(t for row in state for t, old in row.values() if not old) == 1
    deltas = []
    for p in range(n):
        expected = sum(prob * (minimum_count(new, m) - 3)
                       for new, prob in successors(state, p))
        deltas.append(expected)
    assert deltas == [Fraction(-2), Fraction(0), Fraction(0),
                      Fraction(-1), Fraction(-1)] + [Fraction(1)] * (n - 5)
    drift = sum(deltas, Fraction(0)) / n
    assert drift == Fraction(n - 9, n)
    return drift


for n in range(10, 41):
    for m in (2, 1000000):
        drift = trial(n, m)
    print('PASS n', n, 'expected_min_old_count_drift', drift)
