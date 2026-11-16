# Empty-owner terminal gain at arbitrary capacity, length three

Independently reviewed working proof, integrated on 16 November 2026. Uses the separately reviewed arbitrary-capacity callback; this local lemma alone is not the global convergence theorem.

## Statement

For ell=3 and c>=3, suppose C_a is empty, holder p caches a as an actual oldest entry, and p caches a nonholder. A finite legal path strictly increases N_a while retaining all original holders at the endpoint. Other original copies may have positive ages.

## Construction for c>=4

Select an oldest non-a identity s in C_p. If s is a nonholder, choose any other residual t when one exists. Otherwise choose a nonholder t (distinct from s). Activate p->a with extras s,t, or just s when that is all the available extras. These choices satisfy the exact packet size. The empty reply deletes a, while p retains all other residents, incremented once. Owner a obtains fresh p and the selected residuals.

Execute a->s. This is legal because s was a maximum-age residual and is older than fresh p. If t exists, request is {a^0,p^1,t^(T+2)}; otherwise it is {a^0,p^1}. Thus s holds protected a,p and t when present, with possible MIN decreases. The owner retains t: its old size is at most three, mandatory deletion leaves at least c-2>=2 vacancies, and even a three-entry reply requires at most one victim. If s was already a holder, self-a filtering gives at most two usable reply identities, so no victim is required. This is the only case in which retention of t matters later.

Activate frozen p->s, still an actual oldest choice. If t exists, include t among its extras, and if a second extra is required choose any other residual u. If t does not exist, p has only s, so there are no extras. The request consists of fresh p and t,u when present. Of these, only u can be novel at s.

Choose the reply to contain a and p whenever the pre-request cache has at least two entries, as it does. If its cache has a third entry, choose the third reply as follows. If s is full and u is novel, choose x in C_s minus {a,p,t}; such x exists because c>=4. Then x is not in the incoming request and is an eligible victim. Evict x for u and retain a. If s is not full or u is not novel, no victim is necessary, so choose any required third identity. If the cache has only two entries, the full two-entry reply is {a,p}. Thus s retains a^0.

The reply self-filters p. The active p has at least two vacancies: it previously lost a and now deletes s, so at most c-2 residents remain. At most two usable reply entries remain; hence p receives a^0 without any active eviction. All original holders are present again.

If s was initially a nonholder, it is an additional holder, proving strict gain. Otherwise the chosen companion t was a nonholder and its row was never touched. The owner still caches t, so arbitrary-capacity learned-target nonholder recovery creates an additional holder without losing an original one.

The already proved full-capacity-three terminal gadget handles c=3.

## Boundary checks

- With only one residual s, p->a and a->s send fewer than three identities exactly as required; p->s requests only fresh p, and no responder eviction occurs.
- If c>=4 but s has only three entries after the owner request, a novel u uses a vacancy rather than forcing a victim.
- Choosing x is needed only for a full s and a novel u; then x cannot equal u, and fresh p/retained t are the only other request identities.
- The owner need not preserve t when s is a nonholder, since the gain already follows from restoring p while preserving s.

## Final integration status

This working result is now integrated in the manuscript after independent end-to-end and actual-text audits. See [the audit record](LENGTH-THREE-AUDIT.md). Earlier candidate wording in this research history is superseded by that status; no formal-verification or external-review claim is made.
