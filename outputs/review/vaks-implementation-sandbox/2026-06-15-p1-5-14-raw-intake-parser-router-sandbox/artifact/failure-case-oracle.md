---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-5-14-raw-intake-parser-router-sandbox
status: implemented_pending_review
truth_boundary: sandbox_oracle_only
---

# Failure Case Oracle

| Failure case | Primary expected code |
|---|---|
| `missing-original-hash.json` | `RP_ORIGINAL_HASH_MISSING` |
| `weak-md5-original-hash.json` | `RP_WEAK_HASH` |
| `unknown-source-type.json` | `RP_UNKNOWN_SOURCE_TYPE` |
| `route-modality-mismatch.json` | `RP_ROUTE_MODALITY_MISMATCH` |
| `lazy-routing-missing.json` | `RP_LAZY_ROUTING_REQUIRED` |
| `heavy-parser-always-on.json` | `RP_HEAVY_PARSER_ALWAYS_ON` |
| `router-confidence-as-truth.json` | `RP_ROUTER_CONFIDENCE_AS_TRUTH` |
| `router-truth-confidence-direct-field.json` | `RP_AUTHORITY_CLAIM_FORBIDDEN` |
| `parser-config-hash-missing.json` | `RP_PARSER_CONFIG_MISSING` |
| `dependency-install-requested.json` | `RP_DEPENDENCY_INSTALL_FORBIDDEN` |
| `full-runtime-core-dependency.json` | `RP_RUNTIME_CORE_DEPENDENCY_FORBIDDEN` |
| `gpl-license-unreviewed.json` | `RP_LICENSE_REVIEW_REQUIRED` |
| `cloud-model-locality-unreviewed.json` | `RP_MODEL_LOCALITY_UNREVIEWED` |
| `parser-confidence-as-truth.json` | `RP_PARSER_CONFIDENCE_AS_TRUTH` |
| `parser-truth-confidence-direct-field.json` | `RP_AUTHORITY_CLAIM_FORBIDDEN` |
| `retained-outputs-missing.json` | `RP_RETAINED_OUTPUTS_MISSING` |
| `retained-output-hash-missing.json` | `RP_OUTPUT_HASH_MISSING` |
| `retained-output-direct-authority-field.json` | `RP_AUTHORITY_CLAIM_FORBIDDEN` |
| `scratch-only-output.json` | `RP_OUTPUT_SCRATCH_ONLY` |
| `protected-output-path.json` | `RP_PROTECTED_PATH_TARGET` |
| `obsidian-vault-output-path.json` | `RP_PROTECTED_PATH_TARGET` |
| `anchors-missing.json` | `RP_ANCHORS_MISSING` |
| `anchor-source-hash-missing.json` | `RP_ANCHOR_HASH_MISSING` |
| `anchor-direct-evidence-support.json` | `RP_AUTHORITY_CLAIM_FORBIDDEN` |
| `parser-output-reviewed-status.json` | `RP_OUTPUT_STATUS_NOT_RAW_OR_CANDIDATE` |
| `parser-markdown-reviewed-knowledge.json` | `RP_AUTHORITY_CLAIM_FORBIDDEN` |
| `action-basis-allowed.json` | `RP_ACTION_BASIS_FORBIDDEN` |
| `truth-mutation-allowed.json` | `RP_TRUTH_MUTATION_FORBIDDEN` |
| `promotion-direct-authority-field.json` | `RP_AUTHORITY_CLAIM_FORBIDDEN` |
| `private-web-no-auth.json` | `RP_PRIVATE_ACCESS_UNAUTHORIZED` |
| `account-cookies-used.json` | `RP_PRIVATE_ACCESS_UNAUTHORIZED` |
| `source-card-reviewed.json` | `RP_SOURCE_CARD_NOT_RAW` |
| `source-card-relations-top-level.json` | `RP_SOURCE_CARD_AUTHORITY_FIELD` |
| `source-card-protected-target.json` | `RP_PROTECTED_PATH_TARGET` |
| `source-card-direct-evidence-support.json` | `RP_AUTHORITY_CLAIM_FORBIDDEN` |
| `candidate-not-provisional.json` | `RP_CANDIDATE_NOT_PROVISIONAL` |
| `candidate-direct-reviewed-knowledge.json` | `RP_AUTHORITY_CLAIM_FORBIDDEN` |

Expected failures are sandbox validation results only. Passing this suite does
not approve real parser execution, dependency installation, Obsidian sync,
reviewed knowledge, evidence support, action basis, commit, push, or mainline
merge.
