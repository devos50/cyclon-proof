# Concrete obstacles to elementary c=ell=2 label-bias mixing arguments

## One-step identity frequency can drift away from stationarity

For n>=4, distinguish owner a, another vertex j, and I=V\{a,j}. Choose a
cyclic derangement g of I. Set

    C_a={j^0}, C_j=empty, C_i={a^0,g(i)^1} for every i in I.

The overlay is weakly connected and N_a=n-2 peers cache a. Every I initiator
selects its strictly oldest g(i), sends its own fresh identity and a^1, and
receives a^0 in the reply. Both endpoints retain a, so N_a is unchanged.
Vertex j no-ops. Owner a initiates toward empty j and creates one fresh a
copy there, so N_a increases by one. Therefore

    E[N_a(next)-N_a] = 1/n > 0.

At the unique label-invariant stationary law, E N_a=E(total descriptors)/n
<=2. Thus for n>=5 the already overrepresented identity has strictly
positive one-step mean drift. Frequency alone cannot have a uniform
one-step linear restoring drift. With C_a empty, I=V\{a}, and the same
construction, N_a=n-1 has exactly zero one-step drift despite maximal bias.

This does not rule out multistep drift or a potential containing ages and
local structure.

An exact age-only comparison makes the missing information explicit. Keep
the same identity caches above but swap the two ages at every i in I:
C_i={a^1,g(i)^0}. Now each I initiator selects a and loses its a copy, while
owner a still creates one and j still no-ops. The mean drift becomes

    (1-|I|)/n=(3-n)/n,

instead of +1/n. The identity overlay, every cache occupancy, N_a and all
other identity frequencies are identical in the two states. Therefore an
identity-only aggregate cannot close this transition law; ages genuinely
change both its magnitude and sign.

## No fixed weighted row-Hamming contraction under synchronous initiators

Take four distinct peers p,q,r,s and states

    X: C_p={q}, C_q={s}, C_r={s}, C_s=empty;
    Y: C_p={r}, all other caches identical to X.

All ages are zero. For larger populations every remaining peer may have
singleton cache {s}. Both overlays are weakly connected. With the same next
initiator in both chains, all choices are deterministic:

* If p initiates, both new C_p equal {s}, but X gains p only in C_q and Y
  gains p only in C_r. One row disagreement becomes two.
* Any other initiator leaves exactly the original disagreement at p.

For fixed positive row weights w_v, the initial distance is w_p and the
expected next distance is

    (1-1/n)w_p + (w_q+w_r)/n.

Uniform nonexpansion would require w_q+w_r<=w_p for every distinct p,q,r.
Interchanging p and q yields 2w_r<=0, impossible for positive weights.
Thus no fixed positive weighted row-Hamming distance is even uniformly
nonexpansive under common-initiator coupling. With equal weights the n=4
example gives expected distance 5/4 from initial distance one.

This does not rule out other couplings, metrics depending on local states,
or a distance tailored to the output at one observer. Indeed in the p
activation branch that observer's cache coalesces while disagreement moves
to other peers.

## Arbitrarily large ages at a fixed n cannot force unbounded mixing time

The established uniform all-age minorization with T_n<=16n^2 and
gamma_n>=(4n)^(-T_n) implies a finite worst-case mixing bound depending only
on n. Therefore any genuine superpolynomial lower bound must use a family
with n increasing. Sending an age parameter to infinity at a fixed network
size cannot itself produce arbitrarily large worst-case mixing times under
this model. No growing-n superpolynomial bottleneck construction has been
proved here.
