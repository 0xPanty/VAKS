---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: light
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: source_collision
derived_from:
  - raw/papers/2026-06-07-deng-han-obsidian-language-units-source.md
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
  - obsidian-workbench
  - educational-knowledge-graph
  - language-units
  - curriculum-knowledge-modeling
  - source-collision
  - fulltext-required
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - source_ref: raw/papers/2026-06-07-deng-han-obsidian-language-units-source.md
    selector_type: crossref_metadata
    selector_value: "Crossref API: DOI, title, Boyang Deng / Hou Han, IEEE, ICET 2025, Chongqing, pages 675-680, references"
  - source_ref: raw/papers/2026-06-07-deng-han-obsidian-language-units-source.md
    selector_type: researchgate_metadata_lines
    selector_value: "ResearchGate lines 4-12,17-29,60-70: title, DOI, ICET venue, authors, no full text available"
  - source_ref: raw/papers/2026-06-07-deng-han-obsidian-language-units-source.md
    selector_type: icet_program_lines
    selector_value: "ICET program lines 2086-2091: ET1193 schedule slot, title, authors, presenter, affiliation"
  - source_ref: raw/papers/2026-06-07-deng-han-obsidian-language-units-source.md
    selector_type: source_collision_anchor
    selector_value: "Astrolabe arXiv:2604.10435 abstract carries the content-addressable hypergraph / ordered references / plugin records / width-depth decomposition claims"
reference_layer_tag: ref/obsidian-language-units-kg
reference_layer_label_zh: Obsidian 语言单元知识图谱
reference_layer_scope: "educational language-unit KG / source-collision aware candidate reference only"
borrow_value: medium
borrow_order:
  - "P1: Keep as an Obsidian + language-unit knowledge graph source, especially for medium-granularity domain unit modeling."
  - "P1: Preserve the source-collision warning: content-addressable hypergraph claims should not be attributed to Deng/Han without IEEE full-text verification."
  - "P2: Language/curriculum unit graphs may help VAKS think about scope, sequence, task, and competency context in structured source intake."
  - "P3: Use IEEE/ICET publication status only as provenance; venue status is not truth confidence or architecture authority."
avoid:
  - "Do not treat the content-addressable hypergraph mechanism as verified for this paper."
  - "Do not import Astrolabe's SHA-256 / arbitrary-width refs / plugin record / width-depth decomposition into Deng/Han."
  - "Do not treat IEEE indexing, venue label, or ResearchGate page as evidence support for architectural claims."
  - "Do not promote this into reviewed VAKS schema, relation model, pattern, or decision without full text."
  - "Do not overstate this as a top-tier CS/HCI paper; verified venue is ICET 2025 educational technology."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Reviewing full IEEE text or designing educational/language-unit source modeling in VAKS."
  support_when: "Discussing Obsidian as a domain-expert graph authoring surface, language/curriculum unit decomposition, or medium-granularity knowledge objects."
  risk_when: "Any source starts mixing Deng/Han with Astrolabe or treats publication metadata as confirmation of graph architecture details."
  cold_references:
    - raw/papers/2026-06-07-deng-han-obsidian-language-units-source.md
tags:
  - candidate
  - provisional
  - ieee
  - icet-2025
  - obsidian
  - knowledge-graph
  - language-units
  - education
  - source-collision
  - candidate-only
---

# Candidate Distillation: Obsidian Language Units KG

## Boundary

This note is provisional orientation.

It distills public metadata for Deng / Han's IEEE ICET paper and records a
source-collision warning. It is not reviewed knowledge, not a decision, not a
formal pattern, and not action basis.

Strongest safe use now:

```text
Obsidian + language-unit knowledge graph as a candidate education-domain reference
```

Unsafe use now:

```text
borrowing detailed hypergraph architecture from this paper
```

because the full IEEE text was not accessible, and the named hypergraph mechanism
matches a separate 2026 arXiv paper.

## 一句话

这篇先别当成“Obsidian 内容可寻址超图”的确认来源。

更稳的读法是：

```text
Deng/Han = Obsidian 做语言单元知识图谱的教育技术应用来源。
Astrolabe = 内容可寻址超图机制的真正公开匹配来源。
```

人话：

```text
这篇可以留下，但要贴一个醒目的防串线标签。
它可能对“怎么把领域单元做成 Obsidian 图谱”有用；
但你摘要里最硬的超图机制，不能先算到它头上。
```

## 借用优先级

### P1: `obsidian_as_authorable_kg_substrate`

候选结论：

```text
Obsidian 可以作为领域专家可写、可链接、可维护的知识图谱底座。
```

已验证来源：

```text
title + DOI metadata + ICET program:
Building a Comprehensive Knowledge Graph on Language Units Based on Obsidian
```

VAKS 可借：

```text
markdown-first graph authoring
domain experts can maintain notes before graph formalization
links/tags/frontmatter can act as light graph scaffolding
```

边界：

