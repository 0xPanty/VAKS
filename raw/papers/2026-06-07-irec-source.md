---
type: source
status: source-captured
title: "Irec: A Metacognitive Scaffolding for Self-Regulated Learning through Just-in-Time Insight Recall: A Conceptual Framework and System Prototype"
source_id: 2026-06-07-irec-source
source_uri: https://arxiv.org/abs/2506.20156
source_url: https://arxiv.org/abs/2506.20156
source_type: paper
authors:
  - Xuefei Hou
  - Xizhao Tan
publisher: arXiv
venue: arXiv cs.HC
published_at: 2025-06-25
updated_at: 2025-06-25
captured_at: 2026-06-07
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-07
extraction_tool: arXiv abstract page + arXiv e-print TeX source
extraction_model: Codex
version_or_commit: arXiv:2506.20156v1
source_status: active_work_in_progress
raw_location: raw/papers/2026-06-07-irec-source.md
processing_mode: arxiv-abstract-and-tex-source-read
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
review_priority: normal
review_owner: Codex
formalization_status: source-plus-candidate-distillation
confidence_cap_reason: "v1 paper is a conceptual framework and prototype description; arXiv comments say final flowcharts, public GitHub repository, and reproducibility package are planned for v2."
source_hashes:
  arxiv_eprint_tar_gz_sha256: "51DC455BA1B4E4DD603A425A7274C3AE485A4AD865D296F579C2FF642C7599D0"
  engtest_tex_sha256: "80AD12CEAD1D4336FEBB32B3E3F9AC66DA5C5E972DE0C1E8C57BD56433E613A8"
topics:
  - ai-pkm
  - personal-knowledge-graph
  - metacognitive-scaffold
  - self-regulated-learning
  - just-in-time-recall
  - hybrid-retrieval
  - human-in-the-loop
projects:
  - verified-action-knowledge-system
source_family: irec-insight-recall
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - candidate:context_triggered_insight_recall
  - candidate:jitai_for_context_activation
  - candidate:human_ai_tag_mapping_with_fallback
  - candidate:guided_inquiry_as_reflection_deepener
tags:
  - paper
  - arxiv
  - irec
  - ai-pkm
  - candidate-source
---

# Source Record: Irec

## Why Saved

This paper is directly relevant to VAKS because it starts from the same pain
point as many recent AI + PKM references:

```text
Obsidian / Logseq style graph tools help networked thinking,
but manual links, tags, and graph hygiene become a cognitive burden.
```

Irec's useful framing is not "build another graph app." It frames recall of
personal past insights as a just-in-time metacognitive scaffold.

## Source Boundary

```text
arXiv abstract page and v1 TeX source = source provenance.
This card = raw/source record.
Candidate distillation = orientation and routing only.
No reviewed VAKS knowledge is created by this record.
No truth confidence, reviewed relation, decision, or action basis is created.
```

Important version note:

```text
The arXiv page marks this as v1 and says finalized flowcharts, public GitHub
source code, and a reproducibility package are planned for v2.
```

So this source should be treated as a conceptual / prototype reference, not as
a mature evaluated system.

## Source Identity

- Paper: `Irec: A Metacognitive Scaffolding for Self-Regulated Learning through Just-in-Time Insight Recall: A Conceptual Framework and System Prototype`
- Authors: Xuefei Hou, Xizhao Tan
- arXiv: `2506.20156`
- Submitted: 2025-06-25
- Primary URL: https://arxiv.org/abs/2506.20156
- DOI: https://doi.org/10.48550/arXiv.2506.20156
- Subjects: Human-Computer Interaction, Artificial Intelligence, Information Retrieval
- Version read: `arXiv:2506.20156v1`

## Extraction Anchors

```yaml
anchors:
  - arxiv_page:
      url: https://arxiv.org/abs/2506.20156
      fields: title/authors/abstract/comments/subjects/submission_history
  - tex_source:
      file: engtest.tex
      lines: "60-69"
      meaning: abstract, keywords, v1 note
  - tex_source:
      file: engtest.tex
      lines: "72-94"
      meaning: introduction, PKM/SRS pain, contribution claims
  - tex_source:
      file: engtest.tex
      lines: "132-186"
      meaning: theoretical model and JITAI mapping
  - tex_source:
      file: engtest.tex
      lines: "187-335"
      meaning: architecture, workflow, retrieval, reranking, tag mapping, engineering claims
  - tex_source:
      file: engtest.tex
      lines: "337-384"
      meaning: illustrative calculus scenario
  - tex_source:
      file: engtest.tex
      lines: "386-435"
      meaning: limitations, roadmap, code availability
```

## Initial Signals

```text
context-triggered recall can be framed as activation, not truth
past user insights are useful cognitive artifacts, not reviewed claims
JITAI gives a clean language for when to intervene and when to stay silent
hybrid retrieval should combine semantic, lexical, and graph/tag paths
learning/review modes can change recency/frequency/relevance weights
LLM tag mapping needs human validation and fallback rules
guided inquiry can deepen reflection, but can also amplify fixation or LLM error
```

## Current Limits

```text
No large controlled empirical evaluation in v1.
No public code or reproducibility package available in v1.
The JITAI implementation is mostly user-event triggered, not truly adaptive to real-time user state.
Static reranking weights and simple retrieval model remain future-work items.
Historical insight recall can create cognitive fixation if flawed prior insights are overtrusted.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-07-irec-candidate-distillation.md
```

## Next Step

If this becomes architecture-relevant later, review it against:

```text
Activation / Dev Context
Context Pack preparation
Point Collision and feedback loops
Viewer / Obsidian workbench
Agent memory quarantine
```

Do not promote until a separate evidence-aware review checks v2, code, empirical
evidence, or a working implementation.
