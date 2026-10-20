# Diagnostic c=ell=2 simulations: no observed condensed hub

These are finite Monte Carlo diagnostics, not a mixing proof or a certified
stationary estimate. The independent numerical-age kernel uses uniform
global initiators, uniform oldest ties and uniform passive victim subsets.

Settings: n=20,50,100; three initializations (a universal zero anchor with
all residual ages zero; the same with residual ages 1,000,000; a random
connected overlay); three reproducible seeds per setting; 1,000 rounds per
run, one round=n global activation events. Measurements after round100,
every10rounds. Script: /private/tmp/cyclon-c2-montecarlo.py.

| n | Mean maximum indegree, averaged across starts | Full-cache fraction |
|---|---:|---:|
|20|5.01|0.9972|
|50|5.80|0.9997|
|100|6.34|0.9999|

The post-burn mean of the maximum descriptor age was approximately1.5 for
all populations and starts. The identity maximizing indegree changed over
10-round intervals; its persistence probability was close to1/n, with no
signal of a persistent condensed hub in these runs.

For n=100 and the large-age universal-anchor start, the original hub's
mean indegree across three seeds was84.7after1round,60after2,11after5,
and0.67after10 (initially99). The 1,000,000-age descendants disappeared by
rounds2--4 atn20,4--6 atn50,and5--7 atn100. The old-age extinction time was
checked each round; ages generated after initialization cannot reach the
threshold within these runs, so this criterion is unambiguous.

These data suggest that the explicit common-atom mixing bound is extremely
pessimistic for the tested starts. They do not exclude an adverse family of
initial states or establish the absence of condensation asymptotically.
