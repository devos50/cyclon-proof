# Protected MIN, shuffle length 3: cooperative callback with a common zero target

Fix capacity c >= 3 and a peer a. Let I be exactly the peers whose current cache
contains a at age zero. Assume p is outside I, distinct from a, cached by a, and
that a^0,p^0 are present at every q in I. Other descriptors and ages are
arbitrary; residual identities need not stay inside I.

Under mandatory oldest removal, protected received identities, MIN duplicates,
and shuffle length3, there is a positive-probability controlled path that adds
at least one zero-age a copy, preserves every old zero-age a copy, and does not
decrease the total number of a copies. A safe length bound is c(n+c+1)+1.
This remains conditional: the common zero-target hypothesis is used.

## Clearing a zero head or exposing an outside head

Suppose the owner's actual oldest partner is Q in I. Freeze a and every peer
outside I; keep only Q active. Reserve a,p as outgoing extras, and prescribe
replies from I to contain a,p. Removing these reserved descriptors gives exact
shuffle length1 with configured capacity c-2. Stop before Q would select an
outside-I residual partner, or when Q has no residual descriptor.

The reserved ages remain0 at event boundaries. Every residual age and both
reserved ages increment by1 at activation, so a largest-age residual is a legal
full-cache oldest partner, including on ties. Thus no anchor need be selected
while any residual descriptor remains. Empty reduced initiators are skipped.

Within |I|+c events the block stops. Each first I-responder visit teaches fresh
Q^0 to that responder, persistently throughout this Q-only block. A repeat
returns {a^0,p^0,Q^0}, whose residual Q is filtered as self, and strictly shrinks
Q's residual cache. There are at most |I|-1 first visits and c-2 shrinking
repeats. A boundary partner is exposed without executing the boundary event.
The bound remains valid if configured c-2 exceeds the local population.

The owner is unchanged, every I peer still has a^0,p^0, and either

  (i) C_Q={a^0,p^0}; or
  (ii) Q's oldest residual descriptor r lies outside I, and a,p,r all lie in C_Q.

## Owner step

Activate a and select its unchanged actual oldest partner Q. Include p as an
extra and fill any required second extra arbitrarily. In case(i), reply with
{a^0,p^0}; in case(ii), reply with {a^0,p^0,r^b}. These are valid reply sizes.
The owner filters self a, already knows p, and receives at most the one outside
identity r. Hence the mandatory vacancy suffices, no retained extra is evicted,
the owner's cache size cannot grow, and its number of cached I identities
strictly drops. Its retained p is refreshed to0.

Q receives fresh a^0 and the p descriptor; both are received-protected, and MIN
keeps its a,p ages0, regardless of the second extra. Other I peers are passive.
Thus the same hypotheses persist until an owner activation selects outside I.
No step adds an I identity to the owner's cache. At most c zero-head removals
are possible. The outside target p stays cached, so an outside contact must
occur after these removals. Fresh a^0 then creates a new zero copy, every old
zero holder stays, and no other a identity is lost. This proves the claim.

The count c(n+c+1)+1 covers c clearing blocks, c owner-head removals, and one
final owner contact. The former closed-residual lemma is the special case
where only case(i) occurs.
