---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "lyz-code/blue-book"
source_url: "https://github.com/lyz-code/blue-book"
checked_commit: "90bd269ddb4e9432a868f641b06cffa01d31d8a4"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/lyz-code-blue-book-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/lyz-code-blue-book-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/lyz-code-blue-book-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order: P2
routing_hint:
  - mkdocs_personal_wiki
fit_layer:
  - publishing
  - activation
  - vault-health
  - source-hygiene
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - agent-write-boundary
avoid:
  - "Do not import personal wiki content as VAKS knowledge."
  - "Do not copy scheduled commit/push automation into VAKS."
  - "Do not ignore Windows-invalid filenames in retained source snapshots."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing navigation-tree governance, maintenance lint, or path-portability checks."
  support_when: "When comparing MkDocs publication, explicit nav trees, edit links, CI publishing, and pre-commit health checks."
  risk_when: "When automation or personal content could mutate/publish VAKS without review."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/lyz-code-blue-book-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - mkdocs
  - source-hygiene
---

# Strong Candidate Distillation: lyz-code / blue-book

## What This Source Actually Is

This is a large personal wiki published as a MkDocs book. It has an explicit
navigation tree, many topic pages, contribution entry points, pre-commit checks,
and scheduled GitHub Pages automation. Normal Windows checkout failed because
some image filenames contain question marks.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Personal wiki purpose and contribution paths. | Public docs should expose edit/issue paths. | Personal content is not VAKS knowledge. |
| `mkdocs.yml` | Large explicit navigation hierarchy. | Manual navigation can be durable and auditable. | Nav position is not truth. |
| `docs/**/*.md` | Broad personal wiki corpus. | Topic files can scale under a publish system. | Content must not be absorbed. |
| `.github/workflows/gh-pages.yml` | Scheduled dependency update, formatting, commit, push, build, deploy. | Automation boundary is visible. | Too risky for VAKS default. |
| `.pre-commit-config.yaml` | Lint/security/format hooks. | Maintenance lint can catch source hygiene issues. | Lint is not review. |
| `docs/img/*?v=*` | Windows-invalid filenames. | Path portability checks are mandatory for snapshots. | Checkout failure limits retention. |

## Strong Borrow Points

1. **Explicit navigation can beat implicit graph browsing.**  
   The MkDocs nav tree is manually curated and auditable. VAKS can borrow this
   for public indexes or recovery maps where order matters.

2. **Edit/issue affordances support public correction.**  
   The README encourages PRs/issues/email. VAKS can adapt this as feedback
   intake, while keeping feedback separate from truth mutation.

3. **Pre-commit maintenance checks are useful as health gates.**  
   Private-key detection, large-file checks, markdown lint, and prose lint map
   well to maintenance manifests and source hygiene.

4. **Scheduled self-mutating automation is a boundary warning.**  
   The workflow updates dependencies, formats, generates content, commits, and
   deploys. VAKS should not adopt that as a default because it crosses write,
   publish, and review boundaries.

5. **Path portability is a real retention risk.**  
   The invalid filenames prove that repo snapshots need cross-platform filename
   checks before treating a source as locally retained.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Activation | Explicit nav/recovery tree. | Adapt. |
| Publishing | MkDocs book with edit paths. | Reference. |
| Vault Health | Pre-commit/lint checks. | Strong adaptation. |
| Source Hygiene | Windows-invalid paths. | Required check. |
| Agent Gateway | Self-mutating CI. | Risk only. |

## Local De-Dup / Collision

This overlaps with documentation repos and digital-garden publishing sources.
Its distinct value is explicit MkDocs navigation plus maintenance lint and
automation-risk boundaries.

## Fusion Judgment

Borrow as P2 for navigation, maintenance lint, edit/feedback paths, and path
portability. Reject scheduled commit/push automation as a VAKS default.
