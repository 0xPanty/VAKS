---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p2-18-bases-cockpit-prototype
status: implemented_pending_review
truth_boundary: sandbox_oracle_only
---

# Failure Case Oracle

| Failure case | Primary expected code |
|---|---|
| `base-missing.json` | `BC_REQUIRED_BASE_MISSING` |
| `base-missing-key-column.json` | `BC_BASE_KEY_COLUMNS_MISSING` |
| `review-candidates-approves.json` | `BC_BASE_APPROVES_FORBIDDEN` |
| `context-packs-infer-ready.json` | `BC_READY_INFERENCE_FORBIDDEN` |
| `feedback-mutates-truth.json` | `BC_TRUTH_MUTATION_FORBIDDEN` |
| `operator-replaces-validators.json` | `BC_REPLACES_VALIDATORS_FORBIDDEN` |
| `reviewed-write-enabled.json` | `BC_REVIEWED_WRITE_FORBIDDEN` |
| `promotion-enabled.json` | `BC_PROMOTION_FORBIDDEN` |
| `action-basis-enabled.json` | `BC_ACTION_BASIS_FORBIDDEN` |
| `operator-missing-status-flag.json` | `BC_OPERATOR_STATES_INCOMPLETE` |
| `dirty-state-judges-knowledge.json` | `BC_DIRTY_STATE_AS_KNOWLEDGE` |
| `hash-match-as-support.json` | `BC_HASH_AS_SUPPORT` |
| `activity-as-confidence.json` | `BC_ACTIVITY_AS_CONFIDENCE` |
| `navigation-creates-authority.json` | `BC_NAVIGATION_AUTHORITY_FORBIDDEN` |
| `navigation-reviewed-write.json` | `BC_NAVIGATION_REVIEWED_WRITE_FORBIDDEN` |
| `navigation-target-missing.json` | `BC_NAVIGATION_TARGET_MISSING` |
| `source-artifact-links-missing.json` | `BC_SOURCE_ARTIFACT_LINKS_MISSING` |
| `non-claims-missing.json` | `BC_NON_CLAIMS_MISSING` |
| `prototype-boundary-invalid.json` | `BC_PROTOTYPE_BOUNDARY_INVALID` |
| `real-base-file-created.json` | `BC_RUNTIME_OR_SYNC_FORBIDDEN` |
| `obsidian-sync-enabled.json` | `BC_RUNTIME_OR_SYNC_FORBIDDEN` |
| `runtime-started.json` | `BC_RUNTIME_OR_SYNC_FORBIDDEN` |
| `mcp-write-tool.json` | `BC_RUNTIME_OR_SYNC_FORBIDDEN` |
| `background-service.json` | `BC_RUNTIME_OR_SYNC_FORBIDDEN` |
| `dependency-install.json` | `BC_RUNTIME_OR_SYNC_FORBIDDEN` |
| `commit-or-push.json` | `BC_RUNTIME_OR_SYNC_FORBIDDEN` |
| `write-path-outside-slice.json` | `BC_WRITE_PATH_OUTSIDE_SLICE` |
| `protected-path-base.json` | `BC_PROTECTED_PATH_TARGET` |
| `obsidian-case-protected-path.json` | `BC_PROTECTED_PATH_TARGET` |

Expected failures are sandbox validation results only. Passing this suite does
not approve real Bases files, production UI, reviewed knowledge, evidence
support, action basis, promotion, sync, commit, push, or mainline merge.
