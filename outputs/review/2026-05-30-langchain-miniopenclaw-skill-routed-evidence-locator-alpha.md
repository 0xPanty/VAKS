---
type: source-review
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
source_name: lyxhnu/langchain-miniopenclaw
source_url: https://github.com/lyxhnu/langchain-miniopenclaw
checked_commit: 8497d999640e85190c9dc567086b04e85949f1f8
review_mode: read-only source/code review
fusion_decision: adapt
confidence: medium-high
tags:
  - miniopenclaw
  - skill-routed-retrieval
  - evidence-locator
  - source-navigation
  - rag-playbook
  - alpha-detail-mining
---

# MiniOpenClaw Alpha Review: Skill-Routed Evidence Locator

## One-Line Judgment

`langchain-miniopenclaw` 的聪明点不是向量检索本身，而是：

```text
Before retrieval, make the agent read the right skill/playbook for how to retrieve.
```

说人话：

```text
它不是让 RAG 更玄学。
它是先教 agent 怎么查，再让 agent 去查。
```

这对我们的价值很明确：

```text
在 Evidence Packet 之前，加一个轻量的取证导航层。
它负责更准地找到 evidence span，不负责判断真假。
```

## Source Identity

Primary repo:

```text
https://github.com/lyxhnu/langchain-miniopenclaw
```

Checked commit:

```text
8497d999640e85190c9dc567086b04e85949f1f8
```

Local read-only sandbox clone:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\langchain-miniopenclaw
```

Repo current public metadata checked via GitHub API on 2026-05-30:

```text
created_at: 2026-03-10
pushed_at: 2026-03-10
language: Python
stars: 182
forks: 29
```

## What This Repo Solves

It is a local, file-first, auditable agent workbench:

```text
local files as source
Markdown skills
visible prompt components
visible tool calls
visible retrieval cards
local knowledge directory
optional memory RAG
```

README anchors:

- Repo: https://github.com/lyxhnu/langchain-miniopenclaw
- File-first / visible-agent idea: https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/README.md#L7-L34
- Capabilities: https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/README.md#L39-L54
- Request flow: https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/README.md#L68-L79
- File-as-memory and skill-as-plugin concepts: https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/README.md#L194-L236
- Current limits / roadmap / rag-skill reference: https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/README.md#L249-L283

It does not solve:

```text
claim truth
evidence warrant
challenge taxonomy
reviewed relation promotion
action basis sufficiency
```

It solves:

```text
how an agent chooses a retrieval workflow
how it navigates a mixed local knowledge directory
how it keeps retrieval/tool traces visible
how it avoids blind whole-file loading
```

## Core Design Observed In Code

### 1. Skill Snapshot First, Full Skill Later

The agent does not load every `SKILL.md` in full. It first reads a compact skill catalog.

Source anchors:

- Skill scanning: `backend/tools/skills_scanner.py:28`
- Snapshot builder: `backend/tools/skills_scanner.py:47`
- Snapshot refresh: `backend/tools/skills_scanner.py:64`
- Local snapshot: `backend/SKILLS_SNAPSHOT.md:1`
- System prompt includes snapshot: `backend/graph/prompt_builder.py:7`
- On save, skill edits refresh snapshot: `backend/api/files.py:59`

GitHub anchors:

- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/tools/skills_scanner.py#L28
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/tools/skills_scanner.py#L47
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/graph/prompt_builder.py#L7
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/SKILLS_SNAPSHOT.md#L1

Design extraction:

```text
Show the model a compact capability map first.
Only load the full playbook when the task matches.
```

Plain value:

```text
Misa 不需要每次读完整资料库规则。
Codex 不需要每次读所有 review 模板。
先看轻量 skill/context map，再按需打开完整规则。
```

Our fit:

```text
This strengthens Activation Tier and progressive loading.
It is retrieval routing, not truth.
```

### 2. The RAG Skill Is The Real Precision Layer

The most important file is `backend/skills/rag-skill/SKILL.md`.

It defines the actual retrieval discipline:

```text
read data_structure.md
select relevant directories/files
for PDF/Excel, read processing references first
use grep/local read/pdftotext/pdfplumber/pandas by file type
iterate up to 5 retrieval rounds
return answer with source and approximate location
```

Source anchors:

- Layered directory index: `backend/skills/rag-skill/SKILL.md:11`
- Do not use Glob to test directory existence: `backend/skills/rag-skill/SKILL.md:28`
- "Learn before processing": `backend/skills/rag-skill/SKILL.md:34`
- Overall flow: `backend/skills/rag-skill/SKILL.md:48`
- Answer organization and provenance: `backend/skills/rag-skill/SKILL.md:100`
- Keyword strategy: `backend/skills/rag-skill/SKILL.md:111`
- Max 5 iteration retrieval loop: `backend/skills/rag-skill/SKILL.md:123`
- PDF strategy: `backend/skills/rag-skill/SKILL.md:166`
- Excel strategy: `backend/skills/rag-skill/SKILL.md:189`
- JSON strategy: `backend/skills/rag-skill/SKILL.md:215`
- Do not whole-read JSON: `backend/skills/rag-skill/SKILL.md:227`
- Do not whole-read large files: `backend/skills/rag-skill/SKILL.md:316`

GitHub anchors:

- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/skills/rag-skill/SKILL.md#L11
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/skills/rag-skill/SKILL.md#L34
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/skills/rag-skill/SKILL.md#L48
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/skills/rag-skill/SKILL.md#L123
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/skills/rag-skill/SKILL.md#L166
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/skills/rag-skill/SKILL.md#L189
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/skills/rag-skill/SKILL.md#L215

Design extraction:

```text
High-precision retrieval is often a workflow problem before it is an embedding problem.
```

Plain value:

```text
不要一上来就向量搜。
先问：这是架构资料、PDF、Excel、JSON、repo 还是普通 markdown？
不同资料走不同取证路线。
```

Our fit:

```text
This becomes a pre-Evidence-Packet evidence locator.
It helps find evidence spans, but does not certify them.
```

### 3. `data_structure.md` Works As Collection Map

The knowledge directory has a root `data_structure.md`, and each major domain directory can have its own `data_structure.md`.

Source anchors:

- Root collection map: `backend/knowledge/data_structure.md:1`
- E-commerce domain map: `backend/knowledge/E-commerce Data/data_structure.md:1`
- AI report domain map: `backend/knowledge/AI Knowledge/data_structure.md:1`
- Financial report domain map: `backend/knowledge/Financial Report Data/data_structure.md:1`
- Safety domain map: `backend/knowledge/Safety Knowledge/data_structure.md:1`

GitHub anchors:

- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/knowledge/data_structure.md#L1
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/knowledge/E-commerce%20Data/data_structure.md#L1
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/knowledge/AI%20Knowledge/data_structure.md#L1
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/knowledge/Financial%20Report%20Data/data_structure.md#L1

Design extraction:

```text
Give the retriever a human-readable map of the collection before asking it to search files.
```

Relation to earlier PageIndexRag alpha:

```text
PageIndexRag:
  source-internal structure map

