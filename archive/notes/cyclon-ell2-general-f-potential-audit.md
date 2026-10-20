# Independent audit: general ell=2 outward-gain proof

AUDIT RESULT: PASS, for every n and every c>=3 (with c<=n-1 globally), under
received-identity protection, MIN duplicate merging, mandatory oldest removal,
and integer ages. No half-dense hypothesis is used.

Auditor: mandatory_path. This note audits the mathematical argument proposed
by mandatory_enumeration; it is not a protocol change.

## Exact invariant concerning the initial zero source

Initially choose owner a empty, all h anchor holders zero, and a holder p0
with a cached nonholder. Let B be the OTHER h-1 initial holders. During the
main tracking phase only the current tracked holder initiates. Every b in B
remains passive, retains its received-protected a^0, and never becomes the
tracker. A nonholder becomes tracker only at a forced migration, when the
previous tracker loses its sole a copy. Thus the complete holder set is
always B union {current tracker}. The initial tracker p0 can later reappear
as a tracker, but only after being a nonholder and receiving the migrated
a. It cannot become an untracked additional zero holder: retaining a at the
old tracker while inserting it at a nonholder would already be the desired
strict holder gain.

A cached nonholder predecessor is preserved at the tracker. Initially it is
the specified target. Every holder-response event leaves it unsent and cannot
evict it. If selected, that selected partner is a nonholder and the next
migration installs the previous tracker freshly at the new tracker. Owner
contact uses that predecessor as extra.

## Auxiliary colors

Mark every initially stored descriptor OLD. Fresh self descriptors are YOUNG;
copies carry their color; a duplicate merge is YOUNG iff either input is
YOUNG. These are proof-only tags. OR tags cannot be destroyed by MIN merges.
Every anchor a remains OLD because its owner is frozen. Every identity b in B
is permanently OLD everywhere: b never initiates, hence no fresh self b is
ever generated. In particular every selected partner in B has an OLD
identity descriptor at the active tracker, even if its numerical age is0.
This is the point that avoids the earlier reset-of-anchor-age obstruction.

Let F count all YOUNG cache entries at all nonowners. It is bounded by nc.
The main phase continues only while the tracked cache is full. An underfull
tracker gives a finite strict holder gain by fixed-tracker service: holder
replies contain a, giving at most one new usable ID and never increasing its
cache; a cached nonholder remains unsent; repeated holder responders shrink
the cache. The first nonholder contact retains a because mandatory removal
leaves two vacancies. An earlier owner contact uses the double callback below.

## Holder responder in B

Let full tracker p contact b in B and send fresh p plus a. If b already knows
p, reply {a^0,p}; the active cache loses its partner and receives no new usable
ID, becoming underfull, so the underfull finish gives a strict holder gain.

Otherwise b newly accepts fresh YOUNG p. If b is underfull it loses no resident,
so any legal reply containing a gives F a strict increase from this fresh p.
If b is the singleton anchor, the tracker becomes underfull and finishes.

If b is full, it needs one victim distinct from incoming-protected a. Its
c-1 nonanchor entries cannot all be YOUNG IDs already at the active cache:
only c-2 IDs of the active cache can occur there, because active a is OLD and
identity b is absent from b's own cache. Choose a victim D that is OLD or
YOUNG with identity absent at the active cache. Reply {a^0,D}. A YOUNG victim
is copied as a new protected YOUNG at the active tracker, compensating its
loss at b; an OLD victim causes no YOUNG loss. The mandatory selected b is
OLD, and the active extra a is OLD and protected by its incoming duplicate.
Thus fresh new p adds at least one uncompensated YOUNG entry: F increases
strictly. Other YOUNG duplicates preserve their colors under OR.

This victim-existence count remains valid even when colors for the same ID
differ at the two endpoints: it uses the c-2 shared-IDENTITY bound, not the
incorrect assumption that a YOUNG copy at b implies a YOUNG copy at p.

## Nonholder responder

If a nonholder q has any ID in the active pre-cache P union {p}, include one
such ID in the two-entry reply. It is duplicate or self-filtered at p (and
cannot be q itself). At most one new valid reply remains, so mandatory
removal suffices and p retains a while q newly accepts it: strict holder gain.
These reply choices have feasible victims. If q knows p, only a is new;
return p plus a victim when needed. If q does not know p, both outgoing IDs
are new and all returned old entries are eligible victims.

