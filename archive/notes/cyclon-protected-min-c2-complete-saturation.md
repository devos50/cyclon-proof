# Protected + MIN CYCLON, c=ell=2: every closed class contains a universal anchor

Model: static weakly connected overlay on n>=3 labelled peers; capacity2;
shuffle length2; mandatory oldest-partner removal; every valid received
identity retained; duplicate ages merged by MIN; sent resident identities
appearing in the incoming packet protected from replacement. Every prescribed
oldest tie, initiator, and legal packet/victim choice has positive probability.
Ages are nonnegative integers. The proof also allows configured capacity2 when
a controlled induced subpopulation has fewer than3 peers.

We use the proved ell=1 arbitrary-capacity common-atom theorem and the proved
conditional universal-zero-anchor -> canonical-H theorem. We do not assume
any source-only random fairness or an unproved irreducibility assertion.

## 1. Source-only zero gain

Fix owner a. Let I={v!=a : C_v contains a^0}. Keep only a active. Every contacted
peer receives fresh a^0, protected at the responder; therefore I never loses a
member during source-only activation. If a contacts any peer outside I, its
size increases immediately.

If a currently caches a target z outside I, then a can force a zero gain in
at most K=n+c-1 events (here c=2). Until the first zero gain all encountered
responders belong to I. Always send target z as extra when another partner is
selected. Each responder returns a, plus z when it knows z (otherwise its only
other permissible entry). The received a is the source's self and is discarded,
so at most one usable new identity arrives and target z cannot be evicted.
Each responder learns z at first contact and retains it while passive; repeats
then reply {a,z}, add no new usable identity, and strictly shrink the source's
cache. The first-visit/shrink argument forces contact with z in at most K.

More generally, if a can reach any peer outside I along a directed cache path,
a source-only zero gain has a finite controlled witness. Choose a simple path
of minimum length d from a to outside I. Every internal path vertex lies in I.
Let z be its first head, retained as extra while any other partner is selected.
If the selected partner is z, reply its next path head (and a), shortening the
path by one, or obtain the zero gain if z itself is outside I. If the selected
partner is a later internal path vertex, its reply likewise sends its next
head to a, giving a strict shortcut. If it is off the path, the path is
untouched and z remains cached. Until a shortcut or zero gain occurs, repeats
of an off-path responder return {a,z} and shrink the source cache. Hence after
finitely many first visits/shrinks the path shortens. Iterate d times.

Consequently, in a closed communicating class, a state maximizing |I| has
R_a (the vertices directed-reachable from a) contained in I union {a}.

## 2. Positive-age copies cannot occur at a zero-count maximum

In a closed communicating class choose a state maximizing k=|I|. Suppose a
peer p stores a^A with A>0. If its selected oldest partner is a, then p->a
touches no prior zero holder and makes owner a know the nonzero peer p freshly.
Section1's cached-target zero-gain controller contradicts maximal k.

Otherwise c=2 forces C_p={a^A,u^B}, with u an oldest partner. Send {p^0,a^(A+1)}.
Received protection and capacity2 force C_u'={p^0,a^b}. If u previously stored
a^0, MIN gives b=0, its full reply returns a^0 to p, and p becomes a new zero
holder while u retains its zero: contradiction. Otherwise b>0, p cannot have
become a zero holder, and u was not a zero holder. Activate u, whose uniquely
oldest entry is a^b; it contacts owner a and sends {u^0,p^1}. No old zero holder
is touched and owner a now knows the nonzero peer u. The cached-target
controller again gives a zero gain, contradiction.

Thus every a descriptor in a maximum-k state has age0: the set I is exactly
all nonowner a holders. This conclusion applies to every state of that closed
class that attains k.

## 3. A maximum-k state with empty owner exists

At any maximum-k state, Section1 gives R=R_a subset I union {a}. By definition
all caches at vertices of R use only IDs in R. All nonowner vertices of R
contain a^0. Freeze every vertex outside R. If R={a}, the owner is already empty. If
R={a,b}, then C_b={a^0} and C_a={b}; the direct a->b exchange empties the
owner while preserving b's a^0. If |R|>=3, apply the conditional universal-zero-
anchor -> canonical-H construction to the induced population R, with a as
final root and capacity2. The path ends with C_a empty and every old R nonowner
still containing a^0. All outside vertices were untouched, so all old I
members remain zero and |I|=k. Ages at intermediate states need not stay zero;
only the endpoint property is needed. Closedness keeps the entire path in the
same class.

## 4. Four-event outward infection with empty owner

Assume C_a is empty, C_p={a^0,x^A}, and x does not contain a^0; C_x is otherwise
arbitrary, including a possible positive a descriptor. Perform

  p->x ; x->a ; a->p ; x->p.

The first step is legal because x's nonnegative age is oldest or tied with
anchor age0. Its incoming two identities force C_x={p^0,a^1}: if x had a
positive a descriptor, MIN with1 still gives1. (If x had no a descriptor, the
same result holds.) After that step p cannot contain x: it removed x, and x's
reply cannot contain its own ID.

The second step is forced by the ages0,1 at x. It leaves
  C_a={x^0,p^1}, C_x={p^1}.
The third step is forced toward p, and its incoming pair {a^0,x^1} is retained
at p. Thus C_p={a^0,x^1} exactly. The fourth step is the singleton x->p; p's
full reply contains a^0 and x^1. At x the self entry x is discarded, giving
C_x={a^0}; at p the incoming fresh x^0 refreshes its resident x and leaves a^0
protected/unaffected. Every old a^0 holder except p was untouched; p's zero is
restored, and x is an additional zero holder. Hence this path raises k by one.

