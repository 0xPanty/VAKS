---
record_kind: candidate_distillation
status: draft
provisional: true
title: "Kwipu：VAKS 本地 Obsidian Graph RAG / MCP 查询候选"
created_at: "2026-06-14"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
source_ref: "raw/repos/2026-06-14-benmaster82-Kwipu-source.md"
derived_from:
  - "raw/repos/2026-06-14-benmaster82-Kwipu-source.md"
  - "raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip"
  - "wiki/summaries/2026-06-14-benmaster82-Kwipu-architecture-review.md"
  - "outputs/review/project_lens_overlays/2026-06-14-benmaster82-Kwipu-vaks-local-graph-rag-overlay.md"
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
  - retrieval
  - local-graph-rag
  - obsidian
  - mcp-readonly-query
  - derived-cache
  - misa-vaks-bridge
possible_project_refs:
  - verified-action-knowledge-system
  - misa
point_anchor_refs:
  - "raw/repos/2026-06-14-benmaster82-Kwipu-source.md#Inspected Repository Areas"
  - "raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip:README.md"
  - "raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip:geode_graph.py"
  - "raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip:kwipu_mcp_server.py"
  - "raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip:lang_config.py"
borrow_value: strong
borrow_order:
  - "P1: local Obsidian/Markdown graph retrieval sidecar with retrieval receipts"
  - "P1: thin read-only MCP query tool for MISA/VAKS context access"
  - "P2: derived-cache lifecycle with content hashes, model manifest, and incremental update"
  - "P3: multilingual BM25/temporal/synonym query-route reference"
avoid:
  - "Do not treat Kwipu graph triples as VAKS reviewed relations."
  - "Do not treat vector/BM25/temporal scores as support, trust, confidence, or action readiness."
  - "Do not expose reviewed-write MCP tools before permission tiers and operation receipts exist."
  - "Do not make the graph index or storage_graph directory the VAKS source of record."
  - "Do not rely on anti-hallucination prompt alone for evidence support."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the task is specifically to design or implement VAKS retrieval receipt sandbox, local graph retrieval sidecar, or MISA read-only VAKS query bridge"
  support_when: "designing bucketed retrieval, derived cache lifecycle, Obsidian structural-edge extraction, or read-only MCP access"
  risk_when: "someone proposes graph triples, retrieval scores, or MCP responses as reviewed support or action basis"
  cold_references:
    - "raw/repos/2026-06-14-benmaster82-Kwipu-source.md"
    - "raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip"
tags:
  - candidate
  - provisional
  - strong-distillation
  - kwipu
  - graph-rag
  - obsidian
  - mcp
  - retrieval
  - candidate-only
---

# 候选蒸馏：Kwipu

## 说人话

Kwipu 不是那种“大而全知识系统”。它厉害的地方很实际：

```text
把一堆 Markdown / Obsidian 笔记
变成本地图谱 + 混合检索 + 可被 agent 查询的 MCP 工具。
```

这对 VAKS 有帮助，尤其是补这块：

```text
VAKS 怎么更聪明地“找到该看的东西”
```

但它补不了这块：

```text
这个东西能不能作为证据、reviewed knowledge、reviewed relation、action basis
```

一句话：

```text
Kwipu 可以帮 VAKS 做更好的本地检索侧车。
VAKS 仍然要自己守住证据、审核、行动依据这条线。
```

## 直接评分

| 维度 | 分数 | 判断 |
|---|---:|---|
| 本地 Obsidian/Markdown 检索参考 | 8.5/10 | 很贴近 VAKS，结构轻，代码集中。 |
| 作为 VAKS 权威知识层 | 2/10 | 不合适；自动图谱和回答不能当 truth。 |
| 作为 MISA read-only 查询桥 | 8/10 | 一个 `query_graph` MCP 工具的形态很对。 |
| 直接拿来生产用 | 4/10 | 需要 Python 3.11、Ollama、依赖、中文/测试/receipt 补强。 |
| 设计借鉴价值 | 8/10 | 图检索、结构边、混合检索、增量缓存都值得借。 |

