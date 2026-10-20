import sys
from random import Random
from statistics import mean
sys.path.insert(0, '/Users/martijndevos/Documents/decentralized-learning-simulator/docs/peer-sampling-convergence/mandatory-removal')
from verify_thesis_anchor import Actual


def initial(n, kind, rng):
    if kind.startswith('hub'):
        x = [{} for _ in range(n)]
        for p in range(1, n):
            r = p + 1 if p + 1 < n else 1
            x[p] = {0: 0, r: 1000000 if kind == 'hub_old' else 0}
        return x
    x = [{} for _ in range(n)]
    order = list(range(n)); rng.shuffle(order)
    for j, p in enumerate(order[1:], 1):
        x[p][rng.choice(order[:j])] = rng.randrange(4)
    for p in range(n):
        if rng.randrange(4):
            q = rng.choice([q for q in range(n) if q != p and q not in x[p]])
            x[p][q] = rng.randrange(4)
    return x


def trial(n, kind, seed, rounds=1000):
    rng = Random(1000003 * n + 7919 * seed)
    z = Actual(initial(n, kind, rng), 2)
    indeg = [0] * n
    for row in z.x:
        for q in row: indeg[q] += 1
    maxima = []; fulls = []; empties = []; ages = []; hubs = []; persistence = []
    checkpoints = {}
    old_clear = None
    last_leader = None
    for t in range(1, rounds * n + 1):
        p = rng.randrange(n)
        P = z.x[p]
        if P:
            q = rng.choice([q for q in P if P[q] == max(P.values())])
            Q = z.x[q]
            extra, reply = set(P) - {q}, set(Q)
            outgoing = {p} | extra
            needed = max(0, len(Q) + len(outgoing - set(Q) - {q}) - 2)
            victims = rng.sample(sorted(set(Q) - outgoing), needed)
            for r in P: indeg[r] -= 1
            for r in Q: indeg[r] -= 1
            z.step(p, q, extra, reply, vq=victims)
            for r in z.x[p]: indeg[r] += 1
            for r in z.x[q]: indeg[r] += 1
        if t % n == 0:
            r = t // n
            if kind == 'hub_old' and old_clear is None:
                if max((age for row in z.x for age in row.values()), default=0) < 1000000:
                    old_clear = r
            if r in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000):
                checkpoints[r] = indeg[0]
            if r >= 100 and r % 10 == 0:
                maxima.append(max(indeg))
                fulls.append(sum(len(row) == 2 for row in z.x) / n)
                empties.append(sum(not row for row in z.x) / n)
                ages.append(max(age for row in z.x for age in row.values()))
                hubs.append(indeg[0] == max(indeg))
                leader = rng.choice([p for p in range(n) if indeg[p] == max(indeg)])
                if last_leader is not None: persistence.append(leader == last_leader)
                last_leader = leader
    return dict(max_indeg=mean(maxima), full=mean(fulls), empty=mean(empties),
                max_age=mean(ages), initial_hub_max=mean(hubs),
                leader_persist_10rounds=mean(persistence), old_clear_round=old_clear,
                initial_hub_indeg=checkpoints)


for n in (20, 50, 100):
    for kind in ('hub_zero', 'hub_old', 'random'):
        answers = [trial(n, kind, seed) for seed in range(3)]
        numeric = {k: round(mean(a[k] for a in answers), 4)
                   for k in ('max_indeg', 'full', 'empty', 'max_age', 'initial_hub_max', 'leader_persist_10rounds')}
        print('n', n, kind, numeric, 'old_clear_rounds', [a['old_clear_round'] for a in answers],
              'initial_hub_n_by_round', {r: round(mean(a['initial_hub_indeg'][r] for a in answers), 2)
                                         for r in answers[0]['initial_hub_indeg']}, flush=True)
