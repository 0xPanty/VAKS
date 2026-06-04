---
record_type: pain-report
status: draft
created: 2026-06-01
trial_id: vaks-e2e-trial-001
scope: sandbox-only
main_vault_write: false
schema_change: false
runtime: none
scripted: false
final_conclusion: false
---

# 疼点报告：VAKS End-to-End Trial 001

## Boundary

This report records friction from the first manual VAKS end-to-end trial.

It does not propose final fixes, does not modify the main vault, and does not conclude architecture changes.

Main vault checked after file creation:

```text
git status --short --untracked-files=all: empty
git diff --name-only: empty
```

Scratch root:

```text
C:\Users\Administrator\Documents\资料库_e2e_trial_2026-06-01_scratch
```

## Trial Flow Evidence

| Step | Required flow | Sandbox evidence |
|---|---|---|
| 1 | raw -> candidate -> manual review -> verified node -> context pack -> feedback | `raw/papers/2026-06-01-alce-source.md`; `outputs/review/2026-06-01-step1-alce-candidate-review.md`; `wiki/claims/2026-06-01-citation-quality-needs-separate-review.md`; `context-packs/2026-06-01-step1-alce-context-pack.md`; `outputs/feedback/2026-06-01-step1-feedback-event.md` |
| 2 | add 2-4 sources -> point collision -> Evidence Packet -> review queue | 3 added source records; `outputs/review/2026-06-01-point-collision-citation-support.md`; `outputs/review/2026-06-01-review-queue-citation-support.md`; `wiki/claims/2026-06-01-fine-grained-citation-support-needed.md` |
| 3 | real question -> context pack -> coverage_map / evidence_sufficiency | `context-packs/2026-06-01-citation-action-basis-context-pack.md`; `outputs/qa/2026-06-01-query-run-q1-citation-action-basis.md` |
| 4 | feedback event -> similar question -> activation / scope-fit change | `outputs/feedback/2026-06-01-feedback-event-q1-too-action-basis-shaped.md`; `outputs/qa/2026-06-01-query-run-q2-source-linked-answer-after-feedback.md` |

## 卡死

| Pain | Step | Field / rule | What happened |
|---|---|---|---|
| No true hard stop, but source independence could not be established from fields alone. | Step 2 | `source_family`, `upstream_sources`, source independence judgment | Four papers were distinct, but all came from the attributed-LLM citation family. The available fields flagged likely shared family but did not answer "independent enough for confidence?" |
| Action-basis wording did not map cleanly to a design-policy question. | Step 3 | `evidence_sufficiency.checked_for: action_basis` | The question asked whether cited answers can be action-ready in principle, not whether a concrete action should proceed. The field forced a concrete gate shape onto a policy answer. |

## 太重

| Pain | Step | Field / rule | What happened |
|---|---|---|---|
| Evidence Packet was heavy for one narrow abstract-backed point. | Step 1 | `evidence_packet`, `omission_check`, `strongest_rebuttal`, `minimal_revision_needed` | The packet clarified scope, but writing all fields for a tiny claim felt heavier than the value returned. |
| Repeating Evidence Packet fields across four sources became tiring. | Step 2 | per-source `rationale`, `evidence_support`, `reviewer_note` | The repeated structure was useful for audit but too verbose for a first collision. |
| Full coverage_map was large for one simple answer. | Step 3 | `coverage_map` | Seven rows were needed to answer one real question responsibly. Useful, but expensive. |
| Feedback-event frontmatter is too long for small scope-fit corrections. | Step 4 | `feedback-event` template | A simple "answer was too broad" signal required many fields, including numeric deltas that had no calibration guide. |

## 缺失

| Pain | Step | Field / rule | What happened |
|---|---|---|---|
| No clean place to say "abstract-only, intentionally scoped" on Source. | Step 1 | Source record vs `source_access` | Source record has `processing_level`, but source access quality lives later on candidate/claim evidence. This made `processing_level: heavy` feel misleading. |
| No compact format for support/refine collision. | Step 2 | `point_collision`, `review_queue_item.item_type` | The first useful collision was convergence, not contradiction. Existing taxonomy handled it, but awkwardly via `synthesis_needed`. |
| Missing coverage label for local rule plus external support. | Step 3 | `coverage_status` | The answer depended on VAKS local rules plus external evidence. `weakly_supported` was the closest label, but it hides the mixed source of support. |
| No calibration guide for feedback deltas. | Step 4 | `signal_strength`, `signal_confidence`, `activation_delta`, `scope_fit_delta` | Numeric values were manual guesses. They made the record look more precise than it was. |
| No runtime means activation change is manual narrative. | Step 4 | feedback activation / scope-fit | The Q1 -> Q2 change was inspectable in records, but not mechanically proven. |

## 含糊

| Pain | Step | Field / rule | What happened |
|---|---|---|---|
| `processing_level` and `source_access` are easy to confuse. | Step 1 | Source processing vs evidence access | A source can be important enough for heavy processing while the actual inspected evidence is abstract-only. |
| `needs_full_source_read` creates pressure to justify not reading everything. | Step 1 | `omission_check.needs_full_source_read` | For a narrow abstract-supported claim, `false` was defensible, but the field made it feel like a shortcut. |
| `item_type` is too single-choice for real review items. | Step 2 | `review_queue_item.item_type` | The collision was synthesis_needed, missing_evidence, and scope_limit at the same time. |
| `required_next_step: needs_review` is too vague. | Step 3 | `evidence_sufficiency.required_next_step` | The missing review could mean full paper review, more diverse sources, or a production failure case. |
| Feedback improves activation, but without a runtime it is only visible if query-run records are written carefully. | Step 4 | feedback boundary | The concept works manually, but ordinary use will not tolerate this much recordkeeping. |

## Lazy-Gate Findings

What worked:

```text
ordinary capture was not burdened because this trial intentionally entered promotion / context-pack / action-basis gates.
```

What hurt:

```text
once a point enters review, the templates invite many fields even for small claims.
```

The main risk is not that VAKS cannot run. It can run. The main pain is that the first realistic run already needs a compressed path for:

```text
small reviewed claim
support/refine collision
scope-fit feedback
```

## Do Not Conclude Yet

This report is pain evidence only.

Do not automatically:

```text
edit SCHEMA.md
add runtime
add new lane
promote trial claims into main vault
turn these pains into final architecture changes
```

Repair choices are intentionally left for the user and Opus.

