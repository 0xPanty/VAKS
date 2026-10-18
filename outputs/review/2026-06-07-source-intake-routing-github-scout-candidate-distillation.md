---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/repos/2026-06-07-langgenius-dify-source.md
  - raw/repos/2026-06-07-infiniflow-ragflow-source.md
  - raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
  - raw/repos/2026-06-07-run-llama-llama-index-source.md
  - raw/repos/2026-06-07-deepset-ai-haystack-source.md
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
  - source-intake-routing
  - obsidian-workbench
  - context-pack-builder
possible_project_refs:
  - VAKS
point_anchor_refs: []
borrow_value: strong
borrow_order:
  - "P1: source route front door and lane-labeled workbench UX"
  - "P2: metadata filters, routers, traces, citation/clickback display"
  - "P3: parser/connector/ingestion pipeline recipes as future adapters"
tags:
  - candidate
  - provisional
  - github-scout
  - source-intake-routing
---

# Candidate Distillation: Source-Intake-Routing GitHub Scout

## Boundary

This note is provisional orientation.

It can guide the `source-intake-routing` sandbox and Obsidian workbench design.
It is not reviewed knowledge, not a decision, not a formal pattern, and not
action basis.

GitHub stars, recent commits, repo popularity, README claims, and tool UI are
useful scouting signals only. They do not create truth confidence or adoption
pressure.

## Source Set

Checked on 2026-06-07 via GitHub API and raw file anchors.

| Repo | Stars captured | Pushed at | Checked commit | Why included |
|---|---:|---|---|---|
| `langgenius/dify` | 144154 | 2026-06-06T16:00:22Z | `76fb1b6ea81660475cfb32164823db6b47060397` | Product workbench for dataset/document/RAG pipeline/metadata/retrieval. |
| `infiniflow/ragflow` | 82040 | 2026-06-05T13:59:26Z | `5a04ac0864808bb3309e0b5735b56ad5a03d2efd` | Ingestion templates, document/chunk APIs, connectors, parsers. |
| `Mintplex-Labs/anything-llm` | 61149 | 2026-06-06T00:16:52Z | `cba598edb57f0850a7cc27f6baf824084ab9f17d` | Source route UI, Obsidian/GitHub/website connectors, citation display. |
| `run-llama/llama_index` | 49958 | 2026-06-04T16:59:44Z | `9aa5ee5cd2a1ecff6ffa2a8cd6af46b87af674b9` | Readers, parsers, ingestion pipeline, router/citation query engines. |
| `deepset-ai/haystack` | 25467 | 2026-06-05T14:24:07Z | `56b5dd335071a415a9998703eed1a53b4c2e8053` | Metadata filtering, routers, pipeline tracing, document store separation. |

## What This Adds To The Sandbox

Previous sandbox state:

```text
metadata prefill improves discovery
lane classifier separates default retrieval
context pack builder v0 creates lane-labeled pack
```

This GitHub scout adds:

```text
source route front door:
  show entry routes like repo, article, Obsidian vault, website, video, paper.

ingestion recipe:
  not one heavy flow; choose a small route-specific path.

metadata/router UX:
  metadata filters and routers help retrieval after authority/path filters.

trace/clickback:
  context pack should expose source type, anchor, and trace, but not imply support.

parser/connector humility:
  parser, OCR, connector, chunk metadata are source hygiene, not truth.
```

## Candidate Points

