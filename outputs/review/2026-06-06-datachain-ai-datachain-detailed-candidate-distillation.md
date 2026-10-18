---
type: repo_candidate_distillation
status: candidate_only
created_at: 2026-06-06
source_record: raw/repos/2026-06-06-datachain-ai-datachain-source.md
source_url: https://github.com/datachain-ai/datachain
checked_commit: a8bd465484e7dcb7501cef18d672a95cf27762c3
commit_time: "2026-06-04 21:46:30 +0700"
truth_boundary: candidate distillation only; not reviewed knowledge; not architecture decision; not action basis
review_priority: high
projects:
  - verified-action-knowledge-system
tags:
  - datachain
  - typed-datasets
  - compiled-knowledge-base
  - read-first-agent
  - codex-skill
  - lightweight-toolchain
  - query-run
  - context-pack
  - obsidian-workbench
  - activation-not-truth
---

# DataChain Detailed Candidate Distillation

## 一句话人话结论

DataChain 对 VAKS 最有价值的地方，不是“它能不能当我们的检索引擎”，而是它把 agent 工作流里的一个硬问题做得很清楚：

```text
做过的处理结果必须命名、version、带 schema、带 lineage、能被下一次 agent 先读到。
```

这正好补 VAKS 现在的设计空白：检索层、compiler scripts、Codex skill、Obsidian workbench、query-run receipt 都需要一个“已存在产物如何被发现和复用”的操作契约。

但 DataChain 的 authority 方向不能照搬。DataChain 文档会把 Dataset DB 称为 ground truth，把 Knowledge Base 称为 derived and always accurate。VAKS 必须保留自己的边界：

```text
Markdown reviewed knowledge = truth source
raw / candidate / index / compiled KB / query-run / feedback / tool cache = activation or provenance
```

## DataChain 到底是什么

DataChain 是一个面向非结构化文件和 AI pipeline 的 data context layer。

它的基本链路是：

```text
files in object storage / local storage
-> Python chain operations
-> typed records with Pydantic schemas
-> named versioned datasets
-> Dataset DB registry / lineage / query engine
-> compiled dc-knowledge Markdown
-> agent skill / MCP reads that context before new work
```

它不是：

```text
not an Obsidian vault architecture
not a reviewed-knowledge governance system
not a claim/evidence/warrant model
not a pure RAG retrieval engine
not a safe default write interface for VAKS agents
```

所以它对 VAKS 的借鉴应该是 operating contract，不是 product adoption。

## 架构骨架拆解

### 1. Compute Engine

DataChain 的 Compute Engine 做重活：文件读取、LLM calls、model inference、multimodal extraction、昂贵 per-row I/O。它可以 parallel、async、distributed、checkpoint-recoverable。

VAKS 可借鉴的是：

```text
昂贵的 source intake / ASR / OCR / embedding / extraction
不应该混在普通 query 里悄悄跑
应该有明确 script、receipt、checkpoint、staging、output manifest
```

不要借成：

```text
VAKS 必须引入一个 compute platform
VAKS 普通查询默认触发昂贵重算
```

### 2. Dataset DB

DataChain 的 Dataset DB 保存 typed、versioned datasets。每个 `.save()` 把一条 pipeline 的结果变成可查、可复用、可追 lineage 的数据集。

VAKS 可借鉴的是“artifact discipline”：

```text
每次重要处理输出都应该是可命名、可定位、可复盘的东西
source extraction output
candidate distillation output
context pack manifest
query-run receipt
feedback event
index rebuild receipt
```

但 VAKS 不能照搬 Dataset DB 的 truth 叙事。DataChain 的 dataset 可以是“这个 pipeline 产出的结果”；VAKS 的 reviewed knowledge 才能是“这个 claim 在 scope/warrant 下站得住”。

### 3. Knowledge Base

DataChain 的 Knowledge Base 是 `dc-knowledge/` Markdown：从 Dataset DB 编译出来，给 agent/human 读。它包含 schema、lineage、preview、links。文档明确说 agent 先读 Knowledge Base；如果摘要不够，再 query Dataset DB；如果还是没有，才触发 Compute Engine。

这对 VAKS 很强。它说明“agent 先读什么”不能靠聊天习惯，应该变成 skill / workbench 的固定序列。

VAKS 适配版：

```text
Codex read-first surface:
  1. architecture boundaries / current handoff
  2. reviewed claim / decision / action basis indexes
  3. source card / candidate distillation indexes
  4. context-pack / query-run receipts
  5. raw source drilldown only when needed
  6. action-facing use returns to v0.2.13 warrant gate
```

