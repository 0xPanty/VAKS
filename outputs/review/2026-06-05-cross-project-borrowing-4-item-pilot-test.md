---
type: pilot_test_report
status: pilot
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: cross-project-borrowing-pilot
test_items: 4
formalization_status: candidate-only
truth_boundary: not reviewed knowledge, not architecture decision, not action basis
---

# Cross-Project Borrowing 4-Item Pilot Test

## 结论先说

这个三层流程能跑通，而且比“每条资料都写适合 VAKS / 不适合 VAKS”更清楚。

但这轮测试**不回头修改本地已有 raw source card**。原因很简单：这些 source card 已经是来源备案和候选蒸馏记录，不能为了试点把旧资料改乱。

本轮只新增一份测试报告，用已有 4 个本地材料验证：

```text
raw source card
-> source routing
-> candidate pattern
-> VAKS borrowing ledger
```

## 测试样本

| Test | Source | Type | Why selected |
|---|---|---|---|
| T1 | `raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source.md` | short video | 低到中等价值短视频，测试是否能轻量路由，不强行膨胀 |
| T2 | `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md` | visual-heavy video | 高信息量 RAG 工作台视频，测试一个 source 能否路由到多个 pattern |
| T3 | `raw/repos/2026-06-04-langchain-miniopenclaw-source.md` | repo | repo/code review，测试工作台类模式和风险能否抽离 |
| T4 | `raw/papers/2026-06-04-rf-mem-recollection-familiarity-source.md` | paper | 论文材料，测试实验结果如何只进入 activation pattern，不进入 truth |

## T1：RAG 翻车短视频

### 原 source card 里有什么

这条短视频讲的是 RAG 知识库上线后回答混乱。主要候选点是：

- 按固定字数切分会破坏文档结构。
- 纯向量召回不够，可能需要 rerank / query expansion。
- prompt 要限制只用参考资料、无资料不编。
- 视频里的工具名和指标数字不可靠，ASR 有误听。

### 三层测试

```text
Source Card:
  保留视频来源、ASR、时间轴、候选理解、风险。

Source Routing:
  transferable_candidates:
    - source structure before chunking
    - rerank / query expansion as retrieval quality tools
    - prompt boundary as answer constraint

  source_bound_constraints:
    - 示例指标未验证
    - 工具名 ASR 不可靠
    - 经验叙事不是独立证据

Candidate Pattern:
  - source-structure-first-rag
  - retrieval-is-activation-not-truth
  - simple-first-retrieval-baseline

VAKS Borrowing Ledger:
  source-structure-first-rag: adapt
  retrieval-is-activation-not-truth: adapt
  simple-first-retrieval-baseline: watch
```

### 测试观察

这个样本证明：低到中等价值视频不需要在 source card 里写一大段“适合 VAKS”。它只要路由到已有 pattern 就够。

这能减轻以后短视频 intake 的负担。

## T2：RAGLab 视觉工作台视频

### 原 source card 里有什么

这条视频主要信息在画面：RAGLab 画布展示 Simple RAG、Fusion Retrieval、BM25、RRF、Query Rewriting、HyDE、Reranking、Context Window、GraphRAG、PageIndex、TreeIndex、RAGAS 等节点。

关键候选点是：

- RAG 流程需要可视化/可检查。
- 文档结构和表格会影响 chunking。
- BM25 + vector + RRF 说明检索不是单一路线。
- RAGAS 是诊断，不是 truth。
- GraphRAG 关系和 community summary 是候选上下文，不是 reviewed relation。

### 三层测试

```text
Source Card:
  保留 ASR、视觉观察、关键帧、17 项画面列表、RAGLab 节点说明。

Source Routing:
  transferable_candidates:
    - visual retrieval workbench
    - source structure first
    - retrieval pipeline visibility
    - RAGAS/eval as diagnostics
    - graph/entity/relation as candidate context

  source_bound_constraints:
    - RAGLab UI 是产品/演示特定
    - RAGAS 分数不是证据支持
    - 可视化节点不是 reviewed relation

Candidate Pattern:
  - visual-workbench-for-retrieval-diagnostics
  - source-structure-first-rag
  - retrieval-is-activation-not-truth
  - graph-and-ontology-as-candidate-context
  - search-to-analysis-before-answer

VAKS Borrowing Ledger:
  visual-workbench-for-retrieval-diagnostics: prototype
  source-structure-first-rag: adapt
  retrieval-is-activation-not-truth: adapt
  graph-and-ontology-as-candidate-context: watch
```

### 测试观察

这个样本证明：高信息量视频可以路由到多个 pattern，但 source card 不需要承担完整项目判断。

它也暴露一个风险：如果 pattern 太多，会让 routing 表变重。后续做减法时，可以把弱路由放到 source card，不一定都进 pattern bank。

## T3：miniopenclaw repo

### 原 source card 里有什么

这个 repo 是本地运行、文件优先、可审计的 AI Agent 工作台原型。候选点是：

- Memory、prompt、skills、workspace 以文件形式可见。
- 向量索引只是可重建缓存。
- 前端 inspector 能看 tool/retrieval/raw messages。
- 会话和工具记录落盘。
- 风险是未跑通 clone/runtime，license 未确认，terminal tool 安全薄，memory 没有 VAKS 分层。

