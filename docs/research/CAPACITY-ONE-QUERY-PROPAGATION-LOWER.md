# Capacity-one fixed-query propagation lower bound

`paper/capacity-one-query-lower-bound.tex` proves a genuinely sample-level lower bound at c=L=1: for every fixed error epsilon in (0,1), worst-start conditional one-ID query mixing requires at least n log n - O_epsilon(n) global events. At (1-delta)n log n, the query TV error tends to one.

Start with a zero-age directed label cycle. The exact capacity-one rotation and a circular metric give total edge-length drift E[W_next|state] <= (1+1/n) W. Cyclic symmetry plus at most one empty row converts this into a conditional query-distance bound. A metric-ball test, with real-radius optimization, gives TV >= max(0,1-sqrt(8n)*(1+1/n)^(t/2)/(n-1)).

This improves the constant-error fixed-query baseline from Omega(n) to Omega(n log n). It is separate from the capacity-one Omega(n^1.5) full-state lower; that stronger full-state result is not asserted for a query. No extension to c>=2 is claimed: descriptor duplication there breaks the simple length drift.

Check: `python verification/verify_c1_query_propagation.py`. Exact finite checks cover every connected capacity-one identity state for n<=5, all its initiator transitions, and cycle-start conditional query laws. They corroborate but do not replace the general proof.
