---
record_kind: sandbox_exclusion_contract
slice_id: 2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Runtime Artifact Exclusion Contract

## Purpose

This pilot validates a JSON manifest of retrieval-visible items and verifies
that runtime artifacts are excluded before they can be selected, cited as
support, treated as reviewed knowledge, or used as action basis.

It intentionally uses synthetic manifests rather than scanning the real vault.
That keeps P1-10 sandbox-local and repeatable while proving the exclusion
contract.

## Input Format

Input is one JSON file:

```json
{
  "record_kind": "runtime_artifact_exclusion_manifest",
  "scenario_id": "example",
  "expected_valid": true,
  "expected_codes": [],
  "exclude_runtime_artifacts": true,
  "items": []
}
```

Each item includes:

```json
{
  "id": "item_id",
  "path": "relative/or/stable/path",
  "artifact_kind": "runtime_cache",
  "runtime_artifact": true,
  "seen_by_retrieval": true,
  "selected": false,
  "excluded": true,
  "excluded_reason": "runtime_artifact_excluded",
  "pack_role": "none",
  "authority_bucket": "runtime_artifact"
}
```

## Runtime Artifact Kinds

- `python_cache`
- `bytecode_cache`
- `test_output`
- `suite_output`
- `verifier_output`
- `execution_log`
- `temporary_receipt`
- `generated_receipt`
- `scratch_file`
- `lockfile`
- `runtime_cache`
- `derived_index`
- `temporary_download`
- `transient_state`
- `benchmark_output`

## Durable Non-Runtime Kinds

- `source_record`
- `raw_anchor`
- `reviewed_note`
- `reviewed_summary`
- `decision_record`
- `candidate_note`
- `project_overlay`
- `feedback_record`
- `sandbox_contract`
- `sandbox_verification_doc`
- `fixture`
- `failure_case`
- `source_map`
- `next_step_doc`

These durable kinds may still be sandbox/candidate/process material. They are
not automatically reviewed knowledge or action basis.

## Path-Based Runtime Detection

The pilot also treats paths as runtime when they contain markers such as:

```text
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
.cache
tmp/
temp/
scratch/
run-output
suite-output
verification-output
generated-receipts
runtime-cache
derived-index
```

The path check normalizes `_`, `-`, and spaces for these marker families. For
example, `suite_output.json`, `suite-output.json`, and `suite output.json` are
treated as the same runtime-output family.

or end with runtime suffixes such as:

```text
.pyc
.pyo
.log
.tmp
.lock
.sqlite
.db
```

## Blocking Codes

| Code | Meaning |
|---|---|
| `RA_INVALID_RECORD_KIND` | Manifest record_kind is wrong. |
| `RA_MISSING_SCENARIO_ID` | Manifest lacks scenario_id. |
| `RA_MISSING_RUNTIME_FILTER` | Manifest lacks exclude_runtime_artifacts. |
| `RA_RUNTIME_FILTER_DISABLED` | Runtime filter is false or runtime artifact appears while disabled. |
| `RA_MISSING_ITEMS` | Manifest item list is empty or missing. |
| `RA_INVALID_ITEM` | Item is not a JSON object. |
| `RA_MISSING_ITEM_ID` | Item lacks id. |
| `RA_MISSING_ITEM_PATH` | Item lacks path. |
| `RA_UNKNOWN_ARTIFACT_KIND` | Item kind is not in the runtime/durable registry. |
| `RA_DUPLICATE_ITEM_ID` | Item ids are not unique. |
| `RA_RUNTIME_ARTIFACT_MISLABELED` | Path/kind indicates runtime but runtime_artifact is false. |
| `RA_RUNTIME_ARTIFACT_NOT_EXCLUDED` | Retrieval-visible runtime artifact is not excluded. |
| `RA_RUNTIME_ARTIFACT_BAD_EXCLUSION_REASON` | Runtime artifact exclusion reason is not `runtime_artifact_excluded`. |
| `RA_RUNTIME_ARTIFACT_SELECTED` | Runtime artifact is selected for query context. |
| `RA_RUNTIME_ARTIFACT_AS_SUPPORT` | Runtime artifact is used as support, evidence_support, or support anchor. |
| `RA_RUNTIME_ARTIFACT_ACTION_BASIS` | Runtime artifact is allowed or used as action basis, including action-basis pack roles. |
| `RA_RUNTIME_ARTIFACT_AUTHORITY_BUCKET` | Runtime artifact carries reviewed/raw/support/action authority bucket. |
| `RA_RUNTIME_ARTIFACT_CLAIMS_AUTHORITY` | Runtime artifact claims truth, support, approval, action basis, promotion, or mainline readiness. |

## Output Format

The validator prints JSON with:

- `valid`;
- `issue_codes`;
- item-level issues;
- runtime artifact ids;
- selected item ids;
- excluded runtime artifact ids;
- non-claims.

## Non-Claims

This pilot is not:

- a mainline retrieval filter;
- a production file scanner;
- reviewer approval;
- evidence support;
- reviewed knowledge;
- action basis;
- product acceptance by itself;
- permission to enter the next slice without GPT-5.5 extra-high product
  acceptance.
