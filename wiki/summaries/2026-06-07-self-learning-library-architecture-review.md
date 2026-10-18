---
type: library_review
status: draft
library_name: "Self-Learning Library"
repo_url: https://github.com/LLK-LL/Self-Learning-Library
source_url: https://github.com/LLK-LL/Self-Learning-Library
paired_video: raw/videos/2026-06-07-bilibili-self-learning-library-source.md
checked_commit: 046daf301b361b6cd8de43114b2fdd780adadc0f
commit_time: "2026-06-05T11:24:44+08:00"
source_status: active
reviewed_at: 2026-06-07
domain: local self-learning knowledge-base harness for Codex-style AI work
related_projects:
  - verified-action-knowledge-system
current_branch:
  - local-harness
  - activation-tier
  - feedback-ledger
  - review-queue
  - context-pack
extracted_patterns:
  - local-harness-as-ai-memory
  - correction-to-rule-loop
  - selective-rag-before-task
  - evidence-reasoning-output-layering
  - no-regression-guard-from-memory
  - workflow-governance-not-content-rule
fusion_decision: adapt
borrow_value: strong
confidence: medium
evidence_count: 18
cross_validated_with:
  - Bilibili BV1cM7C6BEsM transcript
  - README.md
  - PROJECT_HARNESS_WORKFLOW.md
  - tools/kb_rag.py
  - tools/paper_iteration.py
negative_evidence:
  - runtime was not executed in this review
  - repository is a fresh prototype
  - paper-writing contents are domain-specific
  - lexical/graph scoring is diagnostic routing, not truth confidence
  - one token-savings report showed no token saving for its sample query
extension_potential: high
relations: []
tags:
  - self-learning-library
  - library-review
  - strong-borrow
  - local-harness
  - self-growing-knowledge-base
  - selective-rag
  - no-regression-guard
  - layered-vault
  - workflow-governance
  - candidate-only
---

# 库分析：Self-Learning Library

## 它解决什么问题

它解决的不是“怎么建一个好看的 Obsidian vault”，而是：

```text
AI 会忘记上下文
AI 会重复犯已经修过的错
用户纠错散落在聊天里
任务开始前不知道该读哪些旧规则
生成出来的总结/报告容易被误当成真理
```

它的回答是一个本地 harness：

```text
task starts
-> read project harness
-> retrieve relevant local rules
-> turn retrieval into a checklist
-> do the work
-> run no-regression guard
-> collect reusable lessons
-> only when requested, run iteration/generalization
```

## 核心设计

仓库由三部分组成：

- Root workflow: `AGENTS.md` 和 `PROJECT_HARNESS_WORKFLOW.md` 让 agent 从项目根目录看到约束。
- Layered vault: `10_Project_Change_Log` 到 `70_Iterative_Thinking` 表示工作记录、记忆、规则、治理、稳定规则、监督、冲突、受限规则和输出报告。
- Local scripts: `tools/kb_rag.py` 做轻量本地检索，`tools/paper_iteration.py` 做图谱/证据/冲突/泛化迭代。

架构重点：

```text
evidence layer = concrete memories and change logs
reasoning layer = rules, conflicts, limits, workflow governance
output layer = generated reports and summaries
```

