---
type: sandbox_manifest
status: candidate_only
created_at: 2026-06-07
scope: source intake tag routing sandbox manifest
truth_boundary: sandbox manifest only
---

# Manifest

## Inputs

```text
Pro report pasted by user on 2026-06-07.
Current mainline commit: 0cea747 docs: merge source intake control flow guardrails.
Current recovery entry: 00_handoff/2026-06-06-source-intake-control-flow-mainline-merge-handoff.md.
Current audit: outputs/review/source-intake-control-flow-sandbox-2026-06-06/checks/mainline-merge-audit.md.
```

## Candidate Architecture Files

```text
00_PRO_REQUIREMENT_MAP.md
01_MAINLINE_CANDIDATE_DELTA.md
02_FIELD_CONTRACT.md
03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md
04_SUGGESTED_CONFIRMED_FORBIDDEN.md
05_TOPIC_ENTITY_KP_DESIGN.md
06_RETRIEVAL_MVP_LANE_CLASSIFIER.md
07_TOPIC_REGISTRY_CANDIDATE.md
08_ENTITY_ALIAS_CANDIDATE.md
09_KP_ID_LINT_CONTRACT.md
10_OTHER_ROLE_CLASSIFIER.md
11_VAULT_DISTILLATION_BORROWINGS.md
12_ARTIFACT_REGISTRY_CANDIDATE.md
13_CONTEXT_PACK_BUILDER_V0_CONTRACT.md
14_OBSIDIAN_WORKBENCH_ENTRYPOINTS.md
15_INTAKE_METADATA_PREFILL_OPTIMIZATION.md
16_SOURCE_CARD_VS_CANDIDATE_METADATA_SPLIT.md
17_TOPIC_RETRIEVAL_PACK_MVP.md
18_SOURCE_INTAKE_ROUTING_WORKBENCH_LANDING.md
19_SOURCE_INTAKE_ROUTING_WORKBENCH_HARDENING.md
20_EVIDENCE_SUPPORT_CHECK_REFERENCE_DISTILLATION.md
21_EVIDENCE_SUPPORT_CHECK_V0_LANDING.md
22_ANSWER_DRAFT_SMOKE_V0_OPUS_REVIEW_BRIEF.md
23_REAL_LOCAL_PRESSURE_AND_BLIND_REVIEW_PACKET.md
23A_AUTHOR_RECORDED_RESULTS_AFTER_BLIND_RUN.md
24_BLIND_OPUS_REVIEW_ABSORPTION.md
```

## Mainline Candidate Snapshots

```text
mainline-candidate/SOURCE_INTAKE_METADATA_ROUTING_ADDENDUM.md
mainline-candidate/templates/source-record.md
mainline-candidate/templates/video-source.md
mainline-candidate/templates/candidate-distillation.md
mainline-candidate/templates/query-run.md
mainline-candidate/templates/topic-retrieval-pack.md
mainline-candidate/templates/intake-metadata-suggestion-sidecar.md
```

## Sandbox Tools

```text
tools/vaks-retrieval-mvp.ps1
tools/vaks-kp-lint.ps1
tools/vaks-usage-layer-lint.ps1
tools/vaks-intake-metadata-lint.ps1
tools/vaks-context-pack-builder-v0.ps1
tools/vaks-context-pack-lint.ps1
tools/vaks-query-intent-router-v0.ps1
tools/vaks-evidence-support-check-v0.ps1
tools/vaks-answer-draft-skeleton-v0.ps1
tools/vaks-answer-draft-smoke-lint-v0.ps1
```

## Fixtures