### 4. Skill and MCP

DataChain 把 Skill 和 MCP 拆开：

```text
Skill = local agent instruction package, local dc-knowledge + SQLite registry
MCP = hosted Studio endpoint, central registry, teams/ACL/scale
```

VAKS 可借鉴：

```text
先做 local read-first Codex skill
MCP 先做 read-only resources
suggest-only tools 只写 quarantine / patch / outputs
reviewed-write 继续 parked
```

不要借成：

```text
马上做通用远程写接口
agent 有权改 reviewed knowledge
skill 输出可以自我审批
```

## 对 VAKS 检索层的具体提升

### 提升 1：检索不只是 search，而是先找“已有工作”

Pro 那轮讲的是 query planner + hybrid recall + pack compiler + claim binding。DataChain 补的是另一个角度：很多问题根本不该从 raw chunk search 开始，而该从“已有处理产物和索引”开始。

VAKS 可以把 retrieval intake 设计成：

```text
query intake
-> check compiled workbench/index/read-first surface
-> exact lookup over source IDs / headings / decisions / candidate slugs
-> hybrid recall over notes and snippets
-> optional source/candidate/query-run registry lookup
-> pack compiler
-> claim-to-evidence binding when action-facing
```

这样检索的第一步不是“塞向量库 top-k”，而是问：

```text
这个问题是不是已经有 source card?
有没有 candidate distillation?
有没有 reviewed decision?
有没有之前的 query-run receipt?
有没有 context pack manifest 可复用?
```

### 提升 2：registry 比 dashboard 更重要

DataChain 的 Dataset DB registry 价值在于：agent 不用遍历文件系统猜“有没有做过”，可以查到 named/versioned datasets、schema、dependencies、lineage。

VAKS 对应物不是 DB truth，而是 lightweight registry / compiled index：

```text
source_id -> source card -> candidate distillation -> extracted candidate points
query_run_id -> pack_id -> selected anchors -> feedback events
artifact_id -> produced_by -> input_refs -> output_refs -> warnings
```

这能直接改善 VAKS 检索命中率，因为命中不再只靠全文搜索，而有一条结构化导航线。

### 提升 3：identifier-first, payload-later

DataChain 的 Knowledge Base 页面先给 schema、lineage、preview、links，而不是把全部数据塞给 agent。这个和 Anthropic context engineering 的方向一致。

VAKS 的 context pack 可以借成：

```text
先给 item_id / path / heading / selector / why_included / citable_status
再给短 snippet / contextualized snippet
只有 drilldown 时才打开完整 raw/source
```

这会让 VAKS 的 pack 更像“编译产物”，不是“长文本拼盘”。

### 提升 4：query-run 也应该是可复用 artifact

DataChain 让每次 `.save()` 都变成一个可复用 dataset。VAKS 不应该把每次 query-run 都升成知识，但重要 query-run 应该能留下 receipt：

```text
query_run_id
query_type / risk_type
retrieval_profile
indexes_used
candidate_counts
pack_id
selected_items
warnings / fallbacks
used_anchor_refs
feedback_ref
```

这不是“把查询历史当真理”，而是让下一次 agent 不必盲目重跑。

## 对 VAKS compiler scripts / toolchain 的具体提升

DataChain 的 skill 里有几条规则非常适合 VAKS：

```text
read index first
reuse over rebuild
one stage = one script
one script = one saved output
expensive compute saves full substrate, task filters downstream
intermediate JSON is disposable, Markdown output is durable
stop on auth/connection errors
do not hand-edit compiled knowledge directory
```

VAKS 最小吸收版：

| VAKS Script | DataChain-like contract | Forbidden |
|---|---|---|
| `ingest-source` | input URL/file/snapshot; output source card + receipt | candidate promotion |
| `make-candidate` | input source card/raw; output candidate distillation + candidate point list | reviewed write |
| `update-index` | input notes/artifacts; output compiled index + freshness receipt | semantic truth pass |
| `make-context-pack` | input query/mode/scope; output pack manifest/items/receipt | final decision/action basis |
| `record-feedback` | input query_run_id/event; append event log | truth mutation |
| `sync-obsidian` | copy declared artifacts, hash verify | alter content semantics |

DataChain 的 staging/atomic idea 对 VAKS 很关键：

```text
write temp/staging
validate required fields / links / selectors
publish named artifact
write receipt
never silently overwrite without version/ref
```

## 对 VAKS Codex Skill 的具体提升

DataChain 的 core skill 和 knowledge skill 分工很有意思：

```text
core skill = SDK mechanics / code rules
knowledge skill = methodology / planning / layer choice / KB maintenance
```