仓库多次强调：只有 evidence layer 参与 support score，reasoning/output 只是导航和审计。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:1-22` | Local self-learning knowledge-base harness. | Treat local knowledge as an operating workflow for AI work. | Project claim, not independent proof. |
| `README.md:24-31` | Evidence, reasoning, output layers. | Strong layer boundary reference. | Layer names are not VAKS schema. |
| `README.md:36-60` | Mermaid task flow with RAG, checklist, no-regression, collection, iteration. | Full harness loop. | Must be adapted, not copied. |
| `README.md:127-133` | Default `kb_rag.py --limit 3`, avoid loading workflow/evidence/output for ordinary tasks. | Selective retrieval discipline. | Token saving is not guaranteed. |
| `PROJECT_HARNESS_WORKFLOW.md:1-26` | Harness is project-root primary workflow. | Project-local entrypoint matters. | Do not globalize. |
| `PROJECT_HARNESS_WORKFLOW.md:55-64` | Retrieve supervision/final/conflict/limited/intermediate layers; expand evidence only when needed; exclude output layer. | Good activation order. | Folder order is source-local. |
| `PROJECT_HARNESS_WORKFLOW.md:71-84` | Resolve conflicts by source priority and scope. | Scope-aware conflict handling. | Paper priorities not universal. |
| `PROJECT_HARNESS_WORKFLOW.md:86-107` | No-regression and purity guards. | Corrections become execution checks. | Manuscript-specific wording not reusable. |
| `PROJECT_HARNESS_WORKFLOW.md:123-136` | Script reuse guard before new helper creation. | Process governance can save repeated work. | Local command inventory differs. |
| `PROJECT_HARNESS_WORKFLOW.md:138-153` | Collection workflow routes change log, memories, rules, then iteration. | Correction-to-rule loop. | VAKS should map this to existing layers, not import folders. |
| `tools/kb_rag.py:268-296` | Lexical scoring and layer boosts. | Lightweight prioritization. | Score is routing, not truth. |
| `tools/kb_rag.py:333-378` | Graph-expanded retrieval via wikilinks/incoming links. | Association activation sample. | Graph expansion is not reviewed relation. |
| `tools/kb_rag.py:482-525` | Baseline vs selected retrieval token accounting. | Useful diagnostic. | Estimated tokens only. |
| `tools/kb_rag.py:533-605` | Evidence expansion gate and workflow route. | Lazy evidence expansion reference. | Returned context is not support. |
| `tools/paper_iteration.py:389-408` | Graph support from evidence-layer nodes only. | Strong support-boundary pattern. | Implementation is local/prototype. |
| `tools/paper_iteration.py:1425-1444` | Final vs limited rule promotion with conflicts. | Lightweight promotion intuition. | Thresholds are local. |
| `tools/paper_iteration.py:1873-1878` | Evidence rule: only memory/change notes are evidence graph. | Output/report separation. | Still not VAKS review authority. |
| `70_Iterative_Thinking/layered_graph_overview.md` | Layer flow and evidence-only support rule. | Good visual model. | Output layer, not evidence. |

## 当前支线价值

当前支线：

```text
VAKS activation / feedback / review queue / context pack / local harness design
```

它对当前支线：

```text
refines
```

具体价值：

- 给 VAKS 的 `Activation Tier` 一个具体工程样本：任务开始前只读相关局部上下文。
- 给 `Feedback Ledger` 一个闭环样本：纠错可变成 no-regression guard 和 review pressure。
- 给 `REVIEW_QUEUE` 一个分流样本：冲突、受限、泛化分开处理。
- 给 `Context Pack` 一个提醒：输出报告和检索命中不是证据。
- 给项目本地 `AGENTS.md` / harness 文件一个强参考：约束应在项目根可见。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Capture | Concrete task records and corrections become source-like memories. | adapt |
| Understand | Summaries and retrieved rules become task checklist. | adapt |
| Review | Conflict/limited/final split resembles review routing. | adapt carefully |
| Connect | Wikilinks and graph expansion help activation. | adapt |
| Activation | Strong selective retrieval pattern. | adapt |
| Context Pack | Do not load everything; expand evidence lazily. | adapt |
| Decision / Action | No-regression guard can protect action. | adapt with gates |
| Feedback | Corrections become future guards, not truth mutation. | adapt |
| Risk | Scores/reports can be mistaken for authority. | keep as risk |

## 值得提炼的模式

1. `project-local-harness-entrypoint`
2. `correction-to-no-regression-guard`
3. `selective-rag-before-context-pack`
4. `evidence-only-support-layer`
5. `conflict-limited-final-rule-routing`
6. `workflow-governance-separated-from-content`

## 不值得照搬的部分

- 论文写作 vault 内容。
- 数字文件夹命名。
- 一次 token-saving report 的指标结果。
- 具体 lexical score / layer boost 常数。
- 自动推广到 `40_Final_Generalized_Rules` 的本地阈值。

## Adoption Judgment

```yaml
fusion_decision: adapt
borrow_value: strong
borrow_order: P1
runtime_executed: false
promotion_status: none
```

人话：

```text
值得打 strong-borrow，算 P1。
但强的是 harness 逻辑，不是仓库内容。
它适合指导 VAKS 的本地记忆闭环和激活流程，不适合直接作为 reviewed knowledge 或主线自动化。
```
