---
type: source-review
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
source_name: YiTangMJ/PageIndexRag-Web + YiTangMJ/GraphRAG-Example
source_url:
  - https://github.com/YiTangMJ/PageIndexRag-Web
  - https://github.com/YiTangMJ/GraphRAG-Example
checked_commit:
  pageindexrag_web: 13e3eaf49711f099697ca832be7309b2a3602af6
  graphrag_example: cb989aa424495480e46574e9f2577a052291c817
review_mode: read-only source/code review
fusion_decision: adapt
confidence: medium-high
tags:
  - pageindex
  - source-structure-map
  - graphrag
  - graph-context
  - evidence-primary-context
  - heavy-source-navigation
  - vectorless-rag
  - alpha-detail-mining
---

# YiTangMJ Repo Alpha Review: Source Structure Map + Evidence-Primary Graph Context

## One-Line Judgment

PageIndexRag-Web 的聪明点不是 Web 系统本身，而是：

```text
Heavy source should be navigated by structure before it is mined for candidate points.
```

也就是：

```text
长文档 / 强资料
-> 先生成 source structure map
-> 再从结构节点里选 evidence-bearing sections
-> 再打开原文 span 生成 candidate point / Evidence Packet
```

这适合窄吸收到本项目。它不替代主架构，不替代 Evidence Packet，不替代 reviewed relation，也不替代 context pack coverage。

## Source Identity

Primary repo:

```text
https://github.com/YiTangMJ/PageIndexRag-Web
```

Checked commit:

```text
13e3eaf49711f099697ca832be7309b2a3602af6
```

Local read-only sandbox clone:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\PageIndexRag-Web
```

Upstream concept repo:

```text
https://github.com/VectifyAI/PageIndex
```

Important note:

```text
This review inspected PageIndexRag-Web code directly.
The upstream PageIndex repo was used as concept/context only in this pass.
Do not treat upstream benchmark or service claims as locally validated.
```

## What This Repo Solves

It turns documents into a visible tree and then performs document Q&A in two phases:

```text
1. Build a semantic / structural tree over the document.
2. Ask an LLM to select relevant tree nodes from the skeleton.
3. Open selected nodes' text.
4. Generate an answer with node references.
```

The repo README describes PageIndex as vectorless and reasoning-based. It says the system uses document structure plus LLM reasoning rather than vector DB search, and that non-PDF/Markdown formats are converted to Markdown before the same tree pipeline.

Source docs:

- Repo: https://github.com/YiTangMJ/PageIndexRag-Web
- README concept lines in local clone: `README.md:20`, `README.md:41`, `README.md:47`, `README.md:203-L209`
- Chinese project explanation: `项目说明.md:15`, `项目说明.md:22`, `项目说明.md:195-L196`

## Core Design Observed In Code

### 1. Skeleton-First Retrieval

The backend strips full text from the tree before search:

- Local: `server/services/tree_service.py:21-L32`
- GitHub: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/tree_service.py#L21-L32

Then the RAG pipeline sends the skeleton to the model to select node IDs:

- Local: `server/services/chat_service.py:68-L109`
- GitHub: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/chat_service.py#L68-L109

Only after node selection does it open node text / summary and assemble answer context:

- Local: `server/services/chat_service.py:120-L156`
- GitHub: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/chat_service.py#L120-L156

Design extraction:

```text
Do not throw raw long text into retrieval first.
First build a compressed structural map.
Use the map to choose where to look.
Then open the exact source region.
```

Boundary for our system:

```text
Node selected by LLM = activation / navigation.
Node selected by LLM != evidence support.
Node selected by LLM != reviewed relation.
```

### 2. Natural Structure Before Artificial Chunking

Markdown handling extracts headings, line numbers, and section text:

- Local: `pageindex/page_index_md.py:32-L89`
- GitHub: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index_md.py#L32-L89

It then builds a tree from heading levels:

- Local: `pageindex/page_index_md.py:190-L219`
- GitHub: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index_md.py#L190-L219

Optional tree thinning merges small nodes:

- Local: `pageindex/page_index_md.py:89-L187`
- GitHub: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index_md.py#L89-L187

Design extraction:

```text
Prefer source-native sections, headings, page ranges, line ranges, and tables.
Use generic chunking only as fallback when native structure is weak.
```

Boundary for our system:

```text
Structure is source navigation, not truth.
Summary is briefing, not support.
```

### 3. PDF Structure Repair And Hygiene

For PDFs, the repo tries TOC detection, TOC transformation, physical page mapping, verification, retry/fix, and fallback to no-TOC processing.

Important anchors:

- TOC/no-TOC processing: `pageindex/page_index.py:568-L643`
- TOC verification: `pageindex/page_index.py:892-L944`
- Fallback / mode switch: `pageindex/page_index.py:951-L989`
- Large-node recursive split: `pageindex/page_index.py:992-L1019`
- Final tree parser: `pageindex/page_index.py:1021-L1055`
- Main PDF pipeline: `pageindex/page_index.py:1058-L1085`

GitHub anchors:

- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index.py#L568-L643
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index.py#L892-L944
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index.py#L951-L989
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index.py#L992-L1019
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index.py#L1021-L1055
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index.py#L1058-L1085

Design extraction:

```text
If source structure is inferred, track confidence and repair pressure.
The structure map should expose whether headings/page anchors are native, converted, inferred, or weak.
```

Possible field for our system:

```yaml
structure_confidence: high | medium | low
structure_basis: native_headings | toc_detected | llm_inferred | converted_markdown | fallback_chunk
structure_review_due_when:
  - missing_toc
  - weak_heading_detection
  - page_anchor_uncertain
  - converted_format_loss
  - source_version_change
