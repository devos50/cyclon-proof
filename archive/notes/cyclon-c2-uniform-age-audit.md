# Independent audit: uniform finite-set accessibility for c=ell=2

Exact kernel as in main.tex Section7, including arbitrary eligible sent-entry victims with positive support. All membership sizes n>=3 are allowed. Arbitrary initial finite ages; no connectivity assumption needed for the age-reset statement.

## Responder normalization

If the initiator p holds two entries {u,r} and chooses partner u!=r, its full outgoing packet is{p^0,r^(a+1)}. Eligible choices can make the responder's post-cache exactly{p,r}, preserving pre-existing copies of either identity (and their ages) when they are duplicates. Proof: both absent =>insertboth, replacing all needed old slots; exactlyoneknown =>retainthatknownentryandreplaceanyotheroldentry; bothknown =>nochange.

If the initiator is forced to lose its nonpartner r, its reply contains two usable entries. Hence the responder initially contains neither p nor r. Normalization therefore gives the responder exactly{p^0,r^(a+1)}, where a+1>=1. Its next initiation selects r uniquely.

## Old-descriptor forcing in at most n events

Track an old descriptor of identity r at holder p. If singleton, select r immediately. Otherwise normalize every non-r responder as above. If r is retained at p, keep p as sole initiator. Previously visited responders remain frozen with cache{p,r}. Revisiting one yields reply{p,r}, both filtered at p (self p and duplicate r), leaving p with singleton r; the next event selects r. There are at most n-2 distinct non-r/non-p responders. Thus n-2 distinct visits, one repeat, and final selection cost at most n events.

If r is forced out earlier, follow its copied entry to the responder; its next initiation selects r uniquely by the preceding observation. This case also costs at most n events.

Existing immune peers contain a fresh r. Normalization preserves that duplicate. They cannot become a forced-transfer destination: their reply includes r, so it cannot contain two usable entries at a holder already storing old r. Thus no immune node is activated as a tracker holder.

After the final old-r selection at holder q, q contains no r. Home peer r can retain or insert q: if q new, insertion is mandatory; if q duplicate, at most one other usable incoming entry exists and the other victim can be selected. Thus r stores q.

## Callback forcing in at most n events

Activate only source r, protecting target q whenever possible. Stop immediately whenever a responder lacking identity r accepts the fresh self descriptor r^0; it becomes a new immune peer. If q is selected first, q has remained untouched and r-free, so it accepts fresh r and is the new immune.

If neither occurs yet, every responder already knows r. Normalize its cache to{r,q}, retaining its existing r (fresh if already immune). Its reply contains self r, so at most one entry is usable at source r; target q is automatically retained. Repeat visits return{r,q}, both filtered (self r, duplicate q), leaving q singleton. At most n-2 distinct other responders, one repeat, and one final q selection again cost n events.

Each old-selection/callback iteration therefore costs at most2n events and adds a distinct immune peer. At most n-1 iterations erase all old copies of one identity. Repeat all n identities; extinction is irreversible because newly generated self descriptors are fresh and copies retain their marks.

## Result

All initially present descriptors and their copied descendants can be erased in at most
 L=2n^2(n-1)
events, uniformly in the initial ages. Every remaining age is at most L. Therefore the finite set F={all cache states with ages<=L} is accessible from every initial state within L events with a uniform positive probability.

For the uniform choices specified in Section7, every designated event has probability at least1/(4n): initiator1/n, oldest tie at least1/2, responder victim choice at least1/2. Buffers are deterministic at c=ell=2; no optional protected initiator victim choice is needed (the one remaining resident either fits or is forced out). Hence P_x(tau_F<=L)>=(4n)^(-L).

One may pad arbitrarily to exactly L events: once all initial lineages have vanished, they cannot reappear, and every remaining descriptor was born at a nonnegative execution time, so its age at absolute time L is at most L. Consequently P^L(x,F)>=(4n)^(-L), even though F need not be closed at later times. Repeated blocks give a geometric tail for hitting F and finite expected return times to F. This does not by itself prove one communicating class or uniform local marginals.

## Weak connectivity for every ell=2 and arbitrary c

An initiator has at most one sent nonpartner extra r, and can replace at most that one resident. Every responder victim appears in its two-entry reply.

Case1: the responder's post-cache contains the initiator p. Then p and q remain adjacent. Any responder victim x is either newly accepted at p or was already present there. In the latter case x made one reply a duplicate, so at most one reply was usable, fitting p's mandatory-removal vacancy; p has no extra victim and retains x. Thus each lost q-x edge is represented by q-p-x. If p loses its extra r, both replies were usable, so neither reply was r. If q previously knew r, it cannot evict r because r was not sent; otherwise q accepts outgoing r. Thus each lost p-r edge is represented by p-q-r.

Case2: q no longer contains p. Then p was an old q resident returned in the reply and selected as a victim after incoming fresh p was filtered as a duplicate. The sole possible other incoming entry r must be new and inserted at q. At p, returned p is a self entry, so at most one reply is usable; the extra r is retained. Therefore p-r-q reconnects p and q. There is at most one responder victim (p) and no initiator extra victim. All other edges persist.

The singleton/empty cases are immediate. Thus every deleted old edge has endpoints connected afterward; weak components are preserved for ell=2, even when c>2.
