---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref:
  - raw/repos/2026-05-29-graphrag-source.md
derived_from:
  - https://github.com/microsoft/graphrag
  - https://microsoft.github.io/graphrag/
  - https://microsoft.github.io/graphrag/index/default_dataflow/
  - https://microsoft.github.io/graphrag/query/overview/
  - https://microsoft.github.io/graphrag/query/local_search/
  - https://microsoft.github.io/graphrag/query/global_search/
  - https://microsoft.github.io/graphrag/query/drift_search/
checked_at: 2026-06-14
checked_commit: 6d02c2355c3fed4c49007572fbe951d73258a37f
package_version_checked: "graphrag 3.1.0 from packages/graphrag/pyproject.toml"
source_status: active
source_type: repository-documentation
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order:
  - "P1: TextUnit/source-anchor and query-mode stratification for retrieval receipts."
  - "P2: Community reports as theme briefings with drilldown anchors."
  - "P3: Provider/cache/config modularity as future optional plugin boundary."
avoid:
  - "Do not import the full GraphRAG runtime as VAKS core."
  - "Do not treat LLM-extracted entities, relationships, claims, community reports, ranks, or map-reduce ratings as reviewed knowledge."
  - "Do not let GraphRAG indexing, prompt tuning, or query output bypass VAKS review, support, sufficiency, temporal, and action gates."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Building the P1.5 retrieval sandbox or a concrete retrieval receipt/query routing prototype."
  support_when: "Designing context-pack preparation, multi-representation retrieval, graph-neighborhood activation, or derived cache adapters."
  risk_when: "Any design starts treating graph rank, community report, extracted relation, or retrieval hit as support/truth/action basis."
  cold_references:
    - raw/repos/2026-05-29-graphrag-source.md
    - https://github.com/microsoft/graphrag/tree/main/packages/graphrag/graphrag
tags:
  - candidate-only
  - strong-distillation
  - microsoft
  - graphrag
  - retrieval-stratification
  - context-pack
---

# Strong Candidate Distillation: Microsoft GraphRAG

## Boundary

This is a heavy candidate distillation for architecture planning.

It is not reviewed knowledge, not a decision, not a formal pattern, and not
action basis. It can guide the VAKS retrieval/context-pack upgrade plan only
after preserving the normal VAKS boundary:

```text
GraphRAG helps decide what to read.
VAKS decides what can support, be reviewed, and be acted on.
```

## Plain Judgment

Microsoft GraphRAG is a strong reference for the retrieval and context-pack
side of VAKS. It is not a stronger truth system than VAKS.

In plain language:

```text
GraphRAG is good at turning a corpus into queryable structure:
documents -> text units -> entities / relationships / optional claims
-> communities -> community reports -> local/global/DRIFT search.

VAKS is stronger at deciding authority:
raw vs candidate vs reviewed vs action basis,
evidence support vs provenance,
retrieval score vs trust,
and feedback vs truth mutation.
```

Borrow strength: strong for retrieval architecture; weak for truth/action
authority.

## Source / Code Anchors Inspected