```text
fixtures/source-card-confirmed-metadata.md
fixtures/source-card-forbidden-authority-tags.md
fixtures/candidate-distillation-kp-refs.md
fixtures/candidate-distillation-bad-kp.md
fixtures/project-overlay-confirmed.md
fixtures/query-run-action-review.md
fixtures/query-run-tag-first-failure.md
fixtures/topic-retrieval-pack-source-intake.md
fixtures/intake-metadata-suggestion-sidecar.md
fixtures/artifact-registry-source-intake.md
fixtures/context-pack-builder-v0-source-intake.md
fixtures/obsidian-workbench-entrypoint-source-intake.md
fixtures/source-intake-route-map.json
fixtures/query-intent-router-v0.json
fixtures/usage-layer-bad-authority-leak.md
fixtures/source-card-prefilled-discovery-metadata.md
fixtures/source-card-no-prefill-control.md
fixtures/source-card-bad-prefill-authority.md
fixtures/intake-metadata-suggestion-bad-persistent.md
fixtures/evidence-support-check-v0-source-intake.json
fixtures/evidence-support-check-v0-negative-source-intake.json
fixtures/evidence-support-check-v0-mixed-source-intake.json
fixtures/evidence-support-check-v0-revised-source-intake.json
fixtures/evidence-support-check-v0-e2e-mixed-source-intake.json
fixtures/evidence-support-check-v0-e2e-revised-source-intake.json
fixtures/evidence-support-check-v0-pack-containment-source-intake.json
fixtures/evidence-support-check-v0-pack-repair-source-intake.json
fixtures/evidence-support-check-v0-real-local-smoke-boundary.json
fixtures/evidence-support-check-v0-real-local-action-basis-negative.json
```

## Checks