### 三层测试

```text
Source Card:
  保留 repo URL、代码锚点、限制、未验证状态、license 风险。

Source Routing:
  transferable_candidates:
    - file-first agent workbench
    - prompt / skill / memory as visible files
    - index as rebuildable cache
    - transparent tool/retrieval stream

  source_bound_constraints:
    - 未本地运行
    - 未观察到 license
    - terminal tool 安全不足
    - memory 单文件不能当 truth

Candidate Pattern:
  - file-first-agent-workbench
  - skills-and-prompts-as-visible-files
  - memory-granularity-and-quarantine
  - visual-workbench-for-retrieval-diagnostics

VAKS Borrowing Ledger:
  file-first-agent-workbench: watch
  skills-and-prompts-as-visible-files: watch
  memory-granularity-and-quarantine: watch
  visual-workbench-for-retrieval-diagnostics: prototype
```

### 测试观察

这个样本证明：repo 类 source 很适合被拆成“可迁移机制”和“源内限制”。以前写“VAKS 可借鉴 / 不可借鉴”容易让它看起来像项目结论；现在限制留在 source routing，VAKS 的姿态留在 ledger，更干净。

## T4：RF-Mem paper

### 原 source card 里有什么

RF-Mem 论文提出 Familiarity / Recollection 双路径：先 probe retrieval，根据平均相似度和熵判断是否熟悉；熟悉走快路径 Top-K，不熟走聚类和多轮 recollection 扩展。

候选点是：

- 检索深度可以按 query 熟悉度/不确定性切换。
- 慢路径要受 beam/fanout/rounds 预算限制。
- 论文结果是实验设置下的 retrieval 结果，不证明 VAKS 应采用。
- 相似度/熵只是 uncertainty proxy，不是 truth。

### 三层测试

```text
Source Card:
  保留论文元数据、方法结构、实验结果、limitations、和视频的补充关系。

Source Routing:
  transferable_candidates:
    - adaptive retrieval depth
    - fast path for familiar query
    - slow path for ambiguous memory query
    - budgeted retrieval expansion

  source_bound_constraints:
    - 主要验证 dialogue-style personalized memory
    - similarity/entropy 不是可靠 truth signal
    - benchmark 数字不等于 VAKS action basis
    - sensitive memory resurfacing risk

Candidate Pattern:
  - adaptive-retrieval-depth
  - memory-granularity-and-quarantine
  - retrieval-is-activation-not-truth

VAKS Borrowing Ledger:
  adaptive-retrieval-depth: watch
  memory-granularity-and-quarantine: watch
  retrieval-is-activation-not-truth: adapt
```

### 测试观察

这个样本证明：论文结果可以进入 pattern，但不需要进入 truth。实验数字只增加 review priority / design pressure，不直接支持项目采用。

## 4 个样本后的总体判断

### 有用的地方

1. Source card 可以变轻。

以后单条资料不必长篇写“适合 VAKS / 不适合 VAKS”。它只要写候选点和路由提示。

2. Pattern bank 能减少重复。

例如 `retrieval-is-activation-not-truth` 在四个样本里都出现。以前每条卡都要重复写一遍；现在可以统一成一个候选模式。

3. Project ledger 让 VAKS 判断更集中。

VAKS 借不借、借到哪里、要过什么 gate，不再散落在每条 source card。

4. 不同材料类型都能适配。

短视频、视觉视频、repo、paper 都能走这套流程。

### 风险

1. Pattern 路由可能过多。

RAGLab 这种重资料很容易路由到 5 个以上 pattern。后续需要做减法：只保留强路由，弱路由留在 source card。

2. Pattern bank 可能变成名词堆。

必须坚持 problem-centered。没有 problem statement 的 pattern 不许保留。

3. Ledger 可能太像 ADR。

VAKS ledger 只能写姿态：watch/prototype/adapt/reject。不能写成正式 decision。

4. 旧 source card 不应批量回改。

已有 source card 是历史 intake 记录。可以在新流程中使用它们，但不要为了统一格式批量重写。

## 是否修改本地旧卡

当前建议：**不改。**

原因：

- 旧卡已经有来源、ASR、候选点和边界，是有效备案。
- 批量回改会增加风险，也会污染工作区。
- 三层试点只需要在 `outputs/review` 做 overlay。
- 未来新 intake 再逐步使用新写法即可。

如果以后确实要改模板，也应该先改模板，不回写旧卡。

## 下一步建议

```text
1. 继续用新视频/仓库测试这套流程。
2. 新 source card 逐步少写“适合 VAKS / 不适合 VAKS”。
3. 只在有明显跨项目价值时新增 candidate pattern。
4. VAKS ledger 只记录有真实项目路由的 pattern。
5. 每 10 条 source intake 后做一次减法：
   - 合并重复 pattern
   - parked 抽象但没用的 pattern
   - 删除没有 problem 的漂亮名词
```

## 当前 Verdict

四个样本测试支持这套三层拆分继续试。

最稳做法是：

```text
旧卡不回改；
新资料按三层路由；
pattern bank 小步增量；
VAKS ledger 集中记录项目姿态；
所有内容继续留在 outputs/review candidate-only。
```

