# VAKS audit shell v1 next-window recovery, full grain

Date: 2026-06-01
Scope: recovery and review context for the VAKS audit-noise reduction lane.
Boundary: this package is context and sandbox output. Main vault remains the source of truth. Do not treat tests, shell views, dashboards, grouping, feedback, or summaries as truth authority.

## 0. One-line state

VAKS main architecture is not being replaced. The current lane is testing whether `audit shell v1` can reduce ordinary audit/log noise while preserving strict evidence discipline for promotion, action-basis, challenge, conflict, known omission, missing anchor, regression, and other high-risk triggers.

## 1. Main vault identity

Main vault:

```text
C:\Users\Administrator\Documents\资料库
```

Latest evidence-guardrail mainline commit at last check:

```text
70f73b7 Add reverse-audit evidence guardrails
```

Note: a later handoff-only recovery commit may exist if the latest route-lock
handoff was updated after this package was assembled. The architecture payload
to inspect remains the evidence-guardrail commit above plus the latest handoff.

Latest handoff-only recovery commit after the audit-shell package check:

```text
f239dca Update audit shell recovery handoff
```

Main-vault status before the handoff-only update: clean.

Important rule: main vault is read-only unless the user explicitly approves writeback. Most work in this lane is sandbox/package-only.

## 2. Core architecture, in project language

Public story:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

Internal loop:

```text
Capture / Provenance
-> Candidate Comprehension
-> Knowledge Calibration / Point Collision
-> Review / Consolidation
-> Association / Reviewed Relations
-> Activation / Dev Context
-> Context Pack
-> Decision / Action
-> Use Ledger / Feedback
-> Cooling / Reactivation / Review Due
```

Durable route-lock:

```text
不是双架构；是一条主路 + 分级入口 + 懒证据闸门。
```

Key boundaries:

- Ordinary capture/query must stay light.
- Strict evidence checks are lazy gates for promotion, action-basis, strong relation, explicit challenge, conflict, stale/contested claim, known omission, risk-sensitive use, or explicit "is this enough" question.
- Feedback improves activation, usefulness, and scope fit; it does not directly change truth confidence.
- Retrieval, association, dashboard, tests, LLM judge, maintenance results, shell summaries, grouping, and feedback are routing/review aids, not truth authority.
- Source count, lineage, group count, same-origin repetition, dashboard pass, or test pass cannot create source independence or evidence support.
- Source anchor and jump-back must remain available for anything that claims evidence support.

## 3. Files to read first in the main vault

Start in the main vault with:

```text
AGENTS.md
00_handoff/ newest handoff
README.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SECOND_BRAIN_MODEL.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
IMPLEMENTATION_BLUEPRINT.md
SOURCE_INTAKE.md
REFERENCE_REVIEW_PROTOCOL.md
MEMORY_TIER.md
DEV_CONTEXT.md
REVIEW_QUEUE.md
FEEDBACK.md
wiki/indexes/knowledge-graph-index.md
wiki/indexes/memory-tier-reference-index.md
templates/architecture-review-window-prompt.md
templates/maintenance-manifest.md
```

## 4. What has already landed in main vault

Committed main-vault change:

```text
70f73b7 Add reverse-audit evidence guardrails
```

That commit added narrow reverse-audit guardrails without changing `SCHEMA.md`:

- Dynamic query-scope identity in `REVIEW_QUEUE.md`.
- Context-memory/current-source support boundary in `REVIEW_QUEUE.md`.
- Transformed evidence as original source anti-pattern under `wiki/anti-patterns/`.
- Knowledge graph index updated for the new anti-pattern.
- Handoff updated for recovery.

Important: this was the only main-vault writeback in this lane so far. Later audit-shell work stayed in sandboxes and packages.

## 5. Earlier pressure points found by E2E trial

A real-content E2E trial showed VAKS can run end to end, but ordinary work became too wordy in concentrated places:

