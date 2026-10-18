---
record_kind: sandbox_scenario_contract
slice_id: 2026-06-15-p1-09-read-only-query-loop-pilot-sandbox
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Scenario Contract

## Purpose

This pilot validates a read-only query loop as a boundary-preserving state
machine. It does not implement real vault retrieval, real feedback writes,
mainline operations, or Obsidian integration.

Each scenario fixture describes one query loop story. The runner generates a
retrieval receipt and, when needed, an operation receipt, then validates those
receipts with the P1-08 sandbox receipt validator.

## Input Format

Input is one Markdown file with flat YAML-like frontmatter:

```yaml
---
record_kind: read_only_query_scenario
scenario_id:
story_kind: ordinary_orientation | action_adjacent | candidate_temptation | stale_decision | feedback_correction | agent_propose_write
expected_valid: true | false
expected_outcome:
expected_codes: []
...
---
```

Only simple scalar values and one-line bracketed lists are supported.

## Positive Outcomes

| Outcome | Meaning |
|---|---|
| `orientation_answer` | Ordinary question receives orientation without full audit. |
| `action_gated_answer` | Action-adjacent answer exposes required gates but does not claim action basis. |
| `candidate_blocked_as_support` | Candidate material is useful but blocked as support/action basis. |
| `historical_only_ready_action_blocked` | Stale decision can explain history while ready action is blocked. |
| `review_due_envelope_truth_unchanged` | Feedback correction emits a sandbox review_due envelope and truth remains unchanged. |
| `proposal_only_with_operation_receipt` | Agent propose-write emits a valid operation receipt and performs no write. |

## Query Loop Blocking Codes

| Code | Meaning |
|---|---|
| `QL_UNKNOWN_STORY_KIND` | Scenario uses an unknown pilot story. |
| `QL_FORBIDDEN_SIDE_EFFECT` | Read-only loop attempts commit, push, sync, write, hook, background service, or similar side effect. |
| `QL_READ_ONLY_ACTION_BASIS_CLAIM` | Read-only loop claims ready action basis. |
| `QL_ORDINARY_QUERY_OVERSTRICT` | Ordinary orientation question is forced through full audit. |
| `QL_ACTION_ADJACENT_MISSING_GATE` | Action-adjacent query lacks context pack, support check, or action readiness check. |
| `QL_CANDIDATE_USED_AS_SUPPORT` | Candidate material is used as support/action basis. |
| `QL_CANDIDATE_WARNING_MISSING` | Candidate temptation lacks visible boundary warning. |
| `QL_STALE_DECISION_READY_ACTION` | Stale decision is used for ready action. |
| `QL_STALE_WARNING_MISSING` | Stale/superseded warning is missing. |
| `QL_FEEDBACK_MUTATES_TRUTH` | Feedback correction mutates truth confidence or reviewed notes. |
| `QL_FEEDBACK_REVIEW_DUE_MISSING` | Explicit correction fails to emit review_due pressure. |
| `QL_OPERATION_RECEIPT_REQUIRED` | Agent propose-write or any operation-receipt-required scenario lacks operation receipt. |
| `QL_AGENT_PROPOSE_WRITE_PERFORMED_WRITE` | Proposal-only story performs a write. |
| `QL_RETRIEVAL_RECEIPT_INVALID` | Generated retrieval receipt fails P1-08 receipt validation. |
| `QL_OPERATION_RECEIPT_INVALID` | Generated operation receipt fails P1-08 receipt validation. |

P1-08 receipt issue codes such as `RV_CROSS_BUCKET_RRF` or
`OV_RECEIPT_CLAIMS_AUTHORITY` are surfaced alongside query-loop codes.

## Output Format

The runner prints JSON containing:

- scenario id and story kind;
- `valid`;
- `outcome`;
- top-level issue codes;
- generated retrieval receipt and receipt validator result;
- generated operation receipt and receipt validator result when applicable;
- explicit non-claims.

## Non-Claims

This pilot is not:

- a mainline query tool;
- a real retrieval engine;
- a feedback writer;
- reviewer approval;
- evidence support;
- reviewed knowledge;
- action basis;
- product acceptance by itself;
- permission to enter the next slice without GPT-5.5 extra-high product
  acceptance.
