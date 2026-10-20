# Proper-shuffle zero-rich bootstrap: the two-entry row corner

This extends the audited three-event bootstrap, under the additional proper
shuffle condition 3<=ell<c. Let I=V\{a,p}, every q in I contain a^0, and
C_p be empty. Suppose the owner's actual oldest partner Q belongs to I and
p is an actual oldest partner at Q. Then a universal zero anchor is reachable
in at most five exchanges, restoring every original zero at the endpoint.
The already audited |C_Q|>=3 case takes three exchanges, so consider

    C_Q={a^0,p^m}.

Execute Q->p with request {Q^0,a^1}; the reply is empty. Then immediately
execute a->Q. Its oldest choice is still legal because a was frozen. The
reply from Q is only a^1, filtered as the owner's self. Thus the owner loses
Q, receives no new ID, and Q receives fresh protected a^0. Peer p remains
{Q^0,a^1}. All original zeros are now restored.

Inspect the owner's cache after this second exchange. If its oldest head
is p, contact p and finish. If its cache is empty, Q received no extras and
is {a^0}. Activate p->a; its empty reply leaves C_p={Q^1}. Then p->Q sends
only fresh p^0, which fits alongside Q's anchor, and receives a^0. This takes
four exchanges total.

Otherwise an actual oldest remaining owner head R lies in I. In the second
exchange choose this R as an outgoing extra. This is a controlled choice
made in advance: the second reply is only self-a, so the post-exchange owner
cache is precisely the old owner cache minus Q with every age incremented.
Q's new cache consists of a^0 and the chosen owner extras, all with ages no
greater than R's, and R's age is at least one. Therefore Q->R is a legal
oldest choice. Perform this as the third exchange, include a as extra, and
require a^0 in the reply. Both Q and R keep their zero, and R receives the
protected fresh descriptor Q^0.

Now perform p->a as the fourth exchange. It is p's unique oldest choice,
since p still has {Q^0,a^1}. The request is {p^0,Q^1}. Require R in the owner
reply, where R is still an oldest owner resident: the third exchange did
not touch the owner. Every usable returned ID belongs to I, has age at most
R's, and R's age is at least one. There are at most ell such IDs. Because
ell<c, all of them fit alongside retained Q^1, so Q cannot be evicted.
Choose R as p's oldest partner for the fifth exchange, and include Q as an
extra.

In this last request the ID Q is already resident at R from the third
exchange. Let b=|C_R|, u be the request size, and h its number of resident
IDs. Then h>=1, u<=ell<c, and a is not in the request. The required victim
count d=(b+u-h-c)_+ satisfies

    d <= b-h-1,        d <= ell-1.

The first bound follows from u<=c-1; the second from b<=c and h>=1.
Hence choose d residents outside the received IDs and outside a, put those
victims and a in the reply, and fill to min(ell,b). Its received protection
preserves every incoming identity, keeps R's old a^0, and gives p a protected
a^0. Every original zero is present at the endpoint, and p is a new zero.

This five-event extension does NOT extend as stated to ell=c: after the
fourth exchange p can have a full cache without identity a, and its full
received buffer at R would then necessarily exclude R's old anchor. The
three-event |C_Q|>=3 lemma remains valid at full shuffle because p still
holds and transmits a positive descriptor at its last exchange.
