---
type: library_review
status: draft
library_name: garrytan/gbrain
repo_url: https://github.com/garrytan/gbrain
source_url: raw/repos/2026-05-26-gbrain-source.md
reviewed_at: 2026-05-26
domain:
  - second-brain
  - knowledge-engine
  - agent-memory
related_projects:
  - verified-knowledge-system
extracted_patterns:
  - markdown-system-of-record-derived-indexes
  - compiled-truth-plus-append-only-timeline
  - epistemology-takes-facts-layer
  - schema-packs-as-living-contract
  - think-gather-synthesize-gap-analysis
fusion_decision: adapt
confidence: high
evidence_count: 1
cross_validated_with:
  - llm_wiki
  - nano-NotebookLM
negative_evidence:
  - copying-full-second-brain-runtime-before-schema-stabilizes
extension_potential: high
---

# 库分析：garrytan/gbrain

## 它解决什么问题

gbrain 解决的不是“资料怎么搜索”，而是“一个 agent / human brain 如何把资料、关系、事实、观点、时间线和回答组织成可长期维护的知识引擎”。

它的目标比普通 RAG 高一层：搜索只返回候选，gbrain 试图返回带证据、判断和缺口的答案。

## 核心设计

```text
Markdown brain repo = system of record
DB / vector index / graph edges / cache = derived indexes
think = gather evidence + synthesize answer + citations + gaps
dream cycle = periodic maintenance + facts -> takes + pattern/concept synthesis
schema pack = page/link/fact rules as versioned contract
```

## 值得提炼的模式

1. `brain / memory / session` 分层：世界知识、agent 操作偏好、当前任务上下文不要混在一起。
2. `compiled truth + timeline`：当前结论和证据历史分离，结论可更新，证据链保留。
3. `takes / facts`：热事实和冷判断分层，并记录谁相信、何时说、置信度、权重、来源。
4. `schema packs`：把页面类型、关系类型、可抽取性、路由规则做成可版本化契约。
5. `think pipeline`：不直接把搜索结果塞给 LLM，而是聚合多路证据后再生成答案和 gaps。
6. `dream cycle`：定期维护、沉淀、找 pattern、找矛盾、重建索引。
7. `retrieval signals with guardrails`：检索信号可以叠加，但需要 floor gate、cache isolation、fail-open、audit。

## 对当前项目的适配点

gbrain 是目前最贴近我们核心架构的外部参考。nano-NotebookLM 更像搜索/图谱操作层，llm_wiki 更像 Obsidian wiki 编译工作台；gbrain 直接补上了我们最需要的 epistemology layer 和 synthesis layer。

适配方式不是 fork，而是抽取：

```text
gbrain runtime
  -> 提炼为我们自己的 SCHEMA.md 字段、节点状态、关系类型、晋级流程和健康检查
```

## 量化判断

- domain: knowledge-engine
- problem: verified second brain / agent context
- maturity: emerging
- complexity: high
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 5
- integration_fit: 4
- evidence_strength: 4
- reversibility: 3

## 交叉验证

- `llm_wiki` 交叉验证：purpose/schema、local API、review queue、graph health 与 gbrain 的 system-of-record / resolver / cycle 思路相近。
- `nano-NotebookLM` 交叉验证：BM25 + vector + RRF + graph neighborhood 与 gbrain retrieval 方向一致，但 gbrain 更完整。
- Obsidian / Markdown 生态交叉验证：Markdown + YAML 作为长期可读格式，适合作为 canonical layer。

## 复杂度和风险

- 直接使用 gbrain 会过度设计：它带 runtime、DB、MCP、minions、OAuth、scheduler、company brain 等一整套产品系统。
- gbrain 的默认 schema 不等于我们的 verified knowledge schema。
- 它的 LLM 自动抽取和 synthesize 很强，但也会带来 hallucination / over-promotion 风险。
- 它的 benchmark 和宣传数字需要独立验证，不能当作当前决策证据。

## 融合判断

- 结论：adapt，不 fork。
- 理由：思想高度匹配，但产品体量和默认领域不匹配。
- 验证方式：先把 fields / relation / gates 写进 `SCHEMA.md`，后续用 10-20 条真实资料跑手工晋级流程，看是否减少混乱、增强复用，而不是马上写搜索引擎。

## 后续行动

1. 在 `SCHEMA.md` 中区分 `fact / claim / take / hypothesis / decision`。
2. 给 claim/pattern/decision 加 `holder/source/confidence/evidence_level/verification_status/valid_from/valid_until`。
3. 给每个 summary 或 decision 增加 append-only evidence timeline。
4. 健康检查里加入 stale decision、unsupported claim、conflicted claim、missing timeline。
5. 未来 context pack 采用 `answer + citations + gaps + negative evidence` 结构。

