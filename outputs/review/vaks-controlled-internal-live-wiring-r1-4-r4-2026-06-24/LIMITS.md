# Limits

- Sandbox-only and read-only.
- No writes to formal Obsidian, wiki, raw sources, Truth Core, DB, API, service,
  network, live LLM, or live retrieval.
- Obsidian testing is represented as a write-policy probe. Blocked paths are not
  written.
- Output bundles may only be written under `outputs/review/` with the controlled
  R1.4 r4 prefix.
- Policy fields are read from `trusted_runtime_context` only. User payload
  policy fields are rejected, and top-level request fields are audit copies.
- The user query hash must match trusted context, case query, draft query, and
  alignment contract.
- Source authority is canonical-path checked. `outputs/review` artifacts,
  `raw/../...` traversal, and percent-encoded path ambiguity cannot self-declare
  as raw source evidence.
- ReleaseSink recomputes `sha256(final_text)` and will not release a final answer
  whose declared `final_sha256` does not match the actual text.
- This can support a supervised internal low-risk enforce trial, not Canary or
  production full enforce.
- Guard failure, parsing failure, empty retrieval, feature-flag error, ACL deny,
  or pre-Guard streaming attempts must fail closed.
