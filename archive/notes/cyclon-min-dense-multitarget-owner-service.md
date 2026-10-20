# Dense capacities: owner-only service with ell-1 outside targets

Use the protected MIN mandatory-removal kernel with 2<=ell<=c and c>=n-2.
Fix an owner a, and let I be its current zero-age holders. Suppose a caches
ell-1 distinct peers T outside I, none equal to a. There is an owner-only
positive-probability path of at most

    c+(ell-1)(n-ell)+1

exchanges to a new zero-age a copy, preserving every old zero-age a copy and
not decreasing the number of a identities. The T ages and all other cache IDs,
ages, and occupancies are arbitrary.

## No active-extra eviction in the dense regime

If the active cache initially has d entries, after mandatory removal its free
slots number c-d+1. There are at most n-d-1 possible valid new identities,
because the active self and all d original cache IDs are excluded from that
set. Since c>=n-2, every valid new incoming identity fits the mandatory and
pre-existing vacancies. Thus no retained active extra ever needs eviction.
This counting holds at every shuffle length.

## Repeat-clearing controller

Keep only a active and always choose all T as its ell-1 extras. Stop at the
first responder outside I; its received fresh a^0 gives the desired gain.
Before then the selected responder is in I and therefore is not in T, so all
T remain available as extras and, by the preceding observation, remain cached
by a. Require each I reply to include its resident a. On a responder's first
visit, fill the other reply entries arbitrarily. Its incoming packet contains
{a^0} union T, all received-protected; hence that responder thereafter contains
this entire ell-entry set. Between owner contacts it is passive and unchanged.
On each repeat visit prescribe exactly {a^0} union T as its reply.

A first visit has at most ell-1 usable incoming identities after self-a is
filtered, so the active cache grows by at most ell-2 after partner removal.
A repeat has no usable new identity, and the active cache strictly shrinks.
There are at most n-ell first I visits, because T has ell-1 distinct non-I
peers and a is the owner. If k first visits and r repeats have occurred, the
active size is at most c+k(ell-2)-r. Continuing forever is impossible because
the ell-1 targets remain cached; in particular the stated loose bound forces
an outside-I response.

Every old zero holder is passive and receives protected fresh a^0, so none
loses its zero. All other peers except the final outside responder are
unchanged. Total a-availability cannot decrease.

This is a conditional service lemma. It does not show that ell-1 distinct
outside-I targets can always be brought into the owner's cache, or address
the last fewer-than-ell-1 targets without further structure.
