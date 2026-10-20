# A zero-rich three-event bootstrap with temporary zero loss

Use the mandatory oldest-removal, received-ID-protected, MIN-duplicate kernel
with any 3 <= ell <= c. Fix distinct peers a,p. Assume

    C_p is empty, and every q in I=V\{a,p} contains a^0.

Suppose the owner's actual oldest partner is Q in I, and p is an actual
oldest partner in C_Q. Assume |C_Q|>=3. There is a controlled path of exactly
three exchanges to a universal zero-age anchor a. Every original zero copy
of a is present again at the endpoint. No underfull-cache, proper-shuffle,
shared-descriptor, or common-age assumption is needed.

1. Activate Q and select p, breaking an oldest tie in its favor if necessary.
   Reserve a as an outgoing extra. Because ell>=3 and |C_Q|>=3, choose at
   least one other outgoing extra R. All such other extras belong to I\{Q}.
   The empty responder p sends nothing. Q retains its incremented a^1, so
   it temporarily loses its zero copy without losing identity a. Peer p
   receives fresh Q^0, a^1, and at least one R descriptor. Every R descriptor
   has age at least one, since Q incremented all its descriptors. The whole
   buffer has size at most ell<=c and fits at the empty peer p.

2. Activate owner a and select Q. This remains an actual oldest choice:
   the previous exchange touched only caches Q and p, and a was frozen.
   Fresh self a^0 is retained and protected at Q, so Q's old zero is restored.
   Any choices of the remaining legal buffer entries, replies and victims
   suffice. Every other original zero holder remains unchanged, and p's
   cache and its numerical ages have not changed since step 1.

3. In p's cache, Q has age zero, a has age one, and every other ID belongs
   to I\{Q} and has age at least one. Therefore an actual oldest partner
   can be chosen among these other IDs; call it R. Activate p with partner
   R, reserve its positive a descriptor as an outgoing extra, and include
   R's a^0 in the reply. Received-ID protection and MIN preserve a^0 at R,
   because incoming a^2 merges with its resident a^0. The received a^0 is
   protected at p and gives it a zero copy. Thus every nonowner stores a^0.

The zero count evolves n-2, n-3, n-2, n-1 at the four macro endpoints. The
identity-holder count rises from n-2 to n-1 at the first exchange and never
falls afterwards. All prescribed choices have positive probability.

The remaining accessibility gap is precise: arbitrary zero-rich states need
not have empty p, nor a currently selected owner head Q whose actual oldest
partner is p and whose cache has at least three entries. This lemma supplies
a repair once that local configuration is reached; it does not establish
that the configuration is always reachable.

## Local-row generalization

The same proof does not require that p be the only nonzero peer. Let I be
all current a^0 holders. It suffices that p is empty, the owner's actual
oldest Q belongs to I, p is an actual oldest partner of Q, |C_Q|>=3, and
C_Q is a subset of {a,p} union I. Every other required outgoing extra from Q
then belongs to I\{Q}; the third exchange still chooses such an old zero
holder. All other nonzero peers are untouched. The endpoint increases Z_a
by exactly one and restores every original zero. The identity-holder count
increases by one as well. The global zero-rich case is a special case in
which the row condition is automatic.
