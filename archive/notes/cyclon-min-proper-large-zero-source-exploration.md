# Proper shuffle: source-only exploration with large zero holders

Use the protected MIN mandatory-removal kernel, 2 <= ell < c. Fix a source a,
and let I be all current zero-age a holders. Suppose each q in I has at least
ell+1 entries. Only a initiates in the following construction. Stop immediately
if its responder lies outside I, since that creates a new zero-age a copy,
preserves every old zero-age a copy, and cannot decrease a-identity count.

## Prescribed cached-target service

For any cached target z of a, retain z until it is selected and, at every
preceding I responder, require a length-ell reply that contains a and excludes
z. This is feasible because each passive cache has at least ell+1 entries;
passive cardinality never decreases. Received fresh a^0 preserves each old
zero anchor. The target-retention buffer-count lemma applies because a is a
filtered self reply; therefore outgoing-extra victims can be chosen away from
z. The target age is exactly A+t after t owner events, with A its initial age.

For each identity s other than a,z, let M_s(t) be its maximum stored age over
all caches, with maximum zero if absent, and K_s(t)=M_s(t)-t. Every K_s is
nonincreasing. When s is the selected partner, no descriptor with identity s
is transmitted: it was mandatorily removed from the initiator, the passive
responder cannot reply with its own self ID, and the only fresh self is a.
Thus M_s(t+1)<=M_s(t), so K_s drops by at least1. Selection requires
K_s(t)>=A. Consequently s is selected at most (M_s(0)-A+1)_+ times. The owner
must therefore select z or contact outside I after finitely many events.

The reply can simultaneously contain any specified other resident ID r,
provided r differs from a,z. This costs only the available second reply slot.

## Directed-path exploration

Assume a directed cache path currently leads from a to a peer outside I.
Choose a shortest such path a,z,...,x, where x is outside I. Use the cached-target
service for z. During this service retain the current first path head. If a
selected I responder is a later node on the chosen path, include its path
successor in the reply, and immediately use the resulting shorter path. If
the selected responder is z, include z's successor and again shorten the path.

These reply requirements are compatible with including a and excluding z:
the path is simple, its successor is neither a nor the earlier head z, and
ell>=2. An off-path responder does not alter any later path node, while its
exchange can retain z. If a path-node's old successor is evicted passively,
that sent victim is received-protected at a, which itself gives the same
shortcut. Thus a finite target-service phase either reaches outside I or
strictly decreases the path distance. There are at most n-1 distance decreases.

Hence the large-zero-holder hypothesis plus directed reachability of any
nonzero holder implies a finite source-only zero gain. The result does not
assert that weak connectivity alone gives such directed reachability, nor that
newly activated outside peers remain large. Those are separate obstacles to a
general proof from arbitrary weakly connected states.
