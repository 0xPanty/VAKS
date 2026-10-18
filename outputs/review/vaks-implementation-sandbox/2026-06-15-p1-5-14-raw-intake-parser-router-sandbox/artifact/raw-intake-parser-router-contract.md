---
record_kind: sandbox_raw_intake_parser_router_contract
slice_id: 2026-06-15-p1-5-14-raw-intake-parser-router-sandbox
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Raw Intake Parser Router Contract

## Purpose

This sandbox proves a narrow contract:

```text
messy raw input
-> modality classification
-> lazy parser route
-> retained extraction bundle
-> source card / candidate routing
-> later review only when needed
```

Parser output is raw or candidate material only. It can improve reading,
search, and candidate extraction. It cannot create reviewed knowledge, evidence
support, reviewed relations, action basis, promotion, or mainline readiness.

## Input Format

```json
{
  "record_kind": "raw_intake_parser_router_manifest",
  "scenario_id": "example",
  "expected_valid": true,
  "expected_codes": [],
  "original": {},
  "router": {},
  "parser": {},
  "outputs": {},
  "anchors": {},
  "boundary": {},
  "source_card": {},
  "candidate_distillation": {}
}
```

Failure-case manifests may use the sandbox-only test shorthand:

```json
{
  "extends": "fixtures/valid-document-extraction-bundle.json",
  "scenario_id": "example-failure",
  "expected_valid": false,
  "expected_codes": ["RP_EXAMPLE"],
  "patch": {}
}
```

`extends` / `patch` is verifier scaffolding only. It is not a product contract
for real intake.

## Required Boundaries

- `original.path`, `original.sha256`, and `original.source_type` are required.
- Original and retained output hashes must be SHA256-like.
- Private/account/cookie-based capture requires explicit user authorization.
- Router classification is trace metadata only and must use lazy routing.
- Heavy parsing cannot run by default for ordinary capture.
- Parser config must preserve adapter name, version, runtime, config hash, and
  known limits.
- This sandbox cannot install dependencies or import a full parser runtime as a
  VAKS core dependency.
- GPL/AGPL/unknown parser lineage requires license review before product import.
- Cloud/default/unknown model locality requires review.
- Retained outputs cannot live only in scratch and cannot target protected
  paths.
- Anchors must preserve source-hash linkage.
- Source cards remain raw provenance records.
- Candidate distillation remains provisional candidate orientation.

## Blocking Codes

| Code | Meaning |
|---|---|
| `RP_INVALID_RECORD_KIND` | Wrong manifest kind. |
| `RP_MISSING_SCENARIO_ID` | Scenario id missing. |
| `RP_AUTHORITY_CLAIM_FORBIDDEN` | A claim or direct field asserts support/truth/review/action/mainline authority. |
| `RP_AUTHORITY_CONFUSION` | A boolean field asserts support/truth/action/promotion/mainline authority. |
| `RP_MISSING_ORIGINAL` | Missing original block. |
| `RP_ORIGINAL_PATH_MISSING` | Missing original path. |
| `RP_ORIGINAL_HASH_MISSING` | Missing or invalid original SHA256 hash. |
| `RP_WEAK_HASH` | MD5 used as original/provenance hash. |
| `RP_UNKNOWN_SOURCE_TYPE` | Unknown source type. |
| `RP_PRIVATE_ACCESS_UNAUTHORIZED` | Private/account/cookie capture lacks explicit authorization. |
| `RP_MISSING_ROUTER` | Missing router block. |
| `RP_UNKNOWN_MODALITY` | Unknown router modality. |
| `RP_UNKNOWN_ROUTE` | Unknown parser route. |
| `RP_ROUTE_MODALITY_MISMATCH` | Source type, modality, and route do not align. |
| `RP_LAZY_ROUTING_REQUIRED` | Parser routing is not lazy. |
| `RP_HEAVY_PARSER_ALWAYS_ON` | Heavy parser is always-on for ordinary capture. |
| `RP_SELECTED_ADAPTER_MISSING` | No selected parser adapter. |
| `RP_SELECTED_BY_MISSING` | Route trace metadata is missing. |
| `RP_ROUTER_CONFIDENCE_AS_TRUTH` | Router confidence claims truth. |
| `RP_MISSING_PARSER` | Missing parser block. |
| `RP_PARSER_CONFIG_MISSING` | Missing parser config fields/hash. |
| `RP_DEPENDENCY_INSTALL_FORBIDDEN` | Sandbox requests dependency installation. |
| `RP_RUNTIME_CORE_DEPENDENCY_FORBIDDEN` | Full parser runtime becomes core dependency. |
| `RP_LICENSE_REVIEW_REQUIRED` | Parser license lineage needs review. |
| `RP_MODEL_LOCALITY_UNREVIEWED` | Model locality is unreviewed. |
| `RP_PARSER_CONFIDENCE_AS_TRUTH` | Parser confidence claims truth. |
| `RP_MISSING_OUTPUTS` | Missing outputs block. |
| `RP_RETAINED_OUTPUTS_MISSING` | Retained output bundle is incomplete. |
| `RP_OUTPUT_SCRATCH_ONLY` | Outputs live only in scratch. |
| `RP_OUTPUT_HASH_MISSING` | Retained output lacks SHA256 hash. |
| `RP_OUTPUT_STATUS_NOT_RAW_OR_CANDIDATE` | Parser output claims reviewed status. |
| `RP_PROTECTED_PATH_TARGET` | Output/source-card target points to a protected or scratch path. |
| `RP_MISSING_ANCHORS` | Missing anchors block. |
| `RP_ANCHORS_MISSING` | No source anchors retained. |
| `RP_ANCHOR_HASH_MISSING` | Anchors lack source-hash linkage. |
| `RP_ANCHOR_SELECTOR_MISSING` | Anchor selector missing. |
| `RP_MISSING_BOUNDARY` | Missing boundary block. |
| `RP_OUTPUT_CLAIMS_AUTHORITY` | Boundary claims support/review/promotion/readiness. |
| `RP_ACTION_BASIS_FORBIDDEN` | Raw/candidate parser artifact allows action basis. |
| `RP_TRUTH_MUTATION_FORBIDDEN` | Parser artifact allows truth mutation. |
| `RP_INVALID_SOURCE_CARD` | Source-card shape invalid. |
| `RP_SOURCE_CARD_NOT_RAW` | Source card is not raw provenance. |
| `RP_SOURCE_CARD_AUTHORITY_FIELD` | Source card contains forbidden authority/proxy fields. |
| `RP_INVALID_CANDIDATE_DISTILLATION` | Candidate distillation shape invalid. |
| `RP_CANDIDATE_NOT_CANDIDATE` | Candidate distillation is not candidate. |
| `RP_CANDIDATE_NOT_PROVISIONAL` | Candidate distillation is not provisional. |

## Non-Claims

Passing this sandbox is not reviewed knowledge, evidence support, reviewed
relation, reviewer approval, action basis, production parser runtime approval,
dependency installation permission, Obsidian sync permission, mainline
readiness, commit permission, or push permission.
