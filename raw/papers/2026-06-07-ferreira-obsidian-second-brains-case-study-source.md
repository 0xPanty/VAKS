---
record_kind: source_card
type: source
status: source-captured
title: "How People Manage Knowledge in their \"Second Brains\" - A Case Study with Industry Researchers Using Obsidian"
source_id: arxiv-2509-20187-obsidian-second-brains-case-study-2026-06-07
source_uri: arxiv:2509.20187
source_url: https://arxiv.org/abs/2509.20187
pdf_url: https://arxiv.org/pdf/2509.20187
source_type: paper
author: Juliana Jansen Ferreira; Vinícius Segura; Joana Gabriela Souza; Joao Henrique Gallas Brasil
publisher: arXiv
published_at: 2025-09-24
captured_at: 2026-06-07
captured_by: Codex
extracted_at: 2026-06-07
extracted_by: Codex
extraction_tool: arXiv abstract/PDF inspection + Invoke-WebRequest metadata check
version_or_commit: "arXiv:2509.20187v1; PDF SHA256 730AD0B69B8577496D225E73E97EDD244623FCE9D3B876FE0481DEFAE3B0C52D"
source_status: active
abstract_http_status_observed: 200
pdf_bytes_observed: 543213
raw_location: raw/papers/2026-06-07-ferreira-obsidian-second-brains-case-study-source.md
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
verification_status: arxiv_metadata_and_pdf_observed_not_independently_peer_reviewed
topics:
  - obsidian
  - second-brain
  - personal-knowledge-base
  - user-study
  - retrieval-strategy
  - pkm
projects:
  - verified-action-knowledge-system
source_family: empirical-obsidian-pkm-case-study
related_outputs:
  - outputs/review/2026-06-07-ferreira-obsidian-second-brains-case-study-candidate-distillation.md
  - outputs/review/project_overlays/VAKS/VAKS-ferreira-obsidian-second-brains-case-study-2026-06-07.md
tags:
  - raw-paper
  - arxiv
  - obsidian
  - pkm
  - candidate-only
---

# Source: Obsidian Second Brains Case Study

## 为什么收录

这是 Obsidian PKM 的真实用户研究，比博客/模板更适合作为证据型参考。论文访谈巴西实验室的 7 位计算机研究员，观察他们如何用 Obsidian 构建、组织和检索个人知识库。

## 来源信息

- arXiv：2509.20187
- 提交时间：2025-09-24
- PDF SHA256：`730AD0B69B8577496D225E73E97EDD244623FCE9D3B876FE0481DEFAE3B0C52D`
- 原文全文：未复制保留；本卡只保留 provenance 和候选抽取。

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  action_basis_allowed: false
truth_mutation_allowed: false
```

## Source Anchors

| Anchor | Observed topic | Candidate extraction | Boundary |
|---|---|---|---|
| arXiv abstract | retrieval strategy influences PKB construction | retrieval and intake must be co-designed | small sample |
| PDF methodology | 7 CS researchers from Brazilian lab, interviews and observation tasks | useful empirical lens | specific population |
| PDF findings | folders, tags, links, inbox, search | real retrieval modes should inform structure | not universal schema |
| PDF discussion | starter structure, flexible reorganization, AI support ideas | AI support should cover create-organize-retrieve-use | feature suggestions only |

## 明显疑点

- Small, specific participant group.
- Obsidian behavior is case-study evidence, not VAKS truth.
- AI support suggestions are design ideas, not implemented results.
