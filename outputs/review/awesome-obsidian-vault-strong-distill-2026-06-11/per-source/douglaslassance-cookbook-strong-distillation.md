---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/douglaslassance/cookbook"
repo_key: "douglaslassance/cookbook"
checked_commit: "765614a129a0bc12b63354389f0a6126b2632efc"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/douglaslassance-cookbook-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/douglaslassance-cookbook-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/douglaslassance-cookbook-anchor-manifest.json
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
  - personal-obsidian-vault
  - ratio-and-technique-notes
fit_layer:
  - candidate-comprehension
  - activation
  - source-hygiene
  - maintenance
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - global-vault-default
avoid:
  - "Do not adopt personal plugin settings as global VAKS defaults."
  - "Do not treat resource links or ratios as reviewed evidence."
  - "Do not infer architecture from folder names alone."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing small concept/reference notes, ratio tables, aliases, or local lint profiles."
  support_when: "When comparing personal Obsidian organization, plugin-assisted hygiene, and reusable technique notes."
  risk_when: "When plugin settings or personal folder taxonomy could be over-generalized."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/douglaslassance-cookbook-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/douglaslassance-cookbook-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - obsidian-linter
  - ratio-notes
---

# Strong Candidate Distillation: douglaslassance / cookbook

## Boundary

This file extracts personal-vault mechanics. It does not promote recipes,
ratios, external links, plugin settings, or folder taxonomy to reviewed VAKS
knowledge.

## What This Source Actually Is

This is a personal Obsidian cookbook vault with folders for ingredients, misc
ratios, savory recipes, sweet recipes, and techniques. It includes Obsidian Git,
LanguageTool, and Obsidian Linter plugin configuration. Some notes use formula
style ratios, resource links, aliases, and compact technique definitions.

For VAKS, this is a low-to-medium borrow source: useful for note ergonomics and
local hygiene, not architecture.

## Source / Vault Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `.obsidian/community-plugins.json` | Linter, LanguageTool, Obsidian Git. | Tool-assisted local hygiene. | Not a global default. |
| `.obsidian/plugins/obsidian-linter/data.json` | Detailed formatting/lint configuration. | Lint can encode house style. | Style lint is not truth review. |
| `Savory/Sourdough.md` | Formula-like ratios, ordered steps, mods, resources. | Ratio/parameter notes can stay readable. | Ratios need evidence if action-critical. |
| `Misc/Grain Cooking Ratios.md` | Table of water ratios and shared method. | Compact reference-table pattern. | Table is candidate reference only. |
| `Techniques/Folding.md` | Alias frontmatter and short technique definition. | Small concept-note pattern. | Definition not reviewed. |

## Strong Borrow Points

1. **Ratio notes can be readable without a database.**  
   The sourdough and grain-ratio notes show that formulas and tables can live in
   plain Markdown. VAKS can borrow this for scope/applicability notes where a
   full formal model would be overkill.

2. **Techniques deserve small concept notes.**  
   Technique notes with aliases are lightweight but useful. VAKS can use this
   pattern for concepts that support retrieval and comprehension without becoming
   claims.

3. **Local lint profiles are useful but contextual.**  
   Obsidian Linter configuration can maintain style and reduce drift. VAKS
   should keep lint profiles project-local and explicit rather than global.

4. **Personal folders are good for activation, weak for ontology.**  
   Folders like `Savory`, `Sweet`, `Misc`, and `Techniques` help browsing. VAKS
   should treat folder paths as activation signals, not reviewed categories.

5. **Resource lists should stay provenance prompts.**  
   Some notes include external resources. VAKS can borrow the habit of keeping
   source links near the note, but evidence support still requires point-level
   checking.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Candidate Comprehension | Ratio and technique notes. | Candidate concept/reference notes. |
| Activation | Folder taxonomy and aliases. | Activation signals only. |
| Source Hygiene | Linter and LanguageTool settings. | Local maintenance profile. |
| Review Queue | Resource links can seed evidence checks. | Review pressure only. |
| Risk / Inhibition | Personal settings can be overfit. | Do not globalize. |

## Local De-Dup / Collision

This overlaps with personal vault/template sources already distilled, but its
distinct value is small reusable ratio/technique notes plus explicit Obsidian
plugin hygiene. It is less useful than HowToCook for strict lint, and less useful
than Obsidian Hub for large catalog structure.

## Anti-Borrow

- Do not copy `.obsidian` settings as project defaults.
- Do not promote ratio tables as action-ready guidance.
- Do not treat folders as reviewed ontology.
- Do not treat resource links as evidence support.

## Candidate Tags

```yaml
domain: personal_obsidian_reference_vault
problem: keep_small_reference_ratios_and_techniques_easy_to_find
pattern:
  - readable-ratio-note
  - tiny-technique-concept-note
  - local-lint-profile
  - folder-as-activation-not-ontology
  - resource-links-as-provenance-prompts
maturity: personal-vault
problem_fit: 3
reuse_value: 3
implementation_cost: 1
integration_fit: 3
evidence_strength: 3
reversibility: 5
```

## Fusion Judgment

Borrow lightly as a P3 support reference for small concept notes and local lint
hygiene. Do not promote its folder structure or plugin settings into VAKS
architecture.
