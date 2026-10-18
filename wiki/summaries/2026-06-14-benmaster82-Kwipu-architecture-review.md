---
type: summary
status: draft
title: "Kwipu architecture review for VAKS local graph retrieval"
created: "2026-06-14"
library_name: "Kwipu"
repo_url: "https://github.com/benmaster82/Kwipu"
source_url: "raw/repos/2026-06-14-benmaster82-Kwipu-source.md"
checked_commit: "908f0e4e300578a22c5fadd4538f75ff7ccfc0b6"
commit_time: "2026-05-18T16:20:42+02:00"
source_status: active
reviewed_at: "2026-06-14"
domain: "local Graph RAG / Obsidian retrieval / MCP query"
related_projects:
  - verified-action-knowledge-system
  - misa
current_branch: "retrieval receipt / local graph sidecar / MISA read-only knowledge access"
extracted_patterns:
  - "local Obsidian graph retrieval sidecar"
  - "wikilink/frontmatter candidate triples"
  - "hybrid vector BM25 temporal retrieval"
  - "derived cache lifecycle manifest"
  - "thin read-only MCP query tool"
fusion_decision: adapt-design-only
inspection_confidence: medium
evidence_count: 15
cross_validated_with:
  - "outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md#6.1 Robust RAG Diagram Integration Plan"
  - "outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md#6.2 Microsoft GraphRAG Strong Distillation Supplement"
  - "outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md"
  - "outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md"
negative_evidence:
  - "No dedicated upstream test suite found."
  - "Runtime was not executed locally because the local Python is 3.10.6 and README requires 3.11+."
  - "Contributor roadmap still asks for retriever attribution logging, evaluation set, and provenance inspector."
  - "Default model string includes a cloud-labelled Ollama model, requiring locality review."
extension_potential: "High as retrieval sidecar and MCP read-only bridge; low as authority model."
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - summary
  - architecture-review
  - kwipu
  - graph-rag
  - obsidian
  - mcp
  - candidate-only
---

# Kwipu 架构评审：VAKS 本地图检索候选

## 一句话判断

Kwipu 对 VAKS 有帮助，而且方向很正：

```text
它适合启发 VAKS 做一个本地、轻量、Obsidian-native 的检索侧车。
```

但它不能替代 VAKS：

```text
它会找到材料。
VAKS 要判断材料能不能当证据、能不能进入 reviewed、能不能作为 action basis。
```

最小融合：

```text
Kwipu-like retrieval sidecar
+ VAKS retrieval receipt
+ VAKS support/sufficiency/action gates
+ read-only MCP
```

## 它解决什么问题

Kwipu 解决的是：

```text
local Markdown / Obsidian vault
-> queryable property graph
-> hybrid retrieval
-> cited natural-language answer
-> optional MCP access for agents
```

它不是：

```text
source provenance system
review queue
evidence support checker
truth calibration engine
action readiness gate
```

## 核心设计

代码非常集中：

```text
geode_graph.py       main app, graph engine, retrievers, watcher, CLI
lang_config.py       multilingual stopwords, temporal keywords, relation patterns
kwipu_mcp_server.py  FastMCP wrapper exposing one query tool
```

数据路径：

```text
notes
-> parse frontmatter + wikilinks
-> extract structural triples
-> LLM path extraction
-> PropertyGraphIndex
-> optional synonym + vector + BM25 + temporal retrievers
-> LLM answer with source names
```

运行路径：

