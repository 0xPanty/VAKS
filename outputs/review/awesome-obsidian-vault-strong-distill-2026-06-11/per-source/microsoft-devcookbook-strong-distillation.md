---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/microsoft/DevCookbook"
repo_key: "microsoft/DevCookbook"
checked_commit: "ed8130e14ae4e2a19d50a5f648b3cfdf21e5920a"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/microsoft-devcookbook-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/microsoft-devcookbook-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/microsoft-devcookbook-anchor-manifest.json
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
  - markdown-compiler
  - parser-tests
fit_layer:
  - candidate-comprehension
  - source-hygiene
  - publishing
  - maintenance
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not auto-commit generated VAKS artifacts into truth-bearing mainline."
  - "Do not treat parser tests as evidence review."
  - "Do not require ordinary VAKS notes to use this exact recipe-style template."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing Markdown-to-typed-object parsers, compiler tests, or generated publishing outputs."
  support_when: "When comparing minimal templates, deterministic slugging, and compile pipelines."
  risk_when: "When generated outputs or auto-commit workflows could mutate canonical records without review."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/microsoft-devcookbook-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/microsoft-devcookbook-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - markdown-parser
  - generated-docs
---

# Strong Candidate Distillation: microsoft / DevCookbook

## Boundary

This file extracts parser/compiler lessons. It does not treat cookbook content,
generated docs, parser tests, or GitHub automation as reviewed VAKS knowledge.

## What This Source Actually Is

DevCookbook is a small open-source cookbook that accepts Markdown recipe files,
parses them into typed Python objects, and compiles a generated documentation
site. It includes a template, parser tests, a recipe dataclass, generated HTML
docs, and a GitHub workflow that runs the compiler.

For VAKS, this is useful as a minimal example of Markdown source becoming a
typed intermediate model before publishing.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `Template.md` | Frontmatter for contributor identity/residence/category plus H1, quote, Ingredients, Directions. | Human-readable template with parseable sections. | Template is not review. |
| `recipe_compiler/parse.py` | Uses frontmatter and Marko AST to extract name, quote, ingredients, instructions. | Parse sections structurally, not with blind string slicing. | Parser output is candidate. |
| `recipe_compiler/recipe.py` | Typed dataclass and deterministic slug. | Derived objects make publishing predictable. | Typed object is not truth layer. |
| `tests/test_parse.py` | Unit tests for parser behavior. | Tests can lock extraction contract. | Test pass is maintenance evidence only. |
| `.github/workflows/compile.yml` | Installs dependencies, compiles docs, auto-commits generated output. | Clear compiler pipeline. | Auto-commit is risky for VAKS. |

## Strong Borrow Points

1. **Markdown should be parsed structurally where possible.**  
   `parse.py` uses a Markdown AST and frontmatter parser. VAKS should prefer
   structured parsers for frontmatter, headings, and lists instead of ad hoc
   regular-expression extraction when building tooling.

2. **A typed derived object can stabilize downstream outputs.**  
   The `Recipe` dataclass gives the compiler one shape to render. VAKS can
   borrow this for derived candidate-point or context-pack objects, while
   keeping Markdown as the canonical source.

3. **Parser behavior deserves tests.**  
   `tests/test_parse.py` checks the expected section extraction. VAKS tooling
   should test source-card parsing, frontmatter validation, relation extraction,
   and sync reports before relying on generated outputs.

4. **Compiler pipeline should be explicit and reversible.**  
   `compile.py` reads recipe files, parses them, renders pages, and writes docs.
   VAKS can borrow this transparent pipeline, but generated outputs must stay
   downstream of source records.

5. **Auto-commit is the wrong default for truth-adjacent artifacts.**  
   The workflow auto-commits generated docs. For VAKS, this is an anti-borrow
   unless the output is strictly non-truth and clearly reviewed as generated.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Candidate Comprehension | Markdown-to-object parsing. | Derived candidate model. |
| Source Hygiene | Parser tests and slug determinism. | Maintenance checks. |
| Publishing | Generated docs from canonical Markdown. | Downstream output. |
| Review Queue | Parser failures can create review pressure. | No automatic truth changes. |
| Risk / Inhibition | Auto-commit generated output. | Do not copy to mainline truth. |

## Local De-Dup / Collision

This overlaps with Grimgrains and Chowdown:

- Grimgrains uses code as source.
- Chowdown uses Jekyll collections and Liquid rendering.
- DevCookbook uses Markdown source plus a typed Python compiler.

The DevCookbook path is closest to a future VAKS tool: Markdown authority,
structured parser, typed derived object, generated output.

## Anti-Borrow

- Do not auto-commit generated VAKS files as if they were reviewed.
- Do not let parser tests become truth confidence.
- Do not force all notes into one rigid template.
- Do not treat generated docs as source.

## Candidate Tags

```yaml
domain: markdown_to_static_compiler
problem: parse_human_markdown_into_typed_objects_for_generated_pages
pattern:
  - markdown-ast-parsing
  - typed-derived-object
  - parser-contract-tests
  - explicit-compile-pipeline
  - auto-commit-risk
maturity: small-working-compiler
problem_fit: 4
reuse_value: 5
implementation_cost: 3
integration_fit: 4
evidence_strength: 4
reversibility: 4
```

## Fusion Judgment

Borrow as a P3 support/risk reference for VAKS tooling. The parser/test/compiler
pattern is valuable; the auto-commit behavior should remain a warning.