```

Boundary:

```text
Low structure confidence does not make the source false.
It only means candidate extraction / evidence search needs more caution.
```

### 4. Node References Are UI-Visible

The backend emits `nodes_found`, then the frontend stores and highlights node references.

Anchors:

- SSE chat route stores referenced nodes: `server/routers/chat.py:23-L46`
- Frontend stores node refs and highlights nodes: `web/src/stores/chat.js:87-L89`
- Assistant message renders node references: `web/src/components/chat/ChatMessage.vue:43-L49`
- Clicking a node ref highlights / scrolls to the node: `web/src/components/chat/NodeReference.vue:1-L24`

GitHub:

- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/routers/chat.py#L23-L46
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/web/src/stores/chat.js#L87-L89
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/web/src/components/chat/ChatMessage.vue#L43-L49
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/web/src/components/chat/NodeReference.vue#L1-L24

Design extraction:

```text
Context preparation should leave a visible trace of which source nodes were selected.
```

For our system this maps to:

```yaml
context_pack_trace:
  selected_source_nodes:
    - source_ref:
      node_id:
      title:
      anchor:
      selection_role: core | support | risk | cold_reference
      why_selected:
  opened_text_ranges: []
  ignored_source_nodes:
    - node_id:
      reason:
```

Boundary:

```text
selected_source_nodes explains attention.
It does not prove the answer.
The final support still needs Evidence Packet / evidence_support / warrant.
```

### 5. Format Conversion Into A Unified Markdown Pipeline

The repo converts TXT / JSON / CSV / Word to Markdown, then sends them through the Markdown tree pipeline.

Anchors:

- TXT conversion: `server/services/converter_service.py:14`
- JSON conversion: `server/services/converter_service.py:85`
- CSV conversion: `server/services/converter_service.py:192`
- Word conversion: `server/services/converter_service.py:269`
- Supported extensions: `server/services/converter_service.py:378`
- Unified conversion dispatcher: `server/services/converter_service.py:395`

GitHub:

- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/converter_service.py#L14-L83
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/converter_service.py#L85-L190
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/converter_service.py#L192-L267
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/converter_service.py#L269-L376
- https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/converter_service.py#L378-L405

Design extraction:

```text
Normalize many source formats into one reviewable structure path.
```

Boundary for our system:

```text
Converted Markdown is a processing artifact.
It cannot replace the original source.
Conversion can lose structure, tables, captions, page positions, or formatting.
Evidence used for promotion/action should still point back to the original source where possible.
```

## Candidate Alpha To Absorb

### Alpha Name

```text
Source Structure Map
```

### Plain-English Definition

For heavy / long / high-impact sources, create a lightweight structural map before extracting candidate points.

The structure map answers:

```text
What sections exist?
Where are they in the source?
Which sections look relevant?
Which sections were opened?
Which relevant-looking sections were ignored and why?
How reliable is the structure itself?
```

### Minimal Schema Sketch

This should stay optional and lazy.

```yaml
source_structure_map:
  status: candidate_navigation
  source_ref:
  created_at:
  created_by:
  structure_basis: native_headings | toc_detected | llm_inferred | converted_markdown | fallback_chunk
  structure_confidence: high | medium | low
  nodes:
    - node_id:
      parent_id:
      title:
      source_anchor:
        page_range:
        line_range:
        heading_path:
      node_summary:
      evidence_granularity: structure_only | summary_only | excerpt_opened | full_node_reviewed
      opened_for:
        - candidate_point
        - evidence_packet
        - context_pack
      selection_note:
  omitted_or_unopened_nodes:
    - node_id:
      reason:
  caveats:
    - summary_is_not_support
    - structure_is_navigation_not_truth