```text
storage_graph persisted locally
watchdog watches source folder
modified file delete+reinsert
deleted file full rebuild
MCP query lazily initializes fast-mode RAG
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:22-45` | Feature list: MCP, incremental updates, storage integrity, graph index, wikilinks/frontmatter, hybrid retrieval. | Confirms local Graph RAG sidecar relevance. | README is orientation, not runtime proof. |
| `README.md:65-82` | MCP server configuration for agent clients. | Thin tool entry reference. | Current tool is query only; keep VAKS write tools blocked. |
| `README.md:104-134` | End-to-end pipeline and file layout. | Simple implementation map. | No VAKS authority bucket layer. |
| `README.md:223-230` | Roadmap/help asks for attribution logging, eval set, provenance inspector. | Confirms gaps VAKS already cares about. | Roadmap text is not implementation. |
| `CONTRIBUTING.md:27-47` | Same future gaps and a stale incremental-update note. | Source hygiene warning. | Documentation drift must be recorded. |
| `requirements.txt:1-7` | LlamaIndex/Ollama/watchdog/MCP/Rich/PyYAML. | Small dependency footprint. | Dependencies were not installed locally. |
| `geode_graph.py:88-113` | Ollama config, model names, chunk size. | Runtime config reference. | Default cloud-labelled model needs review. |
| `geode_graph.py:114-145` | Anti-hallucination prompt with citation and language rules. | Useful answer discipline. | Prompt is not support review. |
| `geode_graph.py:165-267` | BM25 custom retriever over graph text chunks. | Keyword recall route. | BM25 score is activation only. |
| `geode_graph.py:271-337` | Temporal/metadata retriever. | Temporal query route reference. | Temporal hit is not temporal applicability review. |
| `geode_graph.py:340-372` | Read/write lock. | Runtime consistency for local cache. | Not authority control. |
| `geode_graph.py:373-565` | frontmatter/wikilink triple extraction and dedupe. | Candidate graph fragment reference. | Auto triples are not reviewed relations. |
| `geode_graph.py:566-746` | index load/build, embedding manifest, incremental insert/update. | Derived cache lifecycle. | Cache update is not truth mutation. |
| `geode_graph.py:747-848` | PropertyGraphIndex build, structural triple injection, LLM path extraction. | Graph index build reference. | LLM paths are candidates. |
| `geode_graph.py:860-935` | retriever composition and query engine. | Hybrid retrieval implementation. | Needs retrieval receipt and bucket filter. |
| `geode_graph.py:947-1110` | file watcher, MD5 change detection, debounce, incremental update. | Useful cache invalidation pattern. | VAKS provenance should use SHA256. |
| `geode_graph.py:1113-1228` | Ollama/model startup validation and CLI overrides. | Good runtime UX. | Runtime ready is not action ready. |
| `lang_config.py:1-424` | multilingual tokenization, temporal keywords, relation patterns. | Query/router helper reference. | Lacks CJK segmentation today. |
| `kwipu_mcp_server.py:36-87` | FastMCP query tool and lazy RAG instance. | Read-only MCP bridge pattern. | Do not add write authority without operation receipts. |

## 当前支线价值

当前支线：

```text
retrieval receipt / local graph sidecar / MISA read-only knowledge access
```

它对当前支线：

```text
supports / refines / risk_of
```

具体价值：

- Supports: gives a small concrete local Graph RAG implementation.
- Refines: shows how Obsidian structures can feed a graph without changing source notes.
- Supports: gives a simple read-only MCP bridge shape.
- Risk_of: graph triples and cited answers can look more authoritative than they are.

风险：

- Without receipts, retrieval route is opaque.
- Without support checks, file citations can be over-trusted.
- Without authority buckets, raw/candidate/reviewed/overlay can mix.
- Without CJK tests, Chinese-heavy VAKS quality is unknown.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Works with plain Markdown folders and keeps original notes untouched. | adapt |
| Dusk workbench | Could power a future "ask this vault" workbench surface. | watch |
| source ingest | Reads files and extracts structures, but is not a source-card system. | adapt narrowly |
| review queue | Extracted triples can create candidate relation suggestions. | adapt |
| schema / reviewed knowledge | No authority model; cannot write reviewed nodes or relations. | reject |
| memory / dev context | Can provide Support/Cold References for context packs. | adapt |
| feedback | No clear feedback ledger; query failures could become feedback events in VAKS. | watch |
| retrieval / cache | Strong local retrieval/cache reference. | adapt |
| API / MCP / agent access | Thin FastMCP query tool is a strong read-only bridge reference. | adapt |
| viewer / workbench | Terminal UI only; product surface is minimal. | watch |
| publishing | No direct publishing value. | low |
| risk / anti-pattern | Main anti-pattern is graph/retrieval output becoming authority. | adopt as guardrail |

