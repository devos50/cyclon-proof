# Complete convergence theorem for dense three-entry shuffles

## Theorem

For every n>=4 and max(3,n-2)<=c<=n-1, the adopted mandatory-removal,
received-ID-protected, MIN-age CYCLON kernel with fixed shuffle length3
converges from every weakly connected state with arbitrary finite integer
ages to a unique full-state stationary law. The convergence is uniform and
geometric in total variation, with existential parameter-dependent constants.
Every observer has positive stationary availability for every b<=c, and its
ordered b-sample converges to uniform conditional on availability.

This includes every full-capacity instance c=n-1 and every near-full instance
c=n-2 for which length3 is allowed.

The proof uses the independently audited callback construction in
/private/tmp/cyclon-min-dense-ell3-owner-callback.md, the generic ell2 theorem,
the ell3 holder-only first-contact theorem, the universal-zero-anchor-to-H
reduction, and the all-length uniform finite-age reset theorem.

## 1. Strengthened nonholder callback

The dense callback says: if owner a caches p outside its zero set I, a finite
controlled path strictly raises Z_a, preserves every original zero at macro
endpoints, and never lowers N_a. The only temporary zero loss is one prepared
Q->p event followed immediately by a->Q restoring Q^0. Dense no-extra-eviction
retains Q's anchor identity even in that temporary event.

If p is initially an anchor-NONHOLDER, the callback can be strengthened to
achieve both N_a increase by at least1 and strict Z_a increase. If p acquires
a during preparation or the final owner contact, its old absence has already
been repaired; finish the current callback to obtain the promised zero gain.
Otherwise a callback can finish at another positive holder, increasing Z_a
but leaving p absent. Target p remains cached at the owner (dense no-extra-
eviction), and is still outside the new zero set. Apply the callback again.
Since each call strictly raises Z_a, at most n-1 calls can occur while p is
absent. If every other nonowner is already zero, a further callback must reach
p or create its anchor during preparation. Hence N_a increases and Z_a gains.
All old zeros remain secured at the macro endpoints. No numerical uniform
bound on these age-dependent paths is required here.

## 2. Positive-copy zeroification and the total-holder bound

Fix an identity a in a closed communicating class C. Freeze owner a and the
current zero holders. From any positive a copy, the holder-only first-contact
controller either meets a zero holder (refreshing the active copy to0 while
not lowering N_a) or meets the owner (losing one positive copy at P, while
owner a learns fresh P^0). In the latter case the strengthened nonholder
callback restores at least that lost identity and gives strict zero gain.
Thus a positive copy can always be zeroified with N_a nondecreasing and Z_a
strictly increasing, preserving all old zeros at macro endpoints.

Let k be the maximum Z_a attained in C. If a class state has any positive a
copy, repeat the preceding operation until all a copies are zero. Then its
endpoint satisfies N_a=Z_a<=k and N_a is at least the initial count. Therefore

    N_a(x)<=k  for every x in C.

At a maximizing state, N_a=Z_a=k and all a copies are0. A cached owner target
outside I would contradict maximality by the dense callback, so C_a subset I.

## 3. Outward closure and an empty owner

There is no cache edge from h in I to an anchor-nonholder x. Otherwise keep h
alone active and always reserve a and x as extras. Before a nonholder is
contacted, replies contain a and, when known, h,x. The active anchor is
refreshed0. First responders learn h,a,x; repeats return those three, whose
self-h and resident a,x give no new usable identity, strictly shrinking h.
First visits grow its cache by at most1; dense no-extra-eviction retains x.
The owner a need never be selected, because anchor a^0 is no older than the
retained x. Thus a nonholder response eventually occurs. Its fresh incoming
a is retained, and h keeps its own a identity, giving N_a>=k+1, contradiction.

Hence I is residual-outward-closed. Reserve a^0 and apply generic ell2
normalization inside its residual weak components. Normalize each inspected
owner-oldest Q with Q as component root; then C_Q={a^0} and a->Q deletes one
owner entry with its self-only reply. All owner extras belong to I. Repeating
empties the owner while preserving all zeros and residual closure.

## 4. Incoming first contact: capacities at least four

Suppose I is not all nonowners. With a empty and I outward-closed, weak
connectivity gives a J->I edge for J=V\(I union {a}). All J peers lack a.
Freeze I and owner and use ell3 first contact from J. Before the terminal
contact, J-only exchanges cannot generate a. Pause before P->Q in I, freeze
J, and normalize Q's I-component with Q as root, giving C_Q={a^0}. This does
not alter the inspected outside oldest choice. Resume the contact.

If c>=4, at most3 received identities fit beside Q's old anchor. Active P
receives a^0 and Q retains its old a^0, contradicting maximal k. The same
argument handles c=3,n=4: an a-nonholder caches at most n-2=2 identities and
therefore sends at most2, which fit beside the old anchor in capacity3.

## 5. The c=3,n=5 component minimum

This is the only dense case not handled by the preceding vacancy count.
Among class states with Z_a=k, all a copies0, empty owner, and I outward-
closed, minimize d, the number of residual weak components of I. Such states
exist by Steps2-3, and d takes finitely many integer values. Run the same
J-first-contact prefix and normalize terminal Q's component with root Q.
These operations preserve d and all the extremal properties.

A request with at most2 identities gives the previous zero gain. Otherwise
P had exactly the cache {Q,R,S}, with distinct R,S, and sends P^0,R^u,S^v.
The singleton Q replies a^0. Dense no-extra-eviction gives the exact endpoints

    C_P={a^0,R^u,S^v},       C_Q={P^0,R^u,S^v}.

Received-ID protection and capacity3 force Q's old a out. Thus zeros are
swapped: I'=(I\{Q}) union {P}, still N_a=Z_a=k, with the owner still empty.
If either extra R,S was in old J, new zero P has an outward edge to an anchor
nonholder, contradicting Step3 at this new class state. Hence R,S belong to
I\{Q}. If Q's normalized component was nonsingleton, another old zero holder
still caches root Q, now a nonholder, again violating outward closure.
Therefore Q's old component was a singleton. Removing that singleton and
adding P attached to R,S in other old components strictly lowers d. This
contradicts its minimum. Thus the c=3,n=5 state also cannot be nonuniversal.

## 6. One atom and uniform convergence

Every closed class therefore contains a state with universal a^0. The generic
ell2 theorem and universal-zero-anchor reduction at length3 give a finite
path to every labelled canonical H(V,c), so all closed classes share one
fixed canonical atom and are the same class.

The uniform finite-age reset theorem gives a finite family F_B with a uniform
positive hitting probability at a fixed time. Every member of F_B reaches a
closed class and hence the common H. Choose one finite atom path for each of
these finitely many states, maximize the lengths, minimize the positive path
probabilities, and pad at H by its empty-root no-op. Combining with the reset
yields fixed T and gamma>0 such that

    inf_x P^T(x,{H})>=gamma.

The common-atom contraction theorem gives unique stationarity and uniform
geometric total-variation convergence. Label equivariance makes the stationary
law permutation invariant. Relabelled H states give positive availability for
all b<=c; the symmetry argument gives conditional uniform ordered b-samples.