MiniOpenClaw:
  collection-level data_structure map

Together:
  first navigate the collection, then navigate inside the selected source.
```

Our fit:

```text
For source sets / repo reviews / paper batches / architecture references,
maintain a light collection map so Misa/Codex can choose where to look first.
```

Boundary:

```text
Collection map is navigation, not support.
```

### 4. Vector Search Exists, But It Is Not The Alpha

`SearchKnowledgeBaseTool` uses LlamaIndex vector retrieval plus keyword fallback.

Source anchors:

- Knowledge index class: `backend/tools/search_knowledge_tool.py:24`
- Fingerprint by file metadata: `backend/tools/search_knowledge_tool.py:47`
- Load documents as UTF-8 text: `backend/tools/search_knowledge_tool.py:69`
- Rebuild vector index: `backend/tools/search_knowledge_tool.py:85`
- Keyword fallback: `backend/tools/search_knowledge_tool.py:121`
- Combined vector + keyword search: `backend/tools/search_knowledge_tool.py:140`
- Tool output with source and score: `backend/tools/search_knowledge_tool.py:176`

GitHub anchors:

- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/tools/search_knowledge_tool.py#L24
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/tools/search_knowledge_tool.py#L47
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/tools/search_knowledge_tool.py#L69
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/tools/search_knowledge_tool.py#L121
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/tools/search_knowledge_tool.py#L140
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/tools/search_knowledge_tool.py#L176

Important implementation caveat:

```text
The current `_load_documents()` directly calls `path.read_text(encoding="utf-8")` over all files under knowledge/.
In the checked clone, PDF and XLSX files exist under knowledge/.
Local probe confirmed direct UTF-8 reads fail for PDF/XLSX with UnicodeDecodeError.
```

Design extraction:

```text
Do not copy the vector tool as-is.
Copy the workflow discipline around retrieval.
```

Boundary:

```text
Search score is not truth confidence.
Retrieved chunk is not evidence until it supports a specific candidate point.
```

### 5. Memory RAG Is Optional And Traceable

When RAG mode is enabled, `memory/MEMORY.md` is not fully injected. Relevant memory chunks are retrieved and emitted as retrieval events.

Source anchors:

- Prompt builder skips full memory in RAG mode: `backend/graph/prompt_builder.py:30`
- Memory indexer chunking: `backend/graph/memory_indexer.py:76`
- Memory retriever: `backend/graph/memory_indexer.py:123`
- Agent emits `retrieval` event: `backend/graph/agent.py:106`
- Agent formats retrieved memory context: `backend/graph/agent.py:90`
- Frontend retrieval card: `frontend/src/components/chat/RetrievalCard.tsx:7`

GitHub anchors:

- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/graph/prompt_builder.py#L30
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/graph/memory_indexer.py#L76
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/graph/memory_indexer.py#L123
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/graph/agent.py#L106
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/frontend/src/components/chat/RetrievalCard.tsx#L7

Design extraction:

```text
If memory is retrieved dynamically, show what was retrieved.
Do not silently pretend the whole memory was considered.
```

Our fit:

```text
This aligns with Activation Tier:
activated context is visible context, not believed-more context.
```

### 6. Tool Calls And Retrieval Are UI-Visible

The system emits `tool_start`, `tool_end`, `retrieval`, and `done` SSE events and stores tool call traces in session JSON.

Source anchors:

- Chat API streams events: `backend/api/chat.py:29`
- Save assistant segments with tool calls: `backend/api/chat.py:73`
- Agent emits tool start/end: `backend/graph/agent.py:152`
- Session saves tool calls: `backend/graph/session_manager.py:122`
- Thought chain UI: `frontend/src/components/chat/ThoughtChain.tsx:7`
- Inspector can edit memory/skills/prompt files: `frontend/src/components/editor/InspectorPanel.tsx:8`
- File edit whitelist: `backend/api/files.py:15`

GitHub anchors:

- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/api/chat.py#L29
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/api/chat.py#L73
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/graph/agent.py#L152
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/graph/session_manager.py#L122
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/frontend/src/components/chat/ThoughtChain.tsx#L7
- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/frontend/src/components/editor/InspectorPanel.tsx#L8

Design extraction:

```text
Retrieval should leave a visible trail.
```

Our fit:

```text
This can become evidence_locator_trace / context_pack_trace.
```

Boundary:

```text
Trace means auditable path.
Trace does not mean support.
```

### 7. Failure Learning Exists, But Must Be Quarantined For Us

The repo includes a `retry-lesson-capture` skill that can write lessons into the current `SKILL.md` and `memory/MEMORY.md`.

Source anchors:

- Retry lesson skill: `backend/skills/retry-lesson-capture/SKILL.md:1`
- It writes current skill and memory: `backend/skills/retry-lesson-capture/SKILL.md:22`
- It warns against noisy long-term rules: `backend/skills/retry-lesson-capture/SKILL.md:65`

GitHub anchor:

- https://github.com/lyxhnu/langchain-miniopenclaw/blob/8497d999640e85190c9dc567086b04e85949f1f8/backend/skills/retry-lesson-capture/SKILL.md#L1

Design extraction:

```text
Failed attempts can improve future retrieval playbooks.
```

Our boundary:

```text
For Verified Action Knowledge System, automatic lesson writes must become:
  feedback_event
  maintenance_manifest
  review_due
  candidate playbook patch