```

### Trigger Boundary

Use this only for:

```text
heavy source
long PDF
long paper
official spec / manual
large repo documentation
legal / financial / technical report
action-basis source review
explicit omission-check request
```

Do not use it for:

```text
ordinary capture
short article
quick query
light source
low-impact link saving
```

## How It Fits Our Fixed Chain

Current fixed chain remains:

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

Narrow insertion:

```text
source
-> optional source_structure_map
-> candidate point
-> evidence packet
-> evidence-aware review
```

Layer placement:

```text
Capture:
  source record can mention whether a structure map exists.

Understand:
  candidate points can be extracted from selected source nodes.

Review:
  Evidence Packet must still use exact source anchors, not node summary alone.

Connect:
  structure links are source-internal navigation, not reviewed relations.

Act:
  context_pack_trace can list selected_source_nodes / opened_text_ranges.

Feedback:
  missed evidence can create structure_review_due or missed_node feedback.
```

## What It Improves Over Our Current v0.3

### 1. Better Evidence Packet Setup

Evidence Packet needs a point and a source anchor.

Source Structure Map helps locate the source anchor before the review starts.

Before:

```text
long source -> broad summary -> candidate point -> hunt for evidence
```

After:

```text
long source -> structure map -> select node -> open text span -> candidate point -> Evidence Packet
```

This reduces vague source support and URL-only citation pressure.

### 2. Stronger Omission Check

Omission check currently asks:

```text
What risks / scope limits / important sections may be missing?
```

Source Structure Map gives the reviewer a concrete list of unopened or ignored sections.

Possible addition:

```yaml
omission_check:
  unopened_relevant_nodes: []
  ignored_node_reason:
  needs_structure_recheck: true | false
```

### 3. Better Context Pack Trace

Instead of only:

```yaml
used_sources: []
ignored_sources: []
```

For heavy sources we can record:

```yaml
selected_source_nodes: []
opened_text_ranges: []
ignored_source_nodes: []
```

This is still trace / activation, not truth.

### 4. Replaces Naive Chunk-First Default

If future implementation adds RAG, default should not be:

```text
split source into arbitrary chunks -> embed -> retrieve top-k
```

Better default:

```text
preserve source-native structure -> retrieve / reason over structure -> open exact nodes -> evidence check
```

Chunking remains fallback when structure is weak.

## Candidate Points For Review

| Candidate Point | Local Fit | Calibration Output | Review Question |
|---|---|---|---|
| Heavy sources should have an optional source_structure_map before candidate mining. | SOURCE_INTAKE heavy processing, Evidence Packet setup | refines | Should this become a template field or only a review note pattern? |
| Skeleton-first retrieval is activation, not evidence. | MEMORY_TIER / DEV_CONTEXT / context_pack_trace | supports existing boundary | Do we need explicit wording to prevent node selection from becoming support? |
| Node selection trace can refine context_pack_trace. | v0.3 context_pack_trace | refines | Should `selected_source_nodes` be a lazy field for heavy sources only? |
| Structure confidence should create review pressure. | source hygiene / omission_check / review_due | refines | Should weak structure trigger `source_hygiene` or `omission_check`? |
| Native structure should be preferred over arbitrary chunking. | future retrieval implementation | candidate decision | Should this replace chunk-first as future default retrieval policy? |

## Support / Challenge Review

### What Supports Adoption

```text
The code has a clear two-stage RAG pipeline:
tree skeleton selection first, source text opening second.
```

Source anchors:

- `server/services/chat_service.py:68-L156`
- `server/services/tree_service.py:21-L49`

```text
The code uses source-native structure for Markdown and attempts page/TOC structure for PDFs.
```

Source anchors:

- `pageindex/page_index_md.py:32-L89`
- `pageindex/page_index.py:568-L643`
- `pageindex/page_index.py:951-L1055`

```text
The UI makes node references visible.
```

Source anchors:

- `web/src/stores/chat.js:87-L89`
- `web/src/components/chat/ChatMessage.vue:43-L49`
- `web/src/components/chat/NodeReference.vue:1-L24`

### What Challenges Adoption

```text
The repo is mostly a single-document Q&A system.
```

Open issue asking about cross-document retrieval:

```text
https://github.com/YiTangMJ/PageIndexRag-Web/issues/2
```

```text
Graph / LightRAG integration is not implemented.
```

Open issue asking about LightRAG graph integration:

```text
https://github.com/YiTangMJ/PageIndexRag-Web/issues/3
```

```text
The tree can be LLM-inferred and may look more reliable than it is.
```

Mitigation:

```text
Use structure_confidence and structure_basis.
Never let node summary count as evidence support.
```

```text
The repo surfaces "thinking" as UI content.
```

Mitigation for our system:

```text
Do not store raw chain-of-thought as evidence.
Use short selection_rationale / why_selected instead.
```

### Challenge Severity

```text
major if adopting runtime
minor if adopting only Source Structure Map as review/navigation discipline
```

## What We Should Not Absorb

Do not absorb:

```text
FastAPI / Vue runtime
document upload app
SSE streaming workflow
in-memory chat history
LLM config UI
PageIndex as source of truth
node summary as support
node selection as reviewed relation
tree search as evidence sufficiency
cross-document claims not implemented in this repo
LightRAG graph claims not implemented in this repo
raw model thinking as durable proof
```

## Direct Comparison With Our Architecture

PageIndexRag-Web is smarter than naive RAG at:

```text
source-internal navigation
long-document structure preservation
finding which section to open
making retrieval path visible
```

Our architecture is stronger at:

```text
truth boundary
review queue
Evidence Packet
warrant separation
challenge taxonomy
minimal revision
reviewed relation
context-pack coverage
feedback without truth mutation
review_due
action basis
```

Plain comparison:

```text
PageIndex knows where to look inside one source.
Our system decides what can be believed, connected, and used for action after looking.
```

Best fusion:

```text
Use PageIndex-style structure maps before candidate extraction.
Then keep our evidence-aware review as the authority.
```

## Proposed Minimal Adoption

Adopt only this rule:

```text
For heavy long sources, build an optional source structure map first.
Use the map to select source nodes before opening full text.
Node selection is activation/context preparation, not evidence.
Evidence still requires source anchors, warrant, support check, and review.
```

Suggested place if later written into main docs:

```text
SOURCE_INTAKE.md:
  heavy processing may create source_structure_map.