| Anchor | What exists | Design extraction | VAKS boundary |
|---|---|---|---|
| `README.md` / repo overview | Describes GraphRAG as a data pipeline and transformation suite for extracting structured data from unstructured text with LLMs. It also warns indexing can be expensive and the code is not an officially supported Microsoft offering. | Treat as a serious but costly retrieval/indexing system, not a drop-in product dependency. | Do not make it a required VAKS runtime. |
| `docs/index/default_dataflow/` | Knowledge model contains Document, TextUnit, Entity, Relationship, Covariate, Community, and Community Report. | Good strata vocabulary for VAKS derived retrieval/cache. | These strata are not VAKS truth classes. |
| `docs/index/default_dataflow/` TextUnits | TextUnits are chunks used for graph extraction and provenance back to source text. | Strong source-anchor pattern: derived graph objects should point back to source spans/text units. | TextUnit provenance is not evidence support by itself. |
| `docs/index/default_dataflow/` graph extraction | Entities, relationships, and optional claims are LLM-extracted from text units, then summarized. | Useful candidate graph fragment pipeline for heavy sources. | Extracted entities/relationships/claims stay candidate/review input. |
| `docs/index/default_dataflow/` community reports | Community reports summarize communities at different graph granularities and are embedded for downstream search. | Strong theme briefing layer for high-level recall. | Community report is briefing, not truth or support. |
| `docs/query/overview.md` | Query engine supports Local, Global, DRIFT, Basic Search, and Question Generation. | VAKS should expose query modes in retrieval receipt instead of hiding route choice. | Query mode choice cannot promote material. |
| `docs/query/local_search/` | Local search starts from semantically related entities, then pulls text units, relationships, covariates, and community reports. | Good entity-centered context expansion. | Entity relevance is recall, not support. |
| `docs/query/global_search/` | Global search uses community reports in a map-reduce process for whole-dataset themes. | Good macro-pattern/theme route for broad questions. | Map-reduce ratings are not reviewer approval. |
| `docs/query/drift_search/` | DRIFT combines community-level starting context with local follow-up exploration. | Good breadth-then-depth route for hard exploratory queries. | Follow-up expansion must remain bounded by VAKS receipts/gates. |
| `packages/graphrag/pyproject.toml` | Current package version checked as `3.1.0`; dependencies include graph, vector, Azure/storage, NLP, pandas/pyarrow stack. | Confirms this is a real runtime stack with non-trivial operational cost. | Keep optional/plugin/sandbox, not VAKS core. |
| `packages/graphrag/graphrag/data_model/text_unit.py` | TextUnit has text, entity IDs, relationship IDs, covariate IDs, token count, document ID, and attributes. | VAKS can mirror this as a derived `source_text_unit_manifest` for heavy long sources. | Manifest is derived cache; Markdown/source record remains authority. |
| `packages/graphrag/graphrag/data_model/community_report.py` | CommunityReport has summary/full content, rank, embedding, size, period, and attributes. | VAKS can borrow theme brief shape and period/scope metadata. | Rank/embedding/summary must never mean trust. |
| `packages/graphrag/graphrag/query/factory.py` | Separate constructors build local, global, DRIFT, and basic engines from config, model, context builders, and vector stores. | Strong query-route modularity; VAKS can use route-specific context builders. | Route-specific engines stay outside truth/review layer. |
| `packages/graphrag/graphrag/query/indexer_adapters.py` | Reads indexer outputs into query data models and bridges renamed/collated objects. | Good adapter boundary: index outputs are adapted into query objects. | Adapter output cannot become reviewed relation or action basis. |

## What It Actually Solves

GraphRAG solves two RAG weaknesses:

1. Similarity search misses cross-document connections.
2. Plain chunks are weak for whole-corpus theme questions.

Its answer is:

```text
index once:
  documents -> text units -> graph objects -> communities -> reports -> embeddings

query later:
  local search for entity/detail questions
  global search for whole-corpus/theme questions
  DRIFT search for broad-to-local exploratory questions
  basic vector search as baseline
```

For VAKS, that is a retrieval/context architecture, not a knowledge authority
architecture.

## Strong Borrow Points

### P1. TextUnit-style Source Anchoring

GraphRAG's `TextUnit` is the best concrete thing to borrow.

VAKS should not treat a long source as one flat blob during heavy review or
retrieval. For heavy long sources, VAKS can create an optional derived manifest:

```yaml
source_text_unit_manifest:
  source_ref:
  generated_at:
  generation_method:
  units:
    - unit_id:
      source_selector:
      text_hash:
      n_tokens:
      candidate_entity_ids: []
      candidate_relation_ids: []
      candidate_claim_ids: []
      reviewed_support_allowed: false
```

Important: this manifest is not a new truth layer. It is a navigation and
anchor layer for context preparation.

### P1. Explicit Query Modes

GraphRAG's query engine makes route choice visible. VAKS should do the same
inside retrieval receipts:

```yaml
query_mode:
  selected: local_entity | global_theme | drift_explore | basic_vector | hybrid_bucketed
  why_selected:
  authority_buckets_included:
  authority_buckets_excluded:
  selected_context_types:
    - raw_source_anchor
    - candidate_point
    - reviewed_node
    - reviewed_relation_neighborhood
    - theme_briefing
  forbidden_support_types:
    - retrieval_score
    - graph_rank
    - community_report_summary
    - llm_extracted_relation
```

