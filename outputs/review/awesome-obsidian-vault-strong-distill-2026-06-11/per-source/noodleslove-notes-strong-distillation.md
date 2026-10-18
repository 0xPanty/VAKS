---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/noodleslove/notes"
repo_key: "noodleslove/notes"
checked_commit: "ec7705a4c4bf7a3a5160b22a17534488d5c6cdd3"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/noodleslove-notes-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: low
borrow_order: P3
routing_hint:
  - source-hygiene
  - learning-notes
  - api-note-template
fit_layer:
  - capture-provenance
  - candidate-comprehension
  - source-hygiene
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not copy tutorial/course notes as reviewed facts without source provenance."
  - "Do not trust README badges or boilerplate as a source inventory."
  - "Do not let copied curriculum assets enter VAKS without license and source-credit checks."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Rarely; only when designing rough intake for mixed personal study notes."
  support_when: "When comparing low-governance personal note repositories and API-note shapes."
  risk_when: "When source provenance is mixed, README metadata is stale, or copied course material is present."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/noodleslove-notes-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - personal-notes
  - provenance-risk
---

# Strong Candidate Distillation: noodleslove / notes

## Boundary

This file extracts structure and risk lessons from a personal computing-notes
repository. It does not treat the notes, copied curriculum material, API
examples, or interview answers as reviewed VAKS knowledge.

## What This Source Actually Is

`noodleslove/notes` is a mixed personal note vault covering algorithms, data
structures, AWS, blockchain, full-stack development, ML model material, and
project API notes. The repository contains useful real-world clutter: a broad
folder corpus, diagrams/assets, hand-written API notes, interview-style
cheatsheets, and course-derived material.

The most important extraction is not the content. It is the warning that a
large note repo can look valuable while still having weak provenance and stale
metadata.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Best-README-Template boilerplate mixed with a brief notes claim. | README can drift far away from actual vault contents. | README is not inventory truth. |
| `Cheatsheet.md` | SQL interview Q&A in flat numbered form. | Quick-reference notes can be captured as candidate recall. | Answers need evidence before use. |
| `CSES WebDev/APIs/Event-API.md` | Endpoint, method, parameters, request/response examples, errors. | API notes benefit from stable fields and examples. | Example API contract is project-local only. |
| `ML Models/README.md` | Microsoft ML for Beginners curriculum README/badges. | Copied or forked curriculum material needs source-credit quarantine. | Do not import as original VAKS knowledge. |
| Folder set | Algorithms, Data Structures, Full Stack, Blockchain, AWS, ML Models. | Topic folders help rough activation. | Folders are not reviewed taxonomy. |

## Strong Borrow Points

1. **Use stale README detection as an intake lint.**  
   This repo's README still exposes generic template sections while the actual
   content is a mixed technical notes corpus. VAKS should flag README/content
   mismatch during source intake.

2. **API notes need a compact but typed shape.**  
   `Event-API.md` shows a practical shape: endpoint, description, method,
   parameters, request example, response example, and validation errors. VAKS
   can borrow this for project-local API cards, but only as candidate
   comprehension until backed by live code or docs.

3. **Cheatsheets should be routed as recall notes, not truth.**  
   `Cheatsheet.md` is useful for quick orientation and interview preparation,
   but it has no source spans. In VAKS terms, this belongs in candidate notes
   or activation context, not reviewed claims.

4. **Copied curriculum assets require provenance quarantine.**  
   The ML folder includes Microsoft ML for Beginners material and badges. VAKS
   should treat copied/forked course material as source-linked external content
   and avoid turning it into local authored knowledge.

5. **Broad topic folders are activation hints only.**  
   The folder tree helps retrieval, but the taxonomy should not become a
   reviewed knowledge graph.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Detect source-credit and README/content mismatch. | Intake lint. |
| Candidate Comprehension | Personal notes and API examples. | Candidate-only source card. |
| Activation | Topic folders and cheatsheets. | Low-confidence context hints. |
| Review Queue | Missing source evidence and copied material. | `missing_evidence` or provenance review. |
| Risk / Inhibition | Boilerplate and copied course content. | Do not promote without anchors. |

## Local De-Dup / Collision

This overlaps with `keyvanakbary/learning-notes`, `OSSU`, and Microsoft course
material:

- Compared with `keyvanakbary/learning-notes`, this repo is less explicit
  about note-taking method and source attribution.
- Compared with `OSSU`, it is not a maintained curriculum route map.
- Compared with Microsoft curriculum repos, its ML content appears copied or
  embedded, so it should not be treated as an independent design source.

Its unique value is a negative control: it teaches VAKS to separate "large
notes corpus" from "well-governed reusable knowledge."

## Anti-Borrow

- Do not import the SQL answers as facts.
- Do not treat folder names as a stable schema.
- Do not treat copied course README/badges as original source evidence.
- Do not let a broad personal vault bypass provenance checks.

## Candidate Tags

```yaml
domain: personal_learning_notes
problem: mixed_note_corpus_without_strong_source_governance
pattern:
  - readme-content-mismatch-lint
  - api-note-field-shape
  - cheatsheet-as-recall-note
  - copied-curriculum-provenance-quarantine
maturity: personal-mixed-vault
problem_fit: 2
reuse_value: 2
implementation_cost: 2
integration_fit: 2
evidence_strength: 2
reversibility: 5
```

## Fusion Judgment

Borrow lightly. The useful lesson is mostly defensive: VAKS should preserve the
line between personal recall notes, copied source material, and reviewed
knowledge.
