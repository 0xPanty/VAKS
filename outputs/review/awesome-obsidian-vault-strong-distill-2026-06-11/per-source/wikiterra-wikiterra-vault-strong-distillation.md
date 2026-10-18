---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/Wikiterra/wikiterra-vault"
repo_key: "Wikiterra/wikiterra-vault"
checked_commit: "78397aa5b10cb30d7a9182af6ce8b80a8c5f0a28"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/wikiterra-wikiterra-vault-anchor-manifest.json
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
  - publish-boundary
  - plugin-risk
  - contested-content-risk
fit_layer:
  - source-hygiene
  - publishing
  - risk
  - capture-provenance
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not borrow cosmology, flat-earth, NASA, or conspiracy content."
  - "Do not commit bundled Obsidian plugin binaries as a default VAKS pattern."
  - "Do not treat dg-publish flags or edit rules as evidence review."
dev_context_hint:
  default_layer: risk
  core_only_when: "Only as a negative-control source for public-vault risk, plugin hygiene, and publish flags."
  support_when: "When comparing Obsidian Digital Garden publication controls and edit-rule pages."
  risk_when: "When contested or pseudoscientific content, bundled plugins, or image-host dependencies could pollute VAKS."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/wikiterra-wikiterra-vault-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - risk-control
  - digital-garden
---

# Strong Candidate Distillation: Wikiterra / wikiterra-vault

## Boundary

This file is intentionally a risk-focused distillation. The source contains
cosmology, flat-earth, NASA, and conspiracy-oriented material. VAKS should not
borrow the content. The only reusable material is structural: publish flags,
edit rules, plugin hygiene warnings, and public-vault boundary checks.

## What This Source Actually Is

`wikiterra-vault` is a Spanish Obsidian vault published to the web using an
Obsidian garden workflow. It contains many Markdown files with `dg-publish`
frontmatter, a public home page, an editing guide, Obsidian plugin folders,
theme/snippet files, and image-heavy external references.

It is a useful negative-control source: it shows how a public vault can have
publication mechanics while its content remains unsuitable for reviewed
knowledge.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Vault identity, web deployment claim, plugin list, ITS theme settings. | Project-local plugin/theme dependency inventory. | Plugin list is not trust. |
| `index.md` | `dg-home`, `dg-publish`, home page, Telegram route, philosophy/objective text. | Publish flags and public landing note. | Content is high-risk. |
| `wikiterra/edicion.md` | Edit guide, markdown rules, evidence/reference aspirations. | Edit rules can be published inside the vault. | Aspirations do not prove review. |
| `.obsidian/plugins/*` | Bundled plugin JS, manifests, styles, data. | Bundled plugin state is a supply-chain and repo-hygiene risk. | Do not copy default. |
| `.gitignore` | Ignores Digital Garden plugin, Obsidian app state, workspaces, `.env`, media. | Some private/tool state is excluded. | Actual bundled plugins remain. |
| `modelos-Terra/*`, `poder-corrupto/*` | Contested/pseudoscientific/conspiracy content. | Negative control for evidence gate. | Do not borrow content. |

## Strong Borrow Points

1. **Publish flags are useful but not review state.**  
   `dg-publish: true` controls web publication. VAKS can borrow a similar
   separation: public visibility metadata must not imply truth confidence.

2. **A public vault should include edit rules, but edit rules are not evidence.**  
   `wikiterra/edicion.md` defines collaboration norms and asks for references.
   VAKS can borrow the idea of visible contribution rules while requiring
   independent evidence-aware review.

3. **Bundled Obsidian plugins are a repo-hygiene risk.**  
   The vault tracks many `.obsidian/plugins/*` files, including JS. VAKS should
   avoid committing plugin binaries into the knowledge repo unless there is a
   deliberate supply-chain policy.

4. **External image hosting should be treated as fragile provenance.**  
   Many notes rely on Imgur or external wiki image URLs. VAKS should distinguish
   illustrative media from retained source evidence.

5. **High-risk content can still teach architecture boundaries.**  
   The source demonstrates why "public Markdown vault" must be separated from
   "reviewed knowledge system."

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Public vault identity and publish flags. | Source card only. |
| Publishing | Digital Garden style flags. | Visibility metadata, not truth. |
| Source Hygiene | Plugin/theme inventory and ignored state. | Repo hygiene lint. |
| Risk / Inhibition | Pseudoscience/conspiracy content. | Strong no-borrow warning. |
| Review Queue | Edit rules aspire to references. | Still requires evidence packet. |

## Local De-Dup / Collision

This overlaps with Digital Garden docs and Obsidian template repos, but it is
not valuable for design quality in the same way. Its unique value is a negative
control:

- Digital Garden docs explain publish mechanics.
- Wikiterra shows publish mechanics inside a content-risky vault.

Therefore it should be used to harden VAKS boundaries, not to expand content.

## Anti-Borrow

- Do not borrow cosmology/flat-earth/conspiracy claims.
- Do not treat `dg-publish` as review or approval.
- Do not commit plugin binaries by default.
- Do not rely on external image hosts as retained evidence.
- Do not let "objective/evidence" language bypass actual evidence review.

## Candidate Tags

```yaml
domain: public_obsidian_vault_risk
problem: separating_publication_mechanics_from_content_trust
pattern:
  - publish-flag-not-review-state
  - visible-edit-rules-not-evidence
  - bundled-plugin-supply-chain-risk
  - external-image-fragility
  - high-risk-content-negative-control
maturity: public-vault-negative-control
problem_fit: 3
reuse_value: 2
implementation_cost: 2
integration_fit: 3
evidence_strength: 4
reversibility: 5
```

## Fusion Judgment

Do not borrow content. Borrow only as a risk control: public visibility, plugin
state, and edit rules must remain separate from evidence review and truth.
