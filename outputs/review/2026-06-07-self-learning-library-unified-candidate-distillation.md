---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
derived_from:
  - raw/videos/2026-06-07-bilibili-self-learning-library-source.md
  - raw/repos/2026-06-07-llk-ll-self-learning-library-source.md
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
  - local-harness
  - self-growing-knowledge-base
  - selective-rag
  - memory-correction-loop
  - workflow-governance
  - no-regression-guard
  - layered-vault
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - source_ref: raw/videos/2026-06-07-bilibili-self-learning-library-source.md
    selector_type: timestamp
    selector_value: "0036-0064"
  - source_ref: raw/videos/2026-06-07-bilibili-self-learning-library-source.md
    selector_type: timestamp
    selector_value: "0644-0912"
  - source_ref: raw/videos/2026-06-07-bilibili-self-learning-library-source.md
    selector_type: timestamp
    selector_value: "1015-1085"
  - snapshot_ref: raw/repos/_snapshots/LLK-LL-Self-Learning-Library-046daf301b361b6cd8de43114b2fdd780adadc0f.zip
    selector_type: source_code
    selector_value: README.md:1-60
  - snapshot_ref: raw/repos/_snapshots/LLK-LL-Self-Learning-Library-046daf301b361b6cd8de43114b2fdd780adadc0f.zip
    selector_type: source_code
    selector_value: PROJECT_HARNESS_WORKFLOW.md:55-153
  - snapshot_ref: raw/repos/_snapshots/LLK-LL-Self-Learning-Library-046daf301b361b6cd8de43114b2fdd780adadc0f.zip
    selector_type: source_code
    selector_value: tools/kb_rag.py:268-605
  - snapshot_ref: raw/repos/_snapshots/LLK-LL-Self-Learning-Library-046daf301b361b6cd8de43114b2fdd780adadc0f.zip
    selector_type: source_code
    selector_value: tools/paper_iteration.py:389-408
borrow_value: strong
borrow_order:
  - "P1: project-local harness that turns memory into task constraints"
  - "P1: correction -> memory -> rule -> conflict/limited/final routing"
  - "P1: selective local retrieval before work, with explicit evidence expansion boundary"
  - "P1: evidence/reasoning/output layer split; evidence is the only support-contributing layer"
  - "P1: no-regression guard from prior corrections"
  - "P2: lightweight lexical/graph retrieval and token accounting as diagnostic tooling"
  - "P3: paper-writing example vault as a domain-specific demo only"
avoid:
  - "Do not split the video and repository into two knowledge points."
  - "Do not import the paper-writing vault content into VAKS reviewed knowledge."
  - "Do not treat generated rules, graph scores, retrieval scores, or token-savings reports as truth confidence."
  - "Do not copy the exact folder names or workflow as a global default."
  - "Do not turn user correction memory into automatic truth mutation."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "approved VAKS task designs local harness behavior, memory activation, no-regression checks, or correction-to-rule routing."
  support_when: "designing VAKS candidate capture, activation tier, feedback ledger, context-pack preparation, or source-to-rule promotion gates."
  risk_when: "a retrieval/graph/report output is about to be mistaken for reviewed knowledge, truth support, or action basis."
  cold_references:
    - raw/videos/2026-06-07-bilibili-self-learning-library-source.md
    - raw/repos/2026-06-07-llk-ll-self-learning-library-source.md
    - raw/repos/_snapshots/LLK-LL-Self-Learning-Library-046daf301b361b6cd8de43114b2fdd780adadc0f.zip
tags:
  - candidate
  - provisional
  - self-learning-library
  - strong-borrow
  - P1
  - local-harness
  - self-growing-knowledge-base
  - selective-rag
  - memory-correction-loop
  - workflow-governance
  - no-regression-guard
  - layered-vault
  - evidence-boundary
  - candidate-only
---

# Self-Learning Library Unified Candidate Distillation

## Boundary

This note is provisional orientation.

It merges the Bilibili video and the GitHub repository into one knowledge point. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一个知识点，不拆

用户明确要求：

```text
视频先蒸馏，仓库做补充。
这都是一个知识点，别开两个。
```

所以这里的处理方式是：

```text
video = speaker's logic and motivation
repo = implementation/checkable structure
unified candidate = local self-learning harness for AI work
```

## 人话压缩

这个知识点对 VAKS 有价值，而且是 `strong-borrow / P1`。

它讲的不是“Obsidian 文件夹模板”，而是：

```text
让 AI 在本地有一套可回钻的工作记忆。
把用户纠错、失败、导师意见、成功基线记录下来。
下次做事前只检索相关规则，不把整个库塞进上下文。
遇到冲突就进冲突层，不能泛化就进受限层，反复验证的才进稳定规则。
最后用 harness/workflow 约束 AI 的执行顺序和回归检查。
```

对 VAKS 来说，最有价值的一句话是：

```text
记忆不是事实层；记忆是让下一次任务少犯错的约束和候选证据入口。
```

## Candidate Points

### 1. `local-harness-as-ai-memory`

候选结论：本地 Agent 的知识库应该是一个 harness，而不是普通资料夹。它要在任务开始前激活相关记忆，并把记忆转成可执行的检查项。

视频锚点：

- `0036-0064`: 知识库目标是让 AI 有记忆并迭代总结。
- `0192-0258`: 本地电脑作为“本地大脑”的来源。
- `0644-0667`: 记录犯错，让下次不要再犯同样错误。