```text
Obsidian graph = authoring / navigation / activation surface
not reviewed relation graph by default
```

### P1: `source_collision_guard`

候选结论：

```text
When a summary attaches very specific architecture terms to a paper, verify whether those terms actually belong to that source.
```

This source has a collision:

```text
content-addressable hypergraph
SHA-256 identity
ordered arbitrary-width references
opaque plugin records
width/depth decomposition
```

These exact claims publicly match:

```text
Astrolabe: A Content-Addressable Hypergraph for Semantic Knowledge Management
arXiv:2604.10435
```

VAKS 可借：

```text
source identity check before mechanism borrowing
source-collision label in raw/source and candidate notes
full-text gate before architecture adoption
```

### P2: `language_unit_as_mid_granularity`

候选结论：

```text
Language unit can be treated as a mid-granularity knowledge object.
```

VAKS 可借：

```text
not every source unit has to be an atomic claim
some domains need middle objects:
  lesson unit
  curriculum task
  text cluster
  concept sequence
  competency target
```

This is useful when designing:

```text
source cards for courses / curricula / reading programs
knowledge objects that sit between raw source and atomic candidate points
```

边界：

```text
mid-granularity object = organization / comprehension aid
not truth unit unless separately reviewed
```

### P2: `curriculum_kg_needs_scope_sequence_task`

候选结论：

```text
Educational language-unit graphs likely need more than simple concept links.
```

Crossref references point toward:

```text
Chinese curriculum standards
large-unit teaching design
core learning tasks
textbook and language teaching frameworks
```

VAKS 可借 as a question set:

```text
What is the unit?
What sequence does it sit in?
What task or competency is it for?
What source / textbook / standard anchors it?
What is prerequisite vs association vs assessment target?
```

边界：

```text
These are candidate modeling questions, not confirmed Deng/Han schema.
```

### P3: `metadata_only_confidence_cap`

候选结论：

```text
Formal publication metadata can justify preserving a source, but not borrowing its detailed mechanism.
```

Use now:

```text
keep in vault
route for later full-text review
compare with Astrolabe if hypergraph architecture becomes important
```

Do not use now:

```text
architecture decision
relation-model revision
evidence support
action basis
```

## 对用户摘要的校正

Verified:

```text
IEEE proceedings article: yes.
ICET 2025: yes.
Authors: Boyang Deng and Hou Han.
Topic: Obsidian + language units + knowledge graph.
Pages: 675-680.
```

Not verified for this paper:

```text
content-addressable hypergraph
SHA-256 content identity
arbitrary-width ordered reference list
plugin-interpreted opaque record string
width/depth decomposition
```

Likely source of those details:

```text
Astrolabe: A Content-Addressable Hypergraph for Semantic Knowledge Management
arXiv:2604.10435
```

## VAKS 融合判断

### Should Borrow Now

```text
source-collision discipline
Obsidian as a domain-expert KG authoring surface
language/curriculum unit as a mid-granularity modeling object
full-text gate before architecture claims
```

### Should Wait For Full Text

```text
actual graph schema
relation vocabulary
Obsidian implementation path
plugin usage
examples / figures
evaluation method
whether any hypergraph mechanism exists
```

### Should Not Borrow From This Source Now

```text
content-addressable hypergraph
SHA-256 identity
arbitrary-width ordered refs
plugin record model
width/depth decomposition
```

Those may be worth a separate Astrolabe intake, but they should not be attributed
to Deng/Han without full-text verification.

## Candidate Points For Later Review

### CP-001: `language_unit_mid_granularity_object`

Candidate:

```text
VAKS may need mid-granularity source objects for educational/curriculum materials, between raw source records and atomic candidate points.
```

Review need:

```text
Acquire full Deng/Han text and inspect how it defines language units and graph nodes/edges.
```

### CP-002: `obsidian_domain_graph_authoring_surface`

Candidate:

```text
Obsidian can support domain-expert graph authoring before formal graph extraction.
```

Review need:

```text
Check whether Deng/Han uses folders, links, tags, frontmatter, plugins, canvases, or other Obsidian features.
```

### CP-003: `source_collision_before_borrowing`

Candidate:

```text
Named architecture mechanisms should pass a source identity check before being imported into VAKS.
```

Review need:

```text
If content-addressable hypergraph matters, open a separate Astrolabe source card and compare against Deng/Han after full-text access.
```

### CP-004: `publication_status_is_not_architecture_evidence`

Candidate:

```text
IEEE indexing and DOI metadata are provenance signals, not evidence that a specific architecture exists in the paper.
```

Review need:

```text
Keep this as a confidence-cap rule for future paper-scouting intake.
```

## Current Activation Use

Use this candidate note early when a task is about:

```text
Obsidian in education
language-unit / curriculum knowledge graph
domain-expert graph authoring
source collision checks
full-text verification queue
```

Do not use it as:

```text
proof of content-addressable hypergraph architecture
reviewed VAKS pattern
architecture decision
action-ready basis
```
