---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: medium
derived_from:
  - raw/repos/2026-06-07-infiniflow-ragflow-source.md
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
  - source-intake
  - retrieval-activation
  - context-pack
  - agent-gateway
  - misa-vaks-integration
  - feedback-ledger
borrow_value: strong
borrow_order:
  - "P1: context-engine-not-truth-engine for MISA/VAKS scoped context access."
  - "P1: mcp-retrieval-needs-authority-buckets and feedback-adjusts-ranking-not-truth."
  - "P2: parser-chunker-index contract, child-parent locate-then-expand, hybrid retrieval diagnostics."
  - "P2: Dify-compatible adapter and task-recording trace as implementation references."
  - "P3: KG/RAPTOR/code sandbox/full RAGFlow runtime as observation-only references."
avoid:
  - "retrieval-score-as-confidence"
  - "citation-marker-as-evidence-support"
  - "auto-kg-as-reviewed-knowledge-graph"
  - "feedback-as-truth-update"
  - "mcp-all-access-default"
dev_context_hint:
  default_layer: support
  paired_risk_layer:
    - "score/citation/KG/feedback authority confusion"
    - "all-access MCP retrieval"
    - "code execution/sandbox overreach"
  cold_references:
    - raw/repos/2026-06-07-infiniflow-ragflow-source.md
    - raw/repos/_snapshots/infiniflow-ragflow-5a04ac0864808bb3309e0b5735b56ad5a03d2efd.zip
possible_project_refs:
  - verified-action-knowledge-system
  - misa-vaks-integration
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/infiniflow-ragflow-5a04ac0864808bb3309e0b5735b56ad5a03d2efd.zip
    selector_type: source_code
    selector_value: docs/basics/agent_context_engine.md:26-34
  - snapshot_ref: raw/repos/_snapshots/infiniflow-ragflow-5a04ac0864808bb3309e0b5735b56ad5a03d2efd.zip
    selector_type: source_code
    selector_value: api/apps/restful_apis/chunk_api.py:255-372
  - snapshot_ref: raw/repos/_snapshots/infiniflow-ragflow-5a04ac0864808bb3309e0b5735b56ad5a03d2efd.zip
    selector_type: source_code
    selector_value: rag/nlp/search.py:562-720
  - snapshot_ref: raw/repos/_snapshots/infiniflow-ragflow-5a04ac0864808bb3309e0b5735b56ad5a03d2efd.zip
    selector_type: source_code
    selector_value: api/db/services/chunk_feedback_service.py:17-320
  - snapshot_ref: raw/repos/_snapshots/infiniflow-ragflow-5a04ac0864808bb3309e0b5735b56ad5a03d2efd.zip
    selector_type: source_code
    selector_value: mcp/server/server.py:165-570
tags:
  - candidate
  - provisional
  - ragflow
  - rag
  - context-engine
  - retrieval
  - mcp
---

# RAGFlow Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-infiniflow-ragflow-source.md
checked_commit: 5a04ac0864808bb3309e0b5735b56ad5a03d2efd
commit_time: "2026-06-05 21:16:25 +0800"
snapshot: raw/repos/_snapshots/infiniflow-ragflow-5a04ac0864808bb3309e0b5735b56ad5a03d2efd.zip
snapshot_sha256: FF942B3336E7E7900DBFA74812C955E2C345F200B73277631095A55CA99C7AFA
```

## 借鉴序位 / 开发上下文梯度

```yaml
borrow_value: strong
borrow_order:
  P1:
    - context-engine-not-truth-engine
    - mcp-retrieval-needs-authority-buckets
    - feedback-adjusts-ranking-not-truth
  P2:
    - parser-chunker-index-as-source-processing-contract
    - child-parent-locate-then-expand
    - hybrid-search-as-activation-layer
    - retrieval-test-before-agent-use
    - dify-compatible-retrieval-as-adapter-shape
    - task-recording-as-diagnostic-trace
  P3:
    - kg-raptor-as-derived-candidate-context
    - sandbox-code-component-needs-risk-contract
    - full RAGFlow runtime
avoid:
  - retrieval-score-as-confidence
  - citation-marker-as-evidence-support
  - auto-kg-as-reviewed-knowledge-graph
  - feedback-as-truth-update
  - mcp-all-access-default
