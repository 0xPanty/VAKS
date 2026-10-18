---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox
status: pass_product_grade
truth_boundary: sandbox_trace_only
---

# Source Map

## Project Rules Used

| Source | Rule used |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 763-764 | mdvs can be a Markdown frontmatter validation, vault health lint, and local hybrid search sidecar; valid metadata/search rank is not reviewed truth, support, or action readiness. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1492-1595 | mdvs adds no-update validation and local search; `.mdvs/` is derived cache; mdvs validates/finds while VAKS reviews/supports/decides. |
| `SOURCE_INTAKE.md` lines 185-220 | Validators and retrieval compilers must fail closed on enum drift; raw/candidate/overlay/feedback to reviewed/action requires explicit review. |
| `SOURCE_INTAKE.md` lines 740-845 | Retrieval must filter authority bucket first; selected_by is trace metadata, not authority/evidence. |
| `SOURCE_INTAKE.md` lines 1395-1460 | Retrieval rank is not trust; action-facing support must anchor to raw/stable material, not retrieval score or diagnostics. |
| P1.5-14 Product Acceptance report | Reuse JSON manifest, expected `issue_codes`, direct authority field denial, and sandbox-only non-claims style. |

## Artifact Mapping

| Requirement | Artifact coverage |
|---|---|
| No real vault scan | `failure-cases/real-vault-scan-requested.json` |
| No source mutation / auto-update | `failure-cases/source-mutation-requested.json`, `failure-cases/auto-update-enabled.json` |
| No dependency install, real runtime, background service, hooks, or MCP write tool | `failure-cases/dependency-install-requested.json`, `failure-cases/real-runtime-started.json`, `failure-cases/background-indexer-enabled.json`, `failure-cases/mcp-write-tool-exposed.json` |
| Protected path and sandbox/fixtures allowlist checks include input, config, cache, and absolute workspace paths | `failure-cases/protected-input-path.json`, `failure-cases/protected-config-path.json`, `failure-cases/absolute-wiki-claims-input-path.json`, `failure-cases/raw-input-path-not-fixture.json`, `failure-cases/config-path-outside-sandbox.json`, `failure-cases/cache-path-outside-sandbox.json`, `failure-cases/config-path-inside-sandbox-outside-fixtures.json` |
| Referenced copied fixtures must exist and be readable | `fixtures/copied-subset/raw-repo-source.md`, `fixtures/copied-subset/candidate-distillation.md`, `fixtures/copied-subset/reviewed-summary.md`, `fixtures/mdvs.toml.review-copy`, `fixtures/mdvs.toml.inferred-review-required`, `fixtures/cache-manifests/derived-cache-manifest.json`, `failure-cases/missing-copied-input-fixture.json`, `failure-cases/missing-config-fixture.json`, `failure-cases/missing-hit-ref-fixture.json`, `failure-cases/missing-cache-manifest-fixture.json` |
| Required contract blocks cannot be omitted | `failure-cases/missing-scope-block.json`, `failure-cases/missing-validation-block.json`, `failure-cases/missing-config-contract-block.json`, `failure-cases/missing-search-cache-block.json`, `failure-cases/missing-search-block.json`, `failure-cases/missing-vaks-validators-block.json`, `failure-cases/missing-boundary-block.json` |
| Deterministic JSON validation | `fixtures/valid-frontmatter-validation-check.json`, `failure-cases/non-deterministic-output.json` |
| Path-scoped frontmatter contracts | `fixtures/valid-frontmatter-validation-check.json`, `failure-cases/path-scopes-missing.json` |
| Enum drift and forbidden frontmatter fail closed | `failure-cases/unknown-enum-allowed.json`, `failure-cases/forbidden-frontmatter-allowed.json`, `failure-cases/frontmatter-authority-field-allowed.json` |
| Validation pass and health lint are not review pass/support/action readiness | `failure-cases/check-pass-as-review-pass.json`, `failure-cases/valid-frontmatter-as-support.json`, `failure-cases/health-lint-claims-review-pass.json` |
| Inferred config needs manual review and cannot govern schema | `fixtures/valid-manual-review-config-contract.json`, `failure-cases/inferred-config-no-review.json`, `failure-cases/config-schema-governance.json` |
| Search cache is derived/rebuildable/not truth | `failure-cases/cache-not-derived.json`, `failure-cases/committed-cache-truth-db.json` |
| Cache manifest, symbolic cache path, and mismatch handling | `fixtures/cache-manifests/derived-cache-manifest.json`, `failure-cases/cache-manifest-incomplete.json`, `failure-cases/cache-symbolic-path-invalid.json`, `failure-cases/cache-mismatch-used.json` |
| Hybrid search modes and bucket-first policy | `fixtures/valid-hybrid-search-activation-only.json`, `failure-cases/search-modes-incomplete.json`, `failure-cases/bucket-filter-missing.json`, `failure-cases/cross-bucket-fusion.json` |
| Search hit refs, labels, bucket membership, and selected_by trace | `failure-cases/search-buckets-missing.json`, `failure-cases/unknown-bucket.json`, `failure-cases/hit-in-excluded-bucket.json`, `failure-cases/hit-not-in-included-bucket.json`, `failure-cases/hit-ref-missing.json`, `failure-cases/hit-selected-by-missing.json` |
| Search rank/score cannot become trust/support/action | `failure-cases/search-rank-as-trust.json`, `failure-cases/candidate-hit-as-support.json`, `failure-cases/raw-anchor-hit-as-support.json`, `failure-cases/hit-action-basis.json` |
| VAKS validators remain separate | `failure-cases/sidecar-replaces-vaks-validators.json` |
| Direct and alias authority fields are forbidden | `failure-cases/direct-evidence-support-field.json`, `failure-cases/direct-is-truth-field.json`, `failure-cases/direct-promotion-field.json`, `failure-cases/search-hit-direct-action-field.json` |

## Boundaries

- No real mdvs runtime is executed.
- No dependency is installed.
- No real vault is scanned.
- No Markdown source file is written.
- No `.mdvs/` cache is created or committed.
- No raw/wiki/template/tool/Obsidian path is written.
- No evidence support, reviewed knowledge, reviewed relation, reviewer approval,
  action basis, schema governance, promotion, commit, push, or sync is created.