## 值得提炼的模式

### 1. Local Graph RAG sidecar

```text
VAKS vault stays file-first.
Derived graph/cache stays rebuildable.
Sidecar answers queries.
VAKS gates decide authority.
```

### 2. Structural triples from existing Markdown

```text
wikilink + frontmatter
-> candidate graph fragment
-> review queue hint
```

This is valuable because it avoids requiring users to manually model every relation.

### 3. Hybrid retrieval route

```text
synonym
vector
BM25
temporal
```

VAKS should add:

```text
query mode
authority bucket
selected_by
support_allowed false by default
```

### 4. Cache lifecycle manifest

Kwipu checks embedding-model mismatch. VAKS should generalize this:

```text
which vault state
which indexer
which model
which authority bucket rules
which source hash algorithm
```

### 5. Thin read-only MCP first

One tool:

```text
query_graph(question)
```

This is the right default for MISA/VAKS:

```text
read/search first
write only after receipts and gates
reviewed write never by default
```

## 标签与量化

- domain: local Graph RAG / Obsidian retrieval / MCP query
- problem: local Markdown vault needs stronger recall and agent-readable query surface
- pattern: derived retrieval sidecar
- maturity: experimental / small but coherent
- complexity: medium
- problem_fit: 5/5 for retrieval sidecar
- reuse_value: 4/5 for design and sandbox
- implementation_cost: 3/5 for a VAKS-specific sidecar; 4/5 for running Kwipu directly
- integration_fit: 4/5 as read-only sidecar; 2/5 as authority layer
- evidence_strength: 3/5 for source-inspected design, 1/5 for runtime quality
- reversibility: 5/5 if kept derived/rebuildable

## 交叉验证

相似设计来源：

- Microsoft GraphRAG / LightRAG: stronger large-corpus retrieval-strata design.
- mdvs: Markdown validation/search sidecar.
- kk-knowledge-agent: thin knowledge-base MCP bridge for agent use.
- agentmemory: MISA runtime memory bridge, but not VAKS truth.

支持证据：

- Kwipu source code exposes concrete structural triple extraction and hybrid retrieval.
- VAKS plan already calls for retrieval receipts and authority bucket filtering.
- MCP server file shows a clean read-only tool pattern.

反例或失败边界：

- No upstream tests found.
- No local runtime test due Python/dependency/model mismatch.
- No retriever attribution/provenance inspector yet.
- Prompt/citation discipline is not enough for evidence gates.

最小验证方式：

```yaml
pilot_scope: sandbox_only
inputs:
  - small_markdown_vault
  - raw_source_card_fixture
  - candidate_distillation_fixture
  - reviewed_claim_fixture
  - stale_decision_fixture
checks:
  - structural_triples_written_as_candidate_only
  - authority_buckets_recorded_before_retrieval
  - retrieval_receipt_emits_selected_by
  - graph_rank_not_support_failure_case
  - prompt_citation_not_action_basis_failure_case
  - mcp_tool_read_only
pass_result:
  - local retrieval sidecar design candidate
fail_result:
  - keep as design-only reference
```

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Candidate Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Local Graph RAG can improve recall. | VAKS Robust RAG plan says retrieval decides what to inspect, not what to believe. | refines | What receipt fields are needed for graph/vector/BM25/temporal routes? |
| Wikilinks/frontmatter can create graph triples. | VAKS reviewed relations require evidence for the edge itself. | candidate_relation | Can candidate graph fragments be linted away from reviewed relation fields? |
| MCP query tool helps agents use vault knowledge. | Agent memory quarantine forbids direct reviewed truth mutation. | supports_with_boundary | Should first tool be read-only query only? |
| Incremental cache updates improve usability. | Derived cache is not source of record. | refines | What cache manifest proves rebuildability and model compatibility? |
| Prompt-level citations reduce hallucination. | Evidence Support Check says citation correctness is not support. | scope_mismatch | How should answer UI show "citation present but support not checked"? |

