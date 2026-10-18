# Limits

- Replay-only, sandbox-only, read-only.
- No live LLM, live retrieval, DB, network, API, service, or background worker.
- Frozen context packs, drafts, and ClaimSupportMaps are used as replay inputs,
  and replay_inputs.jsonl stores the full input tuples.
- Query-answer relevance and query-context alignment are deterministic
  alignment-id gates across frozen objects, not a learned semantic judge and
  not natural-language relevance validation for unseen live traffic.
- Trace span latency is simulated weighted span latency derived from request
  elapsed time; only the aggregate brake-path timing is measured.
- Stress numbers measure local replay/brake/render logic, not production
  end-to-end latency.
- The positive recommendation is limited to live-shadow wiring. Canary remains
  not evaluated until live-shadow telemetry passes.
- This package grants no reviewed truth, promotion, or action readiness.
