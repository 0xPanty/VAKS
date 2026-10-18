---
type: source
record_kind: source_card
status: source-captured
title: "From Personal Knowledge Management to the Second Brain to the Personal AI Companian"
title_normalized_alias: "From Personal Knowledge Management to the Second Brain to the Personal AI Companion"
source_id: 2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source
source_uri: https://doi.org/10.1145/3688828.3699647
source_url: https://dl.acm.org/doi/10.1145/3688828.3699647
alternate_source_url:
  - https://group.acm.org/conferences/group25/proceedings.php
  - https://dblp.org/rec/conf/group/AalR25.html
  - https://www.wineme.uni-siegen.de/en/team/former-colleagues/rueller/
source_type: paper
subtype: conference_proceeding
authors:
  - 'Konstantin "Kosta" Aal'
  - "Sarah Ruller"
author_name_note: "Sarah Rüller in source metadata; ASCII filename uses ruller."
publisher: ACM
venue: "Companion Proceedings of the 2025 ACM International Conference on Supporting Group Work"
series: "GROUP '25"
published_at: 2025-01-12
captured_at: 2026-06-07
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-07
extraction_tool: Crossref API + GROUP 2025 proceedings page + DBLP + University of Siegen author page
extraction_model: Codex
version_or_commit: DOI 10.1145/3688828.3699647 / pages 90-93
source_status: active
raw_location: raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md
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
confidence_cap_reason: "Public abstract and metadata were read; ACM PDF returned 403 without authorized access, so detailed layer claims from the user summary remain pending full-text verification."
pdf_access_status: "ACM PDF URL returned 403 Forbidden without authorized access; no private cookies or account access used."
source_metadata_quality: high_for_metadata_medium_for_design_details
topics:
  - personal-knowledge-management
  - second-brain
  - personal-ai-companion
  - ai-knowledge-graph
  - proactive-ai
  - privacy
  - user-autonomy
  - group-2025
projects:
  - verified-action-knowledge-system
source_family: ai-second-brain-pkm-companion
upstream_sources: []
verification_status: metadata-and-abstract-captured
candidate_relation_suggestions:
  - candidate:pkm_to_second_brain_to_ai_companion_trajectory
  - candidate:active_companion_over_passive_organizer
  - candidate:multi_stream_personal_knowledge_overview
  - candidate:privacy_autonomy_guardrails_for_personal_ai
tags:
  - paper
  - acm
  - group-2025
  - pkm
  - second-brain
  - personal-ai-companion
  - candidate-source
why_saved: see_body_or_legacy_record
---

# Source Record: Aal / Ruller PKM to Personal AI Companian

## Why Saved

This paper is highly relevant to VAKS because it explicitly frames the evolution:

```text
personal knowledge management
-> second brain
-> personal AI companion
```

The public abstract positions current tools as strong at organizing information,
while the envisioned next step is an AI companion that actively engages with
multiple data streams to create a dynamic personalized knowledge overview.

For VAKS, this is useful as a high-level architecture reference for:

```text
activation
context pack preparation
proactive-but-bounded suggestion
personal knowledge graph / second brain framing
privacy and autonomy guardrails
```

## Source Boundary

```text
DOI/Crossref/DBLP/GROUP page/author page = metadata and abstract provenance.
This card = raw/source record.
Candidate distillation = orientation and routing only.
No reviewed VAKS knowledge is created by this record.
No truth confidence, reviewed relation, decision, or action basis is created.
```

Important access note:

```text
The ACM PDF endpoint returned 403 Forbidden without authorized access.
This intake does not claim to have read the PDF full text and does not store a PDF.
```

The user's summary mentions specific design details such as chat, email, notes,
video, local server, encryption, and multi-layer architecture. This intake records
those as useful leads, but marks them as pending full-text verification.

## Source Identity

- Official title: `From Personal Knowledge Management to the Second Brain to the Personal AI Companian`
- Normalized alias: `From Personal Knowledge Management to the Second Brain to the Personal AI Companion`
- Authors: Konstantin "Kosta" Aal; Sarah Rüller
- Publisher: ACM
- Venue: Companion Proceedings of the 2025 ACM International Conference on Supporting Group Work
- Series: GROUP '25
- Pages: 90-93
- DOI: https://doi.org/10.1145/3688828.3699647
- ACM URL: https://dl.acm.org/doi/10.1145/3688828.3699647

## Key Entity Check

```yaml
official_title_spelling: "Companian"
normalized_alias_spelling: "Companion"
authors:
  - 'Konstantin "Kosta" Aal'
  - "Sarah Rüller"
doi: "10.1145/3688828.3699647"
pages: "90-93"
publisher: "ACM"
series: "GROUP '25"
container_crossref: "The 2025 ACM International Conference on Supporting Group Work"
```

## Extraction Anchors

```yaml
anchors:
  - crossref:
      url: https://api.crossref.org/works/10.1145%2F3688828.3699647
      fields: title/authors/publisher/issued/container/pages/doi/type
  - group_2025_proceedings:
      url: https://group.acm.org/conferences/group25/proceedings.php
      lines: "186-193"
      meaning: title, authors, public abstract, ACM link
  - dblp:
      url: https://dblp.org/rec/conf/group/AalR25.html
      meaning: DOI, closed access status, type, metadata version, pages 90-93
  - university_of_siegen_author_page:
      url: https://www.wineme.uni-siegen.de/en/team/former-colleagues/rueller/
      lines: "429-465"
      meaning: BibTeX-style metadata, abstract, pages, publisher, ISBN
  - pdf_access_attempt:
      url: https://dl.acm.org/doi/pdf/10.1145/3688828.3699647
      result: "403 Forbidden without authorized access"
```

## Initial VAKS Signals

```text
Second brain should evolve from passive storage into active assistance.
Personal AI companion should synthesize multiple personal data streams.
Dynamic personalized knowledge overview can support insight and decision support.
Proactive AI must preserve privacy, user autonomy, and critical thinking.
AI companions should augment human intelligence rather than replace it.
```

## Full-Text Verification Needed

The following user-provided claims are plausible and useful, but were not
independently verified from the accessible abstract in this pass:

```text
exact data streams: chat / email / notes / video
local server + encryption implementation details
multi-layer architecture: data ingestion / graph construction / interaction
specific critique of Obsidian vault limitations
exact claim that Obsidian/Notion are baseline information organization tools
citation count / impact count
```

They should be checked against the ACM PDF or another authorized full-text copy
before promotion, architecture merge, or action-facing use.

## Current Limits

```text
Short companion paper, pages 90-93.
Accessible public evidence is mainly abstract and metadata.
No implementation, empirical validation, or benchmark was verified in this pass.
Architecture details beyond the abstract are pending full-text review.
Citation counts are volatile and were not used as authority.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-candidate-distillation.md
```

## Next Step

If a full PDF or authorized copy is available, run a second pass focused on:

```text
actual architecture layers
exact data sources
privacy/encryption/local hosting details
interaction model
claims about Obsidian / Notion limitations
risks and user autonomy safeguards
```

Do not promote until those anchors are inspected.