not direct reviewed knowledge.
```

## How To Apply This To Our Architecture

Current fixed internal chain:

```text
source
-> candidate point
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

Fusion version:

```text
source
-> candidate point
-> skill-routed evidence locator
-> candidate evidence span
-> Evidence Packet
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

Outer story fit:

```text
Capture:
  capture user query/source and choose whether retrieval is needed

Understand:
  classify query/source type and choose retrieval playbook

Review:
  turn located spans into Evidence Packet items

Connect:
  use source maps / association maps / context pack trace for navigation

Act and Learn:
  record whether retrieval missed, was stale, or produced review_due
```

The new alpha:

```text
Skill-Routed Evidence Locator
```

Minimal schema idea:

```yaml
evidence_locator_trace:
  query:
  selected_playbook: architecture_review | repo_review | paper_pdf | markdown_vault | json_faq | spreadsheet | codebase
  collection_map_used:
    - data_structure.md
    - knowledge-graph-index.md
  candidate_paths:
    - path:
      why_selected:
  retrieval_steps:
    - step:
      tool:
      query_or_pattern:
      path:
      result_summary:
  candidate_evidence_spans:
    - source_path:
      anchor:
      excerpt_summary:
      supports_candidate_point: unknown | partial | likely | no
  limitations:
    - not_all_branches_checked
    - binary_file_extraction_failed
    - no_direct_match