This strengthens the earlier retrieval receipt plan because the route is no
longer hidden inside an answer.

### P2. Community Reports As Theme Briefings

Community reports are useful because they give high-level dataset shape.

VAKS should borrow this as:

```text
theme briefing
pattern briefing
community/context summary
```

but never as:

```text
reviewed claim
reviewed relation
evidence support
truth confidence
action-ready support
```

The product language should be "briefing" or "orientation", not "proof".

### P2. DRIFT As Bounded Exploration

DRIFT's useful alpha for VAKS is not autonomous reasoning. It is:

```text
broad community/theme start
-> generate follow-up retrieval questions
-> local/detail expansion
-> ranked output hierarchy
```

VAKS can use a similar pattern for hard exploratory questions:

```text
Question
-> Theme briefing
-> Follow-up retrieval intents
-> Local source/reviewed-neighborhood expansion
-> Retrieval Receipt
-> Context Pack draft
-> support/sufficiency gates only when needed
```

This should be optional and receipt-bound. It must not auto-promote, auto-write,
or silently mutate reviewed knowledge.

### P2. Adapter Boundary Between Indexing And Querying

GraphRAG separates indexer outputs from query data models through adapters and
context builders. VAKS should keep the same split:

```text
Markdown / source cards / reviewed notes = authority
derived cache / text units / entity candidates / community briefings = query prep
retrieval receipt = trace of selection
context pack = draft envelope
review/action gates = authority decision
```

### P3. Provider, Cache, Vector Store, And Config Modularity

GraphRAG's provider/factory pattern is useful later, but not now as a core
dependency. It belongs to optional plugin/sandbox work after the P0 validators
exist.

## VAKS Fusion Map

| VAKS layer | GraphRAG contribution | Fusion decision |
|---|---|---|
| Capture / Provenance | TextUnit links back to documents/source text. | Strongly adapt as optional heavy-source manifest. |
| Source Intake | Long sources can be split into inspectable units before candidate mining. | Adapt for heavy sources only. |
| Candidate Distillation | Entity/relationship/claim extraction can produce candidate graph fragments. | Use as review input, never reviewed relation. |
| Review Queue | Graph objects can suggest what to inspect and where contradictions may sit. | Candidate relation suggestions only. |
| Reviewed Knowledge | No direct contribution to truth. | Keep VAKS review authority. |
| Retrieval / Cache | Local/global/DRIFT/basic routes, embeddings, graph neighborhoods, community reports. | Strongly adapt as P1.5 retrieval sandbox. |
| Context Pack | Community reports and text units can build better context envelopes. | Use with authority bucket filtering and drilldown anchors. |
| Decision / Action | No direct action readiness. | VAKS gates remain mandatory. |
| Feedback | Query failures can tune retrieval route selection. | Feedback affects activation/usefulness, not truth. |
| Agent Gateway | GraphRAG runtime could be an optional read/retrieval plugin. | Suggest-only/read-only until receipts and validators exist. |
| Product Workflow | Useful "local/global/drift" mental model for advanced search modes. | Hide by default; expose as advanced/debug route labels. |

## Why VAKS Is Better Than Plain GraphRAG

GraphRAG improves recall and corpus-level reasoning. VAKS adds the missing
authority system:

- raw/candidate/reviewed/action separation;
- source provenance versus evidence support;
- graph rank versus trust;
- community report versus proof;
- LLM-extracted relation versus reviewed relation;
- evidence support and sufficiency gates;
- temporal applicability;
- review-gated writeback;
- operation receipts and feedback quarantine.

So the fusion should be:

```text
GraphRAG retrieval brain outside.
VAKS evidence/action spine inside.
```

## What Not To Borrow

Do not borrow:

- full GraphRAG runtime as a required dependency;
- graph database as the VAKS system of record;
- LLM-extracted relation as a reviewed relation;
- community report as source support;
- report rank as reliability;
- map-reduce point rating as reviewer approval;
- prompt tuning as evidence calibration;
- query answer as action basis;
- automatic graph/index update as truth mutation.

