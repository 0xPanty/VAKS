---
record_kind: sandbox_semantic_anchor_contract
slice_id: 2026-06-15-p1-11-semantic-anchor-support-check-sandbox
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Semantic Anchor Support Contract

## Purpose

This sandbox proves a narrow check:

```text
semantic/vector/graph retrieval may route inspection,
but it cannot become evidence support until it resolves to a stable source anchor.
```

It validates synthetic JSON manifests. It does not scan the real vault, modify
any reviewed notes, or create production validators.

## Input Format

Input is one JSON file:

```json
{
  "record_kind": "semantic_anchor_support_manifest",
  "scenario_id": "example",
  "expected_valid": true,
  "expected_codes": [],
  "anchors": []
}
```

Each anchor is an object:

```json
{
  "id": "anchor-1",
  "anchor_kind": "raw_excerpt",
  "support_claimed": true,
  "support_role": "direct_support",
  "source_ref": "raw/articles/example-source.md",
  "selector": "L10-L18",
  "authority_bucket": "raw_anchor",
  "selected_by_semantic": true
}
```

## Stable Support Anchors

Allowed as support when `source_ref`, a stable selector/range/hash, and a
support authority bucket are present:

- `raw_excerpt`
- `raw_snapshot_path`
- `code_line_range`
- `transcript_segment`
- `section_fragment`
- `quote_selector`
- `table_or_code_anchor`
- `hash_anchor`
- `stored_artifact_path`
- `stable_url_with_capture_date`
- `reviewed_support_ref`

`stable_url_with_capture_date` still needs a captured date plus a selector,
fragment, or hash. URL-only provenance is not final support.

## Orientation-Only Anchors

These may help a reviewer know what to inspect next, but cannot be final
support:

- `semantic_vector_hit`
- `embedding_neighborhood`
- `reranker_score`
- `graph_neighbor`
- `graph_relation`
- `association_neighbor`
- `community_summary`
- `retrieval_result`
- `llm_summary`
- `briefing_summary`
- `source_summary`
- `candidate_distillation`
- `project_overlay`
- `feedback_event`
- `url_only`
- `metadata_only`
- `runtime_artifact`
- `generated_receipt`
- `cache_entry`
- `suite_output`

## Authority Buckets

Support anchors must use one of:

- `raw_anchor`
- `source_anchor`
- `stable_anchor`
- `reviewed_support`

Candidate, feedback, runtime, generic reviewed, action, and project-overlay
buckets are blocked for support in this sandbox.

## Runtime Artifact Reuse

The check imports P1-10's runtime artifact detector and uses it for anchor paths
and artifact kinds. Runtime artifacts are blocked even if the semantic layer
selected them.

## Blocking Codes

| Code | Meaning |
|---|---|
| `SA_INVALID_RECORD_KIND` | Manifest record_kind is wrong. |
| `SA_MISSING_SCENARIO_ID` | Manifest lacks scenario_id. |
| `SA_MISSING_ANCHORS` | Manifest lacks a non-empty anchors list. |
| `SA_INVALID_ANCHOR` | Anchor entry is not an object. |
| `SA_MISSING_ANCHOR_ID` | Anchor lacks id. |
| `SA_DUPLICATE_ANCHOR_ID` | Anchor ids are not unique. |
| `SA_UNKNOWN_ANCHOR_KIND` | Anchor kind is not registered. |
| `SA_SUPPORT_ROLE_INVALID` | Support claim lacks direct or inferential role. |
| `SA_INFERENTIAL_SUPPORT_MISSING_REVIEWER_NOTE` | Inferential support lacks reviewer note. |
| `SA_SUPPORT_REQUIRES_STABLE_ANCHOR` | Support claim does not resolve to stable anchor kind and selector. |
| `SA_MISSING_SOURCE_REF` | Support claim lacks source_ref. |
| `SA_MISSING_SELECTOR` | Support claim lacks selector, line range, segment, timestamp, hash, or commit. |
| `SA_URL_ONLY_SUPPORT` | URL-only or metadata-only provenance is counted as support. |
| `SA_SEMANTIC_SCORE_AS_SUPPORT` | Semantic score, rank, or selected_by claims support. |
| `SA_GRAPH_RANK_AS_SUPPORT` | Graph rank, relation, or association score claims support. |
| `SA_CANDIDATE_AS_SUPPORT` | Candidate distillation or project overlay is used as support. |
| `SA_FEEDBACK_AS_SUPPORT` | Feedback is used as support. |
| `SA_SUMMARY_AS_SUPPORT` | Summary/community report is used as support. |
| `SA_RUNTIME_ARTIFACT_ANCHOR` | Anchor points to runtime output, cache, log, generated receipt, or suite output. |
| `SA_RUNTIME_ARTIFACT_AS_SUPPORT` | Runtime artifact is used as support. |
| `SA_AUTHORITY_BUCKET_INVALID_FOR_SUPPORT` | Authority bucket is not a support bucket. |
| `SA_ANCHOR_CLAIMS_REVIEWED_KNOWLEDGE` | Anchor claims truth, review approval, promotion, or reviewed knowledge. |
| `SA_ANCHOR_CLAIMS_ACTION_BASIS` | Anchor claims or permits action basis. |
| `SA_SELF_SUPPORT_LOOP` | Target cites itself, claim note, candidate note, or summary note as support. |

## Output Format

The validator prints JSON with:

- `valid`;
- `issue_codes`;
- anchor-level results;
- non-claims.

## Non-Claims

This sandbox is not:

- evidence support;
- reviewer approval;
- reviewed knowledge;
- action basis;
- mainline readiness;
- a production validator;
- permission to enter the next slice without GPT-5.5 extra-high Product
  Acceptance.
