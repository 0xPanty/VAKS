---
record_kind: sandbox_validator_contract
slice_id: 2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Validator Contract

## Purpose

This pilot validates whether normalized retrieval and operation receipts expose
the P0 boundary facts that later agents need before the P1 read-only query loop.

It intentionally validates compact flat frontmatter receipt instances rather
than implementing a full nested YAML/Markdown parser. This keeps the slice small
and sandbox-local while proving that the key receipt boundaries are
machine-checkable.

## Input Format

Input is one Markdown file with flat YAML-like frontmatter:

```yaml
---
record_kind: retrieval_receipt | operation_receipt
expected_valid: true | false
expected_codes: []
...
---
```

Only Python standard library parsing is used. The pilot accepts simple scalar
values and bracketed one-line lists such as:

```yaml
included_buckets: [reviewed, raw_anchor]
```

## Retrieval Receipt Required Fields

- `record_kind: retrieval_receipt`
- `receipt_id` or `query_id`
- `query_mode`
- `requested_authority_bucket`
- `included_buckets`
- `rrf_scope`
- `selected_item_authority_buckets`
- `selected_item_pack_roles`

## Retrieval Blocking Codes

| Code | Meaning |
|---|---|
| `RV_UNKNOWN_AUTHORITY_BUCKET` | Unknown requested, included, or selected authority bucket. |
| `RV_UNKNOWN_PACK_ROLE` | Unknown selected-item pack role. |
| `RV_CROSS_BUCKET_RRF` | Cross-bucket RRF/rank or non-same-bucket RRF scope. |
| `RV_SELECTED_BY_AS_SUPPORT` | Selected-by trace, retrieval score, or rank treated as support. |
| `RV_GRAPH_RANK_AS_TRUST` | Graph rank treated as trust/support/confidence. |
| `RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT` | Candidate, overlay, source annotation, or feedback item marked support or action basis. |
| `RV_LEGACY_RAW_METADATA_USED` | Legacy raw metadata included in a support-grade receipt. |
| `RV_URL_ONLY_DIRECT_SUPPORT` | URL-only, metadata-only, or summary-only item marked direct support. |
| `RV_MISSING_INDEPENDENT_SUPPORT_ANCHOR` | Claimed support lacks an independent anchor. |
| `RV_RECEIPT_CLAIMS_AUTHORITY` | Retrieval receipt claims truth, support, review approval, action basis, promotion, or mainline readiness. |
| `RV_SUPPORT_BOUNDARY_FLAG_FALSE` | A retrieval boundary flag is explicitly weakened. |

## Operation Receipt Required Fields

- `record_kind: operation_receipt`
- `operation_id` or `receipt_id`
- `actor_tier`
- `operation_mode`
- `actual_write_performed`

## Operation Blocking Codes

| Code | Meaning |
|---|---|
| `OV_UNKNOWN_ACTOR_TIER` | Unknown actor tier. |
| `OV_UNKNOWN_OPERATION_MODE` | Unknown operation mode. |
| `OV_UNKNOWN_TARGET_SCOPE` | Unknown target scope. |
| `OV_ACTOR_TIER_CANNOT_WRITE` | `read_only` or `suggest_only` actor performs a write. |
| `OV_CANDIDATE_WRITE_OUT_OF_SCOPE` | `candidate_write` actor writes outside candidate/sandbox scope. |
| `OV_REVIEWED_WRITE_MISSING_APPROVAL_OR_HASH` | Reviewed, mainline, formal, schema, or protected write lacks approval or checked body hash. |
| `OV_CHECKED_BODY_HASH_MISMATCH` | Checked body hash mismatch invalidates approval for changed body. |
| `OV_SCHEMA_CHANGE_MISSING_OWNER_FINAL` | Schema change lacks owner-final authority. |
| `OV_DESTRUCTIVE_OPERATION_REQUIRES_OWNER_FINAL` | Delete lacks owner-final authority. |
| `OV_ROLLBACK_REQUIRED` | Destructive, schema, reviewed/mainline, or rollback-required operation lacks rollback plan. |
| `OV_MISSING_INTENT_CONFIRMATION` | Significant operation lacks confirmed user intent. |
| `OV_INVALID_ACTION_BASIS` | Candidate, feedback, retrieval, rank, summary, or context material used as action basis. |
| `OV_RECEIPT_CLAIMS_AUTHORITY` | Operation receipt claims truth, review approval, reviewed knowledge, action basis, promotion, or mainline readiness. |
| `OV_OPERATION_BOUNDARY_FLAG_FALSE` | An operation boundary flag is explicitly weakened. |

## Output Format

The validator prints JSON:

```json
{
  "valid": false,
  "issue_codes": ["RV_CROSS_BUCKET_RRF"],
  "authority_non_claims": {
    "validator_pass_not_reviewer_approval": true,
    "receipt_not_evidence_support": true,
    "receipt_not_reviewed_knowledge": true,
    "receipt_not_action_basis": true,
    "sandbox_not_mainline": true
  }
}
```

The suite runner validates all files under `fixtures/` and `failure-cases/`
against their `expected_valid` and `expected_codes` frontmatter.

## Non-Claims

This pilot is not:

- a mainline tool;
- a schema migration;
- a replacement for P0 templates;
- an open enum registry;
- reviewer approval;
- evidence support;
- reviewed knowledge;
- action basis;
- product acceptance by itself;
- permission to enter the next slice without GPT-5.5 extra-high product
  acceptance.
