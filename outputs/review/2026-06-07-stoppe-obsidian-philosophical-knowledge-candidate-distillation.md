---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/papers/2026-06-07-stoppe-obsidian-philosophical-knowledge-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - obsidian-workbench
  - education-scenario
  - graph-as-orientation
  - course-vault
  - collaborative-knowledge-building
  - onboarding-risk
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - source_ref: raw/papers/2026-06-07-stoppe-obsidian-philosophical-knowledge-source.md
    selector_type: official_metadata
    selector_value: "IATED official page: title, V. Stoppe, ICERI2024, pages 7217-7222, DOI 10.21125/iceri.2024.1735"
  - source_ref: raw/papers/2026-06-07-stoppe-obsidian-philosophical-knowledge-source.md
    selector_type: researchgate_lines
    selector_value: "lines 238-263: Markdown files independent of Obsidian, hyperlinks, bidirectional links, graph view"
  - source_ref: raw/papers/2026-06-07-stoppe-obsidian-philosophical-knowledge-source.md
    selector_type: researchgate_lines
    selector_value: "lines 275-386: philosophy student example, morality/utilitarianism, linked/unlinked mentions"
  - source_ref: raw/papers/2026-06-07-stoppe-obsidian-philosophical-knowledge-source.md
    selector_type: researchgate_lines
    selector_value: "lines 388-466: portfolio, collaborative course vault, MOOC/research workshop use"
  - source_ref: raw/papers/2026-06-07-stoppe-obsidian-philosophical-knowledge-source.md
    selector_type: researchgate_lines
    selector_value: "lines 468-514: onboarding burden, voluntary adoption risk, handwritten notes gap, need practical evaluation"
reference_layer_tag: ref/obsidian-education-course-vault
reference_layer_label_zh: 教育场景课程型 Obsidian vault
reference_layer_scope: "education / workbench / orientation reference only"
borrow_value: medium
borrow_order:
  - "P1: Course or semester vault as visible cumulative knowledge surface: notes, links, graph, and linked mentions make learning relationships inspectable."
  - "P1: Obsidian as stage/interface, not storage authority: Markdown files stay outside the app and remain portable."
  - "P2: Portfolio assessment idea: a submitted vault can show how a learner connected concepts over time."
  - "P2: Shared course vault / collaborative wiki idea for seminars, MOOCs, and research workshops."
  - "P3: Linked mentions and unlinked mentions as low-friction relationship discovery hints."
avoid:
  - "Do not treat Obsidian graph lines as reviewed relations."
  - "Do not treat visible links as proof of philosophical understanding."
  - "Do not import classroom/course-vault workflow as VAKS truth architecture."
  - "Do not ignore onboarding cost, teacher/admin burden, voluntary adoption risk, or handwritten-note workflow gaps."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing an education-facing or Obsidian-workbench-facing VAKS interface where course/shared vaults, graph orientation, or portfolio review are the active task."
  support_when: "Discussing graph view, linked/unlinked mentions, course vaults, collaborative knowledge building, or educational PKM examples."
  risk_when: "Any Obsidian link, graph edge, linked mention, portfolio appearance, or shared-vault contribution starts being treated as evidence support, reviewed relation, truth confidence, or action basis."
  cold_references:
    - raw/papers/2026-06-07-stoppe-obsidian-philosophical-knowledge-source.md
tags:
  - candidate
  - provisional
  - obsidian
  - higher-education
  - course-vault
  - graph-as-orientation
  - candidate-only
---

# Candidate Distillation: Stoppe / Obsidian Philosophical Knowledge

## Boundary

This note is provisional orientation.

It distills an ICERI2024 education paper into VAKS candidate signals. It is not
reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话

这篇文章的价值不是“Obsidian 很强”，而是给了一个很朴素的教育场景：

```text
学生跨学期学习哲学概念，
用 Obsidian 把旧课和新课的概念连接起来，
让知识关系逐渐长出来并可见。
```

对 VAKS 来说，它补的是：

```text
workbench / education / visible relationship surface
```

不是：

```text
truth layer / evidence review / action basis
```

## Candidate Points

### CP-001: `obsidian_as_stage_not_storage_authority`

候选结论：

```text
Obsidian 可以被理解为 Markdown 文件的舞台/界面，而不是知识本体的唯一存储权威。
```

VAKS 可借：

```text
Obsidian workbench 显示、编辑、搜索、链接结构化 Markdown。
Markdown/YAML 才是 durable record。
```

不借：

```text
不让 Obsidian UI、graph、plugin 状态反过来定义 truth schema。
```

### CP-002: `graph_view_as_relationship_visibility`

候选结论：