dev_context_layers:
  Support:
    - this distillation
    - architecture review
    - MISA/VAKS overlay
  Risk:
    - score/citation/KG/feedback/all-access/code-execution confusion
  Cold References:
    - raw source card
    - snapshot zip
  Core:
    - only if the active task is drafting or implementing VAKS/MISA read-only context contract
```

这不是采用等级。它只是阅读优先级和开发上下文梯度。

```text
P1/P2/P3/avoid != reviewed knowledge
P1/P2/P3/avoid != action basis
P1/P2/P3/avoid != architecture decision
```

## 人话压缩

RAGFlow 最值得借的不是“又一个 RAG 产品”，而是这条上下文工厂链路：

```text
source
-> parser / chunker / layout envelope
-> embedding + full-text index
-> retrieval test and tuning
-> hybrid search / rerank / metadata filters
-> optional parent-child / ToC / KG / RAPTOR expansion
-> REST / Dify / MCP / Agent retrieval surface
-> answer/citation UX
-> feedback adjusts ranking
```

对 VAKS 的说人话版本：

```text
它能教我们怎么把资料变成可调用的上下文。
它不能教我们把检索结果直接当事实。

VAKS 要借它的：
解析纪律、chunk 可见性、检索测试、上下文接口、反馈入 ranking 的边界。

VAKS 要挡住它的：
score 当 confidence、citation 当 support、KG/RAPTOR 当 reviewed relation、feedback pagerank 当 truth update、MCP 默认全库读取。
```

## Candidate Points

### 1. `context-engine-not-truth-engine`

候选结论：RAGFlow 对 VAKS 最大价值是“上下文引擎”参考，而不是“真值库”参考。它的 Knowledge Core / Memory Layer / Tool Orchestrator 三分法，很适合帮助 MISA 接入资料库时拆清楚读什么、怎么读、读完能不能行动。

锚点：

- `docs/basics/agent_context_engine.md:26-34`
- `docs/basics/rag.md:100-107`
- `README.md:75-77`

对 VAKS 的适配：

```text
VAKS truth layer 仍由 reviewed claims / decisions / relations 管。
RAGFlow-like layer 只能做 activation / context assembly / retrieval diagnostics。
MISA 读到的 context pack 必须带 authority bucket。
```

边界：

```text
context completeness != action readiness
retrieved context != reviewed support
tool retrieval != tool permission
```

### 2. `parser-chunker-index-as-source-processing-contract`

候选结论：RAGFlow 把“解析文件”做成一组清楚的处理合同：source-type chunking method、PDF parser、layout box、media/table context、embedding/full-text index、document engine。VAKS 可以借这个思路强化 source intake：raw source、extraction artifact、chunk/index artifact、candidate point 必须分层。

锚点：

- `docs/guides/dataset/configure_knowledge_base.md:40-58`
- `docs/guides/dataset/configure_knowledge_base.md:94`
- `docs/guides/dataset/select_pdf_parser.md:14-76`
- `rag/flow/parser/parser.py:244-365`
- `rag/flow/parser/parser.py:413-489`
- `rag/flow/parser/parser.py:617-665`
- `rag/flow/chunker/token_chunker.py:32-66`
- `rag/flow/chunker/token_chunker.py:169-368`

对 VAKS 的适配：

```text
raw source = provenance and retained text
extraction artifact = parsed layout / transcript / code anchor map
index artifact = derived retrieval surface
candidate point = review input
reviewed point = later human/evidence-aware review result
```

边界：

```text
parse success != source reliability
layout box != evidence warrant
index artifact != source of truth
```

### 3. `embedding-space-is-index-contract`

候选结论：RAGFlow 文档明确说 dataset 一旦有 chunks，就不能随意换 embedding model，因为必须保持同一 embedding space。VAKS 如果未来做 retrieval cache / context-pack index，也应记录 embedding model、chunker config、index version，把它们当 derived index contract。

锚点：

- `docs/guides/dataset/configure_knowledge_base.md:79-82`
- `api/apps/restful_apis/chunk_api.py:255-327`
- `api/db/db_models.py:882`

对 VAKS 的适配：

```yaml
derived_index:
  source_snapshot: string
  chunker_config: string
  embedding_model: string
  index_backend: string
  built_at: string
  authority: derived_activation_only
