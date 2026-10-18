---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/keyvanakbary/learning-notes"
repo_key: "keyvanakbary/learning-notes"
checked_commit: "ce15cdc2f51607e71912da6856b04b23e540df01"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/keyvanakbary-learning-notes-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: medium
borrow_order: P3
routing_hint:
  - source-type-lanes
  - recall-note-boundary
  - personal-vault-boundary
fit_layer:
  - capture-provenance
  - candidate-comprehension
  - activation
  - publishing
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not treat short recall summaries as evidence packets."
  - "Do not import book/paper/talk summaries wholesale."
  - "Do not allow personal-vault contribution boundaries to substitute for review policy."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing source-type lanes for books, talks, papers, and articles."
  support_when: "When comparing candidate comprehension notes and public projection from a source corpus."
  risk_when: "When recall summaries lack source spans or copyright boundaries are unclear."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/keyvanakbary-learning-notes-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - learning-notes
  - source-type-lanes
---

# Strong Candidate Distillation: keyvanakbary / learning-notes

## Boundary

This file extracts note-process and source-lane lessons. It does not treat the
book, talk, article, or paper summaries as reviewed evidence or as content to
copy into VAKS.

## What This Source Actually Is

`learning-notes` is a personal learning repository with short summaries of
books, talks, articles, and papers. The README frames the notes as recall
written soon after consuming a source. `taking-notes.md` explains the process:
highlight, type by hand, summarize after reading/watching, and iterate later.

It also includes a Jekyll/Just-the-Docs website folder, a backlog, and GitHub
Pages deployment.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Source-type lists with title, author, year, and note link. | Source metadata belongs at the list boundary. | Summary is not source text. |
| `taking-notes.md` | Process for books, articles, and talks; recall and hand typing. | Candidate comprehension can be explicit about method. | Method does not prove accuracy. |
| `papers/map-reduce.md` | Short paper summary with source link and structured sections. | Summary shape can preserve source identity and key concepts. | Not an evidence packet. |
| `backlog.md` | Future article/paper queue. | Backlog is useful but non-truth. | Queue is not commitment. |
| `website/_config.yml` | Jekyll config with folder defaults and nav exclusion. | Public projection can be separated from source notes. | Website config is not schema authority. |
| `.github/workflows/main.yml` | Builds website and deploys GitHub Pages. | Projection workflow is downstream. | Deploy success is not review. |

## Strong Borrow Points

1. **Source-type lanes are useful before schema complexity.**  
   Books, talks, articles, and papers are separated as folders and README
   sections. VAKS can borrow this for light intake routing without creating a
   heavy ontology.

2. **Note-taking method should be explicit.**  
   `taking-notes.md` says summaries are recall artifacts, not the goal itself.
   VAKS source cards should record whether a note is recall, transcript,
   excerpt, summary, or reviewed claim.

3. **Short summaries need source metadata but still lack evidence support.**  
   The paper notes keep title/author/year/source identity, but they do not
   carry point-level evidence packets. VAKS should route them as candidate
   comprehension.

4. **Personal vault contribution boundaries reduce false collaboration scope.**  
   The README says it may be better for others to start their own summaries.
   VAKS can borrow the idea that some vault areas are personal/candidate and
   not general contribution targets.

5. **Public projection can live under a separate `website/` folder.**  
   The website config and deploy workflow keep rendering concerns downstream of
   the notes. This matches VAKS repo-vs-Obsidian-vs-output separation.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Source title, author, year, medium. | Source-type card. |
| Candidate Comprehension | Recall summaries. | Candidate-only summaries. |
| Activation | Folder lanes and README lists. | Retrieval hints. |
| Publishing | Jekyll projection folder. | Downstream website output. |
| Risk / Inhibition | Copyright and no source spans. | No wholesale import or promotion. |

## Local De-Dup / Collision

This overlaps with `noodleslove/notes` and OSSU:

- `noodleslove/notes` is a mixed personal notes corpus with weaker provenance.
- OSSU is a curated curriculum route.
- `learning-notes` is strongest as a source-consumption recall workflow.

Its unique borrow is the explicit method boundary: recall summaries are useful
but should not masquerade as reviewed evidence.

## Anti-Borrow

- Do not copy summaries wholesale.
- Do not treat a recall summary as a source anchor.
- Do not promote paper/book ideas without checking the original source.
- Do not collapse public website config into VAKS schema.

## Candidate Tags

```yaml
domain: personal_source_recall_notes
problem: keeping_consumed_source_summaries_useful_without_overclaiming_evidence
pattern:
  - source-type-folders
  - explicit-note-taking-method
  - recall-summary-boundary
  - backlog-as-nontruth-queue
  - website-projection-subfolder
maturity: personal-public-notes
problem_fit: 3
reuse_value: 4
implementation_cost: 2
integration_fit: 4
evidence_strength: 3
reversibility: 5
```

## Fusion Judgment

Borrow moderately for source-type lanes and note-method disclosure. Keep every
summary candidate-only until original-source evidence is checked.
