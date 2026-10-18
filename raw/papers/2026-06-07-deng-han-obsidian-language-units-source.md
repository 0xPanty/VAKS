---
type: source
status: source-captured
title: "Building a Comprehensive Knowledge Graph on Language Units Based on Obsidian"
source_id: 2026-06-07-deng-han-obsidian-language-units-source
source_uri: https://doi.org/10.1109/ICET67421.2025.11380665
source_url: https://ieeexplore.ieee.org/document/11380665/
alternate_source_url:
  - https://api.crossref.org/works/10.1109%2FICET67421.2025.11380665
  - https://www.researchgate.net/publication/400853940_Building_a_Comprehensive_Knowledge_Graph_on_Language_Units_Based_on_Obsidian
  - https://www.icet.org/files/ICET2025-Program.pdf
source_type: paper
subtype: ieee_conference_proceeding
authors:
  - "Boyang Deng"
  - "Hou Han"
publisher: IEEE
venue: "2025 5th International Conference on Educational Technology (ICET)"
event_location: "Chongqing, China"
event_dates: "2025-09-26 to 2025-09-28"
published_at: 2025-09-26
captured_at: 2026-06-07
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-07
extraction_tool: Crossref API + ResearchGate metadata + ICET 2025 program PDF + IEEE Xplore access attempt
extraction_model: Codex
version_or_commit: "DOI 10.1109/ICET67421.2025.11380665 / IEEE document 11380665 / pages 675-680"
paper_id_or_session_code: ET1193
source_status: active
raw_location: raw/papers/2026-06-07-deng-han-obsidian-language-units-source.md
processing_mode: public-metadata-only-full-text-not-accessed
processing_level: light
processing_tier: light
knowledge_status: raw
overlay_state: none
review_pressure: source_collision
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: medium
review_owner: Codex
formalization_status: source-plus-candidate-distillation
confidence_cap_reason: "Public metadata was verified, but IEEE full text was not accessible in this pass. User-provided content-addressable hypergraph claims match a separate 2026 arXiv paper, Astrolabe, and are not verified for Deng/Han."
pdf_access_status: "IEEE Xplore returned HTTP 418 / Unable to Load Page. Crossref PDF link downloaded an IEEE HTML error page, not the paper PDF."
source_metadata_quality: high_for_metadata_low_for_architecture_details
topics:
  - obsidian
  - knowledge-graph
  - language-units
  - educational-technology
  - large-unit-teaching
  - chinese-language-education
  - source-collision
projects:
  - verified-action-knowledge-system
source_family: obsidian-education-language-knowledge-graph
upstream_sources: []
verification_status: metadata-captured-fulltext-pending
candidate_relation_suggestions:
  - candidate:obsidian_as_authorable_kg_substrate_for_language_units
  - candidate:language_unit_as_mid_granularity_knowledge_object
  - candidate:curriculum_kg_requires_scope_and_sequence
  - candidate:source_collision_content_addressable_hypergraph_astrolabe
tags:
  - paper
  - ieee
  - icet-2025
  - obsidian
  - knowledge-graph
  - language-units
  - education
  - source-collision
  - candidate-source
---

# Source Record: Deng / Han Obsidian Language Units KG

## Why Saved

This paper is relevant to VAKS because it explicitly uses Obsidian as the base
for building a knowledge graph around language units.

The currently verified value is source identity and routing:

```text
Obsidian + language units + knowledge graph + educational technology
```

This makes it worth keeping as a candidate reference for:

```text
medium-granularity knowledge units
education / curriculum source modeling
Obsidian as an authorable graph substrate
```

## Source Boundary

```text
Crossref / ResearchGate / ICET program = public metadata and schedule provenance.
IEEE Xplore full text was not accessed.
This card = raw/source record.
Candidate distillation = orientation and routing only.
No reviewed VAKS knowledge is created by this record.
No truth confidence, reviewed relation, decision, or action basis is created.
```

Important access note:

```text
IEEE Xplore returned HTTP 418 / Unable to Load Page.
The Crossref PDF link downloaded an IEEE HTML error page, not the paper PDF.
No private account, institutional access, or cookies were used.
```

## Source Identity

