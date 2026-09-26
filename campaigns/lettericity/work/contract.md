# Prepared contract

Source: `{"num_vars":n,"clauses":[[signed_literal,...],...]}` with at most three literals per clause. Output a satisfying Boolean `{"assignment":[...]}` or `{"status":"NO-SOLUTION"}`.

Target: `{"vertices":n,"edges":[[u,v],...],"letters":k}` for a simple undirected graph, each edge ordered `u<v`, and alphabet budget `k>=0`. Output `{"order":[vertex,...],"labels":[letter_by_vertex,...],"decoder":[[bool,...],...]}`. The order is a permutation of vertices; labels are in `0..k-1`; the decoder is a directed `k` by `k` Boolean table. For each earlier/later pair, adjacency equals the decoder entry for its ordered labels. `NO-SOLUTION` is valid iff no such representation exists.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.
