---
type: source
status: source-captured
title: "OneFeed: A Unified Generative Framework for Feed Content Enhancement and Query Generation"
source_id: 2026-06-11-guoxun-onefeed-source
source_uri: https://arxiv.org/abs/2606.07972
source_url: https://arxiv.org/abs/2606.07972
source_type: paper
authors:
  - Guo Xun
publisher: arXiv
published_at: 2026-06-06
updated_at: 2026-06-06
captured_at: 2026-06-11
captured_by: Codex
version_or_commit: arXiv:2606.07972v1
doi: https://doi.org/10.48550/arXiv.2606.07972
source_integrity:
  pdf_location: raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/2606.07972v1.pdf
  pdf_sha256: 61d7613b1ce418292e7454ac9fe69d35a73ef03162470356e0e464b87c381ed5
  eprint_tar_location: raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/2606.07972v1-eprint.tar
  eprint_tar_sha256: 8ce240d98b28adbbf6f36108f0ce7975ed46de015dbb44ecab93e90d75b098c7
  abs_html_location: raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/2606.07972v1-abs.html
  abs_html_sha256: 000891cf29a0f8d3cf16be0723eb198b16487879bdb062ad281bae47a6dda64f
  main_tex_location: raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/eprint/main.tex
  main_tex_sha256: 422c7004f3d5dd2975329239e0584db334d21631e3ed3a9b8ffd151be0ba3a6e
  refs_bib_sha256: a1c07384db4aaf0d120d77967aba5198b4282109f4eb1c76cacbd0145e3b8948
  architecture_pdf_sha256: cb449b4e5c7ac3ce9887fe7efc63e5a7261206f33ebef505eb9fd68f41d19375
  alignment_pdf_sha256: 6db7095187ab6a906cd34e9d6ce1b1cdffbe08e06681afeea6647a428aad744d
  pipeline_pdf_sha256: 78b528c31d2d3e799ec60f7a3e220277dbf359e49f6cde3305cecbeac61addf4
  ingest_state: new
adapter_ingest:
  adapter_name: arXiv abs + PDF + TeX source + static full-text inspection
  adapter_version: manual-codex-2026-06-11
  capture_method: arXiv metadata, PDF download, e-print source download, TeX inspection
  extraction_trace:
    - arXiv abs page checked 2026-06-11.
    - PDF downloaded from arXiv and SHA256 recorded.
    - TeX e-print source downloaded, extracted, and SHA256 recorded.
    - main.tex, refs.bib, architecture/alignment/pipeline figures, and arXiv metadata inspected.
    - No model training, benchmark execution, prototype rerun, or independent reproduction performed.
  known_limits:
    - arXiv page lists author as "Guo Xun"; TeX source title block shows "Guoxun" and an example email, so author metadata quality is limited.
    - The paper explicitly labels its tables as expected estimates, not full public-dataset training results.
    - The appendix contains a submission checklist with full training, baselines, ablations, and case studies still to complete.
    - This source is useful for method design, but empirical claims are weak until measured results are available.
source_status: active-preprint
raw_location: raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/
processing_mode: explicit_strong_distill
processing_level: heavy
processing_tier: heavy
knowledge_status: raw
overlay_state: project_sidecar_created
review_pressure: review_due
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
formalization_status: candidate-generated
topics:
  - search-recommendation-fusion
  - query-generation
  - feed-recommendation
  - semantic-id
  - generative-retrieval
  - feedback-loop
  - retrieval-layer
projects:
  - verified-action-knowledge-system
source_family:
  - paper
  - methodological-framework
  - retrieval-and-recommendation
upstream_sources: []
verification_status: primary-source-captured
evidence_granularity: full_source_text_inspected
source_metadata_quality: medium_low
candidate_relation_suggestions: []
tags:
  - source/paper
  - arxiv
  - candidate-only
  - retrieval-layer
  - search-recommendation-fusion
---

# OneFeed Source Record

## Why Captured

The user requested strong distillation of arXiv:2606.07972.

This paper is relevant to VAKS because it tries to unify two interaction modes
that VAKS also cares about:

```text
implicit behavior / feed-like activation
explicit query / search-like retrieval
```