```

边界：

```text
same embedding space != same truth standard
index compatibility != evidence sufficiency
```

### 4. `chunk-visibility-human-intervention`

候选结论：RAGFlow 的 chunk 页面允许用户查看 chunk、看快照、编辑 keyword/question/tag，用检索测试观察效果。这给 VAKS 的 review workbench 很大启发：候选抽取不能只是后台黑盒，应该能看见“哪个 raw span 变成了哪个 candidate point”。

锚点：

- `docs/guides/dataset/configure_knowledge_base.md:103-118`
- `docs/guides/dataset/run_retrieval_test.md:80-97`

对 VAKS 的适配：

```text
source card -> extraction artifact -> candidate point -> evidence packet draft
每一步都能回钻。
人工可以给 route hint / keyword / review_due。
人工不能通过 edit keyword 直接制造 reviewed support。
```

边界：

```text
human edit to retrieval hints != human review
chunk visibility != evidence support
```

### 5. `child-parent-locate-then-expand`

候选结论：RAGFlow 的 parent-child chunking 很适合 VAKS context pack：先用 child chunk 精准定位，再返回 parent context 做理解包络。这比“把最相似的一小段直接喂给 agent”更稳。

锚点：

- `docs/guides/dataset/configure_child_chunking_strategy.md:14-20`
- `api/apps/restful_apis/chunk_api.py:345`
- `rag/nlp/search.py:916`

对 VAKS 的适配：

```text
locate: exact source span / chunk / candidate anchor
expand: parent section / nearby reviewed relation / source card metadata
label: authority bucket and warning code
```

边界：

```text
expanded context != support for every generated statement
nearby text != relevant evidence
```

### 6. `hybrid-search-as-activation-layer`

候选结论：RAGFlow 的 retrieval 不是纯向量搜索，而是 term/full-text、vector、rerank、metadata filter、threshold、top-k 的融合。VAKS 应该把这些视为 activation layer 的 knobs，而不是 trust layer。

锚点：

- `docs/basics/rag.md:71-76`
- `docs/guides/dataset/run_retrieval_test.md:14-45`
- `api/apps/restful_apis/chunk_api.py:255-372`
- `rag/nlp/search.py:562-720`

对 VAKS 的适配：

```text
low-level retrieval: raw/source/text-unit/candidate anchors
high-level retrieval: pattern/theme/project overlays
relation-neighborhood: nearby reviewed context
final pack: bucketed and warning-coded
```

边界：

```text
retrieval score != confidence
rerank score != reviewed relation
metadata filter != scope proof
```

### 7. `retrieval-test-before-agent-use`

候选结论：RAGFlow 建议先在 dataset 上做 retrieval test，再把设置应用到 chat assistant 或 Retrieval component。VAKS 可以借成：任何准备给 MISA/agent 使用的新 retrieval surface，先跑固定 query set，检查 bucket separation、scope fit、known gaps、latency、overinclude。

锚点：

- `docs/guides/dataset/run_retrieval_test.md:80-97`
- `docs/guides/agent/agent_component_reference/retrieval.mdx:128-152`
- `api/db/services/evaluation_service.py:483-559`
- `api/db/services/evaluation_service.py:619-681`

对 VAKS 的适配：

```text
retrieval test result -> maintenance diagnostic
bad result -> review_pressure or index tuning task
good result -> retrieval surface may be useful
good result -> still not action basis
```

边界：

```text
benchmark pass != truth confidence
LLM judge TODO != solved faithfulness
recommendation != automatic repair
```

### 8. `kg-raptor-as-derived-candidate-context`

候选结论：RAGFlow 的 KG / RAPTOR 适合复杂、多跳、长文档 retrieval，但必须作为 derived candidate context。对 VAKS，GraphRAG/RAPTOR 可以帮助激活 source anchors、candidate graph fragments、known related concepts，但不能创建 reviewed relations。

锚点：

- `docs/guides/dataset/advanced/enable_raptor.md:14-37`
- `docs/guides/dataset/advanced/enable_raptor.md:95`
- `docs/guides/dataset/advanced/construct_knowledge_graph.md:14-18`
- `docs/guides/dataset/advanced/construct_knowledge_graph.md:90-104`
- `docs/guides/dataset/run_retrieval_test.md:47-62`

对 VAKS 的适配：

```text
auto KG / RAPTOR -> candidate context aid
reviewed relation -> only after evidence-aware review
stale KG -> maintenance warning, not hidden authority
```

边界：

```text
auto entity graph != knowledge graph truth
PageRank * similarity != relation strength
generated tree summary != reviewed synthesis
```

### 9. `citation-postprocessing-not-evidence-support`

候选结论：RAGFlow 的 citation flow 很实用：answer generation 后补充/修复 citation markers，必要时补取 chunk vectors 做 answer-vs-chunk similarity。VAKS 可以借“答案必须回到 chunk/source anchor”的 UX，但不能把 citation marker 当 evidence support。

锚点：

- `README.md:125`
- `api/db/services/dialog_service.py:62-107`
- `api/db/services/dialog_service.py:485-541`
- `api/db/services/dialog_service.py:671-812`
- `rag/nlp/search.py:242`

对 VAKS 的适配：

```text
citation marker = pointer
evidence item = source span plus support relation to point
warrant = why this span supports this point under this scope
```

边界：

```text
formatted citation != support
nearby chunk != support
citation repair != truth repair
```

### 10. `feedback-adjusts-ranking-not-truth`

候选结论：RAGFlow 的 chunk feedback service 是一个非常清楚的 VAKS 边界案例：用户 upvote/downvote 后可以调整 `pagerank_fea`，并且默认关闭。这适合借给 Use Ledger 的 activation weighting，但绝不能改 truth confidence。

锚点：

- `api/db/services/chunk_feedback_service.py:17-40`
- `api/db/services/chunk_feedback_service.py:52-80`
- `api/db/services/chunk_feedback_service.py:143-245`
- `api/db/services/chunk_feedback_service.py:247-320`
- `rag/utils/es_conn.py:34`
- `rag/utils/ob_conn.py:1244-1267`

对 VAKS 的适配：

```text
positive feedback -> weak usefulness signal
negative feedback -> review pressure or scope warning
explicit correction -> review_due
ranking adjustment -> derived activation index only
truth confidence -> unchanged until review
```

边界：

```text
user liked answer != source supports answer
user disliked answer != source false
pagerank change != knowledge mutation
```

### 11. `mcp-retrieval-needs-authority-buckets`

候选结论：RAGFlow 的 MCP retrieval tool 很接近 MISA 接 VAKS 时需要的“只读 context access”接口，但它的默认行为里有一个危险点：dataset IDs 可省略，然后解析全部可访问 dataset。VAKS 不能让 MISA 默认读全库，更不能让 tool output 混成一个未分桶文本包。

锚点：

- `docs/develop/mcp/mcp_tools.md:10-14`
- `mcp/server/server.py:165-270`
- `mcp/server/server.py:465-570`

对 VAKS 的适配：

```yaml
request:
  caller: misa
  project_scope: required
  intended_use: required
  authority_request: required
  allowed_buckets:
    - reviewed_support
    - candidate_orientation
    - project_overlay_context
    - raw_source_drilldown
