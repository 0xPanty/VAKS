---
record_kind: sandbox_markdown_validation_search_sidecar_contract
slice_id: 2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox
status: pass_product_grade
truth_boundary: sandbox_contract_only
---

# Markdown Validation/Search Sidecar Contract

## Purpose

This sandbox proves a narrow contract:

```text
copied Markdown subset
-> no-update frontmatter validation
-> deterministic JSON lint output
-> derived local search cache
-> bucket-labeled activation/search hits
-> VAKS validators remain separate
```

The sidecar validates and finds. VAKS reviews, supports, and decides.

## Input Format

```json
{
  "record_kind": "markdown_validation_search_sidecar_manifest",
  "scenario_id": "example",
  "expected_valid": true,
  "expected_codes": [],
  "scope": {},
  "runtime": {},
  "validation": {},
  "config_contract": {},
  "search_cache": {},
  "search": {},
  "vaks_validators": {},
  "boundary": {}
}
```

Failure-case manifests may use the sandbox-only test shorthand:

```json
{
  "extends": "fixtures/valid-frontmatter-validation-check.json",
  "scenario_id": "example-failure",
  "expected_valid": false,
  "expected_codes": ["MS_EXAMPLE"],
  "patch": {}
}
```

`extends` / `patch` is verifier scaffolding only. It is not a product contract
for real sidecar use.

Missing-block failure cases may use the sandbox-only patch sentinel:

```json
{ "boundary": { "__delete__": true } }
```

The sentinel is test scaffolding only.

## Required Boundaries

- The sandbox must use copied fixtures only, not the real vault.
- All manifest paths must resolve inside this slice sandbox and, for inputs,
  config contracts, cache paths, and hit refs, inside copied `fixtures/`
  territory.
- Copied Markdown inputs, search hit refs, config contracts, and cache manifest
  refs must exist and be readable.
- `cache_path` may be symbolic when it uses `cache_path_kind:
  symbolic_derived_cache` and a `symbolic:` prefix. Symbolic cache paths do not
  assert that a `.mdvs/` directory was created; they must be paired with a
  readable `cache_manifest_path` fixture.
- The sandbox must not install dependencies, start real mdvs/runtime processes,
  expose MCP write tools, run background indexers, enable watch mode, or install
  hooks.
- Validation must be no-update and deterministic JSON.
- Path-scoped field contracts must be explicit.
- Unknown enum values and forbidden frontmatter fields must fail closed.
- Inferred config requires manual review and cannot govern VAKS schema.
- Search caches are derived, rebuildable, uncommitted, and not truth databases.
- Search uses bucket filtering before relevance/rank fusion.
- Search hits must carry fixture ref, authority bucket, pack role, and
  selected_by trace.
- Search hits must belong to included buckets and must not belong to excluded
  buckets.
- Search rank/score is activation metadata only.
- Only `reviewed_support` hits may use `pack_role: support`; raw/source/stable,
  candidate, overlay, feedback, runtime, and review-input hits cannot be support.
- VAKS validators still run separately.

## Blocking Codes

