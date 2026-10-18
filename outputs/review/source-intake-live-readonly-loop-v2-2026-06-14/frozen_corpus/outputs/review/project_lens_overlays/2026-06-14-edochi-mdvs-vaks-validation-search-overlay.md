---
record_kind: project_overlay
type: project_lens_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
review_pressure: none
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
project_name: "Verified Action Knowledge System / 资料库"
target_ref: "outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md"
target_selector: candidate_distillation
target_hint:
  - type: workflow
    value: "source-intake/frontmatter-validation-search-sidecar"
    status: conceptual
    anchor_version: candidate-workflow-only
  - type: source_card
    value: "raw/repos/2026-06-14-edochi-mdvs-source.md"
    status: healthy
    anchor_version: "2026-06-14"
  - type: repo_snapshot
    value: "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip"
    status: healthy
    anchor_version: "sha256:D035CE40F596C689ABBE985F57051E7A449B01DF1DAA958E35CAD9842D83BEB8"
project_borrow_scope:
  - "Use mdvs as a candidate sidecar for VAKS Markdown frontmatter validation, vault health checks, and agent post-write checks."
  - "Borrow the visible-contract / disposable-cache split: `mdvs.toml` as reviewed config projection, `.mdvs/` as rebuildable ignored index."
  - "Borrow hybrid search with SQL frontmatter filters for activation and context-pack preparation only."
  - "Borrow `check --no-update --output json` as deterministic CI/agent preflight shape."
project_non_borrow_scope:
  - "For VAKS, do not currently borrow mdvs as reviewed knowledge, evidence support, action readiness, or schema authority because it validates structure/search, not truth."
  - "For VAKS, do not trust inferred `mdvs.toml` as architecture policy because it may normalize existing drift."
  - "For VAKS, do not commit `.mdvs/` or treat LanceDB rows as source-of-truth because the index is derived and rebuildable."
  - "For VAKS, do not use mdvs search score/rank as support because retrieval is activation only."
project_reopen_trigger:
  - "User asks to harden VAKS metadata lint or agent write validation."
  - "A sandbox copy of selected VAKS directories is available for mdvs pilot."
  - "VAKS needs a local search/cache sidecar compared against existing retrieval adapters."
  - "Windows/source-build feasibility is verified or a Linux/WSL sandbox is approved."
confirmation_basis:
  - "User explicitly requested distillation and VAKS usefulness judgment."
  - "Official repo, docs, source files, GitHub metadata, release metadata, crates.io metadata, and commit snapshot were inspected."
last_checked_at: "2026-06-14"
expires_at: null
borrow_value: strong
borrow_order:
  - "P1: frontmatter/schema drift lint and agent post-write check"
  - "P2: local hybrid search with typed metadata filters"
  - "P3: JSON Schema interop and agent skill packaging"
avoid:
  - "No mdvs result as reviewed truth."
  - "No search score as support."
  - "No auto-update in CI/action contexts."
  - "No committed `.mdvs/` as authority."
  - "No replacement of VAKS custom validators."
tags:
  - project-lens
  - VAKS
  - mdvs
  - validation
  - local-search
  - candidate-only
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/project_lens_overlays
truth_boundary: "project lens compatibility artifact only; not canonical reviewed knowledge; not action basis"
---

# Project Lens: mdvs as VAKS Validation/Search Sidecar

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide a future VAKS validation/search sandbox, but it cannot act as reviewed knowledge or action basis.

## Project Borrow Scope

For VAKS, borrow mdvs narrowly:

```text
Use it to keep Markdown records structurally clean and easier to find.
Do not use it to decide whether knowledge is true.
```

Concrete borrow:

- `mdvs check --no-update --output json` as post-write/CI preflight.
- Path-scoped frontmatter constraints for record families.
- `mdvs.toml` as visible contract projection.
- `.mdvs/` as ignored, rebuildable local cache.
- Hybrid search + `--where` filters as activation/search sidecar.
- JSON Schema export/import for interop with tools.

## Project Non-Borrow Scope

Do not borrow:

- mdvs as source of truth.
- mdvs search as evidence support.
- mdvs check as review pass.
- mdvs inferred schema as VAKS governance.
- `.mdvs/` as committed database.
- auto-update in CI/action-facing flows.
- replacement of current VAKS validators.

## Reopen Trigger

Reopen this overlay when:

```text
VAKS starts metadata-lint hardening.
Future agent write tools need post-write checks.
Retrieval/cache sandbox compares mdvs with existing VAKS retrieval adapters.
A Linux/WSL or Rust source-build sandbox is available.
```

## Minimal Pilot Gate

```yaml
pilot_scope: sandbox_copy_only
inputs:
  - raw/repos/*.md
  - outputs/review/*candidate-distillation.md
  - outputs/feedback/*.md
  - templates/*.md
commands:
  - mdvs init --dry-run
  - mdvs check --no-update --output json
  - mdvs build --no-update
  - mdvs search "<known query>" --where "<candidate filter>" --output json
checks:
  - no formal vault mutation
  - no source file rewrite
  - inferred schema manually inspected
  - .mdvs ignored/rebuildable
  - mdvs hits labeled activation_only
  - VAKS validators still run separately
pass_result:
  - candidate sidecar contract
fail_result:
  - keep as design reference only
```

## Confirmation

```yaml
confirmation_basis:
  user_request: "这个也蒸馏 看看对我们有没有帮助"
  inspected_source:
    - raw/repos/2026-06-14-edochi-mdvs-source.md
    - raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip
  conclusion: "strong validation/search sidecar reference, not authority layer"
last_checked_at: 2026-06-14
```
