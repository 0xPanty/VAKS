---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "论文入库应从 PDF 文件变成 Obsidian 可审查知识节点包"
created_at: "2026-06-08"
created_by: Codex
processing_tier: medium
knowledge_status: candidate
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - raw/videos/2026-06-08-bilibili-pdf-to-obsidian-knowledge-node-source.md
projects:
  - verified-action-knowledge-system
topics:
  - paper-intake
  - source-bundle
  - pdf-to-markdown
  - obsidian-base
  - reference-linking
  - metadata-extraction
  - evidence-boundary
borrow_value: strong
borrow_order: P1
evidence_strength: low-medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P1
provisional: true
---

# 候选蒸馏：论文入库应从 PDF 文件变成 Obsidian 可审查知识节点包

## 一句话

这条视频对 VAKS 是 P1 借鉴：它给了一个论文类强来源进入资料库的具体形态。论文不应该只作为 PDF 躺在文件夹里，而应该进入一个 source bundle：

```text
PDF
-> Markdown full text
-> optional translated Markdown
-> images/assets
-> metadata/index page
-> summary
-> QA
-> glossary
-> reference links
-> Obsidian Base row
```

但这些自动产物都只是 raw/candidate。它们帮我们准备 review，不替我们完成 review。

## 为什么是 P1

这条直接影响 VAKS 的 source intake / paper intake：

```yaml
borrow_value: strong
borrow_order: P1
borrow_scope:
  - paper-intake
  - source-bundle
  - source-metadata
  - candidate-comprehension
  - reference-linking
  - context-pack-viewer
not_borrow_scope:
  - reviewed truth
  - evidence confidence
  - reviewed relations
  - action basis
```

原因很简单：论文是 VAKS 里天然的强来源类型。如果我们只存 URL、PDF 或摘要，后续 evidence-aware review 会很难。如果我们保留一个结构化 source bundle，后续审查、引用、关联和 context pack 都会轻很多。

## Candidate Point

VAKS 的论文入库可以分成三层：

```text
raw source layer:
  原 PDF、来源 URL、DOI、作者、期刊、发布日期、PDF -> Markdown 全文、图片 / 表格 / 附件。

candidate comprehension layer:
  AI 摘要、术语表、问答、中文翻译、阅读提纲、候选关键词。

candidate relation layer:
  参考文献识别、已有笔记匹配、候选双向链接、相同方法 / 相同问题 / 同一研究方向提示。
```

只有后续 Evidence Packet / Evidence Support Check 才能把某个论文结论变成 reviewed claim 或 action basis。

## 应该吸收

- 论文进入库时保留原 PDF 和 Markdown，不让翻译稿替代原文。
- 每篇论文生成索引页，记录 DOI、作者、期刊、年份、引用数、影响因子、分区、处理状态。
- 生成摘要、术语表、问答，但明确它们是 candidate comprehension。
- 参考文献自动识别和双链只作为 candidate relation。
- 用 Obsidian Base 做论文工作台视图，而不是 truth authority。

## 不应该吸收

- 不要让 AI 自动摘要直接进入 reviewed knowledge。
- 不要让自动双链直接进入 reviewed relation。
- 不要用影响因子 / 引用数 / 分区替代证据判断。
- 不要只保存中文翻译，不保留原文。
- 不要在没有数据源和时间戳的情况下高置信写入引用数、影响因子、分区。

## 对 VAKS 的最小落地建议

```text
不改 core schema。
先新增或明确 paper source bundle 模板：
  raw/videos 这条只是视频来源；
  未来论文来源应有 raw/papers 或 raw/articles/papers 的 source bundle。

每篇论文最少保留：
  source card
  original PDF pointer/hash
  markdown full text
  metadata/index
  candidate summary
  candidate glossary
  candidate QA
  reference-link candidates
```

如果要更轻：

```text
PDF -> Markdown -> source card -> candidate summary -> review queue
```

## 与现有 VAKS 层级的关系

```text
Capture:
  PDF / DOI / metadata / full text markdown.

Understand:
  summary / glossary / QA / translation.

Review:
  Evidence Packet checks exact claim against exact source span.

Connect:
  reference links are candidate until reviewed.

Activation / Context Pack:
  Obsidian Base can surface papers by topic, method, date, status, review queue.

Decision / Action:
  only reviewed evidence can support action.

Use Ledger / Feedback:
  record whether a paper was useful, misleading, outdated, or superseded.
```

## Risk / Inhibition

```text
risk:
  PDF to Markdown can lose tables, formulas, captions, and section structure.
  Translation can distort technical terms.
  AI summary can omit limitations.
  Auto reference links can overconnect unrelated papers.
  Citation counts and impact factors can be stale or source-dependent.

inhibition:
  record converter and metadata source.
  keep original PDF and original English Markdown.
  label all AI outputs as candidate.
  require review before claim promotion.
  mark auto links as candidate_relation.
```

## Support / Challenge Review

- What supports it: 视频描述和转写都明确提出 PDF -> Markdown -> metadata/index -> summary/glossary/QA -> reference links -> Obsidian Base 的流程。
- What challenges it: 视频没有给具体工具名、转换质量测试、数据源、字段 schema 或失败案例。
- Challenge severity: major but bounded
- Scope limits: 只适用于 paper/source intake workflow，不适用于 truth promotion。
- Known risks: 结构丢失、翻译偏差、AI 摘要幻觉、自动关系误连、指标过期。
- Review again when: 准备实现 VAKS 论文入库模板、PDF 转 Markdown pipeline 或 Obsidian Base 论文视图时。
- Action readiness: not_ready

## 融合判断

```text
fusion_decision: adapt
borrow_value: strong
borrow_order: P1
evidence_strength: low-medium
implementation_cost: medium
integration_fit: high
reversibility: high
```