SCHEMA.md:
  optional source_structure_map under source / candidate routing metadata.

REVIEW_QUEUE.md:
  candidate points may cite selected source nodes, but promotion still requires evidence_support.

templates/review-candidate.md:
  optional selected_source_nodes / opened_text_ranges fields.

templates/source-record.md:
  optional structure_map_ref / structure_confidence.
```

Do not write these yet without user confirmation.

## Opus Review Questions

1. Is `source_structure_map` worth adding as a named optional field, or should it remain an informal heavy-source review note?
2. Does this risk making heavy source processing too procedural?
3. Is `structure_confidence` useful, or does it create another pseudo-score?
4. Should node summaries be explicitly capped as `summary_only` evidence granularity?
5. Is this enough to replace future chunk-first RAG default?
6. How should this interact with existing `retrieval_strata.low_level.text_unit_refs`?
7. Should `selected_source_nodes` live in `context_pack_trace`, `coverage_map`, or only in source review output?
8. What is the smallest local trial to test this on existing vault files?

## Final Fusion Judgment

```text
fusion_decision: adapt
alpha_strength: high
implementation_urgency: medium
risk_of_overdesign: medium
main_boundary: structure map is navigation, not truth
```

This is a good alpha because it makes the existing v0.3 evidence discipline easier to apply without expanding the truth core.

It should replace naive chunk-first retrieval as the future default for heavy long sources.

It should not replace evidence-aware review.

---

# GraphRAG-Example Alpha Review: Evidence-Primary Graph Context

## Source Identity

Primary repo:

```text
https://github.com/YiTangMJ/GraphRAG-Example
```

Checked commit:

```text
cb989aa424495480e46574e9f2577a052291c817
```

Local read-only sandbox clone:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\GraphRAG-Example
```

Repo self-description:

```text
ZSTP - 知识图谱系统
Vue 3 + Express knowledge graph construction / visualization / RAG demo.
```

README anchors:

- Repo: https://github.com/YiTangMJ/GraphRAG-Example
- Feature list: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/README.md#L3-L12
- API / file search endpoint: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/README.md#L94-L97
- BFS / extraction prompt settings: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/README.md#L101-L109

## One-Line Judgment

GraphRAG-Example 的聪明点不是它有图谱，而是它没有让图谱冒充证据。

Plain version:

```text
原始文档内容 = 主要依据
知识图谱结构 = 辅助理解
```

This is directly compatible with our boundary:

```text
retrieval / graph / association = context preparation
reviewed evidence / warrant / reviewed relation = action support
```

## What This Repo Solves

It builds a small graph RAG workbench:

```text
file import
-> parse / LLM-extract entities and relations
-> merge into a graph
-> persist graph, files, messages
-> answer with original document snippets plus graph neighborhood
```

Important: the repo stores both extracted graph and original file content. During RAG, file content is searched first, then graph neighborhood is attached as supplementary structure.

## Core Design Observed In Code

### 1. Document-First, Graph-Second Retrieval

The RAG retriever explicitly prioritizes imported document content and treats graph structure as supplementary:

- Local: `src/services/ragRetriever.js:7-L40`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/ragRetriever.js#L7-L40

