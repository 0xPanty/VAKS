---
type: implementation_note
status: pilot
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: cross-project-borrowing-pilot
formalization_status: candidate-only
truth_boundary: not reviewed knowledge, not architecture decision, not action basis
---

# Cross-Project Borrowing Pilot Implementation

## 这次落地了什么

根据 Pro 的完整建议，本次先在 `outputs/review/` 下落地三层试点：

```text
outputs/review/source_cards/
  INDEX.md
  2026-06-04-external-intake-source-routing-ledger.md

outputs/review/candidate_pattern_bank/
  INDEX.md
  source-structure-first-rag.md
  retrieval-is-activation-not-truth.md
  file-first-agent-workbench.md
  adaptive-retrieval-depth.md
  memory-granularity-and-quarantine.md
  graph-and-ontology-as-candidate-context.md
  visual-workbench-for-retrieval-diagnostics.md
  skills-and-prompts-as-visible-files.md
  search-to-analysis-before-answer.md
  simple-first-retrieval-baseline.md

outputs/review/project_borrowing_ledgers/
  INDEX.md
  VAKS.md
```

## 为什么 Source Card 层没有复制 raw files

现有正式 source cards 已经在：

```text
raw/videos/
raw/repos/
raw/papers/
```

因此 `outputs/review/source_cards/` 只做 routing overlay，不复制全文、不替代 raw source card。

这更符合 VAKS 边界：

```text
raw/ = source provenance and source record
outputs/review/source_cards/ = routing overlay for pilot
```

## 三层职责

```text
Source Card / Source Routing:
  这条资料说了什么，有哪些可迁移候选点，哪些不能泛化，可能路由到哪些模式。

Candidate Pattern Bank:
  多个来源里反复出现的可迁移机制。它不是 truth，也不是项目采用。

Project Borrowing Ledger:
  某个项目对某个 candidate pattern 的姿态：watch / prototype / adapt / reject / superseded。
```

## Pro 关键规则如何落地

### Source Card 不写成结论

这次没有把 source routing 写成“VAKS 应采用”。表格里只写：

- transferable candidates
- source-bound constraints
- candidate pattern routes
- project ledger routes

### Pattern 必须 problem-centered

每个 pattern 都写了：

- problem addressed
- mechanism
- applicability
- non-goals and trade-offs
- derived sources
- aliases / near duplicates
- risk of overreach

### Ledger 只记录项目姿态

`VAKS.md` 只写项目对 pattern 的 disposition：

```text
watch
prototype
adapt
reject
superseded
```

没有写成 ADR，也没有写成 reviewed knowledge。

### Source Family 防止假独立支持

source routing ledger 加了 source family：

- sf-rag-engineering
- sf-graph-ontology
- sf-agent-workbench
- sf-memory-retrieval
- sf-obsidian-workflow

它们用于避免“同一作者/同一 repo/同一技术宣传链路的多个材料 = 多个独立支持”的错觉。

### 不引入 truth

所有新文件都写在 `outputs/review/`，并明确：

```text
candidate-only
not reviewed knowledge
not architecture decision
not action basis
```

## 第一批测试素材

本次使用 2026-06-04 已 intake 的材料做测试，包括：

- 21 个 video source cards。
- 2 个 repo source cards。
- 2 个 paper source cards。

这些材料主要覆盖：

- RAG 工程与可视化工作台。
- RF-Mem / MemGAS / CoMe 记忆检索。
- miniopenclaw / OpenClaw / Karpathy LLM Wiki 本地 agent workbench。
- ontology / knowledge graph / METHONTOLOGY。
- Obsidian local workflow。

## 现在不做什么

本次不做：

- 不改 `SCHEMA.md`。
- 不改 `ARCHITECTURE_PRINCIPLES.md`。
- 不把 Candidate Pattern Bank 放进 `wiki/`。
- 不把 Borrowing Ledger 变成 ADR。
- 不把任何 pattern 标成 adopted。
- 不把 retrieval / rerank / dashboard / feedback / source count 接进 truth confidence。
- 不 commit / push。

## 如何一边试一边做减法

接下来几轮外部资料 intake 后，检查：

```text
1. Source card 是否更轻？
2. Pattern bank 是否真的减少重复表达？
3. VAKS ledger 是否能清楚说明“借 / 不借 / 借到哪”？
4. 有没有 pattern 没人引用、太抽象、只有漂亮名词？
5. source_family_id 是否真的抑制假独立支持？
```

做减法规则：

- 没有 problem statement 的 pattern 删除或合并。
- 只来自一个低价值短视频、且无跨项目价值的 pattern parked。
- 近义 pattern 合并到 canonical slug。
- 没有 project route 的点留在 source card，不升 pattern。
- ledger 里长期 watch 但无动作的项可以 parked。

## 当前判断

这次不是“正式引入新架构”，而是把 Pro 的完整逻辑先跑成一个可检查试点。

试点成功的标志不是文件更多，而是：

```text
source 更轻；
pattern 更少更准；
project borrowing 更清楚；
truth 边界更稳。
```

