---
record_kind: sandbox_misa_runtime_memory_vaks_bridge_contract
slice_id: 2026-06-15-p1-5-16-misa-runtime-memory-vaks-bridge-sandbox
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# MISA Runtime Memory / VAKS Bridge Contract

## Purpose

This sandbox proves a narrow bridge contract:

```text
MISA runtime memory quarantine
-> read-only VAKS context-pack fixture fetch
-> receipt-bound feedback_event / candidate_signal / review_due writeback
-> read-only query/retrieval/use-loop trace
-> VAKS action-readiness block when support is insufficient
```

MISA may remember process context. VAKS remains the layer that decides support,
review status, sufficiency, applicability, and action readiness.

## Input Format

```json
{
  "record_kind": "misa_runtime_memory_vaks_bridge_manifest",
  "scenario_id": "example",
  "expected_valid": true,
  "expected_codes": [],
  "scope": {},
  "runtime_memory": {},
  "context_adapter": {},
  "writeback": {},
  "action_readiness": {},
  "boundary": {}
}
```

Failure-case manifests may use sandbox-only test scaffolding:

```json
{
  "extends": "fixtures/valid-bridge-full-contract.json",
  "scenario_id": "example-failure",
  "expected_valid": false,
  "expected_codes": ["MB_EXAMPLE"],
  "patch": {}
}
```

The `extends` / `patch` syntax and `__delete__` sentinel are fixture-suite
helpers only.

## Required Boundaries

- Use copied fixtures only; do not start real MISA or agentmemory runtimes.
- Do not install dependencies, enable hooks, run background services, expose MCP
  write tools, or sync/export Obsidian.
- Runtime memory must stay quarantined and may contain only session
  observations, preferences, pending work, or tool-result memory.
- Runtime observations need sourceObservationIds-style trace.
- Context-pack access is read-only, bucket-filtered, labeled, and warning-rich.
- Context-pack, runtime-memory, writeback, receipt, and use-loop fixture content
  is parsed and cross-checked; fixture refs cannot be mere readable placeholders.
- Candidate/runtime/feedback context cannot become support.
- `selected_by`, memory rank, retention score, and context relevance are trace
  or activation metadata only.
- Writeback is limited to `feedback_event`, `candidate_signal`, and
  `review_due`, each with an operation receipt.
- Receipt IDs and receipt allowed types must bind writeback records.
- Feedback creates use/scope/review pressure only, not truth mutation.
- Candidate signals are not promotion.
- `review_due` is review pressure, not proof of invalidity.
- Action-facing output must still require VAKS action-readiness checks.
- Read-only query/retrieval/use-loop traces must expose labels, warnings, no
  tool writes, and no action basis.

## Blocking Codes

