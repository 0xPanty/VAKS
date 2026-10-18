---
type: source
status: source-captured
title: 'How People Manage Knowledge in their "Second Brains"- A Case Study with Industry Researchers Using Obsidian'
title_normalized_alias: 'How People Manage Knowledge in their "Second Brains": A Case Study with Industry Researchers Using Obsidian'
source_id: 2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source
source_uri: https://arxiv.org/abs/2509.20187
source_url: https://arxiv.org/pdf/2509.20187
alternate_source_url:
  - https://arxiv.org/abs/2509.20187
  - https://research.ibm.com/publications/how-people-manage-knowledge-in-their-second-brains-a-case-study-with-industry-researchers-using-obsidian
  - https://doi.org/10.1007/978-3-032-05008-3_15
source_type: paper
subtype: arxiv_preprint_and_interact_2025_chapter
authors:
  - "Juliana Jansen Ferreira"
  - "Vinícius Segura"
  - "Joana Gabriela Souza"
  - "Joao Henrique Gallas Brasil"
author_name_note: "arXiv/PDF spell Joao without accent; user-provided context uses João."
publisher: arXiv / Springer
venue: INTERACT 2025
series: "Human-Computer Interaction - INTERACT 2025"
published_at: 2025-09-24
conference_publication_date: 2025-09-08
captured_at: 2026-06-07
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-07
extraction_tool: arXiv abs page + arXiv PDF + IBM Research publication page + DOI lookup
extraction_model: Codex
version_or_commit: "arXiv:2509.20187v1 / DOI 10.1007/978-3-032-05008-3_15"
pdf_sha256: 730AD0B69B8577496D225E73E97EDD244623FCE9D3B876FE0481DEFAE3B0C52D
pdf_sha256_scope: "temporary arXiv PDF download on 2026-06-07; PDF not retained as repository artifact"
source_status: active
raw_location: raw/papers/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source.md
processing_mode: official-metadata-and-public-pdf-read
processing_level: medium
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
review_priority: high
review_owner: Codex
formalization_status: source-plus-candidate-distillation
confidence_cap_reason: "Full arXiv PDF was readable and hash-checked, but findings are still from a small qualitative case study and remain candidate until evidence-aware review."
source_metadata_quality: high
topics:
  - obsidian
  - second-brain
  - personal-knowledge-base
  - empirical-study
  - vault-structure
  - retrieval-strategy
  - tags
  - links
  - templates
  - inbox
  - ai-assistance
  - dynamic-reorganization
  - multi-device
projects:
  - verified-action-knowledge-system
source_family: obsidian-second-brain-empirical-pkm
upstream_sources: []
verification_status: metadata-and-pdf-captured
candidate_relation_suggestions:
  - candidate:retrieval_strategy_shapes_vault_structure
  - candidate:context_sensitive_note_creation
  - candidate:dynamic_reorganization_as_normal_vault_behavior
  - candidate:ai_as_metadata_and_retrieval_assistant
  - candidate:multi_vault_multi_device_friction
tags:
  - paper
  - arxiv
  - interact-2025
  - obsidian
  - second-brain
  - pkm
  - empirical-study
  - candidate-source
---

# Source Record: Ferreira et al. Obsidian Second Brains

## Why Saved

This paper is a direct empirical reference for VAKS because it studies how
industry researchers actually build and retrieve knowledge in Obsidian vaults.

The strongest source-backed signal is:

```text
retrieval strategy influences how people create, organize, and maintain notes
```

For VAKS, that matters because source cards, tags, templates, indexes, and
context-pack retrieval should be designed together. Capture structure is not a
neutral filing choice; it shapes what can be found later.

## Source Boundary

```text
arXiv / IBM / DOI metadata = source identity and publication provenance
arXiv PDF = primary readable text for this pass
this card = raw/source record
candidate distillation = orientation and routing only
no reviewed VAKS knowledge is created
no truth confidence, reviewed relation, decision, or action basis is created
```

## Source Identity

- Official arXiv title: `How People Manage Knowledge in their "Second Brains"- A Case Study with Industry Researchers Using Obsidian`
- Normalized title alias: `How People Manage Knowledge in their "Second Brains": A Case Study with Industry Researchers Using Obsidian`
- Authors: Juliana Jansen Ferreira; Vinícius Segura; Joana Gabriela Souza; Joao Henrique Gallas Brasil
- arXiv: https://arxiv.org/abs/2509.20187
- PDF: https://arxiv.org/pdf/2509.20187
- arXiv submitted date: 2025-09-24
- Related DOI: https://doi.org/10.1007/978-3-032-05008-3_15
- IBM publication page: https://research.ibm.com/publications/how-people-manage-knowledge-in-their-second-brains-a-case-study-with-industry-researchers-using-obsidian
- IBM listed publication: INTERACT 2025

