---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - ArthurYangX/nano-NotebookLM
related_concepts:
  - evidence-backed-design-validation
  - source-verification-and-trust-model
related_projects:
  - verified-vault
adoption_status: adapt
tags:
  - graph-layer
  - human-review
  - overlay
  - ai-generated-graph
  - provenance
evidence_count: 1
confidence: high
negative_evidence:
  - full-app-overengineering-before-clean-markdown-vault
---

# 设计模式：Generated Graph + Human Edit Overlay

## 一句话定义

AI 生成的图谱和人类修改不要写进同一个文件；系统图谱保持可重建，人类编辑以 sidecar op log 保存，每次读取时 replay overlay。

## 解决的问题

AI 重新抽取图谱时，容易覆盖人类校正。

如果直接改生成文件，就分不清：

- 哪些关系是 AI 自动抽的。
- 哪些节点是人类确认的。
- 哪些删除是人工判断。
- 哪些内容可以重建，哪些必须保留。

## 核心机制

```text
knowledge_graph.json       系统生成，可重建
mindmap_edits.json         人类编辑 op log

GET graph:
  load generated graph
  load edit ops
  replay ops
  return overlayed graph
```

编辑类型：

- add_node
- update_node
- delete_node
- add_edge
- delete_edge

## 对我们资料库的适配

未来可改成：

```text
compiled_graph.json        AI 编译关系
review_overlay.json        人类审定/驳回/修正
adoption_overlay.json      已采纳实现记录
```

或在 Markdown 文件层：

```text
wiki/claims/*.md           AI 候选主张
wiki/reviews/*.md          人类审查记录
wiki/decisions/*.md        采纳决策
```

关键思想不是文件名，而是：

```text
generated != reviewed
reviewed != adopted
```

## 来源证据

- `api/server.py`：`mindmap_edits.json` sidecar、`apply_edit_ops_with_results`、`_overlay_user_edits`。
- `tests/test_mindmap_edit.py`：验证 replay idempotent、add/update/delete edge、未知 op 不崩、GET overlay 生效。
- `nano_notebooklm/kb/graph_search.py`：GraphRAG 也会应用 delete overlay，避免被用户删除的节点继续参与检索。

## 标签与量化

- domain: graph_governance
- problem: preserving_human_review_over_regeneration
- maturity: proven-in-repo
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 风险边界

- op log 长期增长后需要 compact。
- overlay replay 必须有幂等性测试。
- 删除节点必须同时删除相关边，避免 dangling relation。
- 节点文本变更后，需要清理旧 embedding/cache。

## 项目融合建议

这个模式适合中期采用。

它能补我们“AI 编译”和“人类验证”之间的边界，防止 AI 重跑时覆盖已经审定过的知识。