response:
  buckets_separated: true
  action_basis_allowed: false
  warnings: []
```

边界：

```text
accessible != appropriate
omitted scope != global scope
MCP tool output != action permission
```

### 12. `dify-compatible-retrieval-as-adapter-shape`

候选结论：RAGFlow 最新 commit 是 Dify-compatible retrieval API。这个很适合 VAKS 参考“外部系统希望 retrieval API 长什么样”：query、knowledge_id、metadata condition、top_k、score_threshold、content/score/title/metadata response。但 VAKS 必须额外加 authority metadata。

锚点：

- `api/apps/restful_apis/dify_retrieval_api.py:111-151`
- `api/apps/restful_apis/dify_retrieval_api.py:227-329`

对 VAKS 的适配：

```text
standard adapter fields:
query, scope, top_k, filters, threshold, response chunks

VAKS extra fields:
authority_bucket, warning_code, support_status, review_status, action_basis_allowed
```

边界：

```text
score is retrieval score
metadata title is not evidence
external API compatibility is not VAKS authority compatibility
```

### 13. `sandbox-code-component-needs-risk-contract`

候选结论：RAGFlow 的 code component 把 gVisor、container timeout、OOM classification、artifact filters、AST checks 等放在一起。VAKS/MISA 如果未来允许 code/tool execution，至少需要这类 risk contract；但最好先保持 read-only retrieval。

锚点：

- `docs/guides/agent/agent_component_reference/code.mdx:20-42`
- `agent/sandbox/README.md:7-9`
- `agent/sandbox/README.md:139-179`
- `agent/sandbox/executor_manager/services/security.py:24-207`
- `agent/sandbox/executor_manager/services/execution.py:196-421`

对 VAKS 的适配：

```text
phase 1: read-only context retrieval
phase 2: candidate draft writing with explicit file boundary
phase 3: controlled local scripts after human confirmation
phase 4: never silent arbitrary execution
```

边界：

```text
AST filter != complete security
container success != safe result
artifact collection != artifact trust
```

### 14. `task-recording-as-diagnostic-trace`

候选结论：RAGFlow 的 `RecordingContext` 把生产执行的中间结果记录下来，用于 dry-run/comparison。这对 VAKS 的 source-intake connectors 和 context-pack builders 很有价值：每次 derived artifact 生成应该能留下 execution receipt。

锚点：

- `rag/svr/task_executor_refactor/task_handler.py:60-181`
- `rag/svr/task_executor_refactor/task_handler.py:233-332`
- `rag/svr/task_executor_refactor/recording_context.py:16-35`
- `rag/svr/task_executor_refactor/recording_context.py:57-158`
- `rag/svr/task_executor_refactor/recording_context.py:261-305`

对 VAKS 的适配：

```yaml
execution_receipt:
  task_id: string
  input_sources: []
  parser_config: string
  output_artifacts: []
  diagnostics: []
  warnings: []
  truth_mutation_allowed: false