In particular, at a maximum-k state with C_a empty, no vertex in I can cache
an identity in J=V\(I union {a}). Every I cache therefore consists of a^0 and
at most one residual identity from I. There are no positive a copies by
Section2, so every vertex in J has no descriptor for a at all.

## 5. Minimize the number of residual I components

Consider all states in the fixed closed class with maximum zero count k and
C_a empty. They exist by Section3, and Section4 shows their I residual graph
is closed: all residual IDs lie in I. Its number d of weak components is a
finite integer. Choose such a state minimizing d. If k=n-1 the anchor is
universal, so assume J is nonempty.

Weak connectivity across (I union {a},J), the empty owner, and no I->J edges
imply some nonholder P in J caches a vertex of I. No J vertex can cache a,
because it contains no a descriptor. Inspect an actual oldest partner at P
before any following normalization; P will be frozen during normalization,
so its cache ages and oldest choices are unchanged.

Within I, reserve the anchor a^0 and simulate the proved ell=1 capacity1
kernel on residual caches: skip all residual no-op initiations at empty
residual caches, and otherwise activate a residual-oldest partner q, send
fresh self plus a^1, and reply a^0 plus the residual singleton. MIN resets the
anchor and all other updates are exactly residual ell=1. Each residual
component can therefore be normalized to a zero-age rooted star with any
prescribed root Q. Its root has C_Q={a^0}, while every other component member
v has C_v={a^0,Q^0}. This changes neither its vertex set nor d, leaves P
untouched, and keeps C_a empty.

### Case A: P's selected oldest partner u lies in J

Since P caches an I target Q and capacity is2, C_P={u,Q}. Normalize Q's
residual component to a star rooted at Q, then activate P->u with extra Q.
Incoming protection forces
  C_u={P^0,Q^b}, b>=0.
The bound is b>=0, not necessarily b>=1: an old resident Q^0 may MIN-refresh
it. Nevertheless Q is oldest or tied with P^0, so choose u->Q next, sending
{u^0,P^1}. The responder Q has only a^0 and therefore replies only a^0.
Consequently C_u={a^0,P^1}. The peer P still lacks a: before the first event
both P and u were nonholders and u's preexchange reply contained no a. Thus
u is an a^0 holder with an outward residual edge to the nonholder P.
Section4 gives a zero gain, contradiction.

### Case B: P's selected oldest partner Q lies in I

Normalize Q's residual component to a star rooted at Q, and activate P->Q.
If P was the singleton {Q}, then the one incoming fresh P fits alongside
Q's a^0 without evicting it; P receives a^0 and k increases immediately.

Otherwise write C_P={Q,X}, X!=a,Q. Its outgoing pair is fresh P^0 and
incremented X. Root Q replies only a^0. At Q the incoming two distinct IDs
force its only old a^0 to be evicted, while P retains its extra X and receives
a^0. The new zero set is exactly I'=(I\{Q}) union {P}, and
  C_P'={a^0,X^(oldage+1)}.

If X lies in J, Section4 gives an outward infection and a zero gain.
Suppose X lies in I. If Q's former residual component had at least two
members, any other star member v still has C_v={a^0,Q^0}. But Q is now a
nonholder, so v has an outward edge and Section4 again gives a zero gain.

The only remaining case is that Q's old residual component was the singleton
{Q}. Then X belongs to another residual I component. No other I vertex
cached Q. Replacing the isolated root Q by the new holder P pointing to X
therefore removes one component and adds P to X's existing component. The
owner remains empty, all other zero holders remain unchanged, I' is still
residually closed, and its component count is d-1. This contradicts the
choice of d.

Every case contradicts k<n-1. Hence every closed communicating class contains
a universal zero-age anchor for the fixed prescribed identity a.

## 6. Consequence for full convergence

The previously proved global finite-age reset gives a uniformly accessible
finite family. It guarantees positive recurrent closed regimes and almost-sure
entry into one of them. Section5 gives access from every closed class to a
universal a^0 state. The universal-anchor reduction then reaches the same
fixed labelled canonical H(V,2); canonical H atoms with different orders
communicate. Therefore every closed class contains that same state, so the
closed class is unique. The canonical H state has an empty-root self-loop,
which makes the class aperiodic. The finite-family/reset criterion therefore
gives uniform geometric total-variation convergence to its unique stationary
law. Label equivariance and uniqueness imply uniform conditional peer output,
with the availability/null event stated separately.

For completeness, the finite-family argument gives a common-atom minorization.
Let the uniform age reset have horizon H and hit finite F with probability at
least delta. From each f in F, almost-sure absorption into the union of closed
regimes implies some finite positive-probability path to a closed class; from
there Sections1--5 and the anchor theorem reach the same labelled canonical
state h. F is finite, so choose a common maximum length J and a positive
minimum witness probability epsilon. Pad every shorter path by h's empty-root
self-loop. Then for every initial weakly connected state x,

  P^(H+J)(x,{h}) >= delta*epsilon > 0.

The common-atom skeleton has a unique invariant law and contracts total
variation geometrically, yielding uniform geometric convergence for the full
discrete chain as well. Label equivariance gives uniform stationary local
output conditional on availability. Availability is positive because all
labelled canonical atoms communicate and some have any prescribed observer
nonempty. Conditional output convergence follows from full-state convergence
and that positive limiting availability; temporal independence is not claimed.

No polynomial mixing bound is claimed. The constants J and epsilon above are
existential finite maxima/minima; no efficient access-word bound is proved.