VAKS 未来 Codex skill 也可以拆同样的心智，不一定拆成两个真实文件，但职责要分开：

```text
VAKS mechanics:
  file locations
  source card shape
  script commands
  sync rules
  forbidden writes

VAKS methodology:
  read order
  mode detection
  retrieval vs evidence boundary
  v0.2.13 warrant gate
  Project Overlay sandbox boundary
  stop rules
```

最低可落地 boot sequence：

```text
1. read AGENTS.md / newest handoff / architecture boundaries
2. decide mode: browse / research / review / action
3. read compiled indexes before raw search
4. prefer existing source/distillation/pack artifacts over re-extraction
5. if action-facing, require claim anchor + warrant + gap/risk
6. write only quarantine/candidate/output unless user explicitly opens mainline
```

## 对 Obsidian workbench 的具体提升

DataChain 的 `dc-knowledge/` 给了一个很好的 Obsidian workbench 样例：

```text
compiled markdown
one page per dataset / bucket
schema + lineage + preview + links
human-readable
agent-readable
regenerated from operational layer
```

VAKS 可以借，但要反转 authority：

```text
DataChain:
  Dataset DB = ground truth
  dc-knowledge = derived view

VAKS:
  reviewed Markdown = source of truth
  compiled workbench/index/Bases = derived navigation
```

VAKS workbench 可以先只做：

```text
Reviewed Knowledge Index
Decision / Action Basis Index
Source Intake Index
Candidate Distillation Index
Query-run / Context-pack Receipt Index
Feedback / Review Due Index
```

每个 view 都必须能点回 source note 或 selector-grade anchor。

## CAST 方法论怎么借

DataChain 的 CAST 是：

```text
Container = 文件是什么，不完整解码
Asset = 抽取/解码后的原始可工作数据
Sense = 模型对数据说了什么，embedding/classification/transcription
Task = 针对当前问题的组合、过滤、排序、评估
```

这个很像 VAKS 一直在摸的边界：

```text
Source substrate
-> Extracted content / candidate comprehension
-> Model-derived activation signals
-> Query/task-specific context pack or action basis
```

可以借作“思考模板”，不要借作正式 schema。原因：

```text
VAKS 不是文件数据 pipeline 产品
VAKS 已有 raw/candidate/reviewed/decision/action/feedback 层
再加 CAST 对象层会制造第二套分类系统
```

最小借法：

```text
toolchain rule:
  expensive source/model output should preserve reusable substrate before task-specific filtering

skill rule:
  before solving a task, ask whether an existing substrate artifact already covers it
```

## 哪些现在该吸收

现在该设计：

1. `compiled-kb-as-read-first-surface`

给 VAKS 一个轻量 compiled index/workbench 层。先放 outputs/review 或 wiki/indexes 候选，不改 truth schema。

2. `versioned-operational-artifacts`

给 source extraction、candidate distillation、context pack、query-run、feedback event 统一最小 manifest 字段。

3. `staged-atomic-toolchain-writes`

写进 compiler/toolchain contract：staging、required fields、receipt、hash/check、no silent overwrite。

4. `reuse-before-recompute-agent-rule`

写进 Codex skill / operating layer：先查已有 artifact 和 index，再做新抓取/新摘要/新 pack。

5. `one-stage-one-script-toolchain`

把 ingest-source、make-candidate、update-index、make-context-pack、record-feedback 拆清楚。

## 下一阶段再吸收

1. `checkpoint-and-delta-as-derived-layer-hygiene`

等 source intake / index rebuild 脚本稳定后，再设计 checkpoint/delta 规则。

2. `artifact-version-diff`

用于比较新模型/新 prompt/新 extraction 版本，尤其适合重新蒸馏 repo、视频、论文批次。

3. `compiled-obsidian-bases`

把 index/workbench 和 Obsidian Bases 对齐，但仍保持 view-only。

4. `local-cache-backed-viewer`

必要时可以用 SQLite/Parquet/cache 加速检索，但不作为 truth store。

## 应该 parked

1. DataChain runtime as VAKS core dependency

现在不需要。先借设计，不引入平台。

2. Dataset DB as VAKS source of truth

明确不做。VAKS source of truth 仍是 Markdown reviewed knowledge。

3. CAST as new object model

不扩对象层。只借 substrate-vs-task 思路。

4. Remote write-capable MCP

继续 parked。先 read-only resources / suggest-only tools。

5. Agent-produced dataset as reviewed fact

不做。Agent outputs 只能进 candidate/quarantine/feedback。

## 风险和反证

