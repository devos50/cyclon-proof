# Primary sources and model provenance

The bibliography in [paper/main.tex](../paper/main.tex) is retained in full. These links identify the main external references, rather than proving the current working claims.

- [PEERSWAP: A Peer-Sampler with Randomness Guarantees](https://arxiv.org/pdf/2408.03829), 2024. Starting motivation and comparison. PEERSWAP and the adopted CYCLON kernel are different processes; a PEERSWAP mixing estimate is not automatically a CYCLON estimate.
- [CYCLON: Inexpensive Membership Management for Unstructured P2P Overlays](https://acropolis.aueb.gr/~spyros/www/papers/Cyclon.pdf), Voulgaris, Gavidia, and van Steen, 2005. Original protocol reference.
- [Epidemic-Based Self-Organization in Peer-to-Peer Systems](https://acropolis.aueb.gr/~spyros/www/papers/Thesis-Voulgaris.pdf), Voulgaris, 2006, Chapter 2, particularly Figure 2.3, page 19. Source for the adopted received-identity protection and minimum-age duplicate convention.
- [Brief Announcement: Performance Analysis of Cyclon, an Inexpensive Membership Management for Unstructured P2P Overlays](https://doi.org/10.1007/11864219_45), Bonnet, Tronel, and Voulgaris, DISC 2006, pages 560–562. An earlier basic-shuffling, single-node in-degree Markov model reports a much smaller mixing estimate. Transferring it to this oldest-first process requires justifying the projection and controlling local identity bias.

The exact research target is [MODEL.md](MODEL.md). Its independent uniform initiator scheduler, merge semantics, underfull-cache behavior, and deterministic-time availability conditioning are explicit. Calling a result “CYCLON convergence” without those qualifications would conceal relevant model differences.

A complete novelty and related-work review remains a future publication task. No claim of priority or publication readiness follows from this bibliography.
