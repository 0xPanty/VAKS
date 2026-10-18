---
record_kind: source_card
type: source
status: source-captured
title: "Astrolabe: A Content-Addressable Hypergraph for Semantic Knowledge Management"
source_id: arxiv-2604-10435-astrolabe-content-addressable-hypergraph-2026-06-07
source_uri: arxiv:2604.10435
source_url: https://arxiv.org/abs/2604.10435
pdf_url: https://arxiv.org/pdf/2604.10435
source_type: paper
author: Xinze Li
publisher: arXiv
published_at: 2026-04-12
captured_at: 2026-06-07
captured_by: Codex
extracted_at: 2026-06-07
extracted_by: Codex
extraction_tool: arXiv abstract/PDF inspection + Invoke-WebRequest metadata check
version_or_commit: "arXiv:2604.10435v1; PDF SHA256 EFDDABBA9190C64CB06B05A348113D55C25DE2240E70AA7A6A44C1AEDC44591A"
source_status: active
abstract_http_status_observed: 200
pdf_bytes_observed: 614542
raw_location: raw/papers/2026-06-07-li-astrolabe-content-addressable-hypergraph-source.md
raw_text_status: not_retained_full_pdf
processing_mode: paper-review
processing_level: medium-heavy
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
verification_status: arxiv_metadata_and_pdf_observed_design_proposal
topics:
  - semantic-knowledge-management
  - content-addressable
  - hypergraph
  - semantic-relations
  - graph-runtime
  - plugins
projects:
  - verified-action-knowledge-system
source_family: semantic-graph-knowledge-runtime-proposal
upstream_sources:
  - https://github.com/MathNetwork/Astrolabe
related_outputs:
  - outputs/review/2026-06-07-li-astrolabe-content-addressable-hypergraph-candidate-distillation.md
  - outputs/review/project_overlays/VAKS/VAKS-li-astrolabe-content-addressable-hypergraph-2026-06-07.md
tags:
  - raw-paper
  - arxiv
  - hypergraph
  - semantic-relations
  - candidate-only
---

# Source: Astrolabe Content-Addressable Hypergraph

## 为什么收录

这篇提出超越普通双向链接图谱的知识结构：关系不是简单边，而是可以有自己内容和引用列表的记录。它对 VAKS 的价值在未来 graph/relation/runtime 设计，不是当前 Markdown/YAML truth layer 替换方案。

## 来源信息

- arXiv：2604.10435
- 作者：Xinze Li
- 提交时间：2026-04-12
- PDF SHA256：`EFDDABBA9190C64CB06B05A348113D55C25DE2240E70AA7A6A44C1AEDC44591A`
- 提到实现：https://github.com/MathNetwork/Astrolabe

## Source Anchors

| Anchor | Observed topic | Candidate extraction | Boundary |
|---|---|---|---|
| Abstract | content-addressable hypergraph; SHA-256 id; ordered ref list; plugin record | relation as first-class record | proposal, not VAKS implementation |
| Related work | Obsidian/Roam/Logseq links lack semantic content | backlinks are too weak for reviewed relations | not a reason to drop Markdown |
| Data model | entry id/ref/record; width/depth decomposition | complex relation object model | too heavy for current core |
| LeanNets plugin | semantic edge records, statement/proof split, semantic propagation | future domain plugin model | math-specific demo |

## 明显疑点

- Design proposal, math-centered demo.
- Hash identity does not equal truth, support, or review.
- Full graph runtime migration would violate current VAKS boundaries.
