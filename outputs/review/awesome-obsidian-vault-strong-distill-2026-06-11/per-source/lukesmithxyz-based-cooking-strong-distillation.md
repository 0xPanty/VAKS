---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/lukesmithxyz/based.cooking"
repo_key: "lukesmithxyz/based.cooking"
checked_commit: "2d8642ec41ccc6162ec3123c15024dd3d22cc33b"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/lukesmithxyz-based-cooking-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/lukesmithxyz-based-cooking-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/lukesmithxyz-based-cooking-anchor-manifest.json
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
  - lightweight-source-contract
  - static-publish-boundary
fit_layer:
  - capture-provenance
  - candidate-comprehension
  - source-hygiene
  - publishing
  - activation
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - truth-confidence
avoid:
  - "Do not import the recipe content as VAKS knowledge."
  - "Do not adopt source-specific licensing or contribution culture as global VAKS policy."
  - "Do not let static-site deployment imply reviewed status."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing lightweight intake contribution rules, source filename hygiene, or simple Markdown-to-site publication boundaries."
  support_when: "When comparing minimal templates, author metadata separation, and tag reuse constraints."
  risk_when: "When contribution rules or deployment workflows could be mistaken for evidence review or promotion."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/lukesmithxyz-based-cooking-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/lukesmithxyz-based-cooking-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - markdown-template
  - static-publishing
---

# Strong Candidate Distillation: lukesmithxyz / based.cooking

## Boundary

This file extracts VAKS design lessons from the repository structure and
contribution workflow. It does not treat recipes, tags, or popularity as
reviewed knowledge.

## What This Source Actually Is

`based.cooking` is a simple Hugo-backed recipe site where source recipes live as
Markdown files under `content/`. It uses a small recipe template, separate author
metadata, a static asset folder, and a deployment workflow that rebuilds the
website from the repository.

For VAKS, the useful object is the source contract: how a low-friction public
collection keeps submissions consistent enough to publish without creating a
heavy schema.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Contribution rules for file placement, naming, tags, images, authors, and license. | Good example of an intake contract written in ordinary language. | Project-specific policy only. |
| `example.md` | Frontmatter with title, tags, date, author; body sections for ingredients and directions. | Minimal template can standardize capture without over-modeling. | Template fields are not evidence review. |
| `data/authors/` | Optional author JSON files referenced by recipe `author`. | Separate contributor metadata from content records. | Contributor metadata is provenance/context, not truth. |
| `config.toml` | Hugo source-to-site configuration. | Repo Markdown remains source; generated site is a surface. | Publish surface does not promote content. |
| `.github/workflows/upload.yml` | Server-side rebuild on push. | Deployment can be downstream of source, not a source of knowledge. | Do not borrow as VAKS automation until explicitly designed. |

## Strong Borrow Points

1. **Plain-language source contract before schema.**  
   The README tells contributors where files go, how filenames should look, how
   tags should be reused, and how images should be handled. VAKS can borrow this
   for ordinary source intake: most users need a short contract before they need
   a formal schema page.

2. **Minimal frontmatter plus stable body sections.**  
   `example.md` shows that a small set of metadata fields and predictable
   headings can make a corpus easy to index. VAKS can reuse the pattern for
   light source records: keep the schema small, then let review layers add
   strictness later.

3. **Author identity is a linked side record.**  
   `data/authors/` prevents every content note from carrying full contributor
   metadata. VAKS can adapt this as a general provenance principle: keep source
   identity, contributor identity, and extracted candidate points separate.

4. **Tag reuse is explicit intake hygiene.**  
   The repo asks contributors to reuse existing tags when possible. VAKS can
   borrow the same idea for `tags/topics`: new tags should be candidate routing,
   not accidental taxonomy expansion.

5. **Image provenance and size rules belong at capture.**  
   The image rules combine ownership, format, size, and path expectations. VAKS
   can mirror this for retained screenshots, PDFs, and media-derived artifacts:
   provenance and retention constraints should be decided at capture time.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Lightweight file naming, media policy, author key. | Borrow as intake hygiene. |
| Candidate Comprehension | Minimal body headings for consistent extraction. | Useful for light templates. |
| Review Queue | Tag reuse reduces duplicate routing labels. | Candidate routing only. |
| Activation | Tags and static index support quick browsing. | Activation, not truth. |
| Publishing | Hugo site generated from Markdown source. | Keep repo-vs-publish boundary. |

## Local De-Dup / Collision

The earlier shallow file classified this as a lightweight cooking vault. This
strong pass adds the reusable mechanisms: contribution contract, author metadata
separation, tag hygiene, media provenance, and static publish boundary.

It overlaps with Obsidian Hub on repo-to-publish separation, but this source is
lighter and more useful for ordinary intake rules. Hub is stronger for generated
catalog automation; `based.cooking` is stronger for contributor-facing
simplicity.

## Anti-Borrow

- Do not borrow recipe tags as VAKS ontology.
- Do not make public-domain licensing the default for VAKS source records.
- Do not use deployment workflow as a permission to automate Obsidian sync or
  promotion.
- Do not turn simple templates into reviewed knowledge schemas.

## Candidate Tags

```yaml
domain: lightweight_markdown_collection
problem: keep_public_submissions_consistent_without_heavy_schema
pattern:
  - plain-language-intake-contract
  - minimal-frontmatter-and-stable-headings
  - sidecar-author-metadata
  - tag-reuse-before-tag-creation
  - media-provenance-at-capture
maturity: proven-small-static-site
problem_fit: 4
reuse_value: 4
implementation_cost: 1
integration_fit: 4
evidence_strength: 4
reversibility: 5
```

## Fusion Judgment

Borrow as a P3 support reference for light intake ergonomics. Its main value is
showing how far a tiny Markdown contract can go before heavier VAKS review
machinery is needed.
