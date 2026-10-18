---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
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
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-06-07-agricidaniel-claude-obsidian-candidate-distillation.md
source_card: raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md
architecture_review: wiki/summaries/2026-06-07-agricidaniel-claude-obsidian-architecture-review.md
target_selector: implementation_level_ai_obsidian_wiki_tooling
target_hint: "Use only as active-project borrowing context for VAKS skill/runtime/workbench design."
project_borrow_scope:
  - skill catalog as explicit action surface
  - hot/index/log as activation and recovery spine
  - per-file locking and hook gates as future AI write safety reference
  - local-first retrieval cache with explicit egress gate
  - methodology router as filing-policy adapter
  - lint/verifier outputs as diagnostics and review pressure
  - canvas/dashboard as workbench reference
project_non_borrow_scope:
  - For VAKS, do not borrow generated wiki pages as reviewed truth because VAKS requires raw/candidate/reviewed/action-basis separation.
  - For VAKS, do not borrow auto-research as a default because source intake must remain explicit and candidate-only.
  - For VAKS, do not borrow auto-commit hooks as a default because commits are separate user decisions.
  - For VAKS, do not borrow broad vault write access because write boundaries must stay path-scoped and intent-scoped.
  - For VAKS, do not borrow retrieval score, hot cache, dashboard, or lint report as action basis because they are activation/diagnostic layers.
borrow_tags:
  - P1/skill_catalog_as_action_surface
  - P1/hot_index_log_recovery_spine
  - P1/per_file_locking_for_ai_writes
  - P2/local_first_retrieval_with_egress_gate
  - P2/methodology_router_as_filing_policy
  - P2/lint_verifier_as_diagnostics
  - P3/canvas_dashboard_workbench_layer
do_not_borrow_tags:
  - avoid/generated_wiki_as_reviewed_truth
  - avoid/auto_research_default
  - avoid/auto_commit_default
  - avoid/broad_vault_write_default
  - avoid/retrieval_score_as_authority
  - avoid/one_methodology_as_global_default
project_reopen_trigger:
  - "When designing VAKS skill runtime or helper registry."
  - "When adding lock/sync/hash safety for AI file writes."
  - "When implementing retrieval/cache or context-pack preparation."
  - "When building an Obsidian/Codex workbench, dashboard, or canvas view."
  - "When considering auto-research, auto-commit, hooks, or broad vault write access."
confirmation_basis: "User explicitly requested distillation after repo triage; current public GitHub snapshot inspected at commit cb93ff6d82f9c35a08bf6010e7fac36dfddc827b."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: AgriciDaniel Claude Obsidian

## Boundary

This is a VAKS project-side overlay.

It can guide active design discussion, but it cannot act as reviewed knowledge, decision, truth confidence, or action basis.

## Project Borrow Scope

For VAKS, the strong borrow is:

```text
explicit skills
-> explicit trigger / scope
-> local manual check
-> raw/candidate artifact
-> sync/hash safety
-> optional review/feedback pressure
```

The practical borrowing list:

- Use a skill catalog / trigger map as an action surface, but keep VAKS explicit intake words.
- Use `hot/index/log` style files as activation/recovery/navigation, not truth.
- Use per-file locking and hook deferral as future safety reference for multi-agent writes.
- Use local-first retrieval with explicit egress consent; keep authority buckets separate.
- Use methodology routing as filing policy, not ontology or truth tier.
- Use lint/verifier outputs as diagnostics and review pressure, not promotion.
- Use canvas/dashboard only as workbench/view layer.

## 借鉴标签

```yaml
P1:
  - skill_catalog_as_action_surface
  - hot_index_log_recovery_spine
  - per_file_locking_for_ai_writes
P2:
  - local_first_retrieval_with_egress_gate
  - methodology_router_as_filing_policy
  - lint_verifier_as_diagnostics
P3:
  - canvas_dashboard_workbench_layer
avoid:
  - generated_wiki_as_reviewed_truth
  - auto_research_default
  - auto_commit_default
  - broad_vault_write_default
  - retrieval_score_as_authority
  - one_methodology_as_global_default
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

```text
generated wiki -> reviewed truth
auto-research -> default intake
auto-commit hook -> default repo behavior
broad vault write -> default permission
retrieval score -> support/confidence/action basis
PARA/LYT/Zettelkasten -> global architecture default
```

Why:

```text
VAKS is not just an AI wiki.
VAKS has to preserve source provenance, candidate comprehension, review,
reviewed relations, action basis, and feedback boundaries.
```

## Minimal Absorption Suggestion

No schema change needed now.

If we borrow anything soon, borrow only these helper-level ideas:

```text
1. A visible skill registry for VAKS intake helpers.
2. A hot/index/log recovery convention for active project context.
3. A future per-file lock helper before multi-agent writes.
4. A retrieval/cache experiment that starts local-only and candidate-only.
```

## Reopen Trigger

Reopen when adding:

- formal VAKS skill runtime;
- Codex/Obsidian workbench UI;
- multi-agent file writes;
- retrieval/cache pipeline;
- maintenance lint/report tooling;
- auto-research or auto-commit proposals.

## Confirmation

```yaml
confirmation_basis: "User explicitly said to distill; current public repo snapshot inspected."
last_checked_at: 2026-06-07
```
