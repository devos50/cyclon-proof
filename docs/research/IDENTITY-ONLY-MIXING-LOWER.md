# Identity-only mixing lower bound

`paper/identity-mixing-lower-bound.tex` proves, for every admissible capacity and shuffle length, a lower bound using zero initial ages and only the cache-identity projection. With mu = (n-1)(1-1/n)^t, worst-case identity-state TV is at least max(0, 1-(2c+4)/mu).

A singleton in-star supplies the witness. Never-initiated leaves remain unchanged and uncontactable, so the hub's occupancy dominates coupon survivors. Stationary expected occupancy of a fixed identifier is at most c by label exchangeability. The resulting fixed-error lower is Omega(n log(n/c)) when c=o(n), and Omega(n log n) for fixed c.

This does not assert a comparable lower for one fixed peer's single queried identifier. It strengthens the *scope* of the existing arbitrary-age coupon argument by witnessing identity disorder without large initial ages; it does not supersede the stronger capacity-one depth lower bound.

Check: `python verification/mandatory-removal/verify_identity_coupon_lower.py`. Exact finite checks corroborate the initial-identity invariant and coupon moments, not the all-parameter mathematical proof. Independent reviewers: mixing_route and rate_audit.
