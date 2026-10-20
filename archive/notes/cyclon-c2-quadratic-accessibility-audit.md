# Independent audit: root's O(n^2) common-atom accessibility improvement

The new Q-only residual clearing replaces expensive full-component star
normalizations in intermediate saturation stages. Its invariants pass.

## Root-only residual clearing

Suppose all a descriptors are zero, Q is a zero holder, owner a is frozen,
and Q's residual cache has at most one entry. Activate Q only, choosing its
residual partner (legal oldest or tie against a^0), sending a as extra.
At a zero-holder partner, the full reply contains a^0 and at most one
residual entry. Thus Q's a-copy remains zero and its residual update is
exactly capacity-one singleton dynamics. Passive partners learn Q and
retain Q until this clearing block ends; a repeat therefore returns Q,
filtered as self, and clears Q's residual cache. Before a repeat there
can be at most n-1 distinct partners. So <=n exchanges suffice to clear
Q, or to encounter a nonholder if the clearing is stopped there.

## Owner emptying or a strict zero gain

Inspect the owner's actual oldest Q. If Q is a nonholder, a->Q gains
immediately. Otherwise Q is a zero holder. Freeze the owner and perform
the stopped root-only clearing above.

If Q becomes residual-empty, C_Q={a^0}. Resume a->Q; its reply filters as
self, so the owner loses Q and receives no usable identity. All zero
holders remain zero. At most two owner heads can be removed this way.

If the clearing instead encounters a nonholder x, execute Q->x, then
immediately a->Q. At the first event C_x is forced to {Q^0,a^1}; Q may
retain a positive copy or lose its anchor. The frozen owner's oldest
choice Q is unchanged, so the second event is legal and protected fresh
a^0 restores Q's zero regardless of its reply. Other old zero holders
were only passive, with protected anchors. Thus all old k zeros are now
restored, and x adds one positive a copy.

Next x->a is forced, since a^1 is older than Q^0. This removes x's positive
copy and the owner receives protected fresh x^0. Now ALL a copies are
zero again, their count is the old k, and the owner caches the nonholder
x. The cached-target owner-service lemma contacts some nonholder, at
latest x, within n+2 owner events, preserves the k zeros, and gives a new
fresh zero. No positive copies are generated during owner-only service.

Only one earlier owner head can have been removed before this terminal
boundary branch. A safe total is <=3n+6 exchanges for either empty owner
or a strict Z gain, independent of all numerical ages.

## Empty-owner incoming boundary saturation

If a zero holder already caches a nonholder, use the four-event infection
gadget. Otherwise the residual zero-holder graph is outclosed.

Run the original incoming-boundary case distinction, but normalize ONLY
the chosen Q root by Q-only residual clearing. Its component need not be
made a star. After clearing, the component is still weakly connected, Q
is its empty root, and each other vertex has residual outdegree <=1.
If the component is nontrivial, some other v has a residual edge to Q;
thus C_v={a^0,Q^B} for some B>=0. That is enough for the existing
four-event infection when Q loses its anchor. The old star proof used
B=0, but the infection lemma accepts arbitrary finite B.

The only nongain branch again has Q as an isolated component, so its
root clearing costs zero and the branch costs one P->Q exchange. At
most n-1 component reductions precede a gain. The final gain attempt
costs at most n+6. Hence a safe incoming saturation cost is <=2n+6.

Together with owner emptying, each all-zero strict-gain macro costs
<=5n+12. Positive-copy strict-gain macros cost <=n+4: at most two
pair-forcing exchanges give the owner a cached nonholder, followed by
the same <=n+2 cached-target owner service. Across the entire execution
there are at most n-1 strict gains of Z.

Universal-anchor saturation is therefore O(n^2), and the existing final
capacity-one star canonicalization is also O(n^2). A conservative explicit
common-atom horizon can be chosen proportional to n^2; the root is
selecting the final safe constant in main.tex.
