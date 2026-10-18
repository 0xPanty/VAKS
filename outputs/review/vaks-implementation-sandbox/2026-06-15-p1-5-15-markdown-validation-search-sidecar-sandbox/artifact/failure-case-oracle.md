---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox
status: pass_product_grade
truth_boundary: sandbox_oracle_only
---

# Failure Case Oracle

| Failure case | Primary expected code |
|---|---|
| `absolute-wiki-claims-input-path.json` | `MS_PROTECTED_PATH_TARGET` |
| `real-vault-scan-requested.json` | `MS_REAL_VAULT_SCAN_FORBIDDEN` |
| `source-mutation-requested.json` | `MS_SOURCE_MUTATION_FORBIDDEN` |
| `protected-input-path.json` | `MS_PROTECTED_PATH_TARGET` |
| `raw-input-path-not-fixture.json` | `MS_PATH_OUTSIDE_SANDBOX` |
| `config-path-outside-sandbox.json` | `MS_PATH_OUTSIDE_SANDBOX` |
| `cache-path-outside-sandbox.json` | `MS_PATH_OUTSIDE_SANDBOX` |
| `config-path-inside-sandbox-outside-fixtures.json` | `MS_PATH_OUTSIDE_FIXTURES` |
| `missing-copied-input-fixture.json` | `MS_FIXTURE_PATH_MISSING` |
| `missing-config-fixture.json` | `MS_FIXTURE_PATH_MISSING` |
| `missing-hit-ref-fixture.json` | `MS_FIXTURE_PATH_MISSING` |
| `missing-cache-manifest-fixture.json` | `MS_FIXTURE_PATH_MISSING` |
| `dependency-install-requested.json` | `MS_DEPENDENCY_INSTALL_FORBIDDEN` |
| `background-indexer-enabled.json` | `MS_BACKGROUND_INDEXER_FORBIDDEN` |
| `real-runtime-started.json` | `MS_REAL_RUNTIME_FORBIDDEN` |
| `mcp-write-tool-exposed.json` | `MS_MCP_WRITE_TOOL_FORBIDDEN` |
| `protected-config-path.json` | `MS_PROTECTED_PATH_TARGET` |
| `missing-scope-block.json` | `MS_MISSING_SCOPE` |
| `missing-validation-block.json` | `MS_MISSING_VALIDATION` |
| `missing-config-contract-block.json` | `MS_MISSING_CONFIG` |
| `missing-search-cache-block.json` | `MS_MISSING_CACHE` |
| `missing-search-block.json` | `MS_MISSING_SEARCH` |
| `missing-vaks-validators-block.json` | `MS_MISSING_VAKS_VALIDATORS` |
| `missing-boundary-block.json` | `MS_MISSING_BOUNDARY` |
| `auto-update-enabled.json` | `MS_NO_UPDATE_REQUIRED` |
| `non-deterministic-output.json` | `MS_DETERMINISTIC_JSON_REQUIRED` |
| `path-scopes-missing.json` | `MS_PATH_SCOPES_MISSING` |
| `unknown-enum-allowed.json` | `MS_ENUM_DRIFT_ALLOWED` |
| `forbidden-frontmatter-allowed.json` | `MS_FORBIDDEN_FRONTMATTER_ALLOWED` |
| `frontmatter-authority-field-allowed.json` | `MS_FORBIDDEN_FRONTMATTER_ALLOWED` |
| `check-pass-as-review-pass.json` | `MS_CHECK_PASS_AS_REVIEW_PASS` |
| `valid-frontmatter-as-support.json` | `MS_FRONTMATTER_AS_SUPPORT` |
| `health-lint-claims-review-pass.json` | `MS_AUTHORITY_CONFUSION` |
| `inferred-config-no-review.json` | `MS_INFERRED_CONFIG_REVIEW_REQUIRED` |
| `config-schema-governance.json` | `MS_CONFIG_SCHEMA_GOVERNANCE_FORBIDDEN` |
| `cache-not-derived.json` | `MS_CACHE_NOT_DERIVED` |
| `committed-cache-truth-db.json` | `MS_CACHE_COMMITTED_AS_TRUTH` |
| `cache-manifest-incomplete.json` | `MS_CACHE_MANIFEST_INCOMPLETE` |
| `cache-symbolic-path-invalid.json` | `MS_CACHE_SYMBOLIC_PATH_INVALID` |
| `cache-mismatch-used.json` | `MS_CACHE_MISMATCH_USED` |
| `search-modes-incomplete.json` | `MS_SEARCH_MODES_INCOMPLETE` |
| `bucket-filter-missing.json` | `MS_BUCKET_FILTER_NOT_FIRST` |
| `cross-bucket-fusion.json` | `MS_CROSS_BUCKET_FUSION` |
| `search-buckets-missing.json` | `MS_BUCKETS_MISSING` |
| `unknown-bucket.json` | `MS_UNKNOWN_BUCKET` |
| `hit-in-excluded-bucket.json` | `MS_HIT_BUCKET_OUT_OF_SCOPE` |
| `hit-not-in-included-bucket.json` | `MS_HIT_BUCKET_OUT_OF_SCOPE` |
| `hit-ref-missing.json` | `MS_HIT_REF_MISSING` |
| `search-rank-as-trust.json` | `MS_SEARCH_RANK_AS_TRUST` |
| `candidate-hit-as-support.json` | `MS_SEARCH_HIT_AS_SUPPORT` |
| `raw-anchor-hit-as-support.json` | `MS_SEARCH_HIT_AS_SUPPORT` |
| `hit-action-basis.json` | `MS_ACTION_BASIS_FORBIDDEN` |
| `hit-selected-by-missing.json` | `MS_SELECTED_BY_MISSING` |
| `sidecar-replaces-vaks-validators.json` | `MS_REPLACES_VAKS_VALIDATORS` |
| `truth-mutation-allowed.json` | `MS_TRUTH_MUTATION_FORBIDDEN` |
| `direct-evidence-support-field.json` | `MS_AUTHORITY_CLAIM_FORBIDDEN` |
| `direct-is-truth-field.json` | `MS_AUTHORITY_CONFUSION` |
| `direct-promotion-field.json` | `MS_AUTHORITY_CLAIM_FORBIDDEN` |
| `search-hit-direct-action-field.json` | `MS_AUTHORITY_CLAIM_FORBIDDEN` |

Expected failures are sandbox validation results only. Passing this suite does
not approve reviewed knowledge, evidence support, action basis, schema
governance, production search runtime, dependency installation, Obsidian sync,
commit, push, or mainline merge.
