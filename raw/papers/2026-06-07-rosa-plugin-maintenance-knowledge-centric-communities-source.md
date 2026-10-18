---
record_kind: source_card
type: source
status: source-captured
title: "Not Only for Developers: Exploring Plugin Maintenance for Knowledge-Centric Communities"
source_id: arxiv-2602-17018-plugin-maintenance-knowledge-centric-communities-2026-06-07
source_uri: arxiv:2602.17018
source_url: https://arxiv.org/abs/2602.17018
pdf_url: https://arxiv.org/pdf/2602.17018
source_type: paper
author: Giovanni Rosa; David Moreno-Lumbreras; Raula Gaikovina Kula
publisher: arXiv
published_at: 2026-02-19
captured_at: 2026-06-07
captured_by: Codex
extracted_at: 2026-06-07
extracted_by: Codex
extraction_tool: arXiv abstract/PDF inspection + Invoke-WebRequest metadata check
version_or_commit: "arXiv:2602.17018v1; PDF SHA256 B0C0B43333CC4A7A73DB7D6B4E317243D88C4D5EB193BD0B2EF99C74D37642EC"
source_status: active
publication_status: accepted_to_SANER2026
abstract_http_status_observed: 200
pdf_bytes_observed: 481395
raw_location: raw/papers/2026-06-07-rosa-plugin-maintenance-knowledge-centric-communities-source.md
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
verification_status: arxiv_metadata_and_pdf_observed_early_results
topics:
  - obsidian
  - plugin-ecosystem
  - software-maintenance
  - knowledge-centric-community
  - runtime-workbench
  - skills
projects:
  - verified-action-knowledge-system
source_family: obsidian-plugin-ecosystem-study
related_outputs:
  - outputs/review/2026-06-07-rosa-plugin-maintenance-knowledge-centric-communities-candidate-distillation.md
  - outputs/review/project_overlays/VAKS/VAKS-rosa-plugin-maintenance-knowledge-centric-communities-2026-06-07.md
tags:
  - raw-paper
  - arxiv
  - obsidian
  - plugin-ecosystem
  - candidate-only
---

# Source: Plugin Maintenance for Knowledge-Centric Communities

## 为什么收录

这篇论文以 Obsidian 插件生态为例，研究非纯开发者社区如何形成和维护插件生态。它对 VAKS 的价值在 runtime/plugin/skill/workbench 治理，不是 truth core。

## 来源信息

- arXiv：2602.17018
- 提交时间：2026-02-19
- 状态：Accepted to SANER2026
- PDF SHA256：`B0C0B43333CC4A7A73DB7D6B4E317243D88C4D5EB193BD0B2EF99C74D37642EC`

## Source Anchors

| Anchor | Observed topic | Candidate extraction | Boundary |
|---|---|---|---|
| Abstract | 396 plugins, LLM topic modeling, 6 plugin themes | plugin taxonomy can guide tool routing | LLM labels are not final taxonomy |
| Methodology | registry snapshot, README enrichment, BERTopic | ecosystem analysis can be data-driven | sampling and model bias |
| Results | PR activity across topics | maintenance metrics can inform adoption gates | PR activity is not safety/quality |
| Limitations | early results, sample subset, PR-only metric | use as preview, not final authority | needs future validation |

## 明显疑点

- Research preview, not full longitudinal study.
- PR activity is a maintenance signal only.
- Plugin ecosystem relevance does not imply plugin adoption.
