# Uniform outward-holder gain via maximum YOUNG ages

Potential new strengthening of lem:generaloutwardgain. No main.tex edits.

In the existing controlled trajectory, mark every initial descriptor old; fresh selves are young; duplicate marking is young-OR, numerical merging MIN. The existing proof establishes F nondecreasing, strict at zero-holder contacts and at migrations selecting an old partner. Thus a constant-F unfinished segment consists only of nonholder migrations selecting YOUNG partner descriptors.

Let t0 be the number of events since initial marking at the start of such a plateau. Every young descriptor's numerical age is at most t0, independently of all initial ages: fresh copies start at zero, each event increments by at most one, copies preserve this bound, and MIN of a mixed duplicate cannot exceed the young input's age.

During the plateau, use local time u and define Y_s(u) as the maximum numerical age among young copies of identity s anywhere (zero if absent). Then J_s(u)=Y_s(u)-u is nonincreasing. If identity s is selected as partner, its active copy is removed, s is not the sole extra (which is a), its responder cannot return self s, and fresh p has another identity. Thus all remaining young s copies have unchanged or smaller ages; J_s drops by at least one. This argument concerns actual young copies and is unaffected by old copies of the same identity elsewhere.

The current anchor a stays old and, during migrations without refresh, has age A+u, where A>=0 is its plateau-start age. Every selected partner copy is young and oldest, so Y_s(u)>=A+u and hence J_s(u)>=A at selection. Identity s can therefore be selected at most (Y_s(0)-A+1)_+ <=t0+1 times. Summing gives plateau length <=n(t0+1).

There are <=nc strict-F events, hence <=nc+1 plateau/next-strict-event chunks. With U=t0+1, a chunk updates U' <= (n+1)U+1 <= (n+2)U. Starting U=1 gives total unfinished prefix length <=(n+2)^(nc+1), independent of initial ages. Add <=n+c+2 terminal-gadget events for a safe outward gain horizon.

This should be independently audited before integrating. It strengthens the existing age-dependent finite-path claim to a fully uniform controlled horizon. It does not supply a practically useful typical mixing rate: counting the probability of this single controlled word remains extremely pessimistic.