## Support / Challenge Review

What supports it:

- Source files show a concrete local Graph RAG path.
- FastMCP wrapper is simple and read-only.
- Incremental cache and storage manifest address practical local-use friction.

What challenges it:

- No test/eval/provenance inspector yet.
- CJK support is not present in language config.
- Authority bucket, support check, and action readiness are absent.
- Default model naming creates a local/cloud posture question.

Challenge severity:

```text
major for direct authority use
minor for design-only retrieval sidecar borrowing
```

Scope limits:

```text
Use as retrieval/cache/MCP reference only.
Do not use as reviewed knowledge, reviewed relation, or action-basis layer.
```

Known risks:

- Graph relation hallucination.
- Cross-bucket retrieval mixing.
- Source citation over-trust.
- Agent query output used as decision basis.
- Cache drift hidden from answer users.

Review again when:

- VAKS starts P1.5 retrieval sandbox.
- MISA needs a read-only vault query bridge.
- CJK/Chinese vault fixtures are ready.
- Retrieval receipt validator exists.

Action readiness:

```text
not_ready
```

## 对当前项目的适配点

Best VAKS shape:

```text
Vault files
  -> Structural extractor
  -> Candidate graph fragments
  -> Derived graph/vector/BM25/temporal cache
  -> Bucket-filtered retrieval
  -> Retrieval receipt
  -> Context pack draft
  -> Evidence Support Check
  -> Evidence Sufficiency Gate when needed
  -> Action Readiness
```

MISA bridge:

```text
MISA
  -> MCP read-only query
  -> VAKS retrieval receipt
  -> returned context with boundary labels
  -> candidate/feedback write only in later gated path
```

## 可拓展性

- 是否适合作为插件/适配层：yes, as read-only retrieval sidecar or MCP query reference.
- 是否会绑定核心结构：should not; keep derived and rebuildable.
- 未来替换成本：low if VAKS owns receipt/cache contracts.
- 可迁移路径：start with structural extractor and receipt examples before running full graph runtime.

## 复杂度和风险

- Medium runtime complexity.
- Medium dependency complexity.
- Low license risk due MIT.
- High authority-confusion risk if graph triples or answers are over-trusted.
- Medium localization risk for Chinese vaults.

## 不可行点 / 避坑

- Do not install as mainline dependency now.
- Do not let `storage_graph/` become a committed source of record.
- Do not use MCP response as support/action basis.
- Do not allow graph triples into reviewed relations.
- Do not merge raw/candidate/reviewed/overlay into one top-k pool.
- Do not rely on file citations without source-span/support checks.

## 融合判断

- 结论：adapt / design-only now; sandbox later.
- 理由：strong fit for local retrieval and MCP read access, but missing VAKS authority controls.
- 验证方式：P1.5 local Graph RAG retrieval sidecar sandbox with receipt and failure cases.

## 直接判断

- Direct use: no, not now.
- Fork: no.
- Design-only: yes, strong.
- Reject: no; reject only authority-layer or write-enabled use.
- Current branch value: strong for retrieval receipt and MISA read-only bridge.
- Whole architecture value: medium-high as derived retrieval/cache layer.
- Risk: major if graph/retrieval/prompt output is treated as evidence support or reviewed relation.
- Next action: keep as candidate reference; add to total research plan and future P1.5 sandbox list.

## 后续行动

Do not update core architecture from this file alone.

If implementation starts later, first build:

```text
retrieval receipt template
authority bucket filter
candidate graph fragment fixture
read-only MCP tool contract
failure cases for rank/citation/triple over-trust
```