```yaml
candidate_points:
  - kp_ref: KP-001
    point: "source-intake-routing 工作台需要先给用户一个 source-route 前门，而不是只给全文搜索框。"
    source_refs:
      - raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
      - raw/repos/2026-06-07-langgenius-dify-source.md
      - raw/repos/2026-06-07-infiniflow-ragflow-source.md
    evidence_status: source_anchor_only
    review_question: "VAKS 的第一个 Obsidian 入口页是否应按 source route 分区？"

  - kp_ref: KP-002
    point: "metadata filters / routers 应作为检索切片，而不是 authority 或 action-basis 判断。"
    source_refs:
      - raw/repos/2026-06-07-deepset-ai-haystack-source.md
      - raw/repos/2026-06-07-langgenius-dify-source.md
      - raw/repos/2026-06-07-run-llama-llama-index-source.md
    evidence_status: source_anchor_only
    review_question: "当前 metadata prefill lint 是否足够覆盖 router/filter 误用？"

  - kp_ref: KP-003
    point: "context pack builder 应显式显示 trace、lane、source type 和 citable status。"
    source_refs:
      - raw/repos/2026-06-07-deepset-ai-haystack-source.md
      - raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
      - raw/repos/2026-06-07-run-llama-llama-index-source.md
    evidence_status: source_anchor_only
    review_question: "v0 builder 是否应增加 source_type / source_route / selector fields？"

  - kp_ref: KP-004
    point: "ingestion pipeline 可以是 route-specific recipe，但不应成为所有 source 的强制重流程。"
    source_refs:
      - raw/repos/2026-06-07-infiniflow-ragflow-source.md
      - raw/repos/2026-06-07-run-llama-llama-index-source.md
      - raw/repos/2026-06-07-deepset-ai-haystack-source.md
    evidence_status: source_anchor_only
    review_question: "VAKS 是否需要为 repo / article / video / paper 各写一个轻量 route recipe？"

  - kp_ref: KP-005
    point: "citation/clickback/source icon 适合工作台体验，但必须和 evidence support 分开。"
    source_refs:
      - raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
      - raw/repos/2026-06-07-run-llama-llama-index-source.md
      - raw/repos/2026-06-07-deepset-ai-haystack-source.md
    evidence_status: source_anchor_only
    review_question: "context pack item 是否必须显示 action_basis_allowed=false/true？"
```

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order:
  P1:
    - "AnythingLLM/Dify/RAGFlow: source route front door and visible workbench lanes."
    - "Haystack: metadata filtering / router / trace language."
  P2:
    - "LlamaIndex: reader/parser/ingestion/router/citation stage separation."
    - "RAGFlow: route-specific ingestion recipes and chunk metadata as retrieval helper."
  P3:
    - "Dify/RAGFlow/AnythingLLM full platform UX as future comparison only."
```

Meaning:

```text
This is project-usefulness gradient only.
It is not truth confidence, adoption, review, or action readiness.
```

## Avoid

```text
Do not adopt a full RAG/agent platform as VAKS core.
Do not turn connector/parser/chunk objects into truth-layer objects.
Do not treat citation UI as evidence support.
Do not treat GitHub stars or recent push as quality proof.
Do not use metadata filters before authority/path/status filters.
Do not make every ordinary source run through a heavy ingestion pipeline.
```

## Dev Context Hint

```yaml
dev_context_hint:
  default_layer: support
  core_only_when: "designing or testing the source-intake-routing Obsidian workbench entrypoint or context pack builder v1"
  support_when: "working on source routes, metadata filters, context pack traces, connector/parser boundaries, or citation/clickback UI"
  risk_when: "a proposed design makes RAG platform objects, metadata, citation UI, or parser output look like reviewed support"
  cold_references:
    - raw/repos/2026-06-07-langgenius-dify-source.md
    - raw/repos/2026-06-07-infiniflow-ragflow-source.md
    - raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
    - raw/repos/2026-06-07-run-llama-llama-index-source.md
    - raw/repos/2026-06-07-deepset-ai-haystack-source.md
```

## Practical Design Takeaway

For the next sandbox step, build the `source-intake-routing` workbench around:

```text
1. Start Here
2. Source Routes
3. Current Rule
4. Candidate Orientation
5. Raw Drilldown
6. Project Overlay
7. Audit / Why
8. Generated Topic Packs
9. Known Exclusions
```

The most important change:

```text
Make the front door explicit.
Then keep every item lane-labeled.
```

## Open Questions

```text
1. Should source_route become a source-card discovery field in the sandbox?
2. Should context pack item shape include source_type and source_route?
3. Should the first Obsidian entrypoint use source route buttons/sections before topic sections?
4. What is the smallest route recipe for repo, article, paper, video, and Obsidian note?
5. How do we show citation/clickback without making it look like evidence support?
```

## Forbidden

```text
project_borrow_scope in raw source cards
decision outcome
formal pattern
action basis
truth confidence
reviewed relation
```