The context formatter writes document content first and graph structure second:

- Local: `src/services/ragRetriever.js:52-L93`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/ragRetriever.js#L52-L93

The answer prompt repeats the boundary:

- Local: `src/services/llmApiService.js:90-L109`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/llmApiService.js#L90-L109

Design extraction:

```text
The context pack should tell the model which material is primary evidence
and which material is only structural / associative help.
```

Boundary for our system:

```text
Graph neighborhood can explain where to look.
Graph neighborhood cannot prove the answer.
```

### 2. Reversible Import Batch

Each imported file becomes a batch. Extracted nodes and edges get `sourceFile`, and import history records the file-level batch. A batch can be removed later.

Anchors:

- Local: `src/stores/graphStore.js:125-L187`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/stores/graphStore.js#L125-L187
- Backend persistence / deletion by `sourceFile`: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/server/routes/graphs.js#L63-L91
- Backend import removal: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/server/routes/graphs.js#L127-L162
- UI import history delete button: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/components/import/ImportHistory.vue#L1-L30

Design extraction:

```text
LLM extraction / parser extraction should be batch-addressable and reversible
before anything becomes reviewed knowledge.
```

Possible field for our system:

```yaml
extraction_batch:
  batch_id:
  source_ref:
  created_by: parser | llm | human_assisted
  candidate_points_created: []
  candidate_relation_suggestions_created: []
  status: active | withdrawn | superseded
  withdrawal_reason:
```

Boundary:

```text
Batch withdrawal applies to candidate extraction artifacts.
It must not erase reviewed decisions or reviewed relations.
Reviewed material should instead get review_due / superseded_by.
```

### 3. Bounded Graph Neighborhood Activation

The repo finds seed nodes from query keywords and expands a BFS neighborhood with configurable depth and node cap.

Anchors:

- Seed search scoring: `src/services/graphService.js:30-L70`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/graphService.js#L30-L70
- BFS subgraph: `src/stores/graphStore.js:205-L244`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/stores/graphStore.js#L205-L244
- Settings surface for BFS depth / max nodes: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/README.md#L101-L109

Design extraction:

```text
Association activation needs an explicit budget.
Depth and max node count should be trace metadata, not hidden behavior.
```

Possible field for our system:

```yaml
association_activation_trace:
  seed_refs: []
  expansion_basis: keyword_seed | reviewed_relation_neighborhood | source_structure_node
  max_depth:
  max_nodes:
  returned_nodes:
  returned_relations:
  omitted_due_to_budget:
```

Boundary:

```text
BFS depth does not mean confidence.
Graph score does not mean support.
Repeated relation does not mean truth.
```

### 4. Visible Retrieval Context

The repo saves the last retrieval context and lets the UI show the retrieved context.

Anchors:

- Query stores context and attaches it to assistant message: `src/composables/useRagQuery.js:21-L36`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/composables/useRagQuery.js#L21-L36
- RAG store keeps `lastContext`: `src/stores/ragStore.js:8-L39`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/stores/ragStore.js#L8-L39
- Context viewer shows keywords and text: `src/components/rag/ContextViewer.vue:1-L14`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/components/rag/ContextViewer.vue#L1-L14

Design extraction:

```text
Every action-ready answer should be able to replay what context was actually supplied.
```

For our system this strengthens existing:

```text
Context pack trace
Action basis trace
Use ledger / feedback review_due
```

Boundary:

```text
Visible context is auditability.
Visible context is not proof by itself.
```

### 5. LLM Extraction Quarantine Parser

The repo expects LLM extraction output to be messy and normalizes common variants.

Anchors:

- Extraction entry and text truncation: `src/services/llmExtractor.js:8-L29`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/llmExtractor.js#L8-L29
- JSON / code-block / quirk parsing: `src/services/llmExtractor.js:37-L87`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/llmExtractor.js#L37-L87
- Sanitization: `src/services/llmExtractor.js:99-L122`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/llmExtractor.js#L99-L122
- Node / edge alias normalization: `src/services/llmExtractor.js:179-L199`
- GitHub: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/llmExtractor.js#L179-L199

Design extraction:

```text
Untrusted extraction should be robustly parsed, normalized, and quarantined.
```

Boundary:

```text
Parser success only means "candidate artifact was captured".
It does not mean "claim is true".
```

Important risk:

```text
The repo truncates LLM extraction input at 4000 chars.
For our evidence discipline this must create omission risk / partial-source caveat.
```

### 6. Original File Content Stays Available

The importer saves full plain text content to backend for later RAG search, while separately merging extracted graph data.

Anchors:

