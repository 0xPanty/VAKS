# Semantic Support Judge A Packet

Please judge only the visible rows in `semantic-support-judge-a.zip`.

Fill only the Judge A columns in the enclosed CSV. This Judge A zip intentionally does not expose Judge B or arbiter fill columns.

Scoring:

- relevance: 0 = not relevant, 1 = partially relevant, 2 = directly relevant.
- sufficiency: 0 = does not support the claim, 1 = weak or partial support, 2 = sufficient support for this read-only answer/use claim.

Boundary:

- This is an excerpt-based semantic support judgment packet.
- It is not a Source Intake P0 pass check.
- It is not a production runtime validation.
- Do not use hidden expected outcomes, case IDs, author-side self-checks, or package mapping files.
- Judge from the visible `query`, `answer_use_claim`, and `anchor_excerpt` only.
- If the excerpt is insufficient or truncated, score 0 or 1 and explain in notes.
- Do not request or use the full Pro review package. `anchor_source_hash` and `frozen_snapshot_ref` are return-side audit fields only.