仓库锚点：

- `README.md:1-22`
- `README.md:36-60`
- `PROJECT_HARNESS_WORKFLOW.md:1-26`

对 VAKS 的适配：

- 可借为 `Activation Tier` / `Dev Context` / `Context Pack` 的工作前激活模型。
- 不要把它变成自动写 truth 的 runtime。
- Harness 文件应是项目局部入口，不应成为全局模板默认。

### 2. `correction-to-rule-loop`

候选结论：用户纠错和工作记录可以进入一个分层循环：

```text
concrete change log
-> reusable memory
-> intermediate rule
-> conflict / limited / final generalized rule
-> future no-regression guard
```

视频锚点：

- `0680-0912`: 输入、分析/打分、冲突、泛化、受限、输出。

仓库锚点：

- `PROJECT_HARNESS_WORKFLOW.md:138-153`
- `tools/paper_iteration.py:1425-1444`

对 VAKS 的适配：

- 可增强 `Feedback Ledger`：负反馈/显式纠错应制造 review pressure 或 no-regression guard。
- 可增强 `REVIEW_QUEUE`：冲突、受限、泛化要分开。
- 不可直接让 correction 自动改 truth confidence。

### 3. `selective-rag-before-task`

候选结论：任务前先做轻量本地检索，只加载相关规则；普通任务不加载全部证据，不加载输出层。

仓库锚点：

- `README.md:127-133`
- `PROJECT_HARNESS_WORKFLOW.md:55-64`
- `tools/kb_rag.py:482-605`

对 VAKS 的适配：

- 适合 VAKS 的 `Activation Tier` 和 `Context Pack` 生成。
- 普通 query 轻；promotion / action basis 才严格。
- 检索结果是 activation，不是 support。

边界：

```text
retrieval hit != evidence support
score != confidence
selected context != reviewed knowledge
```

### 4. `evidence-reasoning-output-layering`

候选结论：本地知识库应该把证据、推理/规则、输出报告分开，只有证据层可以贡献 support。

仓库锚点：

- `README.md:24-31`
- `tools/paper_iteration.py:389-408`
- `tools/paper_iteration.py:1873-1878`
- `paper_writing_obsidian_vault/70_Iterative_Thinking/layered_graph_overview.md`

对 VAKS 的适配：

- 与 VAKS 的 raw / candidate / reviewed / action basis 边界高度相容。
- 可作为“输出层不是证据”的反复提醒。
- 适合形成一个未来轻量 diagram 或维护检查项。

### 5. `no-regression-guard-from-memory`

候选结论：历史纠错不只是归档，还能变成下一次任务结束前的 no-regression guard。

仓库锚点：

- `README.md:18-21`
- `README.md:179-190`
- `PROJECT_HARNESS_WORKFLOW.md:86-107`

对 VAKS 的适配：

- 对用户明确说过的错误、偏好、边界很有价值。
- 适合放在 action 前的 lazy gate。
- 不能让“用户曾经说过”自动变成事实支持。

### 6. `workflow-governance-not-content-rule`

候选结论：工作流规则和内容规则必须分开。流程可以约束 AI 怎么做，但不应污染最终内容或 reviewed knowledge。

仓库锚点：

- `PROJECT_HARNESS_WORKFLOW.md:86-107`
- `PROJECT_HARNESS_WORKFLOW.md:123-136`
- `tools/paper_iteration.py:1425-1444`

对 VAKS 的适配：

- 很适合 VAKS 的 process evidence / approval integrity 边界。
- 可提醒：review checklist、dashboard、maintenance report 都不是 truth。

## 对 VAKS 的强价值

强在四点：

1. 它把“记忆”做成任务前激活和任务后纠错循环，而不是静态笔记。
2. 它把“检索”限制在选择性上下文，不让全部 vault 变成 prompt 噪声。
3. 它把“泛化/冲突/受限”拆开，避免把局部规则误升成通用规则。
4. 它把“输出报告”明确放在 output/audit 层，不让报告变成证据本身。

## 不能直接借

- 论文写作 vault 的具体内容不能进 VAKS。
- `10/20/30/40/45/50/60/70` 这套数字文件夹不应原样复制进主线。
- 轻量 RAG 的 lexical/graph score 不能变成 confidence。
- `kb_rag_token_savings_latest.md` 的一次 token 结果不能当性能结论。
- 视频里的模型评价、产品趋势、网页端评价，都是 speaker opinion，不是事实依据。

## 标签等级

```yaml
tagging_decision: tagged
tag_level: strong-borrow
borrow_value: strong
borrow_order_primary: P1
```

人话：

```text
算 P1。
它值得 VAKS 优先吸收为“本地 harness / 纠错记忆 / 选择性检索 / no-regression guard”的候选参考。
但只进候选层，不进 reviewed knowledge，不直接变主线规则。
```

## 下一步触发条件

重新打开这条候选的条件：

- VAKS 要设计项目本地 `AGENTS.md` / harness 入口。
- VAKS 要做 Activation Tier 到 Context Pack 的选择性检索。
- VAKS 要把用户纠错变成 no-regression guard。
- VAKS 要建立 conflict / limited / generalized 的轻量晋级流程。
- 有人把 retrieval score、graph score、generated report 当 truth 时，需要拿这条做风险提醒。
