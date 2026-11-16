# Conditional query lower bound

`paper/query-mixing-lower-bound.tex` supplies an all-parameter, fixed-observer bound for a uniform b-identifier query conditioned on availability. Set M=binomial(n-1,b). Its worst-case TV error is at least max(0,(1-1/n)^t-1/M), for every 1<=b<=c and every allowed shuffle length.

The witness observer starts with a fixed b-set and no incoming references. Until it first initiates, it cannot be contacted and its available query returns exactly that set. The conditioning denominator is explicitly retained in the proof. Ordered samples have the same lower bound by testing their underlying set.

At fixed error this gives Omega(n), not Omega(n log n). At accuracy O(1/M), it gives n log M-O(n); for b=1 and error O(1/n), this is Omega(n log n). The b=n-1 case correctly gives zero.

Check: `python verification/mandatory-removal/verify_query_coupon_lower.py`. Finite exact checks corroborate the untouched-observer invariant, availability, conditional mass, and TV inequality; they do not replace the general proof.
