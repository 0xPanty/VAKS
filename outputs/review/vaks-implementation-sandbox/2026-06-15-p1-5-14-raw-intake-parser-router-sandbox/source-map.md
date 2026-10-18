---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-5-14-raw-intake-parser-router-sandbox
status: implemented_pending_review
truth_boundary: sandbox_trace_only
---

# Source Map

## Project Rules Used

| Source | Rule used |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 204-214 | Future raw parser router must keep parser output raw/candidate and preserve original hash, parser config, retained outputs, anchors, and boundary flags. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1299-1336 | OmniParse is a raw-material parser router reference; VAKS-owned bundle wraps original/parser/outputs/anchors/boundary. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1337-1365 | Borrow lazy modality routing and extraction bundle wrapper; reject parser markdown as reviewed knowledge, confidence as truth, parser output as action basis, full runtime core dependency, unreviewed license/runtime, private crawling, and always-on heavy parsing. |
| `SOURCE_INTAKE.md` lines 95-151 | Raw/candidate/reviewed boundaries and retrieval policies are orthogonal; source cards are raw and candidate distillations are candidate, not action basis. |
| `SOURCE_INTAKE.md` lines 255-320 | Source cards are provenance only; forbidden fields include truth score, action basis, top-level relations, confidence, freshness, relevance, source quality, cross-source count, and proxy support. |
| `SOURCE_INTAKE.md` lines 1049-1074 | Source hashes and adapter ingest are hygiene only; adapter output may create raw/candidate material but not reviewed nodes, truth confidence, reviewed relations, verification status, or action readiness. |
| `SOURCE_INTAKE.md` lines 1400-1459 | Action-facing support must anchor to raw/stable material; distillation, retrieval score, evaluator output, and feedback cannot be final support anchors. |
| P1.5-13 Product Acceptance report | Reuse JSON manifest, expected `issue_codes`, non-claims, failure oracle, and authority-confusion hardening style. |

## Artifact Mapping

| Requirement | Artifact coverage |
|---|---|
| Preserve original hash | `fixtures/valid-document-extraction-bundle.json`, `failure-cases/missing-original-hash.json`, `failure-cases/weak-md5-original-hash.json` |
| Route by modality lazily | all positive fixtures, `failure-cases/route-modality-mismatch.json`, `failure-cases/lazy-routing-missing.json` |
| Do not run always-on heavy parsing | `failure-cases/heavy-parser-always-on.json` |
| Router/parser confidence is not truth | `failure-cases/router-confidence-as-truth.json`, `failure-cases/parser-confidence-as-truth.json` |
| Router/parser direct truth-confidence fields are forbidden | `failure-cases/router-truth-confidence-direct-field.json`, `failure-cases/parser-truth-confidence-direct-field.json` |
| Preserve parser config and limits | all positive fixtures, `failure-cases/parser-config-hash-missing.json` |
| No dependency install or full runtime import | `failure-cases/dependency-install-requested.json`, `failure-cases/full-runtime-core-dependency.json` |
| License and locality remain gates | `failure-cases/gpl-license-unreviewed.json`, `failure-cases/cloud-model-locality-unreviewed.json` |
| Retain extraction outputs with hashes | all positive fixtures, `failure-cases/retained-outputs-missing.json`, `failure-cases/retained-output-hash-missing.json` |
| Retained output direct authority fields are forbidden | `failure-cases/retained-output-direct-authority-field.json` |
| Output cannot be scratch-only or protected | `failure-cases/scratch-only-output.json`, `failure-cases/protected-output-path.json`, `failure-cases/obsidian-vault-output-path.json` |
| Anchors are required and source-hash linked | all positive fixtures, `failure-cases/anchors-missing.json`, `failure-cases/anchor-source-hash-missing.json` |
| Anchor direct authority fields are forbidden | `failure-cases/anchor-direct-evidence-support.json` |
| Parser output stays raw/candidate | `failure-cases/parser-output-reviewed-status.json`, `failure-cases/parser-markdown-reviewed-knowledge.json` |
| Parser output cannot become action/truth | `failure-cases/action-basis-allowed.json`, `failure-cases/truth-mutation-allowed.json` |
| Parser output cannot claim promotion by direct field | `failure-cases/promotion-direct-authority-field.json` |
| Private/account capture needs authorization | `failure-cases/private-web-no-auth.json`, `failure-cases/account-cookies-used.json` |
| Source cards remain raw provenance | `failure-cases/source-card-reviewed.json`, `failure-cases/source-card-relations-top-level.json`, `failure-cases/source-card-protected-target.json` |
| Source-card direct authority fields are forbidden | `failure-cases/source-card-direct-evidence-support.json` |
| Candidate distillation stays provisional and non-authority | `failure-cases/candidate-not-provisional.json`, `failure-cases/candidate-direct-reviewed-knowledge.json` |

## Boundaries

- No real parser runtime is executed.
- No dependency is installed.
- No real source is read.
- No raw/wiki/template/tool/Obsidian path is written.
- No evidence support, reviewed knowledge, reviewed relation, reviewer approval,
  action basis, promotion, commit, push, or sync is created.