| Code | Meaning |
|---|---|
| `MS_INVALID_RECORD_KIND` | Wrong manifest kind. |
| `MS_MISSING_SCENARIO_ID` | Scenario id missing. |
| `MS_AUTHORITY_CLAIM_FORBIDDEN` | Claim or direct field asserts support/truth/review/action/promotion/schema authority. |
| `MS_AUTHORITY_CONFUSION` | Boolean field asserts support/truth/action/promotion/mainline authority. |
| `MS_MISSING_SCOPE` | Scope block missing. |
| `MS_REAL_VAULT_SCAN_FORBIDDEN` | Real vault scan/read requested. |
| `MS_SOURCE_MUTATION_FORBIDDEN` | Source mutation requested. |
| `MS_INPUT_PATHS_MISSING` | Copied fixture input paths missing. |
| `MS_PROTECTED_PATH_TARGET` | Input/cache/config path points to protected territory. |
| `MS_PATH_OUTSIDE_SANDBOX` | Manifest path resolves outside this slice sandbox. |
| `MS_PATH_OUTSIDE_FIXTURES` | Manifest path is inside the sandbox but outside copied fixture/cache territory. |
| `MS_FIXTURE_PATH_MISSING` | Referenced copied fixture file does not exist. |
| `MS_FIXTURE_PATH_UNREADABLE` | Referenced copied fixture file cannot be read. |
| `MS_RUNTIME_SHAPE_INVALID` | Runtime block is present but not an object. |
| `MS_DEPENDENCY_INSTALL_FORBIDDEN` | Dependency installation requested. |
| `MS_REAL_RUNTIME_FORBIDDEN` | Real mdvs/runtime execution requested. |
| `MS_BACKGROUND_INDEXER_FORBIDDEN` | Background indexer, watch mode, service, or hook requested. |
| `MS_MCP_WRITE_TOOL_FORBIDDEN` | MCP write tool or write-capable sidecar requested. |
| `MS_MISSING_VALIDATION` | Validation block missing. |
| `MS_VALIDATION_MODE_INVALID` | Validation mode is not check. |
| `MS_NO_UPDATE_REQUIRED` | Auto-update or update-capable validation requested. |
| `MS_DETERMINISTIC_JSON_REQUIRED` | Deterministic JSON output missing. |
| `MS_PATH_SCOPES_MISSING` | Path-scoped field contracts missing. |
| `MS_ENUM_DRIFT_ALLOWED` | Unknown enum is allowed instead of fail-closed. |
| `MS_FORBIDDEN_FRONTMATTER_ALLOWED` | Forbidden authority fields are allowed. |
| `MS_CHECK_PASS_AS_REVIEW_PASS` | Validation pass is treated as review pass. |
| `MS_FRONTMATTER_AS_SUPPORT` | Valid frontmatter is treated as evidence support. |
| `MS_MISSING_CONFIG` | Config contract block missing. |
| `MS_CONFIG_CONTRACT_MISSING` | Visible config contract path missing. |
| `MS_INFERRED_CONFIG_REVIEW_REQUIRED` | Inferred config lacks manual review gate. |
| `MS_CONFIG_SCHEMA_GOVERNANCE_FORBIDDEN` | mdvs config claims VAKS schema governance. |
| `MS_MISSING_CACHE` | Search cache block missing. |
| `MS_CACHE_NOT_DERIVED` | Search cache is not derived/rebuildable. |
| `MS_CACHE_COMMITTED_AS_TRUTH` | `.mdvs`/search cache is committed or treated as truth DB. |
| `MS_CACHE_MANIFEST_INCOMPLETE` | Cache manifest fields/hash missing. |
| `MS_CACHE_SYMBOLIC_PATH_INVALID` | Symbolic cache path lacks the required `symbolic:` prefix. |
| `MS_CACHE_MISMATCH_USED` | Stale/mismatched cache is used silently. |
| `MS_MISSING_SEARCH` | Search block missing. |
| `MS_SEARCH_MODES_INCOMPLETE` | Semantic/BM25/hybrid modes not declared. |
| `MS_BUCKET_FILTER_NOT_FIRST` | Search ranks before authority bucket filtering. |
| `MS_CROSS_BUCKET_FUSION` | Search fuses relevance across authority buckets. |
| `MS_BUCKETS_MISSING` | Included/excluded buckets missing. |
| `MS_UNKNOWN_BUCKET` | Unknown authority bucket. |
| `MS_HIT_BUCKET_OUT_OF_SCOPE` | Search hit bucket is not included or is explicitly excluded. |
| `MS_SEARCH_RANK_AS_TRUST` | Search rank/score claims trust/confidence. |
| `MS_SEARCH_HITS_MISSING` | Search hits missing. |
| `MS_INVALID_SEARCH_HIT` | Search hit shape invalid. |
| `MS_HIT_REF_MISSING` | Search hit fixture ref missing. |
| `MS_HIT_ROLE_MISSING` | Search hit pack role missing/unknown. |
| `MS_SELECTED_BY_MISSING` | Search hit selected_by trace missing. |
| `MS_ACTION_BASIS_FORBIDDEN` | Sidecar or hit allows action basis. |
| `MS_SEARCH_HIT_AS_SUPPORT` | Non-reviewed search hit is marked support. |
| `MS_MISSING_VAKS_VALIDATORS` | VAKS validator block missing. |
| `MS_REPLACES_VAKS_VALIDATORS` | Sidecar replaces VAKS validators. |
| `MS_MISSING_BOUNDARY` | Boundary block missing. |
| `MS_TRUTH_MUTATION_FORBIDDEN` | Sidecar allows truth mutation. |

## Non-Claims

Passing this sandbox is not reviewed knowledge, evidence support, reviewed
relation, reviewer approval, action basis, schema governance, production search
runtime approval, dependency installation permission, Obsidian sync permission,
mainline readiness, commit permission, or push permission.
