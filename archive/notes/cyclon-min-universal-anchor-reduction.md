# Protected + MIN: a universal zero-age anchor implies access to the common atom

Exact model: mandatory oldest removal; all valid received identities retained;
duplicates merged using minimum age; ell=2, c>=2. Fix a node a. Assume every
p != a stores a descriptor a of age zero. C_a and all residual ages are arbitrary.
Then the canonical zero-age top-c sink fan H with empty root a is accessible by
a finite positive-probability path. Neither residual connectivity nor empty C_a
is assumed.

## 1. Exact controlled reduction to ell=1

Freeze a. On W=V\{a}, call C_p\{a} the residual cache (capacity c-1). When its
residual cache is nonempty, activate p and choose an oldest residual partner q.
This is legal in the actual cache: a has age0 before increment, so every oldest
residual age after increment is at least a's age1. Choose extra a, yielding
outgoing {p^0,a^1}. Prescribe the reply {a^0,t}, where t is the chosen residual
reply from q; if q has no residual entries, the reply is just {a^0}.

At q, incoming a^1 merges with resident a^0 and stays0. At p, reply a^0 refreshes
the incremented anchor to0. The remaining identity/age/victim updates are exactly
the protected+MIN mandatory ell=1 kernel with capacity c-1. In particular, a full
responder with a new p has exactly one required residual victim t; active p's
single residual reply fits its mandatory vacancy. Stop an active residual
clearing block when it reaches the singleton actual cache {a^0}, before activating
it toward a. Thus every residual weak component can be transformed using the
proved ell=1 theorem, with a globally prescribed root within that component.
The owner's C_a is unchanged and every anchor age remains0.

## 2. Empty the owner's cache

If C_a is nonempty, choose an actual oldest q in C_a (before its next activation).
Use the reduction to canonicalize q's residual component with q as its residual
root. Then C_q={a^0}; C_a and all its ages are unchanged because a is frozen.
Activate a toward q. Its reply is only a, discarded as self at a. Consequently
C_a loses q and receives nothing. The responder q retains a^0 and receives at
most one residual extra, which fits because c>=2. All other W anchor copies
remain0. Residual ages may now be positive, but the reduction handles arbitrary
residual ages on the next iteration.

Repeat at most c times to make C_a empty.

## 3. Merge residual components using a four-event zero-age gadget

With a frozen and empty, use the reduction to canonicalize each residual weak
component. Let u,v be roots of two different components, so
C_u=C_v={a^0}, C_a=empty. All residual component ages are zero. Perform:

  u -> a ; v -> a ; a -> v ; a -> u.

The complete state table on (a,u,v), omitting unaffected nodes, is:

  initially:     (empty,       {a0}, {a0})
  after u->a:    ({u0},        empty,{a0})
  after v->a:    ({u0,v0},     empty,{u0})
  after a->v:    ({u0},        empty,{u0,a0})
  after a->u:    (empty,       {a0}, {u0,a0}).

At the third event choose v in the zero-age oldest tie. The sent extra u has
age1, but MIN with the received/resident u^0 resets it to0 at both endpoints.
The last event is forced by a's singleton cache. All caches involved have size
at most2, so the same table is legal at every c>=2. Other caches are untouched.

The residual edge v->u joins the components, while all W anchor copies and the
empty owner are restored, with zero ages. Repeat for every other residual root,
using u as common root. This costs four events per component eliminated.

## 4. Reach H

The residual graph on W is now weakly connected. Apply the ell=1 reduction once
more to reach its canonical top-(c-1) sink fan. Together with the universal a^0
and empty C_a, this is exactly the top-c sink fan H on V ordered with a last.
All ages are zero. Every prescribed action has positive probability.

## Scope and remaining gap

This is a conditional common-atom accessibility theorem. It does NOT prove that
a universal zero-age anchor can be reached from every weakly connected state.
That is the remaining structural step for ell=2.

The reduction itself generalizes to ell>=2: reserve a in outgoing extras and
replies, and the residual kernel has shuffle length ell-1 and capacity c-1.
The four-event merging gadget also remains legal for larger shuffle lengths,
because all involved caches are underfull and of size at most2. A general-ell
common-atom induction would still require universal-anchor accessibility plus
the preceding residual-shuffle case.