- Title: `Building a Comprehensive Knowledge Graph on Language Units Based on Obsidian`
- Authors: Boyang Deng; Hou Han
- DOI: https://doi.org/10.1109/ICET67421.2025.11380665
- IEEE Xplore: https://ieeexplore.ieee.org/document/11380665/
- Publisher: IEEE
- Venue: 2025 5th International Conference on Educational Technology (ICET)
- Location: Chongqing, China
- Event dates: 2025-09-26 to 2025-09-28
- Pages: 675-680
- ICET program slot: ET1193, 17:30-17:45
- Presenter: Boyang Deng
- Affiliation in ICET program: South China Normal University, China

## Key Entity Check

```yaml
document_id: "11380665"
doi: "10.1109/ICET67421.2025.11380665"
publisher: "IEEE"
conference: "2025 5th International Conference on Educational Technology (ICET)"
event_location: "Chongqing, China"
pages: "675-680"
authors:
  - "Boyang Deng"
  - "Hou Han"
crossref_affiliation:
  - "South China Normal University, School of Chinese Language and Literature, Guangzhou, China"
program_affiliation:
  - "South China Normal University, China"
```

## Extraction Anchors

```yaml
anchors:
  - crossref_api:
      url: https://api.crossref.org/works/10.1109%2FICET67421.2025.11380665
      meaning: DOI, title, authors, IEEE publisher, ICET 2025 venue, event date/location, pages, references
  - researchgate_metadata:
      url: https://www.researchgate.net/publication/400853940_Building_a_Comprehensive_Knowledge_Graph_on_Language_Units_Based_on_Obsidian
      lines: "4-12,17-29,60-70"
      meaning: title, September 2025, DOI, ICET venue, authors, no full text available
  - icet_program:
      url: https://www.icet.org/files/ICET2025-Program.pdf
      lines: "2086-2091"
      meaning: program slot, title, authors, presenter, affiliation, paper code ET1193
  - ieee_access_attempt:
      url: https://ieeexplore.ieee.org/document/11380665/
      result: "HTTP 418 / Unable to Load Page"
  - crossref_pdf_link_attempt:
      url: http://xplorestaging.ieee.org/ielx8/11379869/11380405/11380665.pdf?arnumber=11380665
      result: "HTML error page, not PDF; SHA256 CF7BF49AD9C890D04340FAD0896BB17C7FBFCA1C0D103CA4771AA8AF241ABE97 belongs to error page only"
```

## Source Collision: Hypergraph Claims

The user-provided summary attaches the following mechanism to this IEEE paper:

```text
content-addressable hypergraph
SHA-256 identity
arbitrary-width ordered references
opaque plugin-interpreted records
width / depth decomposition
```

In public search, this exact mechanism matches a different paper:

```text
Astrolabe: A Content-Addressable Hypergraph for Semantic Knowledge Management
arXiv:2604.10435
author: Xinze Li
submitted: 2026-04-12
```

Astrolabe's arXiv abstract explicitly says entries are identified by the SHA-256
hash of their content, carry an ordered reference list of arbitrary width, store
an opaque record string interpreted by plugins, and admit width/depth
decompositions.

Therefore, in this VAKS record:

```text
content-addressable hypergraph details are not attributed to Deng/Han
until the IEEE full text is obtained and checked.
```

## What Can Be Safely Inferred Now

From verified metadata and references, this paper is most likely about:

```text
building a knowledge graph for language units
using Obsidian as an authoring / organization substrate
within educational technology and Chinese language curriculum contexts
```

Crossref references are mainly around:

```text
Chinese language curriculum standards
large-unit teaching design
language learning tasks
curriculum / textbook research
knowledge modeling in education
```

## Initial VAKS Signals

```text
Language unit can be treated as a useful mid-granularity knowledge object.
Obsidian may serve as a low-friction graph authoring surface for domain experts.
Curriculum or language-unit graphs need sequence, scope, task, and competency context.
Formal conference metadata does not equal full-text architecture verification.
Source collision checks are important before borrowing named mechanisms.
```

## Full-Text Verification Needed

Check the IEEE full text before using any of these for architecture:

```text
actual graph data model
relation types and language-unit schema
how Obsidian links/tags/plugins are used
whether there is any hypergraph or content-addressing mechanism
whether there is an implementation, diagram, or evaluation
what "comprehensive" means operationally
how language units are decomposed or sequenced
```

## Current Limits

```text
Full text was not accessible in this pass.
No abstract from IEEE Xplore was available through public access here.
Public metadata supports identity and topic, not detailed architecture claims.
The strongest hypergraph claims appear to belong to Astrolabe, a separate source.
No VAKS schema, reviewed relation, decision, or action basis should be changed from this record.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-07-deng-han-obsidian-language-units-candidate-distillation.md
```