```

Boundary:

```text
`supports_candidate_point` is a locator guess.
Final support still belongs to Evidence Packet / Evidence Support Check.
```

## Misa / Codex Use

### Misa

Misa should use this for high-precision query routing:

```text
user asks
-> Misa classifies query type
-> Misa selects retrieval playbook
-> Misa reads reviewed context/context pack first
-> if more source lookup is needed, Misa uses locator trace
-> Misa answers from reviewed/context-pack material
-> if evidence is missing/stale/conflicting, Misa emits review_due or candidate_signal
```

Misa may create:

```text
feedback_event
review_due
candidate_signal
evidence_locator_trace
```

Misa must not create:

```text
reviewed_node
reviewed_relation
truth_confidence_change
```

### Codex

Codex should use this for source review and detail mining:

```text
user gives repo/paper/source
-> Codex selects repo/paper/source playbook
-> Codex reads collection/source map
-> Codex locates code/evidence anchors
-> Codex writes Evidence Packet or review artifact
-> Codex proposes, but does not silently alter mainline architecture
```

Codex may create:

```text
source-review artifact
evidence_locator_trace
candidate_point
candidate_relation_suggestion
Evidence Packet draft
maintenance_manifest
```

Codex promotes reviewed knowledge only after:

```text
evidence-aware review
user confirmation when mainline docs are touched
```

## Scenario Simulation

### Scenario 1: Architecture Query

Question:

```text
为什么我们说 graph / association 不能当 truth?
```

Old way:

```text
search "graph truth association"
read some hits
answer
```

New way:

```text
classify as architecture query
-> choose architecture retrieval playbook
-> read knowledge-graph-index / memory-tier-reference-index / SCHEMA / MEMORY_TIER
-> search specific terms:
   Association Neighborhood Activation
   candidate_relation_suggestions
   reviewed relation
   Evidence Support Check
-> assemble context pack trace
-> answer from reviewed architecture text
-> if conflict/missing source appears, emit review_due
```

Difference:

```text
Not keyword search first.
Map first, then search inside selected map branches.
```

### Scenario 2: Repo Alpha Review

Task:

```text
Review a new repo and extract usable alpha.
```

Old way:

```text
read README
rg keywords
summarize
```

New way:

```text
choose repo-review playbook
-> inspect file tree
-> identify entrypoints, core modules, examples, tests, docs
-> read source anchors for each claim
-> create alpha candidates with code links
-> classify fit:
   current_branch_value
   whole_architecture_value
   risk
   adoption boundary