```text
Graph view 可以帮助学习者看见概念之间的关系。
```

文章里的例子是：

```text
What is morality?
-> Kant / Deontology / Social Contract / Utilitarianism
```

后续 `Utilitarianism` 又连接到：

```text
Bentham / Mill / happiness
```

VAKS 可借：

```text
graph view = orientation surface
```

不借：

```text
graph edge != reviewed relation
link density != understanding
cluster != evidence support
```

### CP-003: `linked_and_unlinked_mentions_as_discovery_hints`

候选结论：

```text
linked mentions 和 unlinked mentions 可以把潜在关系重新拉回用户视野。
```

VAKS 可借：

```text
unlinked mention / lexical reappearance / backlink neighborhood
-> candidate relation suggestion
-> review input
```

不借：

```text
未链接提及不能自动变成关系。
同词出现不能自动变成证据。
```

### CP-004: `course_vault_as_portfolio`

候选结论：

```text
学生提交一个 vault 作为课程 portfolio，可以让教师看到学生如何连接课程主题。
```

VAKS 可借：

```text
portfolio-like context pack:
  show records
  show links
  show growth over time
  show what is still candidate
```

边界：

```text
portfolio 展示的是学习过程和连接痕迹，不是自动证明理解质量。
```

### CP-005: `shared_course_vault_as_cumulative_wiki`

候选结论：

```text
一个课程或研究工作坊可以维护共享 vault，让不同学期学生继续积累和链接内容。
```

VAKS 可借：

```text
collaborative knowledge surface
cross-session / cross-cohort accumulation
shared notes as candidate inputs
```

必须加的边界：

```text
shared contribution != reviewed knowledge
shared vault needs ownership, stewardship, and review rules
```

### CP-006: `onboarding_cost_as_adoption_gate`

候选结论：

```text
复杂工具的上手成本会限制真实使用，尤其是自愿使用时。
```

VAKS 可借：

```text
any workbench/tooling layer needs low-friction entry,
clear training path,
and defaults that do not demand graph maintenance from ordinary users.
```

这点和 VAKS 的轻/中/重 intake 很一致：

```text
普通捕获要轻，
重要提升才严格。
```

### CP-007: `handwritten_annotation_gap`

候选结论：

```text
传统 Obsidian/personal wiki workflow 对 tablet PDF 批注、手写笔记整合并不天然友好。
```

VAKS 可借：

```text
source intake should not assume all valuable learning artifacts are typed Markdown.
```

未来若处理教育/学习场景，需要考虑：

```text
PDF annotation
image or handwritten notes
OCR/ASR confidence
source artifact retention
```

## Fusion Fit

### 对 VAKS 有用的地方

```text
1. 支持 Obsidian as IDE / workbench，而不是 database authority。
2. 支持 graph as orientation，而不是 truth。
3. 支持 course/shared vault 作为 collaborative candidate surface。
4. 支持 onboarding cost 作为工具设计约束。
```

### 最小优雅吸收

只吸收一个小规则就够：

```text
Obsidian graph is a learning/review visibility surface,
not a reviewed relation surface.
```

再吸收一个教育/workbench 参考：

```text
course vault / portfolio vault can show how understanding grows over time,
but promotion still needs review.
```

## Open Questions

```text
1. 如果 VAKS 做教育/学习模式，portfolio pack 应显示哪些字段？
2. shared vault 里的多人贡献如何标记 provenance 和 review state？
3. unlinked mentions 是否适合作为 candidate_relation_suggestions 的轻信号？
4. 学生/普通用户的最低可用入口是什么，才能不被 Obsidian 复杂度劝退？
5. 手写/PDF/图片批注如何进入 source intake，而不污染 Markdown truth layer？
```

## Routing Hint

```yaml
route_to:
  - Viewer / Obsidian workbench support reference
  - education-facing VAKS explanation
  - portfolio/context-pack UX idea
  - candidate relation suggestion from linked/unlinked mentions
  - onboarding/adoption risk layer
review_required_before:
  - reviewed pattern
  - education product workflow
  - shared vault implementation
  - action basis
```

## 不要误吸收

```text
不要把 Obsidian link 当 reviewed relation。
不要把 graph view 当 knowledge graph authority。
不要把课程 shared vault 当 reviewed wiki。
不要把学生提交的 vault 当自动评分证据。
不要忽略培训、设备、教师维护、手写/PDF 工作流这些现实成本。
```

## Next Review Trigger

触发复查的条件：

```text
出现真实课堂实践报告或学生反馈
VAKS 开始设计教育/学习用 workbench
VAKS 开始设计 shared vault / collaborative intake
VAKS 开始处理手写笔记或 PDF 批注 source intake
```