结论：

```text
design-only / sandbox-reference now
read-only sidecar pilot later
mainline authority no
```

## Candidate Point 1: local Graph RAG should be a derived sidecar

Kwipu 的形态很适合做 VAKS 的一个外置检索脑：

```text
VAKS Markdown vault
-> derived graph/vector/BM25/temporal index
-> retrieval receipt
-> context pack draft
-> VAKS support/sufficiency/action gates
```

关键是顺序不能反：

```text
graph answer -> reviewed truth
```

这个路径必须禁止。

VAKS 的正确融合应该是：

```text
Kwipu-like sidecar finds candidate context.
VAKS decides whether the context is support, review input, or just activation.
```

## Candidate Point 2: Obsidian structure can create candidate graph fragments

Kwipu 会从两种 Markdown 结构抽三元组：

```text
YAML frontmatter
Obsidian [[wikilinks]]
```

这对 VAKS 很有用，因为我们的库本来就是 Markdown/Obsidian-first。

但 VAKS 必须加一句硬边界：

```text
wikilink/frontmatter triple = candidate relation suggestion
not reviewed relation
```

最小借法：

```yaml
candidate_graph_fragment:
  extracted_from:
    - wikilink
    - frontmatter
  subject:
  relation:
  object:
  source_anchor:
  relation_state: candidate
  reviewed_relation_allowed: false
```

这能帮 review queue 更快发现关系，但不会污染正式图谱。

## Candidate Point 3: hybrid retrieval needs receipts

Kwipu 的 retrieval 组合是：

```text
LLM synonym expansion (optional)
vector similarity
BM25 keyword scoring
temporal / metadata matching
```

这个组合很适合 VAKS 的 P1.5 retrieval sandbox。

但 VAKS 要补三件事：

```text
authority bucket filter
retrieval receipt
support boundary check
```

正确输出不是：

```text
top_k result = support
```

而是：

```yaml
selected_item:
  path:
  bucket: raw | candidate | reviewed | overlay
  selected_by:
    - vector
    - bm25
    - temporal
  selected_for: activation_only | review_input | support_candidate
  support_allowed: false
  reason:
```

只有后续 Evidence Support Check 才能判断某个具体 point 有没有被独立 anchor 支持。

## Candidate Point 4: derived cache lifecycle is worth borrowing

Kwipu 有几个小而实用的工程点：

```text
storage_graph persisted locally
.kwipu_meta.json records embedding model
file content hash cache
watchdog debounce
modified file = delete + reinsert
deleted file = full rebuild
```

对 VAKS 的启发：

```text
derived cache must know how it was built
cache mismatch must fail visible
cache update must not mutate reviewed truth
```

VAKS 版本应该用更硬的元数据：

```yaml
derived_cache_manifest:
  cache_kind: retrieval_graph
  built_from_vault_commit:
  source_root:
  indexer_version:
  embedding_model:
  graph_extractor:
  source_hash_algorithm: sha256
  authority_bucket_filter_version:
  generated_at:
  action_basis_allowed: false
  truth_mutation_allowed: false
```

Kwipu 用 MD5 做内容变更检测可以理解，但 VAKS 的 provenance 仍然应该用 SHA256。

## Candidate Point 5: thin MCP is the right first bridge

Kwipu 的 MCP 服务器只有一个核心工具：

```text
query_graph(question: str) -> str
```

这个方向非常适合 MISA 以后使用 VAKS：

```text
MISA
-> read-only MCP query
-> VAKS retrieval sidecar
-> context answer / candidate context
-> no direct reviewed write
```

VAKS 应该借的是“薄工具”：

```text
read/search/list first
write never by default
candidate/feedback write only after operation receipts exist
reviewed-write tools no
```

## Candidate Point 6: prompt discipline is helpful but not enough

Kwipu 的系统 prompt 要求：

```text
只基于 context 回答
引用来源文件名
不知道就说不知道
同语言回答
不要猜
```

这些都很好，VAKS 应该保留。