```text
checks/coverage-audit.md
checks/retrieval-pressure-test.md
checks/lint-matrix.md
checks/obsidian-sync-check.md
checks/real-vault-retrieval-smoke.md
checks/retrieval-mvp-script-test.md
checks/kp-lint-test.md
checks/five-shortfalls-coverage-audit.md
checks/vault-distillation-borrowing-audit.md
checks/usage-layer-lint-test.md
checks/usage-layer-high-pressure-test.md
checks/intake-metadata-prefill-test.md
checks/real-vault-retrieval-workbench-smoke.md
checks/retrieval-mode-regression-after-builder.md
checks/github-source-intake-routing-scout.md
checks/topic-retrieval-pack-source-intake-generated.md
checks/topic-retrieval-pack-source-intake-formal-vault-generated.md
checks/source-intake-routing-workbench-pack-research-generated.md
checks/source-intake-routing-workbench-pack-source-inspection-generated.md
checks/source-intake-routing-workbench-pack-action-generated.md
checks/source-intake-routing-workbench-pack-query-action-generated.md
checks/source-intake-routing-workbench-pack-query-audit-generated.md
checks/source-intake-routing-workbench-pack-query-project-exploration-generated.md
checks/source-intake-routing-workbench-pack-query-research-generated.md
checks/source-intake-routing-workbench-pack-query-source-inspection-generated.md
checks/source-intake-routing-workbench-pack-query-e2e-action-generated.md
checks/source-intake-routing-workbench-pack-query-e2e-action-repaired-generated.md
checks/source-intake-routing-workbench-high-pressure-test.md
checks/source-intake-routing-workbench-hardening-v0-1-test.md
checks/evidence-support-check-v0-source-intake-generated.md
checks/answer-ready-context-pack-v0-source-intake-generated.md
checks/evidence-support-check-v0-test.md
checks/evidence-support-check-v0-negative-generated.md
checks/answer-ready-context-pack-v0-negative-generated.md
checks/evidence-support-check-v0-negative-pressure-test.md
checks/evidence-support-check-v0-mixed-generated.md
checks/answer-ready-context-pack-v0-mixed-generated.md
checks/evidence-support-check-v0-mixed-pressure-test.md
checks/evidence-support-check-v0-revised-generated.md
checks/answer-ready-context-pack-v0-revised-generated.md
checks/evidence-support-check-v0-revised-flip-test.md
checks/evidence-support-check-v0-e2e-mixed-generated.md
checks/answer-ready-context-pack-v0-e2e-mixed-generated.md
checks/evidence-support-check-v0-e2e-revised-generated.md
checks/answer-ready-context-pack-v0-e2e-revised-generated.md
checks/evidence-support-check-v0-e2e-repair-loop-test.md
checks/evidence-support-check-v0-pack-containment-generated.md
checks/answer-ready-context-pack-v0-pack-containment-generated.md
checks/evidence-support-check-v0-pack-containment-test.md
checks/evidence-support-check-v0-pack-repair-generated.md
checks/answer-ready-context-pack-v0-pack-repair-generated.md
checks/evidence-support-check-v0-pack-repair-test.md
checks/answer-draft-skeleton-v0-pack-repair-generated.md
checks/answer-draft-skeleton-v0-e2e-mixed-blocked-generated.md
checks/answer-draft-skeleton-v0-test.md
checks/answer-draft-smoke-v0-pack-repair-generated.md
checks/answer-draft-smoke-v0-e2e-mixed-blocked-generated.md
checks/answer-draft-smoke-v0-pack-repair-lint-generated.md
checks/answer-draft-smoke-v0-e2e-mixed-blocked-lint-generated.md
checks/answer-draft-smoke-v0-empty-claim-refs-generated.md
checks/answer-draft-smoke-v0-empty-claim-refs-lint-generated.md
checks/answer-draft-smoke-v0-paragraph-blocked-generated.md
checks/answer-draft-smoke-v0-paragraph-blocked-lint-generated.md
checks/answer-draft-smoke-v0-fenced-heading-blocked-generated.md
checks/answer-draft-smoke-v0-fenced-heading-blocked-lint-generated.md
checks/answer-draft-smoke-v0-mismatched-ref-known-limitation-generated.md
checks/answer-draft-smoke-v0-mismatched-ref-known-limitation-lint-generated.md
checks/answer-draft-smoke-v0-omitted-claim-known-limitation-generated.md
checks/answer-draft-smoke-v0-omitted-claim-known-limitation-lint-generated.md
checks/answer-draft-smoke-v0-test.md
checks/real-local-question-pack-answer-draft-smoke-generated.md
checks/real-local-question-pack-smoke-boundary-generated.md
checks/real-local-question-pack-action-basis-generated.md
checks/evidence-support-check-v0-real-local-smoke-boundary-generated.md
checks/answer-ready-context-pack-v0-real-local-smoke-boundary-generated.md
checks/evidence-support-check-v0-real-local-action-basis-negative-generated.md
checks/answer-ready-context-pack-v0-real-local-action-basis-negative-generated.md
checks/answer-draft-skeleton-v0-real-local-smoke-boundary-generated.md
checks/answer-draft-skeleton-v0-real-local-action-basis-negative-blocked-generated.md
checks/answer-draft-smoke-v0-real-local-smoke-boundary-generated.md
checks/answer-draft-smoke-v0-real-local-smoke-boundary-lint-generated.md
checks/answer-draft-smoke-v0-real-local-action-basis-negative-blocked-generated.md
checks/answer-draft-smoke-v0-real-local-action-basis-negative-blocked-lint-generated.md
checks/real-local-answer-draft-smoke-pressure-test.md
```

## Workbench Entrypoints

```text
workbench/source-intake-routing.md
```

## External Scout Artifacts

```text
raw/repos/2026-06-07-langgenius-dify-source.md
raw/repos/2026-06-07-infiniflow-ragflow-source.md
raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
raw/repos/2026-06-07-run-llama-llama-index-source.md
raw/repos/2026-06-07-deepset-ai-haystack-source.md
outputs/review/2026-06-07-source-intake-routing-github-scout-candidate-distillation.md
outputs/review/project_overlays/VAKS/VAKS-source-intake-routing-github-scout-2026-06-07.md
```

## Non-Goals

```text
No mainline writeback yet.
No schema promotion.
No ontology or global tag registry.
No production/global context-pack builder.
No automatic answer generator.
No vector database or API implementation.
No truth-layer mutation.
```
