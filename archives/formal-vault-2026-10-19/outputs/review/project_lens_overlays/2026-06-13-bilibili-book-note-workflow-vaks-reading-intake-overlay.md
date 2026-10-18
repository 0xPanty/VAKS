---
type: review_output
record_kind: project_lens_overlay
status: candidate_only
provisional: true
created_at: 2026-06-13
created_by: Codex
source_ref: raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source.md
candidate_ref: outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md
knowledge_status: candidate
overlay_state: project_lens_only
review_pressure: review_due
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
fit_layers:
  - Capture / Provenance
  - Candidate Comprehension
  - Association / Activation
  - Use Ledger / Feedback
  - Cooling / Reactivation
  - UI / Workbench
tags:
  - vaks-project-lens
  - reading-source-intake-loop
  - candidate-only
  - remembered-is-not-truth
---

# VAKS Reading Intake Overlay

## 人话归位

这条视频可以给 VAKS 补一条很实用的“读书类资料入库”路径：先轻量捕获，后集中加工；先保留原始划线，再写自己的候选卡；先用索引卡看结构，再决定哪些点值得 review；回顾和记忆只影响 activation/feedback，不碰 truth。

它不是正式架构变更，只是项目镜头候选。

## 可落到 VAKS 的最小流程草图

```text
Reading / Article / Video Highlight
-> raw/source inbox
-> own-language candidate card
-> quote/paraphrase/model-output split
-> candidate index card
-> active recall or revisit
-> feedback event / review_due / association candidate
-> evidence-aware review only when promotion/action is needed
```

## 对现有架构的提醒

- `Capture` 应该继续轻，允许用户先把划线和想法接住。
- `Candidate Comprehension` 可以要求“用自己的话说清楚”，但不能因此给 truth confidence。
- `Review Queue` 应接住写不清、互相冲突、缺证据、值得综合的点。
- `Association` 可以接住跨书联想，但 reviewed relation 需要后续审查。
- `Activation` 可以借主动回忆和每日回顾，但 activation tier 不是 truth tier。
- `Use Ledger / Feedback` 可以记录忘记、填错、重写、变清楚、产生联想。

## 不该吸收的部分

- 不把 reminds 绑定成核心依赖。
- 不把 AI 生成框架写成正式分类。
- 不把白板分类当 reviewed relation。
- 不把回顾次数、填空正确率、熟悉感当 evidence support。
- 不把“作者经验有效”当通用学习结论。

## 适合后续 review 的候选标签

```yaml
candidate_pattern:
  id: reading-source-intake-loop
  value: high
  layer: user-facing intake/workbench
  needs_review_before_adoption:
    - source_anchor_required
    - quote_vs_paraphrase_required
    - candidate_point_atomicity
    - feedback_truth_boundary
    - ai_framework_boundary
  possible_future_docs:
    - SOURCE_INTAKE.md
    - REVIEW_QUEUE.md
    - MEMORY_TIER.md
    - templates/source-record.md
```
