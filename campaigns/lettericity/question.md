# 3-SAT → Variable-alphabet lettericity

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

Given a graph G and alphabet budget k, find a vertex order, a letter for every vertex, and a directed decoder on at most k letters such that each earlier/later vertex pair is adjacent exactly when its ordered letter pair is in the decoder.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This addresses recognition when the alphabet is an input parameter, beyond fixed-alphabet structural results.

## Difficulty

Both the order and the partition are free. A hard-looking encoding with a supplied partition need not prove the unrestricted result.

## Literature context

Fixed-alphabet algorithms and supplied-partition formulations do not classify recognition when both the alphabet budget and the partition are part of the problem.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Section 6](https://link.springer.com/article/10.1007/s00453-025-01341-9): Alecu, Kanté, Lozin and Zamaraev, *Lettericity of graphs: an FPT algorithm and a bound on the size of obstructions*, Algorithmica 88, Article 2 (2026), Section 6, explicitly leaves variable-k recognition open and conjectures NP-completeness. Their fixed-k algorithm does not settle this ordinary threshold problem. The research target here is a reduction, not a parameterized reduction.
- [arXiv:2605.07899v1](https://arxiv.org/html/2605.07899v1): Grobler, Morawietz and Sacher, *Towards Settling the Complexity of the Lettericity Problem*, arXiv:2605.07899v1, still states this gap in its introduction. Sections 3 and 4 establish easier retrieval problems and symmetric lettericity. These restrictions do not settle the unrestricted minimization problem. Section 5 proposes extension problems with one supplied solution object; a reduction from one of these to unrestricted lettericity remains an additional obligation.
- [arXiv record](https://arxiv.org/abs/2605.07899): Inspected the Algorithmica conclusion, the 2026 arXiv introduction, definitions, retrieval statements, symmetric-case proof and extension discussion, and the arXiv record. No general settling result was located. The conference version was subsequently identified as CiE 2026; its full text remains inaccessible, as recorded in the follow-up below. The initial WG lead was an erroneous search-snippet attribution. Full citation-chain coverage, unindexed results and unpublished work remain unresolved.
- [10.1007/978-3-032-31348-5_20](https://doi.org/10.1007/978-3-032-31348-5_20): Additional actual queries were "Coloring Extension" "lettericity", "Towards Settling the Complexity of the Lettericity Problem" WG 2026, "letter graphs" "given partition" complexity, "Coloring Extension" "decoder" NP, and "lettericity" "acyclic" partition. The conference publication is reported as CiE 2026, pp. 304–319, DOI 10.1007/978-3-032-31348-5_20. The publisher endpoint was inaccessible. The earlier WG attribution came from conflating neighboring search-result snippets; it is not evidence of a WG version. The arXiv full text remains the inspected source for its theorems.
- [Cycles in Unions of Transitive Tournaments](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.WG.2026.3): The search also located Alecu, Bureo Villafana and Lozin, Cycles in Unions of Transitive Tournaments, WG 2026. Its abstract concerns deleting transitive bitournaments to destroy cycles, rather than choosing pairwise reversals. Only the abstract and metadata were inspected; whether its proofs help the present route is not established.

Fixed from board record `website/questions/lettericity.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
