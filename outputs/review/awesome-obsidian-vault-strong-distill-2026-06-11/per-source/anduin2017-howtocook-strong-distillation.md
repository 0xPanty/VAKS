---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/Anduin2017/HowToCook"
repo_key: "Anduin2017/HowToCook"
checked_commit: "b457738abd37d2621f22d59ff9fb065fcc4528da"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/anduin2017-howtocook-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/anduin2017-howtocook-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/anduin2017-howtocook-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order: P3
routing_hint:
  - domain-specific-lint
  - machine-readable-human-notes
fit_layer:
  - capture-provenance
  - candidate-comprehension
  - review-queue
  - source-hygiene
  - maintenance
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - ordinary-capture-default
avoid:
  - "Do not import recipe content or nutritional claims as VAKS evidence."
  - "Do not apply strict lint to ordinary capture; use it as a lazy gate."
  - "Do not adopt the source-specific public-domain policy as VAKS default."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing promotion/action-basis lint, precision checks, template conformance, or machine-readable note constraints."
  support_when: "When comparing generated indexes, contribution gates, and domain-specific quality rules."
  risk_when: "When strict format requirements could overload lightweight intake or be mistaken for truth review."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/anduin2017-howtocook-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/anduin2017-howtocook-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - domain-lint
  - machine-readable-notes
---

# Strong Candidate Distillation: Anduin2017 / HowToCook

## Boundary

This file extracts VAKS design lessons from HowToCook's precision and linting
system. It does not promote cooking instructions, nutrition statements, or
license posture into reviewed VAKS knowledge.

## What This Source Actually Is

HowToCook is a large community-maintained Chinese recipe repository aimed at
making recipes precise enough for programmers and downstream machine processing.
It has a strict dish template, generated README navigation, automated lint,
pull-request confirmation, and a clear project philosophy around formalization
and reproducibility.

For VAKS, this is one of the strongest P3 sources because it directly tackles
the same tension VAKS has: human-readable notes must sometimes become precise
enough for machines without making every capture step unbearable.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Explains precise recipes for programmers, website/Docker viewer, contribution route, and generated category index. | Public story plus generated navigation. | Navigation is not truth. |
| `dishes/template/.../示例菜.md` | Required title, intro, difficulty, calories, ingredients/tools, calculation, ordered operations, additional content, footer. | Strong domain template with explicit fields and process sections. | Too strict for ordinary VAKS capture. |
| `.github/manual_lint.js` | Checks filenames, headings, required fields, ordered lists, imprecise units, pronouns, footer, image alt text, file references, and description length. | Domain-specific lint as maintenance/review gate. | Lint pass is not evidence support. |
| `.github/pull_request_template.md` | Automated check before human review; license/public-domain checkbox. | Review gating and contributor attestation. | Attestation is process evidence only. |
| `.github/readme-generate.js` | Regenerates README from Markdown files and category map. | Generated navigation from canonical files. | Generated README is activation. |
| `CODE_OF_CONDUCT.md` | States precision, formalization, machine readability, and derivative boundaries. | Project principles can justify strict gates. | VAKS should not inherit source-specific license. |

## Strong Borrow Points

1. **Strictness should be a lazy gate, not the capture default.**  
   HowToCook shows powerful validation, but also why strict rules feel heavy to
   contributors. VAKS should apply similar lint only at promotion, action-basis,
   source-retention, or important-review boundaries.

2. **Domain lint can encode "imprecision pressure."**  
   The lint script rejects vague units, vague quantities, missing wait criteria,
   wrong headings, missing footer, weak alt text, and broken image references.
   VAKS can borrow the principle for evidence packets: flag missing anchors,
   URL-only support, unscoped claims, stale applicability, and unsupported
   confidence.

3. **Template sections can distinguish calculation from operation.**  
   The template separates materials/tools, calculation, operations, and extra
   content. VAKS can adapt this as point/evidence/warrant/scope/risk separation
   rather than mixing everything into one summary.

4. **Generated indexes should be rebuilt from canonical files.**  
   `readme-generate.js` walks Markdown files and regenerates README navigation.
   VAKS can borrow this for candidate indexes and dashboards: generated views
   are rebuilt from canonical records, not hand-maintained as authority.

5. **PR checks before human review are useful process gates.**  
   The PR template says automated checks must pass before human review. VAKS can
   borrow this for review queue hygiene: lint can screen malformed records before
   evidence-aware review, without becoming the review itself.

6. **Project principles explain why the friction exists.**  
   The code of conduct states that the project optimizes for precision and
   machine readability. VAKS should similarly document why certain strict gates
   exist, so they do not feel arbitrary.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Template prompts exact fields and references. | Light capture variant only. |
| Candidate Comprehension | Separate descriptive intro, calculation, operation, extra notes. | Candidate structure inspiration. |
| Review Queue | Lint failures create review pressure. | Maintenance gate, not truth. |
| Evidence-Aware Review | Missing support/scope/risk can be linted. | Promotion/action lazy gate. |
| Activation | Generated README category index. | Activation map only. |
| Risk / Inhibition | Over-strict rules can block ordinary contribution. | Keep lazy-gate boundary. |

## Local De-Dup / Collision

HowToCook overlaps with `based.cooking` on contribution templates and with
DevCookbook on machine parsing. Its distinct value is stricter: domain-specific
lint and explicit machine-readable precision rules.

This source is a strong fit for VAKS maintenance manifests, evidence packet
lint, and promotion/action-basis preflight checks.

## Anti-Borrow

- Do not apply full strictness to every ordinary note.
- Do not confuse lint pass with reviewed truth.
- Do not adopt source-specific Unlicense/public-domain rules as VAKS policy.
- Do not import health, nutrition, or cooking claims without review.

## Candidate Tags

```yaml
domain: machine_readable_human_markdown
problem: make_human_authored_notes_precise_enough_for_downstream_processing
pattern:
  - strict-template-as-lazy-gate
  - domain-specific-lint
  - imprecision-pressure-detection
  - generated-index-from-canonical-files
  - automated-check-before-human-review
  - principles-explain-friction
maturity: large-community-repo
problem_fit: 5
reuse_value: 5
implementation_cost: 3
integration_fit: 5
evidence_strength: 5
reversibility: 4
```

## Fusion Judgment

Borrow strongly, but only as a lazy-gate pattern. HowToCook should influence
VAKS lint, maintenance manifests, and action-basis preflight checks, not
ordinary lightweight capture.
