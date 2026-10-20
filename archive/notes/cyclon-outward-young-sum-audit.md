# Audit of polynomial outward gain via sum of YOUNG ages

The root agent's proposed strengthening passes an independent audit. This note changes no main.tex source.

Let C=nc and t0 be global elapsed events since auxiliary marking (initial descriptors old, fresh selves young, mixed duplicate young-OR with numerical MIN). Let F be the young-copy count and S the sum of numerical ages of all young cache copies. Every young numerical age <= global elapsed, so S<=C times elapsed.

Every unfinished constant-F event is a nonholder migration selecting a young partner. Its pre-exchange responder cache Q is disjoint from active cache P union {active p}. Consequently all reply identities are novel at p, fresh p is new at q, and a is old at both ends. The active loses its young selected partner and its old anchor; the responder receives fresh p^0 and old a. Required responder victims are chosen inside the reply.

Therefore exact young-count change is

    delta F = #young replies - #young responder victims.

On a plateau this is zero, hence every young reply is also a responder victim. Its age transfer q -> p cancels exactly in S; there are no duplicate identities at either endpoint to complicate this statement. The exact remaining age-sum change is

    delta S = f_p - (age of selected partner after increment).

The current anchor stays old, so f_p<=c-1. At local plateau time u its anchor has age A+u and increments to A+u+1 before partner selection; oldest selection forces selected age at least that. Thus

    delta S <= c-2-A-u <= c-2-u.

For plateau length L,

    0 <= S_end <= S_start+(c-2)L-L(L-1)/2.

Hence L <=2c+2 sqrt(S_start) <=2c+2 sqrt(C t0), a safe conservative estimate. Group each plateau with its following strict-F event, if any. For w=t0+1,

    w_next <= w+2c+1+2 sqrt(C(w-1))
           <= (sqrt(w)+sqrt(C))^2,

since C=nc>=2c+1 in the applicable c>=3,n>=c+1 regime. There are at most C strict-F events and C+1 such chunks, so

    elapsed+1 <= [1+(C+1)sqrt(C)]^2
               <= C(C+2)^2 <= (C+2)^3.

The final terminal gadget costs at most n+c+2 further events: two events for owner double callback followed by cached-target owner-only service of length <=n+c; other terminal cases are shorter. Thus a clean uniform outward-gain horizon is

    W(n,c) = (nc+2)^3 + n+c+2.

This horizon is independent of every initial numerical age. No age reset is required before or during this macro. It strengthens lem:generaloutwardgain substantially. It still bounds a controlled witness, rather than typical random dynamics.
