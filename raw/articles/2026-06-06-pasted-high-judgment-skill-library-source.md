---
type: source
status: source-captured
title: "Start with Repetitive, High-Judgment Work: Building Your First Skill Library"
source_id: 2026-06-06-pasted-high-judgment-skill-library-source
source_uri: pasted-text-from-user
source_type: pasted_article
author:
publisher:
published_at:
captured_at: 2026-06-06
captured_by: Codex
raw_text_location: raw/articles/2026-06-06-pasted-high-judgment-skill-library-source/pasted-text.txt
raw_text_sha256: B47FF0526B0EBAA4BF11D5040FC838C306D12EE3F6B2532046EBD61B4EAAB848
processing_mode: immediate
processing_level: light
review_priority: medium
review_owner: Codex
formalization_status: candidate-generated
verification_status: pasted-text-only
confidence: medium for methodology extraction; low for any source-specific or official-doc claim not independently verified here
projects:
  - verified-action-knowledge-system
source_family:
  - agent-skills
  - procedural-memory
  - skill-library
topics:
  - skill library
  - high judgment work
  - failure modes
  - progressive disclosure
  - state source
  - routing
  - skill maintenance
truth_boundary: pasted article and candidate comprehension only; not reviewed knowledge; not architecture decision; not action basis
candidate_relation_suggestions:
  - candidate:high_judgment_work_first_for_skill_library
  - candidate:skill_library_as_sequence_of_judgment
  - candidate:skill_boundaries_state_routing_maintenance
  - candidate:failure_records_over_prompt_collections
related_existing_records:
  - wiki/patterns/skills-as-action-modules.md
  - wiki/patterns/artifact-trigger-and-body-alignment-eval.md
  - wiki/patterns/skill-artifact-iteration-workspace-rollback.md
  - wiki/summaries/2026-06-04-langchain-miniopenclaw-architecture-review.md
related_artifacts:
  - outputs/review/2026-06-06-pasted-high-judgment-skill-library-candidate-distillation.md
  - outputs/review/project_overlays/VAKS-high-judgment-skill-library-2026-06-06.md
tags:
  - source
  - pasted-article
  - skill-library
  - procedural-memory
  - candidate-only
---

# High-Judgment Skill Library Source

## 为什么收录

用户发送一篇关于 building first skill library 的文章，要求继续蒸馏。

这篇材料对 VAKS 的价值不在于“又一个 skill 模板”，而在于它提出了一个选择和维护 skill library 的判断框架：

```text
不要从轻 prompt 开始。
从重复发生、判断重、需要资深人员兜底的 workflow 开始。
把经验中的 stop rules、source of truth、failure modes 和 maintenance rules 固化为 skill library。
```

这和 VAKS 的 agent runtime / procedural memory / review gate 方向相关，但不进入 truth core。

## 原始资料

- Raw pasted text: `raw/articles/2026-06-06-pasted-high-judgment-skill-library-source/pasted-text.txt`
- Raw text SHA256: `B47FF0526B0EBAA4BF11D5040FC838C306D12EE3F6B2532046EBD61B4EAAB848`
- Original URL: not present in pasted text.
- Author / publisher: not present in pasted text.

## 关键内容摘要

文章主张：

- 第一批 skills 不应从轻量 prompt collection 开始。
- 应从重复出现、判断密集、需要人工安心复核的工作开始。
- Skill library 保存的不是“上次怎么说”，而是“下次先查什么、信谁、何时停、错了怎么修”。
- failure records 比 prompt 更有价值，因为它们保留 phase change、材料冲突、反馈歧义、旧经验污染等常见失败。
- Skill library 至少需要五层：Skill Map、Boundaries、State Source、Routing、Maintenance。
- V1 不求大，只要 3-5 个高频高判断 workflow，并定义 when to use、read first、judgment points、output format、human stop rules、patch rules。

## 当前处理结果

- Source card: `raw/articles/2026-06-06-pasted-high-judgment-skill-library-source.md`
- Raw text retained: `raw/articles/2026-06-06-pasted-high-judgment-skill-library-source/pasted-text.txt`
- Candidate distillation: `outputs/review/2026-06-06-pasted-high-judgment-skill-library-candidate-distillation.md`
- VAKS overlay: `outputs/review/project_overlays/VAKS-high-judgment-skill-library-2026-06-06.md`

No VAKS main architecture file was changed by this source.