- Small reviewed claim felt too heavy.
- Support/refine collision format felt awkward.
- `coverage_map` became too large for ordinary answers.
- Feedback records became too long, especially for scope-fit/activation notes.
- Source independence remained a hard human judgment problem.
- `processing_level` vs `source_access` remained easy to confuse.
- Runtime activation was still manual record, not machine proof.

Interpretation: architecture did not collapse. The pain is mostly surface/workflow noise after gates open, not truth-rule failure.

## 6. External research alpha intake

External research suggested the common mature-system answer:

```text
default light, conditionally thick, raw anchors always jump-backable
```

Useful references and borrowed mechanisms:

- Kubernetes Audit Policy: metadata/request/request-response levels, omit low-value stages/fields.
- UK ATRS: Tier 1 public summary + Tier 2 professional detail.
- GRADE: Summary of Findings + Evidence Profile, discrete certainty with reasons instead of fake precise scores.
- GitHub/GitLab review: unresolved-first, resolved folding, move non-blocking follow-up out of main queue.
- Sentry: issue grouping, breadcrumbs/ring buffer, unresolved/for-review/regressed states.
- OpenTelemetry: IsRecording, links, event/link caps, tail sampling, batch compression.
- W3C PROV / PROV-AQ: sparse provenance tuple plus external provenance lookup.
- SLSA/BuildKit: min/max disclosure and separation of external parameters, system parameters, dependencies, byproducts.

Things explicitly not to absorb:

- Do not make PROV/RDF/ontology a new main architecture.
- Do not make grouping evidence strength.
- Do not make lineage source independence.
- Do not let resolved/outdated mean actually resolved for evidence gaps.
- Do not sample away abnormal/high-risk runs.
- Do not use uncalibrated numeric deltas as fake precision.
- Do not let dashboard/retrieval/tests/LLM summaries become truth shortcuts.

See:

```text
09_external_research_intake/VAKS_AUDIT_NOISE_REDUCTION_REPORT_INTAKE.md
11_audit_shell_v1_followup/PRO_REPORT_SUMMARY_AND_NEXT_STEPS.md
```

## 7. Alpha test 1: four local compression ideas

Sandbox:

```text
C:\Users\Administrator\Documents\资料库_alpha_noise_test_2026-06-01_sandbox
```

Package copy:

```text
10_alpha_noise_test/
```

Four tested ideas:

- `compact_evidence_card`
- `compact_coverage_card`
- `support_refine_cluster`
- `categorical_feedback_stub`

Result:

```text
24/24 pass
overall saved: 27.4%
ordinary-case saved: 42.4%
false-lite: 0
ordinary false positives: 0
```

Meaning:

- Direction promising.
- Not product proof.
- It mainly tested typed signals, not raw messy inputs.

## 8. Pro's first major recommendation

Pro said not to keep four separate alpha templates. Collapse them into one product-shaped shell:

```text
audit shell v1
```

Core shape:

```text
[front face]
compact summary, anchor lane, state, open gap, upgrade reason

[expandable back]
full anchor/span, counterevidence, omission, source contributions, history pointers

[full audit]
existing heavy review/coverage/feedback, opened only by hard trigger
```

State/workflow direction:

- unresolved-first queue
- resolved folding
- repeated-event grouping
- regressed reopen
- metadata/compact stubs for ordinary runs
- sparse provenance pointer
- event/link caps

No main-vault schema change. Treat as view/wording/queue convention until proven.

See:

```text
11_audit_shell_v1_followup/PRO_REPORT_SUMMARY_AND_NEXT_STEPS.md
```

## 9. Audit shell v1 pilot

Sandbox:

```text
C:\Users\Administrator\Documents\资料库_audit_shell_v1_pilot_2026-06-01_sandbox
```

Package copy:

```text
12_audit_shell_v1_pilot/
```

Files:

