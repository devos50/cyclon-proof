# Sharp contact time from an empty universal zero anchor

## Exact scope

The unchanged adopted iid mandatory-removal/protected-MIN kernel has **c=L=2**, n>=3. A specified owner q initially has an empty cache, and every other peer stores q at age zero. Its other entry, if present, has arbitrary finite nonnegative integer age. Let tau be the first contact with q. We prove a worst-case expected contact time of order sqrt(n) **within this special family of starts**. This is not a mixing theorem, not an arbitrary-start contact theorem, and not an extension to c>=3.

The existing arbitrary-start c=2 cut-contact estimate has broader scope. The point here is a sharper, tight-order special-state mechanism that uses ordinary iid activations, not a prescribed schedule.

## Exact stopped residual dynamics

Before tau, q remains empty and its own initiations do nothing. Remove its zero descriptor from all outside rows. Each residual row then has at most one entry. In a surviving outside exchange p→r, the anchor is automatically present in both full packets. The exact residual update is the capacity-one update: the responder r becomes {p^0}; the initiator p takes r's previous residual entry, except that an absent or self entry leaves p empty. Numerical ages of replies are unchanged. This is an equality of stopped transition kernels, not an assertion that the survivor law equals the unrestricted residual law.

Call an outside row **ready** when its residual row is empty or its single age is zero. Equivalently, its original cache is entirely zero-aged and can select q as an oldest tie. Let R be the number of ready outside rows, between0 and n-1.

## Monotone readiness before contact

A nonready initiator has one positive residual descriptor, which is uniquely older than q, so it makes a surviving residual contact. If its responder was ready, both updated rows are ready; if the responder was nonready, the responder becomes ready and the initiator is nonready or becomes empty. Thus R increases by at least one.

A ready initiator contacts q with probability1 when its residual is empty and with probability1/2 when its residual entry is zero. If it instead makes an internal exchange, its responder becomes ready, and any loss of readiness at the initiator is offset by that gain. Thus R cannot decrease before tau.

Only two rows change per event, so R can increase by at most two. Consequently, at a surviving state with R=r:

- the probability of contact next event is at least r/(2n) and at most r/n;
- with probability (n-1-r)/n a nonready peer initiates and R increases by at least one;
- q's initiation is a no-op.

No independence between growth and future contact is assumed.

## Upper bound

For any integer1<=k<=n-1, reaching R>=k or contact has expected duration at most

n * sum_{r=0}^{k-1} 1/(n-1-r).

Indeed, at levelr<k the probability of a nonready initiation is (n-1-r)/n; earlier contact or a skipped level only shortens the wait. Once R>=k, it stays at leastk until contact, whose conditional hazard is at least k/(2n). Therefore, uniformly over all allowed special starts,

E[tau] <= B_n(k) := n * sum_{r=0}^{k-1} 1/(n-1-r) + 2n/k
                  <= nk/(n-k) + 2n/k.

Taking k=min(n-1,floor(sqrt(2n))) proves E[tau]=O(sqrt(n)); more precisely this choice gives at most (2sqrt(2)+o(1))*sqrt(n). Alternatively minimize the explicit finite list B_n(k).

Let B_n=min_{1<=k<=n-1} B_n(k), and m_n=ceil(2B_n). Markov's inequality gives P(tau>m_n)<=1/2. Every surviving state remains in the same special family, so the Markov property allows iteration:

P(tau>j*m_n) <=2^(-j), for integersj>=0.

Thus a sufficient confidence-1-epsilon contact horizon is m_n*ceil(log2(1/epsilon)). This tail bound is deliberately simple and is not claimed optimal in epsilon.

## Sharper explicit mean by a birthday-type comparison

The following stronger bound retains the same special scope. Put m=n-1. Consider a scalar chain on readiness counts0,...,m with an absorbing killed state. At countr it increases to r+1 with probability(m-r)/n, is killed with probabilityr/(2n), and otherwise stays. Its transition law is stochastically increasing when killing is ordered above all counts: if r<s, any nonabsorbing output fromr is at mosts, while its killing probability is no larger. The actual next-step readiness law, conditional on its full past and survival, stochastically dominates this chain at the same count. Nonready initiations and killing are disjoint, giving both required upper-tail inequalities. Thus the actual contact time is stochastically dominated by the comparison absorption time started at0, even if R initially exceeds0.