## Key Entity Check

```yaml
arxiv_id: "2509.20187"
arxiv_submission: "2025-09-24"
arxiv_subjects:
  - "Human-Computer Interaction (cs.HC)"
  - "Artificial Intelligence (cs.AI)"
related_doi: "10.1007/978-3-032-05008-3_15"
paper_length: "9 pages, 3 figures"
pdf_sha256: "730AD0B69B8577496D225E73E97EDD244623FCE9D3B876FE0481DEFAE3B0C52D"
participants_from_pdf: "7 Computer Science researchers from a Brazilian research lab"
method_from_pdf: "interviews plus observation tasks in participants' Obsidian vaults"
```

Important correction:

```text
The source-backed participant count in the arXiv PDF is 7, not 9.
This is a small qualitative case study, not a large-scale empirical study.
```

## Extraction Anchors

```yaml
anchors:
  - arxiv_abs:
      url: https://arxiv.org/abs/2509.20187
      lines: "30-52"
      meaning: title, authors, submitted date, abstract, DOI, subjects
  - ibm_publication_page:
      url: https://research.ibm.com/publications/how-people-manage-knowledge-in-their-second-brains-a-case-study-with-industry-researchers-using-obsidian
      lines: "0-9,48-61"
      meaning: INTERACT 2025 listing, date, authors, abstract
  - pdf_abstract:
      url: https://arxiv.org/pdf/2509.20187
      lines: "0-18"
      meaning: abstract and core finding
  - pdf_method:
      url: https://arxiv.org/pdf/2509.20187
      lines: "70-106"
      meaning: case study setup, seven participants, interview and observation method, analysis process
  - pdf_creation_organization:
      url: https://arxiv.org/pdf/2509.20187
      lines: "112-165"
      meaning: note creation context, folders, tags, templates, links, inbox flow
  - pdf_retrieval:
      url: https://arxiv.org/pdf/2509.20187
      lines: "166-206"
      meaning: search, tags, links, sequential navigation, multi-vault confusion
  - pdf_design_implications:
      url: https://arxiv.org/pdf/2509.20187
      lines: "207-236"
      meaning: AI-feature discussion and framework design implications
  - pdf_limitations:
      url: https://arxiv.org/pdf/2509.20187
      lines: "237-245"
      meaning: participant-profile limitation and future work
```

## What The Paper Says

### Method

The study uses a case-study method around Obsidian. The participants were seven
Computer Science researchers from a Brazilian research lab who used Obsidian.
The researchers conducted interviews and included observation tasks in which
participants demonstrated their own vault practices.

### Main Empirical Finding

The paper's most useful finding for VAKS is that participants' expected
retrieval strategy affects how they build and maintain their vault content.

In plain terms:

```text
people do not just retrieve what they previously stored;
they store things in ways shaped by how they expect to retrieve them later.
```

### Observed Obsidian Practices

The PDF surfaces several practical structures:

```text
folders
tags
links
templates
inbox/refinement flows
search
tag-click retrieval
link/backlink-style retrieval
sequential folder/index navigation
multi-vault navigation friction
```

### AI Assistance Direction

The paper frames AI support as design ideas for the knowledge-management
process, especially where creation, organization, retrieval, and use connect.
The safe VAKS reading is:

```text
AI can help with metadata, retrieval, organization suggestions, templates, and context,
but those suggestions are assistance, not reviewed knowledge.
```

## Initial VAKS Signals

```text
Retrieval and capture must be co-designed.
Templates are not cosmetic; they encode future retrieval paths.
Tags are not truth labels; they are retrieval and organization aids.
Inbox/refinement is a natural light-to-medium processing flow.
Vault structures are dynamic and should be easy to reorganize.
Multi-vault and multi-device friction should be treated as product/workbench risk.
AI assistance should stay in metadata/retrieval/context support unless reviewed.
```

## Current Limits

```text
Small qualitative sample: seven Computer Science researchers.
Specific organizational practices are empirical observations, not universal design law.
The paper studies Obsidian users in one research-lab context.
No VAKS schema, promotion rule, or reviewed relation should be changed from this source alone.
Venue prestige and topical relevance do not create truth confidence.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-candidate-distillation.md
```