```text
AUDIT_SHELL_V1_SPEC.md
run_shell_pilot.py
pilot_cases.json
pilot_results.json
AUDIT_SHELL_V1_PILOT_REPORT.md
PROGRESS_NOTE_FOR_PRO_REVIEW.md
```

Result:

```text
112/112 pass
ordinary record reduction: 63.1%
overall visible-line reduction: 29.3%
grouped repeated-event reduction: 56.5%
resolved folding: 100%
false-lite: 0
ordinary false-positive: 0
serious full-audit recall: 100%
review_due precision: 100%
front face violations: 0
over-grouping serious mismatch: 0
```

Meaning:

- Codex did implement a unified shell skeleton, not just rename four alphas.
- But the pilot was still typed-fixture/risk-map based.
- Metrics were too close to the same rule functions that produced shell output.
- Not enough to claim product-grade safety.

## 10. Pro review of shell pilot

Pro verdict:

```text
pass with concerns
```

What Pro accepted:

- Unified shell direction is real.
- Default-light/conditionally-thick direction is right.
- Resolved folding, regressed reopen, unresolved-first, grouping are real product levers.
- Shell boundary did not visibly break evidence discipline in spec.

What Pro rejected or downgraded:

- `112/112 pass` overclaimed.
- `review_due precision = 100%` was label echo.
- `serious recall = 100%` was function self-consistency.
- Anchor retention was a boolean, not real jump-back success.
- Grouping harness too easy.
- Front-face cap almost impossible to fail because it used `min`.
- Result did not prove product readiness.

Pro required next step:

```text
B then A:
1. 96-case adversarial fixture patch
2. then 480 real-data paired pilot if patch passes
```

Required fixes:

- Split oracle/gold labels from implementation.
- Add real jump-back resolver.
- Add review_due recall, not just precision.
- Rewrite grouping battery with near-misses.
- Cover missing trigger/state cases:
  - `decision_outcome`
  - `high_severity_wrong_answer`
  - `reviewer_blocks`
  - `parked_nonblocking`
- Add hidden burden metrics:
  - authoring time
  - reviewer triage time
  - manual classification field count
  - manual grouping decisions
  - front/back expansion count

See:

```text
13_pro_review_feedback/PRO_REVIEW_FEEDBACK_AND_NEXT_ACTION.md
```

## 11. Latest test: 96-case adversarial patch

Sandbox:

```text
C:\Users\Administrator\Documents\资料库_audit_shell_v1_adversarial_96_2026-06-01_sandbox
```

Package copy:

```text
14_audit_shell_v1_adversarial_96/
```

Files:

```text
README.md
ADVERSARIAL_PATCH_SPEC.md
adversarial_cases.psv
anchors.json
raw_sources/
run_adversarial_patch.py
shell_outputs.json
comparison_results.json
ADVERSARIAL_PATCH_REPORT.md
PROGRESS_NOTE_FOR_PRO_REVIEW.md
```

Case design:

```text
96 explicit hand-listed cases
24 over_grouping near-miss
16 false_lite traps
16 anchor_jumpback traps
16 review_due traps
12 state_transition traps
12 authority_leakage traps
```

Important improvement over previous pilot:

- Gold labels live in explicit `adversarial_cases.psv`, not generated by the same `needs_full_audit()` function.
- Shell output is generated separately.
- Comparison is separate.
- Anchor/jump-back resolves against `anchors.json` and local `raw_sources`.
- Review due has both precision and recall.
- Grouping includes near-misses.
- Hidden burden counters are recorded.

Latest run result:

```text
cases: 96
passed: 96
hard_gate_pass: True
false_lite: 0
ordinary_false_positive: 0
review_due_precision: 1.0
review_due_recall: 1.0
valid_anchor_failures: 0
missing_anchor_failures: 0
jumpback_failures: 0
authority_leakage_incidents: 0
feedback_truth_change_incidents: 0
front_face_violations: 0
severe_over_grouping: 0
grouped_reduction_pct: 50.0
visible_front_reduction_pct: 58.7
```