```

边界：

```text
recorded execution != reviewed result
dry-run match != semantic correctness
```

### 15. `memory-rag-same-tech-different-streams`

候选结论：RAGFlow 的 memory docs 明确把 RAG 和 memory 看作相近 retrieval 技术，但处理不同数据流。这个对 MISA 很关键：conversation memory、user preference、procedural note、working state 可以进 memory/activation 层，但不能直接写 VAKS truth。

锚点：

- `docs/basics/rag.md:78-83`
- `docs/guides/memory/use_memory.md:11-15`
- `docs/guides/memory/use_memory.md:44-89`

对 VAKS/MISA 的适配：

```text
raw conversation -> memory raw trace
summary/note -> derived memory
preference/procedure -> project/person-scoped activation
correction -> review_due or candidate feedback event
truth change -> separate review gate
```

边界：

```text
memory retrieval != truth retrieval
preference != fact
conversation continuity != evidence support
```

## Candidate Pattern Bank

| Candidate Pattern | Borrow Strength | VAKS Layer | Keep Out Of |
|---|---:|---|---|
| Context engine as activation service | high | Activation / Context Pack / MISA read API | Truth layer |
| Source-type parser/chunker/index contract | high | Source Intake | Reviewed schema |
| Chunk visibility and manual hints | high | Review workbench | Evidence support |
| Child-parent locate-then-expand | high | Context Pack | Support proof |
| Hybrid search knobs | high | Retrieval diagnostics | Truth confidence |
| Retrieval test before agent access | high | Maintenance / eval diagnostics | Mainline authority |
| KG/RAPTOR derived context | medium | Candidate activation | Reviewed relations |
| Citation insertion/repair | medium | Answer UX / pointer alignment | Evidence Support Check |
| Feedback-to-ranking | high as boundary | Use Ledger / Activation weights | Truth mutation |
| MCP retrieval tool | high | MISA read-only integration | Write permissions |
| Dify-compatible retrieval adapter | medium | External adapter shape | Authority contract by itself |
| Sandbox code component | medium | Future risk contract | Current core |
| RecordingContext trace | medium-high | Execution receipt / regression | Review verdict |
| RAG vs memory stream split | high | MISA memory boundary | Truth mutation |

## Anti-Patterns to Explicitly Block

### A. `retrieval-score-as-confidence`

RAGFlow outputs similarity, vector similarity, rerank scores, PageRank-like features, and hit metrics. None should map to VAKS confidence.

```text
score can say: this chunk may be relevant
score cannot say: this claim is true
```

### B. `citation-marker-as-evidence-support`

RAGFlow citation repair is useful answer hygiene. VAKS evidence support requires source span, point, relation, warrant, scope, and challenge handling.

```text
[12] after a sentence is a pointer.
It is not a warrant.
```

### C. `auto-kg-as-reviewed-knowledge-graph`

RAGFlow KG/RAPTOR chunks can help retrieval. VAKS reviewed relations require review.

```text
auto graph = candidate navigation
reviewed relation = human/evidence-aware consolidation
```

### D. `feedback-as-truth-update`

RAGFlow chunk feedback can adjust ranking. VAKS feedback can affect activation and review pressure only.

```text
feedback may change what shows up earlier.
It must not change what is treated as true.
```

### E. `mcp-all-access-default`

RAGFlow MCP can resolve all accessible datasets if dataset IDs are omitted. VAKS must reject omitted scope for MISA.

```text
no scope = no retrieval
no intended_use = no action-facing pack
```

### F. `enterprise-stack-as-vault-core`

RAGFlow is powerful but heavy. VAKS should not become Docker/MySQL/MinIO/ES/RAGFlow unless a separate runtime decision proves it.

```text
borrow design contracts.
do not swallow the product stack.
```

## Candidate Interface for VAKS/MISA

This is not a final schema. It is a candidate shape extracted from RAGFlow's retrieval surfaces plus VAKS authority boundaries.

```yaml
vaks_context_request:
  request_id: string
  caller: misa
  project_scope: required
  task: string
  intended_use:
    - answer
    - planning
    - code_change
    - candidate_draft
    - review_preparation
    - external_action
  requested_authority:
    - reviewed_only
    - reviewed_plus_candidate
    - raw_drilldown
  retrieval_config:
    source_types: []
    project_overlays_allowed: false
    candidate_allowed: false
    raw_allowed: false
    top_k: 10
    filters: {}