## P1.5 Sandbox Design Addition

Add this under the existing robust-RAG retrieval sandbox:

```text
P1.5-RR-GR: GraphRAG-Inspired Retrieval Strata Sandbox
```

Candidate artifacts:

```text
source_text_unit_manifest.example.yml
retrieval_strata_manifest.example.yml
query_mode_receipt.local_entity.example.yml
query_mode_receipt.global_theme.example.yml
query_mode_receipt.drift_explore.example.yml
theme_briefing_with_drilldown.example.md
graph_candidate_fragment.example.yml
graph_rank_not_support.failure.md
community_report_not_truth.failure.md
```

Acceptance cases:

```text
GR-01 TextUnit source anchor can help locate evidence but cannot itself mark support.
GR-02 Local entity route can select text units, relationships, covariates, and reports, but must output a retrieval receipt.
GR-03 Global theme route can include community/theme briefings only as orientation.
GR-04 DRIFT-style follow-ups must preserve query lineage and cannot silently change user intent.
GR-05 Graph rank, relationship weight, community rank, and map-reduce rating cannot set confidence.
GR-06 LLM-extracted relation cannot create reviewed relation.
GR-07 Community report cannot satisfy evidence sufficiency without raw/reviewed drilldown.
GR-08 Optional GraphRAG runtime/plugin stays read-only/suggest-only until operation receipts and validators exist.
```

## Plugin / Complement Fit

GraphRAG can complement VAKS as an optional external retrieval adapter:

```text
VAKS source vault
-> derived TextUnit / graph / community cache
-> GraphRAG-style local/global/DRIFT retrieval
-> retrieval receipt
-> VAKS context pack
-> VAKS support/sufficiency/action gates
```

It should not be installed as a mandatory plugin before:

1. retrieval receipt validator exists;
2. support boundary validator exists;
3. action readiness validator exists;
4. plugin/agent write operations are quarantined;
5. derived cache can be rebuilt from Markdown/source records.

## Calibration Against Current VAKS

| Candidate point | Local VAKS boundary | Calibration output | Review question |
|---|---|---|---|
| TextUnits improve source navigation. | Source anchors are provenance, not support. | `refines` source intake and context-pack preparation. | Should `source_text_unit_manifest` stay informal or become optional heavy-source artifact? |
| Community reports improve broad recall. | Briefings are not truth. | `refines` activation/context pack. | What UI label prevents users from reading briefings as proof? |
| Local/global/DRIFT routes improve query planning. | Route selection cannot promote. | `refines` retrieval receipt. | Should query modes be exposed to users or only receipts/debug? |
| Extracted graph objects can suggest candidate relations. | Reviewed relations require review. | `risk_of` auto-relation promotion. | What validator catches graph edge -> reviewed relation leakage? |
| GraphRAG runtime is real and modular. | VAKS should not adopt runtime before gates. | `watch` optional plugin. | What P1.5 fixture proves plugin output remains suggest-only? |

## Omission And Risk Check

Known coverage:

- official docs inspected for welcome/process, dataflow, local/global/DRIFT query modes;
- repository HEAD checked on 2026-06-14;
- package structure inspected through GitHub API;
- package version and key source files inspected through raw GitHub files.

Known limits:

- no local clone;
- no runtime execution;
- no benchmark replication;
- no cost test;
- no prompt-tuning experiment;
- no review of every workflow implementation file.

Residual risk:

- GraphRAG is attractive enough to tempt over-adoption;
- generated graph and community reports can look more authoritative than they are;
- indexing cost and prompt tuning can become a maintenance burden;
- "graph" language may confuse retrieval neighborhood with reviewed relation graph.

## Direct Judgment

- Direct use: no.
- Fork: no.
- Design-only: yes, strong.
- Optional plugin/watch: yes, after P0 validators and P1.5 sandbox.
- Current plan value: high for retrieval/context-pack upgrades.
- Whole VAKS value: high for activation and context preparation, low for truth/action.
- Risk: high if graph artifacts are mistaken for reviewed knowledge.
- Next action: keep this as a strong supplement inside the architecture upgrade plan and implement only the smallest P1.5 retrieval sandbox artifacts later.

