---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "dotnet/dotnet-api-docs"
source_url: "https://github.com/dotnet/dotnet-api-docs"
checked_commit: "7340c9a6293ebbb9a1200a8089ca4dd862cf1ce2"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/dotnet-dotnet-api-docs-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/dotnet-dotnet-api-docs-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/dotnet-dotnet-api-docs-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: medium
borrow_order: P2
routing_hint:
  - generated_reference_docs
  - metadata_policy
fit_layer:
  - source-ingest
  - publishing
  - source-hygiene
  - feedback
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
avoid:
  - "Do not treat generated API docs, doc build status, or evaluator scores as VAKS truth confidence."
  - "Do not copy large doc pipeline complexity into VAKS core."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing generated-reference handling, metadata policy by path, or source-code-comment versus vault-note ownership."
  support_when: "When comparing docfx/openpublishing-style build metadata, feedback links, and generated-reference contributor gates."
  risk_when: "When generated reference, model-evaluator scores, or source-code comments could be mistaken for reviewed VAKS claims."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/dotnet-dotnet-api-docs-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - generated-reference
  - docs-pipeline
---

# Strong Candidate Distillation: dotnet / dotnet-api-docs

## What This Source Actually Is

This is a large .NET API reference documentation repository. It is built from
structured XML/reference material, docfx/open publishing configuration, and
dependent conversion packages. It distinguishes API reference docs from
conceptual docs and from API docs maintained in source-code comments.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Repo identity, issue tracking, contribution guidance, and source-code-comment ownership note. | Useful distinction between docs owned here and docs generated/ported from source comments. | Ownership note is process metadata. |
| `docfx.json` | Global metadata, file metadata by path, feedback configuration, contributor openness flags, generated-reference topic labels. | Strong model for path-scoped metadata policy. | Metadata does not prove content. |
| `.openpublishing.publish.config.json` | ECMA XML to YAML conversion, SplitTOC, DiffFolder, preview PR, dependent packages, branch targets. | Strong generated-reference pipeline boundary. | Too heavy for VAKS core. |
| `xml/.../GroundednessEvaluator.xml` | Structured API record with signatures, versions, docs, remarks, and model-performance caveat. | Useful example of versioned structured source plus explicit evaluator limitations. | Evaluator score is diagnostic, not VAKS truth. |
| `CONTRIBUTING.md` | Routes contributors to broader .NET doc process. | Contribution workflow is externalized and role-aware. | Not a VAKS review process. |

## Strong Borrow Points

1. **Generated/reference content needs path-scoped policy.**  
   `docfx.json` maps metadata, topics, language, contributors, and openness by
   path. VAKS can borrow this for generated candidate records: generated areas
   should carry explicit policy and contribution gates.

2. **Source ownership must be explicit.**  
   Some API docs are maintained in source-code comments outside this repo. VAKS
   should similarly record whether a note is canonical, generated from another
   source, or a projection.

3. **Build/publish configuration is process evidence.**  
   Open publishing config proves how docs are generated and previewed, but it
   does not prove the claims in the docs. This distinction maps cleanly to
   VAKS's provenance/support split.

4. **Evaluator caveats are valuable anti-pattern anchors.**  
   The GroundednessEvaluator XML explicitly describes score ranges and warns
   about model-dependent performance. VAKS should borrow this warning style for
   LLM judges and benchmark outputs: diagnostic scores are not truth confidence.

5. **Generated-reference complexity should stay outside the core.**  
   ECMA-to-YAML, SplitTOC, DiffFolder, and build targets are useful references
   for future generated docs, but would overcomplicate the Markdown-first VAKS
   spine today.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture | Source ownership and generated/reference flags. | Strongly adapt. |
| Review Queue | Path-scoped contributor openness can route review responsibilities. | Candidate gate only. |
| Publishing | Preview PR and generated build config. | Future reference. |
| Feedback | GitHub/product feedback metadata. | Feedback ledger input, not truth. |
| Risk | AI evaluator caveats. | Strong anti-pattern support. |

## Local De-Dup / Collision

The earlier shallow file marked this as `technical_docs_reference`. Strong
inspection changes the useful borrow: VAKS should not borrow .NET API content,
but should learn from generated-reference ownership, path metadata, feedback
configuration, and evaluator-score warnings.

## Fusion Judgment

Adapt selectively as a P2 reference for generated/reference material and
evaluation-result boundary language. Do not import the docfx/OpenPublishing
pipeline into VAKS mainline now.