```

```yaml
vaks_context_response:
  context_pack_id: string
  source_snapshot_time: string
  buckets:
    reviewed_support: []
    reviewed_relations: []
    candidate_orientation: []
    project_overlay_context: []
    raw_source_drilldown: []
    feedback_hints: []
  diagnostics:
    retrieval_score: optional
    retrieval_backend: optional
    known_gaps: []
    known_conflicts: []
  warnings:
    - raw_is_provenance_only
    - candidate_not_action_basis
    - project_overlay_not_authority
  action_basis_allowed: false
  required_next_gate: none
```

Key idea:

```text
RAGFlow teaches us the shape of retrieval knobs.
VAKS must add authority buckets and action gates.
```

## Project Fit

### For VAKS

Best-fit uses:

- source intake parser/chunker/index boundary
- retrieval test and context-pack diagnostics
- candidate-only KG/RAPTOR activation
- feedback ledger -> activation ranking
- execution receipts for derived artifact generation
- workbench UI showing chunk/source/candidate lineage

Poor-fit uses:

- replacing Markdown/vault source of truth with a RAG product database
- treating RAGFlow KG as knowledge graph truth
- importing all enterprise dependencies into the core vault
- using citation output as support check

### For MISA

Best-fit uses:

- read-only retrieval adapter inspiration
- explicit dataset/project scope
- tool retrieval / skill retrieval decomposition
- memory stream split: raw conversation, derived memory, procedural notes
- no write to truth without review gate

Poor-fit uses:

- default all-access retrieval
- direct writeback from MISA memory to wiki truth
- giving code component / sandbox execution before read-only context is stable

## Review Questions

1. Should VAKS define a minimal `context_pack_request` / `context_pack_response` before letting MISA query the vault?
2. Should retrieval diagnostics store `retrieval_backend`, `chunker_config`, `embedding_model`, and `index_snapshot` as derived metadata?
3. Should source intake add an optional `extraction_artifact` field family for parser/chunker outputs?
4. Should Use Ledger support an explicit `activation_weight_hint` output that is visibly not truth mutation?
5. Should MISA access require explicit `project_scope`, `intended_use`, and `requested_authority` every time?
6. Should future KG/RAPTOR-like generated graphs live only in `outputs/review` or a separate derived-index folder, never `wiki/claims`?

## 强蒸馏结论

RAGFlow should be treated as a high-value external reference for this lane:

```text
Source Intake -> Retrieval / Activation -> Context Pack -> Agent Gateway -> Feedback Ledger
```

It should not be treated as a reviewed source for:

```text
Truth Confidence
Evidence Support
Reviewed Relations
Action Basis
Main Vault Runtime Decision
```

One-line keeper:

```text
Borrow the context factory; reject the authority confusion.
```
