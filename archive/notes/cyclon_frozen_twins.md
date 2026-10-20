# A frozen connected state for the literal replacement version of enhanced CYCLON

This construction assumes the original seven-step semantics in which the initiating partner is among the replacement candidates, but remains in the cache if no usable new descriptor arrives. Received self and duplicate identities are discarded without refreshing ages. It does not apply if the partner is unconditionally removed before the exchange, or if duplicate descriptors refresh existing ages.

## Four-peer example

Take `n=4`, cache capacity `c=2`, and either shuffle length `ell=1` or `ell=2`:

- `C1={2,3}`, with descriptor `2` strictly older than `3`;
- `C2={1,3}`, with descriptor `1` strictly older than `3`;
- `C3={4,1}`, with descriptor `4` strictly older than `1`;
- `C4={3,1}`, with descriptor `3` strictly older than `1`.

The directed overlay is strongly connected. Every initiation contacts the paired peer (`1<->2` or `3<->4`). For a pair `p,q`, the caches have the form

`Cp={q} union S`, `Cq={p} union S`.

The initiating message replaces `q` by `p` and otherwise contains only entries from `S`, so every received identity is already in `Cq`. The response is a subset of `Cq`, consisting only of `p` and identities in `S`; at `p`, these are respectively self or already present. Thus neither peer receives a usable new identity, and neither cache changes.

The initiator increases every local age by one, preserving its strict internal age ordering. The responder does not increase ages or refresh discarded duplicates. Hence each designated partner remains uniquely oldest indefinitely. The identity state remains fixed under every schedule and every random subset choice.

Uniformly sampling one of the two cache entries therefore stays at TV distance `1/3` from uniform over the other three peers. The full cache remains a point mass at TV distance `2/3` from the uniform two-subset law.

## General family

Let `n=2m>=4` be even and `2<=c<=n-2`. Partition peers into pairs `(p_k,q_k)`, `k=1,...,m`. For each pair choose a set `S_k` of `c-1` peers outside that pair, containing `p_{k+1}` with indices interpreted cyclically. Such a choice exists because `c-1<=n-3` and the external set has `n-2` peers. Define

`C_{p_k}={q_k} union S_k`,

`C_{q_k}={p_k} union S_k`.

Set the paired descriptor's initial age to one and all other descriptor ages to zero. Reciprocal edges connect each pair, and edges to `p_{k+1}` connect all pairs in a directed ring, so the graph is strongly connected.

For every allowed shuffle length `1<=ell<=c`, the same argument shows that all messages carry only known/self identities and no cache identities ever change. Descriptor ages may grow without bound, but the oldest partner at every node remains its assigned pair.

For any fixed node `i`, its uniformly sampled cache peer has permanent total variation distance

`1-c/(n-1)`

from uniform over `U\{i}`. Its full cache has permanent distance

`1-1/binom(n-1,c)`

from the uniform `c`-subset distribution. Thus no asymptotic convergence theorem from all full strongly connected aged initial states is possible for this literal protocol version, including realistic cache and shuffle lengths.

## Why this does not settle every implementation

Unconditionally deleting the oldest partner before receiving a reply destroys the premise: the paired edge is then absent, and the initiating cache can shrink. Refreshing the age of a received duplicate initiator can also break the strict oldest pairing. Both variants require different transition rules and separate analysis. The original prose's statement that the initiator always removes the partner should therefore not be conflated with its stated replacement steps.
