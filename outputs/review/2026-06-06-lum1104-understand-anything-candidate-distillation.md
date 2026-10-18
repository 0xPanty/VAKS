---
type: repo_candidate_distillation
status: candidate_only
created_at: 2026-06-06
source_record: raw/repos/2026-06-06-lum1104-understand-anything-source.md
source_url: https://github.com/Lum1104/Understand-Anything
checked_commit: 5c1e35f90be029efb012a41e1122b08abef5cbb2
truth_boundary: visual analysis workbench candidate only; not reviewed knowledge; not architecture decision; not action basis
review_priority: medium
projects:
  - verified-action-knowledge-system
tags:
  - understand-anything
  - knowledge-graph
  - visual-workbench
  - karpathy-llm-wiki
  - candidate-only
---

# Understand Anything Candidate Distillation

## 一句话人话结论

这个库对 VAKS 有帮助，但不是因为它能自动把知识变真，也不是因为它的图很酷。

真正可借的是这个工作台思路：

```text
先用确定性解析把 Markdown / wikilink / index / raw source 扫成稳定骨架；
再让 LLM 只补隐含实体、候选主张、候选关系；
最后用 dashboard 让人看见关系、邻域、遗漏、冲突和变更影响。
```

对 VAKS 来说，它适合做：

```text
视觉分析工作台
候选关系发现
review 前的地图
source / candidate / overlay 的导航层
新窗口 onboarding 图谱
```

不适合做：

```text
truth layer
evidence support authority
review automation
主架构替代品
全库默认自动扫描器
```

## 它到底是什么

Understand Anything 是一个多平台 agent skill / plugin。主线功能是分析 codebase，把文件、函数、类、依赖、层级、导览和领域流程做成 `.understand-anything/knowledge-graph.json`，再用 dashboard 展示。

但对我们更关键的是 `/understand-knowledge`：

```text
target folder
-> parse-knowledge-base.py
-> scan-manifest.json
-> article-analyzer batches
-> merge-knowledge-graph.py
-> .understand-anything/knowledge-graph.json
-> dashboard
```

它的知识库模式不是普通 Obsidian graph，也不是 RAG 问答。它更像：

```text
Markdown wiki 的 typed graph compiler
```

它会把 wiki 页面、topic、source、entity、claim 变成节点，把 wikilink、category、cites、contradicts、builds_on 等变成边。

## 机制拆解

### 1. Deterministic Parse First

`parse-knowledge-base.py` 先做确定性工作：

```text
检测 index.md / wiki/ / raw/
提取 wikilink
提取 frontmatter / headings / first paragraph
从 index.md 生成 topic
把 wikilink 变成 related edge
把 index section 变成 categorized_under edge
把 raw/ 文件变成 lightweight source node
计算 backlinks
```

这个很适合 VAKS。因为它把最容易做稳的东西先做稳：路径、文件、wikilink、分类、反链。

VAKS 可借：

```text
不要一上来让 LLM 读全库并发明图谱。
先用 repo-local parser 生成可复现 skeleton。
```

### 2. LLM Only Adds Inference

`article-analyzer` 的边界写得很清楚：显式 wikilink 已经由 parser 捕获，它只补隐含实体、claims 和关系。

可借点：

```text
LLM enrichment 是候选补全，不是基础事实。
LLM 失败时 deterministic scan-manifest 仍然可用。
```

这和 VAKS 很合拍：

```text
parser output = structure/provenance/navigation
LLM output = candidate point / candidate relation / review question
review output = only later can become standing knowledge
```

### 3. Typed Node / Edge Vocabulary

它的 knowledge node type 是：

```text
article
entity
topic
claim
source
```

edge type 是：

```text
cites
contradicts
builds_on
exemplifies
categorized_under
authored_by
related
similar_to
```

这比 Obsidian 原生 graph 有意义，因为 Obsidian graph 主要看到“有链接/没链接”。Understand Anything 试图让边有语义。

VAKS 可借：

```text
把图谱边做成可读标签。
让 reviewer 看到这是 support、challenge、scope、supersedes、review_due，还是只是 related。
```

VAKS 不应直接照抄：

```text
claim 太粗。
cites 太弱。
source 太轻。
```

VAKS 需要更严：

```text
claim_under_review
candidate_point
evidence_item
reviewed_claim
reviewed_relation
risk
decision
feedback_event
review_due
action_basis
```

### 4. Merge / Normalize / Dedup

`merge-knowledge-graph.py` 做三件有用的事：

```text
node / edge type alias normalization
entity name dedup
dangling edge drop
layer and tour build
```

VAKS 可借的是 graph hygiene：

```text
候选图谱可以自动检查 dangling refs、重复实体、缺失 required fields。
```

但要加一条 VAKS 规则：

```text
不能静默丢掉重要边。
如果 edge 被 drop，要进入 review / warning / manifest，而不是假装没发生。
```

### 5. Dashboard As Workbench

dashboard 有几点对 VAKS 很有用：

```text
typed node color
layer / cluster overview
focus mode 1-hop neighborhood
search
node details
tour / guided walkthrough
export JSON / PNG / SVG
```

这正好可以帮我们做“资料图标化/图谱化分析”：

```text
看到某个 source 影响了哪些 candidate
看到某个 claim 周围有哪些 support / challenge / risk
看到某个 project overlay 借了哪些 generic knowledge point
看到一个新资料和旧资料撞在哪里
看到哪些 source 只有孤立节点没有进入 review
```

### 6. Codebase Side Also Useful

它的 `/understand` 对 VAKS 不是主要目标，但可以帮助看 VAKS 的工具代码：

