---
record_type: friction-log
status: active
created: 2026-06-01
step: 1
scope: single-source-flow
---

# Step 1 Friction Log: Single Source Flow

## Flow Completed

```text
raw source
-> candidate in outputs/review
-> manual review
-> reviewed wiki claim
-> context pack
-> feedback record
```

## Field Pain

| Question | Observation |
|---|---|
| Which field could not be filled without guessing? | `content_hash`, `archived_url`, and `source_changed` were left blank or unknown. Filling them manually would be fake precision. |
| Which gate felt too heavy? | Evidence Packet felt heavy for one abstract-backed point, even though it did clarify the warrant and scope. |
| Where did it get stuck? | Deciding whether `processing_level: heavy` is honest when only the abstract was inspected. The source is important, but source access is not full. |
| Which rule looked good but was hard to execute? | "Heavy source digests should include omission check" is sensible, but for an abstract-only trial the omission check turns into self-conscious caveats. |

## Lazy-Gate Check

The flow did not burden ordinary capture because this was intentionally a promotion/context-pack trial.

But the template pressure was real: once a point enters review, many fields appear even for a tiny claim.

## Pain Classification

- Too heavy: Evidence Packet for a narrow single-source claim.
- Missing: No clean field for "abstract-only, intentionally scoped" in the Source record.
- Ambiguous: Difference between `processing_level` and `source_access`.
- Not stuck: The main spine itself was followable.