- Import parse / save file content: `src/composables/useFileParser.js:35-L99`, `src/composables/useFileParser.js:157-L181`
- GitHub:
  - https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/composables/useFileParser.js#L35-L99
  - https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/composables/useFileParser.js#L157-L181
- Backend file storage and keyword search: `server/routes/files.js:48-L65`, `server/routes/files.js:78-L129`
- GitHub:
  - https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/server/routes/files.js#L48-L65
  - https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/server/routes/files.js#L78-L129

Design extraction:

```text
Do not keep only the extracted graph.
Keep the source text available so evidence can be re-opened.
```

Boundary:

```text
Stored file text is a source-processing artifact.
Promotion/action still needs source anchor, warrant, support check, and review.
```

## Candidate Alpha To Absorb

### Alpha Name

```text
Evidence-Asymmetric Graph Context
```

### Plain-English Definition

When preparing a context pack, separate the material that can support an answer from the material that only helps orientation.

Minimal expression:

```text
Evidence text first.
Graph neighborhood second.
Graph edges are hints unless reviewed.
```

### Minimal Schema Sketch

This should not become a new truth layer. It is a context-pack discipline.

```yaml
context_pack:
  evidence_text:
    - source_ref:
      source_anchor:
      excerpt:
      support_role: primary | challenge | scope_limit | risk
  graph_neighborhood:
    status: auxiliary_context
    seed_refs: []
    expansion_depth:
    expansion_limit:
    relation_items:
      - relation_label:
        relation_status: reviewed_relation | candidate_relation_suggestion | cooccurrence_hint | llm_extracted_hint
        source_ref:
        allowed_use: orientation_only | reviewed_support
  answer_rule:
    primary_basis: evidence_text
    graph_may: suggest_connections_and_omissions
    graph_must_not: create_truth_confidence_without_review
```

### Trigger Boundary

Use this for:

```text
graph-assisted retrieval
association neighborhood activation
context pack / action basis
candidate relation review
multi-source synthesis where graph hints appear
```

Do not use it for:

```text
ordinary source capture
short source summary
any case where no graph / relation neighborhood is involved
```

## How It Fits Our Fixed Chain

Current fixed chain remains:

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

Narrow insertion:

```text
source
-> candidate extraction batch
-> candidate point / candidate relation suggestion
-> association neighborhood activation
-> context pack:
     evidence_text = primary
     graph_neighborhood = auxiliary
-> action basis
```

Layer placement:

```text
Capture:
  source text and extracted graph artifacts remain separate.

Understand:
  LLM / parser extraction creates candidates only.

Review:
  Graph relation must pass evidence-aware review before becoming reviewed relation.

Connect:
  Graph neighborhood can activate reviewed and candidate relations,
  but relation status must be visible.

Act:
  Context pack/action basis must show what was evidence and what was auxiliary context.

Feedback:
  Bad graph hint creates review_due or candidate withdrawal, not truth mutation.
```

## What It Improves Over Our Current v0.3

### 1. Harder Context Pack Boundary

Our v0.3 already has context pack trace. This repo gives a crisp operational wording:

```text
Original source text is the answer basis.
Graph structure is helper context.
```

That is a useful anti-confusion rule for future GraphRAG / association retrieval work.

### 2. Better Candidate Relation Hygiene

GraphRAG extraction naturally creates many relation-shaped artifacts. This repo's import batch idea gives us a clean candidate quarantine boundary:

```text
extracted relation
-> candidate_relation_suggestion
-> evidence-aware review
-> reviewed_relation only if supported
```

### 3. Bounded Association Activation

Depth and max node budget prevent graph sprawl. We can reuse the principle without adopting the runtime.

### 4. Replayable RAG Context

The visible context viewer maps well to our action-basis audit requirement:

```text
What did the agent see when it answered?
Which parts were text evidence?
Which parts were graph hints?
```

## Candidate Points For Review

| Candidate Point | Local Fit | Calibration Output | Review Question |
|---|---|---|---|
| Context packs should distinguish evidence text from auxiliary graph context. | context_pack_trace / action_basis | refines | Should this become a named subfield in templates? |
| LLM-extracted graph edges should become candidate_relation_suggestions only. | REVIEW_QUEUE / SCHEMA | supports existing boundary | Do we need stronger wording against graph-edge-as-truth? |
| Extraction batches should be reversible before review. | SOURCE_INTAKE / REVIEW_QUEUE | refines | Should candidate artifacts get `extraction_batch_id`? |
| Association activation should record depth / max_nodes budget. | MEMORY_TIER / DEV_CONTEXT | refines | Should this live in activation trace only? |
| Duplicate edge weight is recurrence, not confidence. | ARCHITECTURE_PRINCIPLES | prevents confusion | Should we explicitly ban weight -> truth confidence? |

## Support / Challenge Review

### What Supports Adoption

