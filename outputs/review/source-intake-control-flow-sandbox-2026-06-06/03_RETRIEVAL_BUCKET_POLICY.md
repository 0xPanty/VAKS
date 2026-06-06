---
type: sandbox_retrieval_policy
status: candidate_only
created_at: 2026-06-06
scope: retrieval bucket policy
truth_boundary: candidate retrieval policy only
---

# 03 Retrieval Bucket Policy

## Core Rule

Do not retrieve from one mixed pool.

Use this order:

```text
select mode
-> filter authority bucket
-> run lexical / vector / optional graph inside allowed bucket
-> fuse relevance inside bucket
-> compile pack with status labels
```

## Modes

| Mode | Default buckets | Candidate / overlay use | Action-facing rule |
|---|---|---|---|
| `action_review` | reviewed only; raw anchors for evidence check | review input only | v0.2.13 required |
| `orientation` | reviewed + candidate + confirmed overlay | allowed with provisional label | no action basis |
| `source_inspection` | raw + candidate | backsource / compare / distill | no action basis |
| `project_exploration` | reviewed + candidate + current confirmed overlay | exploratory only | should/must/adopt/reject triggers v0.2.13 |

## RRF / Hybrid Boundary

```text
RRF can fuse lexical + vector + sparse + metadata relevance signals.
RRF cannot fuse authority levels.
Do not use RRF to merge raw, candidate, reviewed, and overlay buckets into one global authority-like ranking.
```

Bad:

```text
raw + candidate + reviewed + overlay -> one ranked list
```

Good:

```text
reviewed bucket:
  BM25 + vector + RRF

candidate bucket:
  BM25 + vector + RRF

overlay bucket:
  project-filtered BM25 + vector + RRF
```

## Pack Labels

Every pack item needs:

```yaml
knowledge_status:
processing_tier:
overlay_state:
review_pressure:
pack_allowed:
action_basis_allowed:
warning_code:
```

Hard boundary:

```text
candidate can orient
candidate cannot support action
overlay can guide project exploration
overlay cannot decide
raw can provide provenance
raw is not support until anchored and warranted
```
