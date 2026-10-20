# Polynomial holder-only first contact for protected+MIN CYCLON, ell=2

This is a strengthening of the already proved reset-or-hit first-contact lemma. It changes neither the protocol nor its buffer sizes. Fix a nonempty frozen peer set G, put S=V\G and s=|S|>=1, and suppose that at least one cache in S contains the identity r in G. Only peers in S are activated before the first S-to-G contact. Capacity is c>=2; shuffle length is exactly two with the usual min(buffer length,available size) completion.

Set

    B=s(s+c),  J=(sc+1)(2s+c),  T=B(J+1)+J.

There is a controlled positive-probability path contacting G in at most T exchanges. Every preterminal initiator contains r, sends r as its extra descriptor, and the reply contains r whenever the responder has r. In particular, the number of r-holding peers does not decrease before a terminal contact with owner r, and no previously frozen r^0 copy is touched.

## 1. Raise the minimum r-age

Let m be the minimum r-age in S. This minimum cannot decrease during any S-internal exchange because r is never created as a fresh self descriptor and protected pair unions preserve the presence of r. Choose a peer p with r-age m, activate only p, and send r as the extra descriptor until either G is contacted or the number of r_m copies decreases. If a responder q has r_m, require its reply to contain r_m and p if p is known. The outgoing r has age m+1, so q keeps its protected r_m, while p is refreshed to r_m. Its remaining reply has at most one usable identity. Thus the active cache never grows; each responder's first visit installs and protects p, and each later visit returns {r,p} and shrinks the active cache by one. A decrease or a contact occurs within s+c exchanges. If q lacks r_m, no new r_m is born and p loses its r_m (even if q returns an older r); the count decreases.

At most s minimum-age copies need to be removed. Hence within B exchanges either G is contacted or the minimum r-age increases by at least one. Starting from any nonnegative ages, after at most B(J+1) exchanges either there is a contact or every r-age is greater than J.

## 2. Auxiliary OR colors, which are not protocol metadata

At this point color every existing descriptor OLD. Every fresh self descriptor subsequently generated is YOUNG. Copies carry their color. When MIN merges two duplicate descriptors, color the result YOUNG if **either** input is YOUNG, independently of which input provides the minimum age. This OR convention is sound: a merged descriptor's age is at most the age of its YOUNG input, so after t routing exchanges every YOUNG descriptor has age at most t. Old descriptors may have small ages; the OR convention deliberately avoids assuming otherwise.

Identity r can never be YOUNG, since owner r is frozen. Its minimum age remains greater than J. Consequently, through the first J routing exchanges, every oldest partner selected by an r-holder is OLD: the selected partner's age is at least that of its r descriptor, whereas every YOUNG age is at most J.

## 3. Routing and monotone YOUNG count

Keep an r-holding active peer p and always send {p^0,r}. If the responder q knows both p and r, return {p,r}. If it knows exactly one of them, return that identity and one other descriptor; if a responder victim is needed, use that other descriptor as the victim. If it knows neither, include all required victims in its reply and fill any remaining reply position arbitrarily. Only sent responder entries outside the incoming pair {p,r} are eligible victims. Choose these victims among OLD descriptors first, or among YOUNG descriptors whose IDs are absent from the initiator's pre-exchange cache and are different from p.

Such victims always exist. The active cache contains two OLD identities, r and its selected partner q, so it contains at most c-2 YOUNG identities. If q knows only one of p,r, at most one victim is needed, and a full responder has c-1 other entries; they cannot all be YOUNG IDs already at p. If q knows neither, r_q=(|C_q|+2-c)^+ victims are needed, while at least |C_q|-(c-2)>=r_q responder entries are OLD or have YOUNG IDs absent at p. Every chosen YOUNG victim is copied to p as a new protected descriptor and compensates its removal at q.

The initiator's only eligible sent extra is the OLD descriptor r. Its selected partner is OLD, and OR merging cannot destroy a YOUNG color. Therefore the total number F of YOUNG cache entries in S never decreases. If the initiator is forced to evict r, the responder cannot previously have known r (otherwise the reply protects r), nor p (otherwise the self-filtered reply leaves at most one usable incoming identity and the compulsory partner vacancy suffices). Thus the responder newly accepts fresh p^0, and F increases by at least one. There can be at most sc forced migrations. Follow the protected copy of r at the responder after every such migration.

Within a phase with fixed initiator p, every first-visited responder subsequently knows and protects both p,r. A repeat visit returns {p,r}, shrinking p's cache by one. There are at most s-1 first visits, each increasing the cache size by at most one, and at most c-1+(s-1) shrinking repeats before a terminal contact or migration. The safe bound 2s+c exchanges covers every phase including its terminal event. At most sc+1 phases therefore contact G in at most J exchanges.

## 4. Probability and endpoint holder preservation

Every prescribed event has probability at least gamma=(n c^5)^(-1) in the original n-peer uniform-initiator chain: one initiator, one oldest tie, one at-most-two reply choice, and at-most-two victim choices suffice for this conservative bound. Hence the probability of a contact by time T is at least gamma^T. For a scheduler normalized on S, replace n by s. The witness may stop early; gamma<=1 makes the common lower bound valid.

At every S-internal event the initiator holds r and sends it protected to the responder. If the responder already holds r, the required reply includes r and protects it at the initiator. If the responder lacks r, it acquires a new protected copy, compensating any initiator loss. Thus the total number of r-holders never decreases. At a terminal contact with a frozen r-holder the same argument holds; contacting owner r may remove one r copy because self filtering prevents the owner from returning r.

## 5. Positive-anchor zeroification corollary

Let a be an identity with at least one positive-age cache copy. Freeze its owner and all a^0 holders; use the holder-only path above with r=a. If it first reaches a frozen zero holder, that holder's a^0 is protected by incoming a, and the active positive holder receives a^0. Total a-holder count is not reduced and the number of zero copies increases.

If the first contact is with owner a, the active peer p loses its positive a copy, while owner a learns p^0. Activate only a, keep p as an extra until it is selected, and while a responder holds a require its reply to contain a and p if known. The returned a is self-filtered, so p remains in the owner's cache and that cache never grows; every repeated responder returns {a,p} and shrinks it. A nonholder must be contacted within n+c events, since p remains a nonholder throughout the callback. At that event the responder accepts fresh a^0, restoring the one lost holder. Existing zeros remain protected; earlier positive responders may also have become zeros. Thus at the block endpoint the total a-holder count is at least its starting value, and the zero-copy count has strictly increased.

Repeated zeroification terminates in at most n-1 blocks with every a-copy at age zero, without reducing the total number of a-holders. Therefore, in a closed communicating class, if k is the maximal number of a^0 holders, every state maximizing it has exactly k total a-holders and no positive copies. No state reachable from it can have more than k total a-holders, since zeroification of such a state would contradict maximality of k.

Verification helper: /private/tmp/verify_cyclon_min_first_contact_fast.py. It uses exact numeric ages and proof-only OR colors; the default run covers 9,100 n=3..15/c/s/seed/age-pattern cases, including high-r routing and low-age OLD descriptors. All checks passed (108 forced migrations, 2,296 completed minimum raises; maximum observed path length 41).