```text
tools/
templates/
scripts
source-card runners
finalization connectors
```

以后如果 VAKS 工具链变复杂，可以用它做 code/tooling architecture map。当前不必。

## 对 VAKS 的高价值借鉴

### A. Visual Workbench, Not Truth Layer

最该吸收的一句话：

```text
graph is a workbench, not a judge.
```

在 VAKS 里，Understand Anything 只能落在：

```text
activation
diagnostic
candidate review preparation
onboarding
source navigation
relationship pressure
```

不能落在：

```text
truth confidence
reviewed relation
evidence support
action readiness
decision approval
```

### B. Skeleton Before Semantics

VAKS 的候选图谱也应该两段式：

```text
Phase 1: deterministic skeleton
- file path
- source card
- artifact links
- wikilinks
- frontmatter
- explicit relation fields
- review queue links

Phase 2: semantic candidate overlay
- possible entity
- candidate point
- possible support/challenge
- missing evidence
- contradiction pressure
- stale/superseded signal
```

### C. Claim Extraction Needs Evidence Packet

Understand Anything 的 claim node 对普通 wiki 很自然，但 VAKS 不能接受裸 claim。

VAKS 适配规则：

```text
LLM extracted claim -> candidate_point
candidate_point + source anchor + warrant + scope/risk + challenge check -> evidence packet
evidence packet reviewed -> reviewed claim / relation
```

少一步都不能变 truth。

### D. Graph Diff Can Become Review Due Radar

它宣传 diff impact analysis。对 VAKS 来说更有意思的是：

```text
new source added
old source updated
candidate relation changed
decision dependency touched
reviewed claim near changed candidate
```

这些可以变成：

```text
review_due hints
context pack freshness warning
downstream affected note list
```

但仍然只是提示，不是自动 invalidation。

### E. Tour Is Useful For Recovery

VAKS 很需要新窗口 recovery 和 reviewer onboarding。

Understand Anything 的 tour 思路可借为：

```text
从 source intake
到 candidate point
到 review gate
到 reviewed knowledge
到 context pack / action basis
到 use ledger / feedback
```

这类 tour 可以是视觉恢复词 / reviewer guide，而不是主 schema。

## 风险和不吸收项

### 1. 图谱权威化风险

最危险的误用：

```text
图上连了线，所以它们有 reviewed relation。
```

VAKS 必须改成：

```text
图上线 = 看见候选关系 / 显式链接 / 导航邻域
reviewed relation = 另有 reviewed record 支撑
```

### 2. `cites` 语义过弱

Understand Anything 里的 `cites` 更像“文章提到/引用 raw source”。

VAKS 的 Evidence Support Check 要求：

```text
source span supports the specific point or relation
```

所以不能把 `cites` 直接当 support。

### 3. Source Node 太轻

它的 raw source node 只是 filename + size，不解析 PDF/binary。

VAKS 需要：

```text
source record
raw artifact
transcript / text unit
evidence item
hash / capture metadata
source anchor
```

因此这个库可以显示 source，但不能代替 VAKS source intake。

### 4. 3000 字截断会漏证据

`parse-knowledge-base.py` 给 LLM 的文章内容截到前 3000 字。做 summary 可以，做 evidence review 不够。

VAKS 适配时要么：

```text
只把它当 candidate scan
```

要么：

```text
用 text-unit / source-anchor adapter 补足 evidence spans
```

### 5. 设计文档比当前实现更大

设计文档写了 Obsidian / Logseq / Dendron / Foam / Zettelkasten 等格式，但当前实际 `understand-knowledge` 目录只看到 Karpathy parser、merge script 和 skill 文件。

判断：

```text
不要按设计文档幻想全格式已成熟。
以当前落地实现为准。
```

### 6. 不要全局安装

Windows installer 会把技能链接到 agent skills 目录，Codex 可用。

但对 VAKS 当前主线：

```text
不建议现在全局安装。
先 sandbox copy / tiny fixture pilot。
```

原因：

```text
全局 skill 会改变 agent 环境；
全库扫描可能生成巨大 .understand-anything；
generated graph 容易被误读成主线资产。
```

## 建议吸收姿态

```text
watch_and_adapt_in_sandbox
```

不是：

```text
adopt_as_core_architecture
```

不是：

```text
install_and_run_on_main_vault_now
```

## 最小 pilot

如果后续要试，建议只做这个：

```text
创建 sandbox fixture:
  - 5 个 raw source records
  - 5 个 candidate distillations
  - 2 个 project overlays
  - 1 个 review queue note

手写或 adapter 生成 graph JSON:
  source_record -> candidate_distillation
  candidate_distillation -> candidate_point
  candidate_point -> support/challenge/scope/review_due
  project_overlay -> borrowed_generic_point

打开 dashboard 看:
  是否能帮助人发现遗漏/冲突/孤立节点
  是否能帮助 reviewer 快速进入
  是否会诱导把候选边当 truth
```

成功标准：

```text
减少定位成本
暴露遗漏/冲突
不污染 main wiki
不把 graph 当 truth
```

失败标准：

```text
图很漂亮但 reviewer 还是不知道证据在哪里
claim 节点没有 source anchor
edge 标签看起来像 reviewed relation
全库扫描后噪声比洞察多
```

## 候选结论

```text
candidate:vaks_visual_analysis_workbench
candidate:deterministic_parse_before_llm_relationships
candidate:graph_output_as_rebuildable_cache_not_truth
candidate:typed_edge_dashboard_for_candidate_review
```

一句话：

```text
它可以帮我们“看见资料之间的候选关系”，但不能帮我们“证明这些关系是真的”。
```

这正是 VAKS 可以借、也必须严防的地方。
