---
record_kind: sandbox_iteration_decision
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B Skeleton vs v1.1 Decision

## Decision

Keep the minimal read-only adapter skeleton as the next sandbox candidate.

Do not promote it to mainline yet.

## What Changed

The previous version, `vaks_b_adapter_v1_1`, was still mainly a pressure-test
mode inside the harness.

This step adds a minimal real adapter skeleton:

```text
read-only VAKS Markdown/YAML
-> chunk manifest JSONL
-> adapter result object
-> bucket-local retrieval receipt
-> same pressure tests
```

The skeleton reuses the v1.1 ranking policy. The improvement is structural:
it now emits the adapter-shaped objects VAKS would need before a real
implementation can exist.

## Structural Artifacts

Generated manifest artifacts:

```text
primary chunk manifest: 3947 chunks
full chunk manifest:    18708 chunks
```

Generated receipt artifacts:

```text
main primary receipts:   30 queries, 300 results
main full receipts:      30 queries, 300 results
holdout primary receipts: 15 queries, 150 results
holdout full receipts:    15 queries, 150 results
```

Field validation passed on manifest and receipt samples. Required fields include:

```text
vaks_record_id
vault_path
heading_or_anchor
selector_or_line_range
source_hash
chunk_hash
record_kind
knowledge_status
review_state
relation_state
retrieval_policy
authority_badge
usage_badge
temporal_badge
warning_code
retrieval_reasons
source_clickback
indexed_at
retrieval_receipt
```

## Main Pressure Set

Skeleton tied v1.1 without regression:

| Corpus | Metric | v1.1 | skeleton | Result |
|---|---|---:|---:|---|
| primary | hit@5 | 30/30 | 30/30 | same |
| primary | hit@10 | 30/30 | 30/30 | same |
| primary | MRR | 1.0000 | 1.0000 | same |
| primary | action leakage | 0.0000 | 0.0000 | same |
| primary | forbidden top1 | 0.0000 | 0.0000 | same |
| primary | cross-bucket violation | 0.0000 | 0.0000 | same |
| full | hit@5 | 30/30 | 30/30 | same |
| full | hit@10 | 30/30 | 30/30 | same |
| full | MRR | 1.0000 | 1.0000 | same |
| full | action leakage | 0.0000 | 0.0000 | same |
| full | forbidden top1 | 0.0000 | 0.0000 | same |
| full | cross-bucket violation | 0.0000 | 0.0000 | same |

## Holdout Pressure Set

Skeleton tied v1.1 without regression:

| Corpus | Metric | v1.1 | skeleton | Result |
|---|---|---:|---:|---|
| primary | hit@5 | 12/15 | 12/15 | same |
| primary | hit@10 | 13/15 | 13/15 | same |
| primary | MRR | 0.7811 | 0.7811 | same |
| primary | action leakage | 0.0000 | 0.0000 | same |
| full | hit@5 | 13/15 | 13/15 | same |
| full | hit@10 | 13/15 | 13/15 | same |
| full | MRR | 0.7591 | 0.7591 | same |
| full | action leakage | 0.0000 | 0.0000 | same |

Query-level regressions:

```text
main pressure: 0
holdout:       0
```

## Boundary

This decision supports:

```text
continue Phase B sandbox from the read-only adapter skeleton
```

It does not approve:

```text
mainline adoption
C-lite
Skills
MCP writes
subagents
formal writeback
production readiness
```

## Next Step

Next step should be a small adapter contract test:

```text
validate manifest completeness
validate receipt completeness
validate bucket-local policy fields
validate no action-basis permission leaks
validate click-back targets resolve to existing files
```

It may continue only if it ties or beats the skeleton metrics and the contract
test passes.