但 VAKS 要更进一步：

```text
source filename citation != evidence support
context-only answer != action-ready
answer-ready != action-ready
prompt instruction != review approval
```

所以 prompt 是第一道刹车，不是最终闸门。

## Candidate Point 7: Kwipu's own roadmap exposes our advantage

Kwipu 贡献文档列出的未来需求包括：

```text
retriever attribution logging
evaluation set
provenance inspector
incremental updates on modification
```

其中增量更新代码里已经实现了，但文档还没完全同步。

这说明两个点：

```text
1. Kwipu 的方向和 VAKS 的 receipt/provenance 很同频。
2. VAKS 已经在设计层提前覆盖了它缺的 authority boundary。
```

所以我们不需要“学 Kwipu 成为 Kwipu”。

我们应该：

```text
借它的轻量本地 Graph RAG 工程形态
用 VAKS 的 receipt/support/action gates 把它补成安全可用
```

## VAKS 融合方案

最小合理版：

```text
P1.5-RR-KW: Local Obsidian Graph RAG Retrieval Sidecar Sandbox
```

输入：

```text
small VAKS fixture vault
raw source card
candidate distillation
reviewed note fixture
overlay fixture
known stale/superseded fixture
```

输出：

```text
structural_triples.candidate.yml
derived_cache_manifest.yml
retrieval_receipt.hybrid_graph.example.yml
mcp_readonly_query_contract.md
auto_triple_not_reviewed_relation.failure.md
retrieval_score_not_support.failure.md
prompt_citation_not_action_basis.failure.md
```

关键验收：

```text
Graph can find.
Receipt can explain why it found.
Support checker can still reject it.
Action readiness remains blocked unless VAKS gates pass.
MCP remains read-only.
```

## Borrow / Avoid

### Borrow

- Local-first Markdown/Obsidian Graph RAG sidecar.
- Wikilink/frontmatter structural triple extraction.
- Hybrid retrieval: vector + BM25 + temporal + optional synonym.
- Storage manifest that detects embedding-model mismatch.
- File watcher debounce and incremental update.
- Thin read-only MCP query tool.
- Startup validation with clear model/Ollama errors.

### Adapt

- Add VAKS authority buckets before retrieval.
- Emit retrieval receipts for every query.
- Save `selected_by` per retriever without turning it into support.
- Use SHA256 and source-root/git commit in derived cache manifests.
- Treat structural triples as candidate graph fragments only.
- Add Chinese segmentation / CJK support if used on this vault.
- Return answer with source paths and support-status placeholders, not just prose.

### Avoid

- Graph index as VAKS source of record.
- Auto extracted relation as reviewed relation.
- Retrieval score as confidence.
- Prompt citation as evidence support.
- MCP write tools before operation receipts.
- Cloud/default model ambiguity in a local-only claim.
- Using toy examples as benchmark evidence.

## Open Questions

- Can the LlamaIndex PropertyGraphIndex flow scale on our real vault size?
- How good is wikilink/frontmatter relation inference on Chinese notes?
- Should VAKS build a custom lightweight structural-triple extractor first, before using LlamaIndex graph runtime?
- Can the MCP response include machine-readable retrieval receipts, not only answer text?
- What is the right split between mdvs search sidecar and Kwipu-style graph sidecar?
- Should MISA consume VAKS through read-only MCP, context-pack export, or both?

## Routing Hint

Route this source to:

```text
retrieval receipt
local graph RAG sidecar
Obsidian structural edges
derived cache lifecycle
MISA read-only context bridge
MCP tool boundary
```

Do not route to:

```text
reviewed truth
reviewed relations
schema authority
action basis
agent writeback
```

## Bottom Line

Kwipu 对我们最有价值的一句话：

```text
VAKS 可以拥有一个很轻的、本地的、Obsidian-native 图检索侧车。
```

但 VAKS 应该比它更强的地方是：

```text
Kwipu answers from retrieved context.
VAKS must prove whether retrieved context can support, whether support is enough, and whether action is allowed.
```