```text
The code clearly separates file retrieval and graph retrieval.
```

Source anchors:

- `src/services/ragRetriever.js:7-L40`
- `src/services/ragRetriever.js:52-L93`

```text
The answer prompt explicitly tells the model that original document content is primary and graph structure is auxiliary.
```

Source anchor:

- `src/services/llmApiService.js:90-L109`

```text
The graph extraction layer is batch-aware and reversible by imported file.
```

Source anchors:

- `src/stores/graphStore.js:125-L187`
- `server/routes/graphs.js:127-L162`

```text
The graph expansion is bounded by depth and max nodes.
```

Source anchors:

- `src/stores/graphStore.js:205-L244`
- `src/services/graphService.js:58-L70`

### What Challenges Adoption

```text
The repo is a demo workbench, not a verified knowledge system.
```

Mitigation:

```text
Borrow only context separation / batch quarantine / activation budget.
Do not borrow truth semantics.
```

```text
Graph edges can be regex, co-occurrence, imported CSV, or LLM output.
```

Mitigation:

```text
Every edge must carry relation_status.
Only reviewed_relation can support action.
```

```text
Duplicate edge weight increments when the same edge appears again.
```

Mitigation:

```text
Treat weight as recurrence / retrieval hint only.
Never map weight to confidence.
```

```text
LLM extraction truncates long text.
```

Mitigation:

```text
Mark partial extraction and omission risk.
For heavy sources, combine with Source Structure Map before extraction.
```

### Challenge Severity

```text
major if adopting graph runtime or database as truth
minor if adopting only Evidence-Asymmetric Graph Context as a context-pack rule
```

## What We Should Not Absorb

Do not absorb:

```text
Vue / Express product shell
SQLite as truth source
D3 graph canvas as knowledge quality
graph edge as reviewed relation
edge weight as confidence
keyword score as support
co-occurrence edge as evidence
LLM-extracted triple as truth
full-content truncation as sufficient evidence
chat history as reviewed knowledge
API settings / model UI
```

## Direct Comparison With Our Architecture

GraphRAG-Example is better than our current docs at showing:

```text
how a graph-assisted RAG context can be assembled visibly
how to keep source text and extracted graph together but separate
how to make graph expansion bounded
how to undo one file's extracted graph candidates
```

Our architecture is stronger at:

```text
truth boundary
source provenance
candidate point review
Evidence Packet
warrant separation
challenge taxonomy
minimal revision
reviewed relation promotion
feedback without truth mutation
review_due
action basis
```

Plain comparison:

```text
GraphRAG-Example helps prepare context.
Our system decides what context is allowed to become action-grade knowledge.
```

Best fusion:

```text
Use GraphRAG-Example's document-primary / graph-supplementary context split.
Keep our evidence-aware review as the authority.
```

## Proposed Minimal Adoption

Adopt only this rule:

```text
When graph or association context is used, context pack must label original evidence text separately from auxiliary graph/context hints.
Graph-derived relation hints can guide review and omission checks, but cannot support an answer or action unless promoted to reviewed_relation through evidence-aware review.
```

Suggested place if later written into main docs:

```text
DEV_CONTEXT.md:
  context pack should separate evidence_text and auxiliary_graph_context.

SCHEMA.md:
  candidate_relation_suggestion may include extraction_batch_id and relation_status.

REVIEW_QUEUE.md:
  extracted graph edges enter review queue as candidate_relation_suggestions.

MEMORY_TIER.md:
  association activation trace may record seed_refs, max_depth, max_nodes.

FEEDBACK.md:
  bad graph hint creates review_due / candidate withdrawal, not truth mutation.
```

Do not write these yet without user confirmation.

## Opus Review Questions

1. Should `evidence_text` / `auxiliary_graph_context` be a formal context pack distinction?
2. Is `extraction_batch_id` useful enough to add to candidate points / candidate relation suggestions?
3. Should relation status be mandatory when graph context appears in an action basis?
4. Should `edge_weight` be explicitly renamed to `recurrence_hint` if ever imported?
5. Is BFS budget trace worth adding now, or only when an implementation exists?
6. How should this interact with existing Association Neighborhood Activation?
7. Should graph context be allowed in ordinary answers, or only review/action basis contexts?
8. What is the smallest test case to verify graph hints do not become support?

## Final Fusion Judgment

```text
fusion_decision: adapt
alpha_strength: medium-high
implementation_urgency: medium
risk_of_overdesign: medium
main_boundary: graph context is orientation, not truth
```

This is a good alpha because it makes future graph/association retrieval safer without adding a new truth engine.

It should replace any future weak wording where graph relation, graph rank, or repeated edge count might accidentally sound like evidence support.

