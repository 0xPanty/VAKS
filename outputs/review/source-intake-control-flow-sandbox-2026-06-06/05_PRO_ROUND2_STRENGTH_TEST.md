---
type: sandbox_strength_test_matrix
status: candidate_only
created_at: 2026-06-06
scope: Pro round-2 source intake control flow strength test
truth_boundary: sandbox matrix only; not reviewed knowledge; not architecture decision; not action basis
---

# 05 Pro Round-2 Strength Test

## Purpose

This supplement adds Pro's later recommendations to the existing Source Intake
Control Flow sandbox and tests whether the guardrails are stronger than the
first 11-check pass.

The target is not a prettier workflow. The target is runtime separation:

```text
processing_tier != authority
candidate != action basis
suggested overlay != confirmed overlay
feedback != truth mutation
relevance fusion != authority fusion
distillation != final evidence anchor
```

## Strength Cases

| ID | Failure case | Expected block / route |
|---|---|---|
| ST-01 | Medium candidate is phrased like a rule and appears in default answer context. | `retrieval_policy: orientation_only`; action/review mode excludes candidate. |
| ST-02 | Semantic match creates persistent overlay without confirmation. | Suggested overlay remains query-run trace only. |
| ST-03 | Project non-borrow warning is read as universal ban. | `project_non_borrow_scope` plus `project_reopen_trigger`; remains project-scoped. |
| ST-04 | Candidate summary outranks raw anchor. | Authority bucket filter blocks candidate as final evidence. |
| ST-05 | Useful feedback makes a source "more true". | Feedback event is append-only; no truth delta fields allowed. |
| ST-06 | Source page/repo/video changed after capture. | Broken/changed source sets `blocked`; no action-facing use. |
| ST-07 | Heavy review is open but not passed. | `heavy_review_open` and `review_status: blocked/open_not_passed` stay out of answer pool. |
| ST-08 | Archived overlay still appears in retrieval. | `overlay_state: archived` and `default_retrieval: false`. |
| ST-09 | Action-facing support points to candidate distillation. | Invalid final support anchor; must return to raw/stable representation. |
| ST-10 | RRF merges raw/candidate/reviewed/overlay into one authority-like ranking. | RRF only fuses relevance inside allowed authority bucket. |
| ST-11 | Confirmed overlay is read outside active project. | `retrieval_scope: active_project_only`; non-project query excludes it. |
| ST-12 | Source card carries adopt/reject or truth score. | Source card remains raw/source identity only. |
| ST-13 | Feedback lacks project/context scope and becomes global negative knowledge. | Feedback requires `project_ref` or `observed_in_context`; no global negative. |
| ST-14 | Project overlay looks like ADR / decision. | Overlay forbids decision outcome, review verdict, action basis, and universal ban. |

## Improvement Lens

Compared with the first sandbox pass, this round adds four harder checks:

```text
1. final evidence anchors cannot point to candidate / overlay artifacts.
2. archived overlays must be drained from default retrieval.
3. source changed / broken anchor creates blocked state.
4. confirmed overlay has active-project-only retrieval scope.
```

