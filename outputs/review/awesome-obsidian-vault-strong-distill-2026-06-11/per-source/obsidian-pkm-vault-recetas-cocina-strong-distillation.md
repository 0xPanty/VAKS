---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/obsidian-pkm-vault/recetas-cocina"
repo_key: "obsidian-pkm-vault/recetas-cocina"
checked_commit: "e5c37700bb25e21891e12c5d9a19d6ee2d9a906b"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/obsidian-pkm-vault-recetas-cocina-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/obsidian-pkm-vault-recetas-cocina-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/obsidian-pkm-vault-recetas-cocina-anchor-manifest.json
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
  - obsidian-vault-template
  - source-vs-export-boundary
fit_layer:
  - capture-provenance
  - candidate-comprehension
  - activation
  - publishing
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - evidence-packet
avoid:
  - "Do not treat recipe source labels as evidence support."
  - "Do not treat exported HTML under docs as a second source of truth."
  - "Do not copy the food taxonomy as VAKS taxonomy."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing Obsidian-native templates, manual category indexes, or vault-to-web source/export boundaries."
  support_when: "When comparing simple frontmatter, wikilink navigation, and generated web output separation."
  risk_when: "When manual indexes or exported copies could drift from canonical Markdown."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/obsidian-pkm-vault-recetas-cocina-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/obsidian-pkm-vault-recetas-cocina-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - obsidian-template
  - vault-export
---

# Strong Candidate Distillation: obsidian-pkm-vault / recetas-cocina

## Boundary

This file extracts Obsidian-vault mechanics from a recipe vault. It does not
promote recipes, nutrition fields, manual category links, or source labels to
reviewed VAKS knowledge.

## What This Source Actually Is

This repository is an Obsidian recipe vault exported to a web site through an
Obsidian webpage export plugin. Its source notes live as Markdown, while the
`docs/` directory contains generated HTML. It includes an explicit recipe
template, manual index notes, images, and some external recipe-book PDFs.

For VAKS, the value is the Obsidian-native source/export boundary and the way a
small domain vault uses frontmatter plus wikilinks without a complex database.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Names the repo as an Obsidian vault exported to web format. | Clear repo source vs web output story. | Export is not review. |
| `receta-template.md` | Frontmatter for name/source/difficulty/time/tags/type and sections for ingredients, preparation, notes, nutrition, sources, references. | Good example of field/section split. | Source labels are not evidence packets. |
| `index.md` | Manual category map with Obsidian wikilinks. | Human-editable navigation can coexist with file hierarchy. | Manual links can drift. |
| `.obsidian/community-plugins.json` | Active export plugin is recorded in vault config. | Tool dependency is visible in the vault. | Plugin output is not authority. |
| `docs/` | Exported HTML files. | Generated publish output can be retained separately. | Do not duplicate authority. |

## Strong Borrow Points

1. **Template separates metadata from body sections.**  
   The template uses frontmatter for routing fields and Markdown headings for
   human-readable procedure. VAKS can borrow this for future light/medium intake:
   metadata routes the note, sections carry comprehension, review fields stay
   elsewhere.

2. **Source labels are captured early but not trusted.**  
   The `fuente` field is useful as a provenance prompt, but the notes mix
   personal, adapted, traditional, and link-based labels. VAKS should capture
   source statements early, then require evidence support checks only when a
   point becomes review/action relevant.

3. **Manual indexes remain valuable when clearly non-authoritative.**  
   `index.md` is easy to read and edit. VAKS can borrow manual indexes for
   activation maps, as long as they are explicitly navigation and not reviewed
   relation graphs.

4. **Exported site should be treated as a downstream copy.**  
   `docs/` contains generated HTML. VAKS should keep this boundary: Markdown is
   canonical; generated HTML, Bases views, dashboards, or context packs are
   surfaces.

5. **Tooling belongs in visible vault metadata.**  
   The `.obsidian` config exposes the export plugin. VAKS can borrow the habit:
   when a generated artifact depends on a plugin/script, record the tool and
   version/path in the artifact or manifest.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Early source field and image/reference sections. | Capture prompt only. |
| Candidate Comprehension | Stable headings for extracted content. | Candidate notes. |
| Association / Activation | Manual wikilink category index. | Activation only. |
| Publishing | `docs/` as generated site. | Downstream copy, not authority. |
| Source Hygiene | Visible plugin dependency. | Manifest/tool provenance. |

## Local De-Dup / Collision

This overlaps with `based.cooking` on Markdown templates and static publishing.
The difference:

- `based.cooking` is stronger for public contribution rules and author sidecar
  metadata.
- `recetas-cocina` is stronger for Obsidian-native wikilinks, vault config, and
  source-vs-export separation inside an Obsidian repo.

Both reinforce the VAKS rule that publishing and navigation do not create
reviewed knowledge.

## Anti-Borrow

- Do not copy the recipe taxonomy into VAKS concepts.
- Do not treat `fuente` as sufficient evidence support.
- Do not retain exported HTML as a second authority over Markdown.
- Do not let manual indexes imply reviewed relations.

## Candidate Tags

```yaml
domain: obsidian_domain_vault
problem: keep_markdown_source_readable_while_exporting_to_web
pattern:
  - frontmatter-routing-body-comprehension-split
  - source-label-as-provenance-prompt
  - manual-index-as-activation-only
  - canonical-markdown-generated-html-boundary
  - visible-plugin-dependency
maturity: small-working-vault
problem_fit: 4
reuse_value: 4
implementation_cost: 2
integration_fit: 4
evidence_strength: 3
reversibility: 5
```

## Fusion Judgment

Borrow as a P3 support reference for Obsidian-native source/export design. It is
most useful for reminding VAKS that a plain vault can stay useful if canonical
Markdown, generated outputs, and navigation aids are not confused.
