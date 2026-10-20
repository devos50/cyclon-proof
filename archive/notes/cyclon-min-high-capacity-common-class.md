# Protected+MIN CYCLON: ell=2 and c>=n-2

Assume c>=3, c<=n-1, weakly connected cache identity graph, and the adopted protected+MIN update. Together with the already proved general-capacity holder-zeroification, source-only reachability, universal-anchor reduction, and uniform finite-age reset, the following establishes a unique common communicating class and uniform geometric convergence for c in {n-2,n-1}. The separate capacity-two theorem covers c=2.

Fix a closed communicating class and an identity a. Let k be the maximum number of a^0 cache copies in the class and choose a maximizer. The positive-anchor zeroification lemma implies that this state has no positive a copies and exactly k total a-holders. Moreover, no reachable state can have more than k total a-holders: normalize all its copies to zero without reducing their number and contradict maximality of k.

Write I for the a^0 holders and J=V\(I union {a}). Source-only target service implies that every vertex reachable from owner a lies in I union {a}; otherwise source-only activation reaches a missing-zero vertex and creates an additional zero. This reachable set is closed and has a universal zero anchor a, so normalize it to its anchored canonical state with C_a empty, freezing other vertices. All k zeros are preserved. We may therefore assume C_a is empty.

## Outward closure of I

Suppose an I-holder p caches a target in J. Activate only p, always sending a as the extra descriptor. While its oldest partner lies in I, require the reply to contain a^0 and p if p is known. The active a copy resets to zero; at most one usable nonanchor reply is received, so the cache never grows, and its original J target is unsent and cannot be a victim. A previously visited responder knows both a and p and returns {a,p}, shrinking the cache. Since the retained nonanchor target has nonnegative age, a^0 is never uniquely oldest; choose a nonanchor in a tie. Thus a J vertex q is contacted within n+c events, without losing any zero beforehand.

At this first J contact, p sends fresh p^0 and a. The responder q newly accepts a, since it has no a copy. If p is underfull, compulsory removal of partner q creates at least two vacancies; the at-most-two reply cannot force any victim, and p retains a. If p is full, |C_p union {p}|=c+1>=n-1. Thus there is at most one possible valid incoming identity outside C_p union {p}. At most one novel usable reply arrives, and the compulsory partner vacancy again suffices. In either case p retains a while q gains it, giving k+1 total a-holders, a contradiction. Therefore every I cache lies in I union {a}.

## An incoming contact adds a zero

If J is nonempty, weak connectivity supplies an edge between J and I union {a}. The owner is empty and J contains no a descriptor; I has no outgoing edge to J. Hence some J cache contains an I identity. Freeze I union {a} and use the holder first-contact lemma on J. Its first terminal exchange is P in J -> Q in I (it cannot contact owner a, since no a identity can be generated within J while owner a is frozen).

Pause immediately before that terminal exchange. Normalize Q's residual I component, after removing its universal a^0 anchor, to a rooted star with Q as its residual root. This is exactly the already proved ell=1 kernel of capacity c-1; if the component has fewer than c peers, use its effective capacity. All residual component IDs remain fixed, its anchor zeros are preserved, and J caches and ages do not change because I is outward closed. Thus the pending oldest partner Q remains legal and C_Q={a^0}.

Execute P->Q. Q receives at most two valid incoming IDs. Since c>=3, its one resident anchor and those two incoming IDs fit without evicting the anchor. P receives a^0 as its sole reply; the compulsory partner vacancy suffices, so P learns and retains a^0. None of the previous k zero holders is lost. This yields k+1 zeros, a contradiction. Hence J is empty and the class reaches a universal a^0 anchor.

The conditional universal-anchor theorem then reaches the same labelled canonical atom H(V,c), rooted at a, from every closed class. Consequently there is exactly one closed communicating class, and its canonical atom has an empty-root self-loop. The uniform finite-age reset hits a finite set from every state with a common probability; finitely many controlled paths from that set to H, padded by its self-loop, give a global Doeblin minorization. Therefore the full age-bearing chain converges uniformly geometrically to a unique stationary law. Label equivariance gives the stated conditional uniformity of peer identities whenever the sampling event is defined.

Independent audit: mandatory_path reports PASS, including the oldest-valid p-only prelude and the anchored residual normalization before the incoming terminal exchange.