| Code | Meaning |
|---|---|
| `MB_INVALID_RECORD_KIND` | Wrong manifest kind. |
| `MB_MISSING_SCENARIO_ID` | Scenario id missing. |
| `MB_AUTHORITY_CLAIM_FORBIDDEN` | Claim or direct field asserts truth/support/review/action/promotion/schema authority. |
| `MB_AUTHORITY_CONFUSION` | Boolean authority field asserts forbidden authority. |
| `MB_MISSING_SCOPE` | Scope block missing. |
| `MB_SCOPE_NOT_SANDBOX_ONLY` | Scope is not copied-fixture sandbox-only. |
| `MB_DEPENDENCY_INSTALL_FORBIDDEN` | Dependency or agentmemory install requested. |
| `MB_REAL_RUNTIME_FORBIDDEN` | Real MISA/agentmemory runtime requested. |
| `MB_HOOKS_FORBIDDEN` | Hooks requested. |
| `MB_BACKGROUND_SERVICE_FORBIDDEN` | Background service or sync requested. |
| `MB_MCP_WRITE_TOOL_FORBIDDEN` | MCP write tool requested. |
| `MB_BROAD_MCP_TOOL_FORBIDDEN` | Broad save/delete/export MCP tool requested. |
| `MB_OBSIDIAN_SYNC_FORBIDDEN` | Obsidian sync/export requested. |
| `MB_WRITE_PATH_OUTSIDE_SLICE` | Allowed write path leaves this sandbox slice. |
| `MB_PROTECTED_PATH_TARGET` | Path points at protected territory. |
| `MB_PATH_OUTSIDE_SANDBOX` | Fixture ref leaves this sandbox. |
| `MB_PATH_OUTSIDE_FIXTURES` | Fixture ref is inside sandbox but outside fixtures. |
| `MB_FIXTURE_REF_MISSING` | Fixture ref field missing. |
| `MB_FIXTURE_PATH_MISSING` | Referenced fixture does not exist. |
| `MB_FIXTURE_PATH_UNREADABLE` | Referenced fixture cannot be read. |
| `MB_FIXTURE_JSON_INVALID` | Referenced JSON fixture is invalid. |
| `MB_MISSING_RUNTIME_MEMORY` | Runtime memory block missing. |
| `MB_RUNTIME_MEMORY_NOT_QUARANTINED` | Runtime memory is not quarantined. |
| `MB_MEMORY_TYPES_INVALID` | Allowed memory type registry invalid. |
| `MB_RUNTIME_DIRECT_VAKS_WRITE_FORBIDDEN` | Runtime memory attempts direct VAKS writeback. |
| `MB_RUNTIME_ENTRIES_MISSING` | Runtime entries missing. |
| `MB_RUNTIME_ENTRY_INVALID` | Runtime entry shape invalid. |
| `MB_MEMORY_TYPE_INVALID` | Runtime memory entry type forbidden. |
| `MB_MEMORY_TYPE_NOT_ALLOWED_BY_MANIFEST` | Runtime memory entry type outside manifest allowlist. |
| `MB_RUNTIME_FIXTURE_TYPE_MISMATCH` | Runtime fixture type does not match manifest entry. |
| `MB_RUNTIME_FIXTURE_AUTHORITY_CONFUSION` | Runtime fixture asserts VAKS authority. |
| `MB_SOURCE_OBSERVATION_TRACE_MISSING` | Runtime observation lacks sourceObservationIds-style trace. |
| `MB_ACTION_BASIS_FORBIDDEN` | Runtime/context/boundary tries to create action basis. |
| `MB_MISSING_CONTEXT_ADAPTER` | Context adapter block missing. |
| `MB_CONTEXT_MODE_INVALID` | Context adapter mode invalid. |
| `MB_CONTEXT_NOT_READ_ONLY` | Context adapter is not read-only. |
| `MB_BUCKET_FILTER_NOT_FIRST` | Bucket filtering missing before context injection. |
| `MB_CROSS_BUCKET_FUSION` | Cross-authority-bucket fusion requested. |
| `MB_CONTEXT_LABELS_MISSING` | Authority labels or warnings missing. |
| `MB_CONTEXT_PACK_REFS_MISSING` | Context-pack fixture refs missing. |
| `MB_CONTEXT_ITEMS_MISSING` | Context items missing. |
| `MB_CONTEXT_BUCKETS_MISSING` | Included/excluded bucket lists missing. |
| `MB_CONTEXT_ITEM_INVALID` | Context item shape invalid. |
| `MB_CONTEXT_FIXTURE_NOT_READ_ONLY` | Context-pack fixture is not read-only. |
| `MB_CONTEXT_FIXTURE_BUCKET_MISMATCH` | Context-pack fixture buckets exceed manifest scope. |
| `MB_CONTEXT_FIXTURE_ITEM_INVALID` | Context-pack fixture item invalid. |
| `MB_CONTEXT_FIXTURE_SUPPORT_MISUSE` | Context-pack fixture misuses support role. |
| `MB_CONTEXT_FIXTURE_ACTION_BASIS` | Context-pack fixture allows action basis. |
| `MB_UNKNOWN_BUCKET` | Unknown authority bucket. |
| `MB_CONTEXT_BUCKET_OUT_OF_SCOPE` | Context item bucket not allowed. |
| `MB_CONTEXT_ITEM_NOT_IN_PACK` | Manifest context item is not present in referenced context-pack fixture. |
| `MB_CONTEXT_ROLE_MISSING` | Context item role missing or invalid. |
| `MB_CONTEXT_HIT_AS_SUPPORT` | Candidate/runtime/feedback context marked support. |
| `MB_SUPPORT_ANCHOR_MISSING` | Support context lacks independent anchor. |
| `MB_CONTEXT_WARNING_MISSING` | Context item lacks warning code. |
| `MB_SELECTED_BY_MISSING` | Context item lacks selected_by trace. |
| `MB_MISSING_WRITEBACK` | Writeback block missing. |
| `MB_WRITEBACK_TYPES_INVALID` | Allowed writeback types invalid. |
| `MB_DIRECT_MEMORY_WRITEBACK_FORBIDDEN` | memory_save/on_memory_write direct VAKS writeback. |
| `MB_WRITEBACK_RECORDS_MISSING` | Writeback records missing. |
| `MB_WRITEBACK_RECORD_INVALID` | Writeback record shape invalid. |
| `MB_WRITEBACK_TYPE_FORBIDDEN` | Writeback record type is forbidden. |
| `MB_WRITEBACK_TYPE_NOT_ALLOWED_BY_MANIFEST` | Writeback record type outside manifest allowlist. |
| `MB_WRITEBACK_RECEIPT_MISSING` | Writeback record lacks receipt id. |
| `MB_WRITEBACK_FIXTURE_TYPE_MISMATCH` | Writeback fixture kind does not match record type. |
| `MB_RECEIPT_ID_MISSING` | Receipt fixture lacks receipt id. |
| `MB_RECEIPT_WRITES_REVIEWED` | Receipt fixture writes reviewed layer. |
| `MB_RECEIPT_ALLOWED_TYPES_INVALID` | Receipt allowed type registry invalid. |
| `MB_RECEIPT_ID_MISMATCH` | Writeback record receipt id differs from operation receipt. |
| `MB_RECEIPT_TYPE_NOT_ALLOWED` | Operation receipt does not allow this writeback record type. |
| `MB_FEEDBACK_TRUTH_MUTATION` | Feedback mutates truth. |
| `MB_CANDIDATE_SIGNAL_PROMOTION` | Candidate signal promotes knowledge. |
| `MB_REVIEW_DUE_INVALIDATES_TRUTH` | review_due invalidates truth directly. |
| `MB_REVIEWED_WRITE_FORBIDDEN` | Bridge writes reviewed/truth layer. |
| `MB_MISSING_ACTION_READINESS` | Action-readiness block missing. |
| `MB_ACTION_READINESS_CHECK_REQUIRED` | VAKS action-readiness check not required. |
| `MB_SUPPORT_SUFFICIENCY_INVALID` | Invalid support sufficiency value. |
| `MB_ACTION_READY_WITH_INSUFFICIENT_SUPPORT` | Insufficient support still marked action-ready. |
| `MB_RUNTIME_MEMORY_AS_ACTION_BASIS` | Runtime memory used as action basis. |
| `MB_ACTION_BLOCKERS_MISSING` | Blocked action state lacks blockers. |
| `MB_ACTION_RECEIPT_MISMATCH` | Action-readiness receipt differs from writeback operation receipt. |
| `MB_MISSING_USE_LOOP_TRACE` | Use-loop trace block missing. |
| `MB_USE_LOOP_NOT_READ_ONLY` | Use-loop trace is not read-only. |
| `MB_USE_LOOP_WRITES_FORBIDDEN` | Use-loop trace includes tool writes. |
| `MB_USE_LOOP_ACTION_BASIS` | Use-loop trace creates action basis. |
| `MB_USE_LOOP_LABELS_MISSING` | Use-loop trace lacks authority labels or warnings. |
| `MB_MISSING_BOUNDARY` | Boundary block missing. |
| `MB_SUPPORT_CREATION_FORBIDDEN` | Bridge creates evidence support. |

## Non-Claims

Passing this sandbox is not production runtime approval, reviewed knowledge,
evidence support, reviewer approval, action basis, schema governance, promotion,
mainline readiness, commit permission, push permission, or Obsidian sync
permission.