It should not replace Evidence Packet, evidence-aware review, or reviewed relation promotion.

---

# Combined Fusion Notes For Opus

## Big Plain-Language Takeaway

The two repos are complementary:

```text
PageIndexRag-Web:
  first find the right place inside a long source.

GraphRAG-Example:
  when graph context is used, keep original text as the main evidence
  and keep graph structure as auxiliary help.
```

Together:

```text
先找对位置。
再打开原文。
图谱只帮忙，不作证。
最后仍然走我们的 evidence-aware review。
```

## Two Alpha Designs To Carry Forward

### Alpha 1: Source Structure Map

Borrow from:

```text
https://github.com/YiTangMJ/PageIndexRag-Web
```

Core source anchors:

- Skeleton from tree: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/tree_service.py#L21-L32
- Skeleton-first chat selection: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/chat_service.py#L68-L109
- Open selected node text: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/server/services/chat_service.py#L120-L156
- Markdown heading tree: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index_md.py#L32-L89
- PDF pipeline / repair anchors: https://github.com/YiTangMJ/PageIndexRag-Web/blob/13e3eaf49711f099697ca832be7309b2a3602af6/pageindex/page_index.py#L951-L1085

Adopt as:

```text
optional heavy-source navigation artifact between source and candidate point
```

Do not adopt as:

```text
evidence
truth confidence
reviewed relation
automatic sufficiency
```

### Alpha 2: Evidence-Asymmetric Graph Context

Borrow from:

```text
https://github.com/YiTangMJ/GraphRAG-Example
```

Core source anchors:

- Document-first / graph-second retrieval: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/ragRetriever.js#L7-L40
- Context labels for original docs and graph structure: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/ragRetriever.js#L52-L93
- Prompt boundary: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/llmApiService.js#L90-L109
- Reversible import batch: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/stores/graphStore.js#L125-L187
- Bounded BFS neighborhood: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/stores/graphStore.js#L205-L244
- Visible context trace: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/components/rag/ContextViewer.vue#L1-L14
- LLM extraction parser / normalization: https://github.com/YiTangMJ/GraphRAG-Example/blob/cb989aa424495480e46574e9f2577a052291c817/src/services/llmExtractor.js#L37-L87

Adopt as:

```text
context pack discipline:
  evidence_text is primary
  graph_neighborhood is auxiliary
  graph-derived relation remains candidate until reviewed
```

Do not adopt as:

```text
GraphRAG as truth layer
SQLite truth source
D3 graph UI as knowledge quality
edge weight as confidence
```

## Relative Strength Of The Original Repos

PageIndexRag-Web:

```text
alpha value: high
direct adoption value: low-medium
best idea: structure-first long-source navigation
main weakness: single-document Q&A demo, not a verified knowledge system
```

GraphRAG-Example:

```text
alpha value: medium-high
direct adoption value: low
best idea: original document is primary, graph is auxiliary
main weakness: demo graph extraction is unreviewed and can look too authoritative
```

Our system:

```text
overall architecture value: higher
reason: it owns verification, review, action basis, feedback, and review_due
```

Best framing:

```text
They provide better sensors.
We provide the trust discipline and action loop.
```

## Minimal Combined Architecture Change

Do not add a new subsystem. Add two small optional disciplines:

```text
1. Heavy source intake may create source_structure_map.

2. Any graph-assisted context pack must separate:
   evidence_text
   auxiliary_graph_context
```

In the fixed chain:

```text
source
-> optional source_structure_map
-> candidate extraction batch
-> candidate point / candidate relation suggestion
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

Important:

```text
The structure map helps decide where to read.
The graph neighborhood helps decide what else to consider.
Neither one decides what is true.
```

## Suggested Later Writeback Targets

Only after user confirmation:

```text
SOURCE_INTAKE.md:
  add optional source_structure_map for heavy long sources.

SCHEMA.md:
  add optional source_structure_map and extraction_batch_id fields.

DEV_CONTEXT.md:
  add evidence_text vs auxiliary_graph_context distinction in context packs.

REVIEW_QUEUE.md:
  clarify extracted graph edges are candidate_relation_suggestions.

MEMORY_TIER.md:
  association activation trace can record depth / max node budget.

FEEDBACK.md:
  bad extraction batch or graph hint creates review_due / withdrawal, not truth mutation.
```

## Proposed Trial Before Mainline Adoption

Small local test:

```text
Take one long source already in the vault.
Create a manual source_structure_map.
Extract 3 candidate points from selected nodes.
Build one context pack with:
  evidence_text
  auxiliary_graph_context / relation hints
Check whether the answer/action basis stays evidence-primary.
```

Success criteria:

```text
less vague source support
clearer omission check
no graph hint treated as reviewed relation
no added burden for ordinary capture
```
