# First contact with a frozen set: protected + MIN, shuffle length two

Use the adopted kernel: mandatory removal of the selected partner, received-ID protection for every resident eligible for replacement, and MIN-age duplicate merging. Fix the full identity set V, |V|=n, capacity c>=2, and shuffle length ell=2. Let G be a nonempty frozen set and S=V\G, |S|=s>=1. Activate only peers in S, and stop immediately when an initiator selects a partner in G. Let tau_G denote this first contact. No frozen cache needs to be read before tau_G.

Assume some cache in S initially contains an identity r in G. The cache identity sets need not be connected. For every exchange before tau_G, both endpoints lie in S. Their augmented cache unions are lossless under received-ID protection. In particular an r-descriptor cannot disappear from all S caches: it is never the selected partner before tau_G, and every nonpartner eviction is transmitted to and retained at the other endpoint. The descriptor identity r therefore remains present until tau_G.

Write

    H = (sc+1)(sc^2+1)(sc 2^c+1),
    K = (sc+1)H,
    B = s(s+c),
    T = B(K+1)+H.

Let

    gamma_out = [sc 2^(4c)]^(-1)
    gamma_global = [nc 2^(4c)]^(-1).

For the chain whose initiator is uniform on S,

    Pr_x(tau_G <= T) >= gamma_out^T.

For a positive-probability witness path in the original chain whose initiator is uniform on V, all prescribed initiators can still lie in S and

    Pr_x(tau_G <= T) >= gamma_global^T.

The second inequality prescribes the S-only witness up to first contact; it does not assert that arbitrary original-chain trajectories preserve the frozen caches. Conditional on continuing to freeze G, iteration of the first bound gives a geometric tail at multiples of T.

## 1. Outside age reset or first contact

The general age-gap lexicographic construction applies to outside caches only, with s in place of n in the number of storage slots. Outside caches may contain all identities in V, and c may exceed s-1. None of the counting arguments uses c<=s-1.

Choose an empty initial age interval (a,a+H], with a=jH and 0<=j<=sc. Color descriptors of initial age<=a YOUNG and those of initial age>a+H OLD; selves born later are YOUNG. Until time H, YOUNG ages stay<=a+H and OLD ages stay>a+H. Mixed duplicate merging selects YOUNG. If the lex controller selects a partner in G, stop successfully. Otherwise both endpoints lie in S, and the same potential

    (sc-F, sum_i f_i^2, sum_i O_i 2^(c-f_i))

strictly decreases. Its finite range gives a controlled path of length at most H which either hits G or leaves every outside age<=K. Arbitrary S-only padding to H preserves the alternative. Every prescribed step has probability at least gamma_out under the normalized S scheduler, or gamma_global under the original scheduler. Thus reset-or-hit has the corresponding lower bound gamma^H.

## 2. Raising the minimum age of r

Before tau_G, let m be the minimum age of any stored r-descriptor in S. The identity r remains present. Its minimum age cannot decrease: its owner is frozen, so no new r-self is created, every transmitted r is inherited from an existing r-copy after a possible local increment, and MIN merging cannot create an age below the existing global minimum.

Pick a holder p of r_m. Keep p active until the number of copies at this fixed age m drops or G is contacted. While a non-r partner is selected, choose r as the one extra outgoing descriptor. Its transmitted age is m+1.

If the responder q does not contain r_m, then its reply cannot contain r_m. The active resident r_m increments to m+1 and cannot be restored to m; no other new copy of age m is created. Hence the number of r_m copies strictly falls. If q belongs to G, first contact has instead occurred and the construction stops.

If q contains r_m, choose its reply to contain r_m and one residual entry, or only r_m if its cache is a singleton. When q knows p, choose p as that residual entry. The outgoing r identity protects q's resident r_m, and MIN merging refreshes p's incremented r back to m. The set of minimum-age holders is unchanged by this exchange.

Remove the anchor r from these caches. The prescribed exchanges are exactly the singleton-shuffle p-only clearing construction on residual caches of capacity c-1: the outgoing residual buffer is the fresh self p, and the reply has at most one residual entry. A responder learns p at its first such contact and retains it under all later p-only contacts; at a repeat, choose p in the reply, so it is filtered as self at the initiator and the active residual cache shrinks. There are at most s-1 first contacts and at most c-1 active residual entries. Consequently within at most s+c-1 exchanges either a responder without r_m is selected, G is contacted, or p's residual cache empties. In the last case p holds only r_m, and its next activation contacts r in G. The age-based partner rule can only make that external contact occur earlier: if r_m is older than every residual entry, it is already selected.

Thus within s+c prescribed exchanges either G is contacted or the count of copies at the current age m strictly falls. There are at most s such copies, and no copy of age m can be born before first contact. Within B=s(s+c) exchanges, either G is contacted or the global minimum r-age increases by at least one. Paths shorter than B can be padded arbitrarily with S-only activations: before first contact the minimum cannot fall, and an earlier G contact is already success.

## 3. Combining the controls

Repeat the minimum-raising construction K+1 times. If G has not been contacted, the global minimum r-age now exceeds K, because ages are nonnegative integers. This takes at most B(K+1) prescribed steps.

Apply the H-step outside reset-or-hit construction. A reset to outside maximum age<=K is impossible: r remains present, and its minimum age cannot fall. Therefore this prescribed path must contact G. The total horizon is T=B(K+1)+H. Each prescribed step has probability at least gamma, so the positive-probability path lower bound is gamma^T. Earlier successful paths need no restriction after their first contact.

This result proves eventual first contact with a frozen set and a uniform, very conservative tail bound. It does not by itself prove that a zero-age anchor survives the responding cache update, that every peer becomes an anchor holder, or that the full chain has a unique stationary class.

## 4. Full-chain cross-cut tail

Let tau_cross be the first exchange with one endpoint in G and the other in S, in either direction, under the original uniform n-peer scheduler. Suppose initially some S cache contains an identity r in G. Until tau_cross, exchanges internal to G never read or alter an S cache, while exchanges internal to S preserve at least one S-stored r. Thus the hypotheses needed for the prescribed S-only first-contact witness remain true at every block start before tau_cross. With p=gamma_global^T, the Markov property gives

    Pr_x(tau_cross > kT) <= (1-p)^k,   k>=0.

The caches and ages in G may evolve arbitrarily between attempted blocks. The prescribed successful event simply selects S initiators throughout its witness, and its probability lower bound is uniform over those G caches. This full-chain conclusion concerns an exchange crossing the cut in either direction; it does not require G to remain frozen on unsuccessful blocks.
