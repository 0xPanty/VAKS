# Limits

- Local Markdown lexical retrieval only.
- No dense, sparse, graph, rerank, RRF, production runtime, or live LLM/tool runtime.
- No ACL evaluation; fields explicitly record `acl_applied: false` and `acl_status: not_evaluated`.
- Claim plans are deterministic sandbox inputs, not an implemented automatic claim splitter.
- Claim support assessment is non-authoritative and does not create reviewed truth.
- Action readiness, operation preflight, and feedback boundary are not run because R0.5 has no action, operation, or feedback truth update.
- Runs are append-only evidence artifacts; do not overwrite a run to make partial results look greener.