Consequently a continuing event has q's entire pre-cache disjoint from
P union {p}, and has two novel reply IDs. The tracker must evict its only
extra a, remains full, and becomes a nonholder; q gains protected a and fresh
p and becomes the tracker. Every YOUNG responder victim is copied as a new
protected YOUNG to p. Fresh p contributes +1 YOUNG at q. The only possible
uncompensated loss is the mandatory partner q if its selected copy is YOUNG.
Therefore

  Delta F >= 1 - 1_{selected q is YOUNG} >= 0.

If selected q is OLD, F increases strictly. This calculation includes all
passive residual copies: those not chosen as victims remain; those chosen
are copied to new IDs at p; incoming duplicate OR tags cannot erase YOUNG.

## Owner contact and the double callback

The owner has stayed empty. A tracked holder u contacting a sends its cached
nonholder predecessor v as extra. It loses a and leaves
C_a={u^0,v^(B+1)}, B>=0. The next owner activation must contact v, sending u.
Fresh a creates a holder at v and restores the temporarily lost holder.
The owner retains u because its one remaining resident plus at most two
reply entries fits c>=3. Peer u remains a nonholder. Owner-only cached-target
service now reaches u or another nonholder, inserting another a while all
old holders passively retain fresh received a. Net holder count increases.
This finite macro ends the proof; its exchanges are not included in the
main-phase F or K accounting.

## Max-age defect K and termination

Suppose a continuing main-phase path were infinite. F is a bounded
nondecreasing integer, so from some finite time T onward it is constant.
No responder in B can then be contacted (that would strictly increase F or
finish with a gain). No OLD nonholder partner can be selected (same reason).
Every subsequent event is a YOUNG nonholder migration. In particular no
other anchor copy is received: the new responder lacked a, so the tracked
anchor's numerical age A_t increases by exactly1 at each step. With t the
number of MAIN-PHASE exchanges, d=A_t-t is constant on this suffix.

For each identity s != a define

  M_s(t)=max({0} union {ages of all currently stored s descriptors}),
  K_s(t)=M_s(t)-t.

The baseline0 handles absent identities and later fresh births. Every
main-phase step increments only the active cache's ages by1, sends only a
as an extra, and creates a fresh self at age0. Every reply copies a passive
pre-age. MIN cannot increase an incoming maximum. Thus M_s(t+1)<=M_s(t)+1,
so K_s is nonincreasing.

If partner s is selected, its active copy is removed BEFORE the packet and
is not sent: the sole extra is a!=s. Responder s cannot return its own ID s,
and the initiator is not s, so no fresh s is born. Every remaining s copy is
passive, hence M_s(t+1)<=M_s(t), including copies residing elsewhere. Therefore
K_s drops by at least1 on every selection of identity s.

Oldest selection gives selected pre-age >= A_t (all active entries receive
the same +1 first). Hence K_s(t)>=d whenever s is selected on the constant-F
suffix. Starting from the finite values K_s(T), each identity s!=a can be
selected only finitely many times while this inequality holds. There are
only n-1 such identities, contradicting infinitely many main-phase events.
The owner selection instead invokes the finite strict-gain macro. Thus the
controlled witness always terminates in a strict holder gain.

## Consequence

Combine this outward-gain lemma with generic positive-copy zeroification,
the general owner-empty extremal lemma, and the already audited incoming
boundary/residual-singleton clearing argument. Every closed class at ell=2,
c>=3 contains a universal zero anchor. The c=2 case was proved separately.
Uniform finite-age reset and finite-family-to-common-atom padding then give
unique stationarity and uniform geometric full-state convergence for EVERY
ell=2 capacity. Conditional local samples are uniform by label symmetry.

No uniform initial-age bound for this outward-gain word is claimed. None is
needed: the global reset family is finite, and finitely many finite access
words to the common atom yield positive uniform constants. The max-age K
argument uses the single-step main-phase clock only; owner/underfull finishing
macros are terminal and are never mixed into its inequalities.