Its value is mostly architectural: shared behavior encoder, two generative
heads, semantic-ID/query alignment, and a closed-loop feedback design. Its
empirical value is currently weak because the paper says the main reported
numbers are expected estimates rather than measured full-dataset results.

## Source Information

- Title: `OneFeed: A Unified Generative Framework for Feed Content Enhancement and Query Generation`
- arXiv ID: `2606.07972v1`
- arXiv page: https://arxiv.org/abs/2606.07972
- PDF: https://arxiv.org/pdf/2606.07972
- DOI: https://doi.org/10.48550/arXiv.2606.07972
- Subject: Computer Science > Information Retrieval
- Submitted: 2026-06-06
- Author metadata:
  - arXiv page: `Guo Xun`
  - TeX source: `Guoxun`
  - confidence: medium-low because source metadata is thin and TeX email appears placeholder-like.

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
action_basis_allowed: false
truth_mutation_allowed: false
```

This source card is provenance only. It does not adopt OneFeed, validate the
paper's expected performance, create reviewed knowledge, or authorize a VAKS
architecture decision.

## Local Raw Artifacts

| Artifact | Path | SHA256 |
|---|---|---|
| PDF | `raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/2606.07972v1.pdf` | `61d7613b1ce418292e7454ac9fe69d35a73ef03162470356e0e464b87c381ed5` |
| arXiv e-print tar | `raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/2606.07972v1-eprint.tar` | `8ce240d98b28adbbf6f36108f0ce7975ed46de015dbb44ecab93e90d75b098c7` |
| arXiv abs HTML | `raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/2606.07972v1-abs.html` | `000891cf29a0f8d3cf16be0723eb198b16487879bdb062ad281bae47a6dda64f` |
| TeX source | `raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/eprint/main.tex` | `422c7004f3d5dd2975329239e0584db334d21631e3ed3a9b8ffd151be0ba3a6e` |
| References | `raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/eprint/refs.bib` | `a1c07384db4aaf0d120d77967aba5198b4282109f4eb1c76cacbd0145e3b8948` |

## Source Anchors Inspected

| Anchor | What It Says | Use |
|---|---|---|
| `arXiv abs page` | Submitted 2026-06-06; subject cs.IR; abstract summarizes shared behavior encoder, feed SID generator, intent query generator, SID-query alignment, closed loop | source identity |
| `main.tex` title note | Current version is a methodological contribution; tables use expected estimates; measured results will come later | empirical downgrade |
| `main.tex` Method | Shared behavior encoder; Feed SID Generator; Intent Query Generator; SID-Query alignment; candidate consistency loss | architecture extraction |
| `main.tex` Experimental Design | Public datasets, weak query construction, temporal split, semantic ID construction, baselines, metrics | protocol extraction |
| `main.tex` Expected Performance | Reported tables are estimates and marked with dagger / inequality notation | not evidence support |
| `main.tex` Limitations | Experiments not fully trained; pseudo queries weak; offline replay not online A/B; query safety unfinished | risk extraction |
| `main.tex` Submission Checklist | Full dataset preprocessing, baseline runs, full OneFeed, ablations, case studies still listed | maturity warning |

## Candidate Points

1. Feed/search unification is a useful retrieval-layer framing for VAKS: implicit
   activation and explicit query should inform each other.
2. Semantic IDs can be treated as structured retrieval anchors, but VAKS must not
   let generated IDs become evidence support.
3. Generated queries can expand candidate retrieval, but must be filtered for
   source scope, safety, and authority bucket.
4. SID-query alignment is a useful conceptual bridge between content anchors and
   user intent.
5. Closed-loop feedback can improve activation/routing, but in VAKS it must not
   mutate truth confidence or reviewed knowledge.
6. The paper's empirical tables are not action-ready evidence because they are
   expected estimates rather than full measurements.

## Obvious Doubts

- The paper is closer to a proposal/protocol than a completed empirical paper.
- Weak pseudo-query construction may overfit metadata and not reflect real search intent.
- Closed-loop self-enhancement risks self-confirming recommendations.
- The user-facing safety/filtering of generated queries is acknowledged but not fully evaluated.
- Author/institution metadata is thin.

## Current Processing Level

```text
heavy source capture + candidate distillation
```

Upgrade to reviewed knowledge only after independent measured results, code/data
availability, or a VAKS sandbox pilot verifies the specific design claims.