```

Difference:

```text
The search process itself becomes auditable and reusable.
```

### Scenario 3: Financial PDF / Spreadsheet Query

Question:

```text
三一重工 2025 Q3 前三大股东是谁?
```

Old RAG:

```text
vector search the PDF or whole knowledge folder
```

New locator:

```text
choose financial-report playbook
-> read Financial Report Data/data_structure.md
-> select 三一重工 2025 Q3.pdf
-> read PDF processing guide
-> extract text/table to temp file
-> grep 股东 / 前十名股东 / 持股
-> read local page span
-> return evidence span with page/location
-> answer with source caveat
```

Difference:

```text
The agent does not ask embeddings to guess a table.
It uses file-type handling to locate the actual table/span.
```

## Relationship To Prior Alphas

PageIndexRag:

```text
source-internal structure navigation
```

MiniOpenClaw:

```text
task/skill-routed retrieval workflow
```

ZLAgent:

```text
agent operation gate and tool safety
```

Our system:

```text
evidence review and action basis
```

Combined:

```text
ZLAgent decides who may operate.
MiniOpenClaw decides which retrieval playbook to use.
PageIndexRag helps navigate inside large sources.
Verified Action decides whether the located evidence actually supports action.
```

## Best Transferable Alphas

### Alpha A: Skill-Routed Retrieval

Use a compact skill/playbook index:

```text
query type -> retrieval playbook -> source map -> evidence locator
```

This should live outside truth schema.

### Alpha B: Collection Map Before Search

Use `data_structure.md`-style maps for source sets:

```text
repo set
paper set
architecture source set
review artifact set
project vault zones
```

For our vault, likely maps already exist as:

```text
AGENTS.md
wiki/indexes/knowledge-graph-index.md
wiki/indexes/memory-tier-reference-index.md
outputs/review/*.md
00_handoff/*.md
```

Potential future small addition:

```text
source_set_map.md for external alpha mining batches
```

Only if needed. Do not overbuild.

### Alpha C: File-Type Source Playbooks

Different sources need different locator rules:

```text
Markdown:
  headings / line anchors / rg

PDF:
  extract text/table first, preserve page anchors

Excel:
  inspect sheets/columns first, then filter/aggregate

JSON:
  inspect schema and fields first, then field-level match

Repo:
  README -> file tree -> entrypoints -> core modules -> tests
```

Our version should output evidence locator traces, not answers directly.

### Alpha D: Evidence Locator Trace

Borrow the visible retrieval/tool trace idea and adapt it:

```text
why this source was selected
what map was used
what search terms were tried
what span was found
what was not checked
```

This can feed:

```text
Evidence Packet
Context pack trace
Omission check
Review due
```

### Alpha E: Retrieval Miss As Feedback

If retrieval fails or produces weak matches:

```text
do not hallucinate
emit review_due / missing_evidence / source_map_gap
```

This aligns with our Feedback Ledger.

## Do Not Import

Do not import:

```text
1. The vector index implementation as-is.
2. Direct UTF-8 indexing of all knowledge files.
3. Search score as truth confidence.
4. Skill-driven automatic edits to reviewed knowledge.
5. Full frontend workbench as a required system component.
6. Memory RAG as truth.
```

Why:

```text
The valuable part is the retrieval workflow discipline.
The current implementation is a teaching/demo workbench and has file-type limitations.
```

## Candidate Point Collision With Current System

| Candidate Point From MiniOpenClaw | Local Reviewed Principle | Calibration Output | Review Question |
|---|---|---|---|
| Retrieval should be routed through a skill/playbook before searching. | Activation Tier and context pack retrieval should stay lightweight and traceable. | refines | Should we name a pre-review `Evidence Locator` step? |
| A collection needs a human-readable map before retrieval. | Source intake already keeps source records light and uses indexes/handoffs. | supports | Should external alpha mining batches get a `source_set_map` only when they grow large? |
| PDF/Excel/JSON need different retrieval methods. | Evidence support must anchor specific spans/items, not just source URLs. | supports | Should Evidence Packet accept a `locator_trace` for binary/structured sources? |
| Retrieval and tool calls should be visible. | Context pack trace records what was used for answers/actions. | supports | Should Misa responses store a lightweight retrieval trace when source lookup occurred? |
| Failure lessons can update skills/memory. | Feedback can create review pressure but cannot mutate truth. | scope_mismatch | Should failed retrieval become `review_due` / maintenance manifest, not auto memory truth? |
| Vector + keyword fallback returns scored chunks. | Similarity is activation, not support/confidence. | risk_of | Keep scores out of reviewed confidence. |

## Fusion Judgment

Conclusion:

```text
adapt
```

Best immediate absorption:

```text
Skill-Routed Evidence Locator
```

Minimal landing:

```text
Do not rewrite the main architecture.
Add this as a named retrieval/locator aid between candidate point and Evidence Packet.
Use it for Misa/Codex workflows before any future schema expansion.
```

One-sentence version:

```text
MiniOpenClaw teaches us that evidence retrieval should be a playbook-guided process, not a blind vector search.
```

Action readiness:

```text
Ready as design alpha.
Not ready as direct code transplant.
```