Poissonize global events independently at rate1. The comparison is realized by m independent rate1/n vertex clocks plus one inert owner clock. Each vertex becomes ready at its first tick; subsequent ticks kill independently with probability1/2. A given vertex has not killed by continuous timeu with probability

g(u/n)=2exp(-u/(2n))-exp(-u/n).

The comparison survival probability is g(u/n)^m. Since the rate1 inter-event intervals are independent of the discrete event marks, expected continuous absorption time equals expected number of global events. Therefore

E[tau] <= U_n := 2n integral_0^1 y^(n-2)(2-y)^(n-1)dy
              = n*B(1/2,n-1)+n/(n-1)
              <= n*sqrt(pi/(n-2))+n/(n-1),

where B is the beta integral. Substitutionv=1-y gives the displayed beta identity. The Gaussian bound(1-v²)^(n-2)<=exp(-(n-2)v²) proves the elementary inequality. Equivalently, the exact rational mean follows fromF(m)=2n/m and F(r)=[n+(m-r)F(r+1)]/[m-r/2].

The exact integral has asymptotic U_n=(sqrt(pi)+o(1))*sqrt(n): underu=z*sqrt(n), log g(u/n)=-z²/(4n)+O(n^(-3/2)) on boundedz, and a Gaussian/exponential bound from-log g(x)>=constant*min(x²,x) justifies integration. Thus the leading upper constant improves from the threshold bound's2sqrt(2) tosqrt(pi). The positive-cycle argument below shows this constant is asymptotically sharp.

The geometric block tail above also holds with block length ceil(2U_n), which is no worse than using the simpler threshold upper bound. No stationary-law assumption enters this comparison.

## Matching-order lower bound

Take q empty and put the other n-1 vertices in a directed residual cycle, every residual age equal to1; also give each row q^0. This is an allowed connected initial state, including the reciprocal residual cycle when n=3. Initially R=0.

On survival afters events, R<=2s. A nonready initiator cannot contact q, so the next-event contact probability is at mostR/n. Hence, for every integer t>=0,

P(tau<=t) <= sum_{s=0}^{t-1} 2s/n = t(t-1)/n.

Put h=floor(sqrt(n)). Summing survival probabilities gives

E[tau] >= h+1 - h(h+1)(h-1)/(3n)
        = (2/3+o(1))*sqrt(n).

Together with the upper bound this proves **Theta(sqrt(n)) worst-case expected owner-contact time in the specified anchored family**. It says nothing by itself about the full-state mixing time or local-sample bias.

## Sharp leading constant

For the positive-age directed residual m-cycle, a surviving internal event is a capacity-one rotation. Its unique directed cycle decreases in length by at most one per event; an empty residual appears only when a two-cycle is canceled. Consequently no residual is empty during the first h=m-2=n-3 global events. In that window ready initiators kill with probability exactly1/2, nonready initiators increase R exactly by one, and surviving ready initiations preserve R. The killed count process therefore has exactly the comparison law through h events.

Let T be the comparison killing time, whose mean is U_n. Its monotonicity bounds the expected remaining time from any count by U_n. For n>=4,

E[(T-h)_+] <= P(T>h)*U_n <= U_n²/h,

and equality of truncated laws yields

U_n-U_n²/(n-3) <= E[tau] <= U_n.

Since U_n=sqrt(pi*n)+O(1) by the beta/Gamma identity and Stirling's formula, the subtracted term is O(1). Thus this specific family and the worst-case anchored family both have expected first contact sqrt(pi*n)+O(1). This is an owner-contact theorem only, not a mixing result.

## Why the direct induction fails at c=3

After removing a universal zero anchor z, residual capacity is two. Let a ready residual responder q be empty and let a nonready residual initiator have P={q^2,u^1}. Its full-shuffle contact p→q leaves residual p={u^2} and q={p^0,u^2}; both are nonready. In the original c=L=3 system add z^0 to every outside row and leave z empty. Thus the simple ready-row count can decrease at the next capacity. A higher-capacity argument needs more information, such as occupancy and numerical-age levels.

## Verification and review

The proof has independent internal audits of the stopped kernel, monotone readiness, competing hazards, threshold bound, and matching lower bound. It is not formally verified or externally reviewed. `verification/check_anchored_two_entry_contact.py` exhaustively checks n=3,4,5 residual configurations with ages0,1,2 using the original full packets and protected/MIN merges, and compares them to the residual update. Finite tests supplement the all-n argument, and do not establish it alone.
