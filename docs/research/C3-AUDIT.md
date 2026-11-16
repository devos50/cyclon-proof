# Capacity-three proof audit record

16 November 2026. This records internal mathematical review of the working proof, not external peer review or formal verification.

## Scope accepted

The final manuscript statements `lem:c3learnedcallback`, `cor:c3zeroify`, `lem:fullshuffletrianglegain`, `lem:c3ownerterminalgain`, `lem:c3outwardgain`, and `thm:c3generaluniform` received independent adversarial reviews, including a separate end-to-end pass and a subsequent pass over the actual final TeX text. No remaining material gap was identified in those reviews.

The convergence theorem covers **exactly `c=ell=3` for every `n>=4`**, under the adopted protected/MIN model, iid uniform initiators, initially weak connectivity, and arbitrary finite nonnegative integer ages. Constants are implicit. It does not prove polynomial mixing, fixed length-three convergence at every larger sparse capacity, or general higher-length convergence.

## Dependency checks

Review covered the exact transition rules, target retention, finite-prefix interpretation of hypothetical infinite owner paths, integer-age divergence and clearing, zeroification, closed-class extrema, directed-path service, empty-owner reduction without assuming outward closure, residual capacity-one/two normalization, outward migration potential, incoming component decrease, finite-reset reachability to closed classes, empty-root padding, common-atom minorization, stationary availability, and label symmetry.

A finite reset family does not by itself supply a self-loop at each reset state. The proof uses a finite reachability/SCC argument for closed-class accessibility and only later the canonical empty-root self-loop for a fixed-horizon minorization.

## Corrections made during review

- Owner-only oldest-pointer coalescence was rejected: an exact 72-event affine cycle exists. The proof instead uses age divergence followed by a legal clearing intervention.
- Received duplicate ages were changed from unjustified equalities to MIN-compatible upper bounds. The relevant terminal arguments need identity duplication, not equality of duplicate ages.
- The zero-holder bridge may use an oldest tie, rather than a strictly oldest residual.
- A forced migration copies the old responder's identity set, not necessarily every numerical age.
- The local one-head callback explicitly checks whether the outside secondary is already oldest before preparing the internal head.
- A callback can reach some nonholder, not necessarily a prescribed one. The owner-terminal restoration proof does not assume prescribed nonholder service.
- The minorization probability is the minimum probability of the **padded** finite paths, including the probabilities of empty-root activations. The corresponding wording in older qualitative common-atom paragraphs was corrected too.

## Corroborating checks

The complete maintained suite passed **37/37** checks. New checks include the exact affine-cycle certificate, 5,100 learned-boundary starts, 5,100 outward-controller starts with exact maximum-age assertions, full-shuffle triangle/restoration cases, and 16,650 dimension-independent local boundary configurations. These finite checks are supporting regression evidence; they are not the arbitrary-population proof.

## Subsequent scope update

The later [general length-three proof](LENGTH-THREE-GENERAL-CONVERGENCE.md) extends the convergence conclusion to every allowed capacity at `ell=3`. This note retains the earlier capacity-three argument and its original audit scope; references here to sparse length-three convergence remaining open describe that earlier stage. Higher shuffle lengths and polynomial mixing remain open.