Trigger-family recall included the previously missing or weak areas:

```text
decision_outcome: 1.0
high_severity_wrong_answer: 1.0
reviewer_blocks: 1.0
```

Hidden burden counters:

```text
manual_fields_total: 686
manual_grouping_review_needed: 96
manual_grouping_applied: 43
front_back_expansions: 49
authoring_time_units_total: 1211
triage_time_units_total: 672
```

Meaning:

- This is stronger than the 112-case pilot.
- It directly responds to Pro's critique.
- It still is not a real-data product proof.
- It should be sent to Pro for review before starting the 480 real-data pilot.

## 12. Current package locations

Full deep research context package:

```text
C:\Users\Administrator\Documents\VAKS_deep_research_context_2026-06-01
C:\Users\Administrator\Documents\VAKS_deep_research_context_2026-06-01.zip
```

Pro-focused review package:

```text
C:\Users\Administrator\Documents\VAKS_pro_review_audit_shell_v1_2026-06-01_package
C:\Users\Administrator\Documents\VAKS_pro_review_audit_shell_v1_2026-06-01_package.zip
```

Alpha/test package:

```text
C:\Users\Administrator\Documents\VAKS_alpha_noise_test_2026-06-01_package
C:\Users\Administrator\Documents\VAKS_alpha_noise_test_2026-06-01_package.zip
```

The latest adversarial patch has been copied into all three package folders and all three zip files.

## 13. Recommended prompt to Pro

Use the latest package, then ask:

```text
我把 Codex 最新一轮 audit shell v1 adversarial patch 打包给你了。请不要只做验收，也不要被 Codex 的现有方向限制住。

请你从三个角度看：

1. 复核这轮 96-case adversarial patch 是否真的回应了你上次的 concerns：
   - oracle 和实现是否拆开了？
   - false-lite、review_due、over-grouping、anchor/jump-back、authority leakage 是否真的测到了？
   - 结果有没有再次自证、放水、指标夸大？

2. 判断方向：
   - audit shell v1 这条路是否仍然值得继续？
   - 现在是否足够进入 480 real-data paired pilot？
   - 如果不够，缺的最关键一刀是什么？

3. 继续找新的可能性：
   - 不要只在现有四个 alpha 里选。
   - 你可以提出新的降噪 / 审计 / queue / provenance / grouping / feedback 设计 alpha。
   - 重点看有没有能进一步降低日志噪音、人工负担、review friction，但不降低 evidence discipline 的机制。
   - 如果有，请给出：机制名、解决哪个痛点、为什么不破坏主架构、最小测试方法、风险。

请按这个格式输出：

A. 总 verdict
B. 这轮 adversarial patch 是否可信
C. 还有哪些 overclaim / blind spot
D. 是否建议进入 480 real-data pilot
E. 新 alpha 候选清单
F. 下一步最优路线
G. 哪些东西绝对不能现在进主库

注意：
- 主库暂时不改。
- 不动 SCHEMA。
- shell / grouping / dashboard / feedback / tests 都不能成为 truth authority。
- 我想听你自己的判断，不要为了顺着 Codex 说。
```

## 14. Next decision point

Do not write this into the main vault yet.

Next correct sequence:

1. Send the latest package to Pro.
2. Ask Pro to review the 96-case adversarial patch and search for additional alpha.
3. If Pro accepts this layer, design the 480 real-data paired pilot.
4. Only after real-data pilot passes hard gates should the team discuss main-vault operation convention wording.

## 15. What not to do next

- Do not claim product-grade readiness from the 96-case patch.
- Do not merge `audit shell v1` into main docs yet.
- Do not change `SCHEMA.md`.
- Do not create a new formal lane system.
- Do not let test pass become architecture truth.
- Do not let grouping, lineage, source count, dashboard, retrieval, or feedback become evidence support.
- Do not hide open gaps, missing anchors, known omissions, or trigger reasons just to get better reduction numbers.