| Risk | Why it matters to VAKS | Handling |
|---|---|---|
| Pre-alpha package status | 工程表面很完整，但成熟度不能按生产稳定假设 | 借 pattern，不直接 adoption |
| Dataset DB ground-truth language | 容易和 VAKS Markdown truth 冲突 | 明确 derived/cache/index 不是真理 |
| "Knowledge Base always accurate" claim | 对 VAKS 来说太强，LLM enrichment 也会错 | compiled KB 只做 navigation/activation |
| Scope mismatch | DataChain 处理文件数据 pipeline，不治理 claim/evidence/decision | 只借 toolchain/workbench/skill |
| Agent save as premise | DataChain 让 agent 从 saved dataset building forward | VAKS 必须加 quarantine + review + warrant gate |
| Platform pull | Studio/MCP/ClickHouse/hosted ACL 很容易把 VAKS带向平台化 | VAKS 现在只做 local lightweight contracts |

## 和 VAKS 当前缺失模块的映射

| VAKS module | DataChain gives | Candidate fit |
|---|---|---|
| retrieval / query | registry-first and compiled-KB-first before raw search | high |
| compiler scripts / lightweight toolchain | one stage per script, named output, staging/save discipline | high |
| viewpoint / hypothesis / decision expression | weak direct value | low |
| Obsidian workbench / Bases / indexes | `dc-knowledge/` markdown as agent/human shared surface | high |
| Codex skill / agent operating layer | skill boot rules, read index first, reuse before rebuild | high |
| API / MCP / Viewer read-first layer | Skill local vs MCP hosted split | medium-high |
| temporal applicability / supersession | dataset versions and derived reruns | medium |
| feedback / query-run running design | saved runs, lineage, delta, checkpoints | medium |
| agent access / tool safety | local skill vs hosted MCP split, but not enough safety detail | medium-low |

## VAKS minimal design sketch inspired by DataChain

```text
VAKS Operation Artifact
  artifact_id
  artifact_type: source_intake | candidate_distillation | query_run | context_pack | feedback_event | index_build
  version_or_run_id
  produced_at
  produced_by: human | codex | script | external_tool
  inputs[]
  outputs[]
  source_refs[]
  selector_refs[]
  tool_or_script
  config_ref
  warnings[]
  freshness_status: new | ok | stale | superseded | review_due
  truth_boundary: activation | provenance | candidate | reviewed
```

This is not a new truth object. It is a receipt shape for derived work.

## Candidate knowledge points to carry forward

| Candidate slug | Type | Borrow scope | Main risk |
|---|---|---|---|
| `compiled-kb-as-read-first-surface` | pattern | Codex/Obsidian read-first workbench | compiled view becomes authority |
| `registry-before-recompute` | pattern | check existing artifacts before new extraction | stale artifact reused without scope check |
| `versioned-operational-artifacts` | concept | typed source/candidate/query-run/context-pack outputs | version mistaken as truth |
| `staged-atomic-toolchain-writes` | pattern | file-in/file-out scripts with receipts | over-platforming |
| `one-stage-one-script-toolchain` | pattern | keep script semantic responsibility single | too heavy for simple capture |
| `expensive-compute-save-full-filter-later` | pattern | ASR/OCR/embedding/extraction reuse | storing too much noisy candidate material |
| `checkpoint-delta-derived-layer-hygiene` | concept | long intake/index rebuild stability | delta treated as full-corpus correctness |
| `skill-methodology-vs-mechanics-split` | pattern | Codex skill design | skill becomes autonomous promotion agent |
| `cast-as-substrate-analogy-not-schema` | boundary | reuse substrate before task-specific result | new schema sprawl |
| `dataset-db-is-not-vaks-truth-source` | anti-pattern boundary | keep VAKS Markdown reviewed truth | DB/cache drift into authority |

## 最硬的一条边界

DataChain 最好的一句话是：

```text
the next agent should not start from raw bytes and a blank script
```

VAKS 可以吸收成：

```text
the next agent should not start from raw notes and chat memory;
it should start from reviewed boundaries, compiled indexes, source records, candidate artifacts, and receipts.
```

但 VAKS 必须再加一句：

```text
none of those compiled/indexed/derived artifacts can bypass reviewed evidence + warrant when action-facing.
```

## Current disposition

```text
recommendation: strong candidate for toolchain / workbench / skill design
mainline now: no
outputs/review candidate: yes
raw source captured: yes
snapshot captured: yes
needs Pro review: optional, useful for compiler/toolchain contract
needs implementation test: later, only after retrieval/toolchain contract draft exists
```
