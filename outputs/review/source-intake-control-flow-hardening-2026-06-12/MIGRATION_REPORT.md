---
type: source_intake_migration_report
status: diagnostic
created_at: 2026-06-12
scope: source intake enum and field normalization
truth_boundary: migration evidence only
---

# Migration Report

## Initial Finding

Before normalization, the current-source-intake audit found:

```text
files scanned: 203
errors: 170
duplicate processing fields: 131
enum registry violations: 39
```

The two largest sources of drift were:

```text
processing_mode / processing_level still present beside processing_tier
non-canonical enum values in overlay_state, promotion_gate, review_pressure,
record_kind, and retrieval_policy.*
```

## Mechanical Normalization

`tools/normalize_source_intake_fields.py` performed a frontmatter-only migration.

It removed:

```text
processing_mode
processing_level
```

It normalized legacy enum values such as:

```text
overlay_state: candidate -> overlay_state: none
overlay_state: project_sidecar_created -> overlay_state: none
promotion_gate: evidence_aware_review_required -> promotion_gate: v0_2_13_required
promotion_gate: evidence_aware_review_and_local_benchmark_required -> promotion_gate: v0_2_13_required
retrieval_policy.policy_kind: candidate_only -> retrieval_policy.policy_kind: orientation_only
retrieval_policy.pack_allowed: context_with_warning -> retrieval_policy.pack_allowed: activation_only
retrieval_policy.warning_code: candidate_not_reviewed -> retrieval_policy.warning_code: candidate_not_action_basis
```

The first migration changed 141 files. A later v2 normalization pass added
canonical `record_kind` serialization, explicit legacy placeholders such as
`why_saved: see_body_or_legacy_record`, and required project-overlay fields
derived from existing project-lens metadata.

This is still a machine-semantics migration, so it must be reviewed as a
governance change, not dismissed as cosmetic. Several mappings above are not
equivalent renames; they compress older local meaning into a smaller canonical
enum set.

## Legacy Semantics Preservation

The v2 normalizer now preserves non-isomorphic future mappings by adding
`legacy_*` fields, for example:

```text
legacy_overlay_state
legacy_promotion_gate
legacy_retrieval_policy_kind
legacy_retrieval_pack_allowed
legacy_retrieval_warning_code
```

For the already-normalized current worktree, `tools/preserve_source_intake_legacy_fields.py`
attempted a conservative recovery by comparing tracked Markdown frontmatter in
`HEAD` with the current worktree. That recovery found:

```text
changed tracked Markdown files: 52
recoverable per-file old->new rows: 0
legacy field insertions: 0
```

This means the exact per-file old enum values for the earlier 141-file pass are
not fully recoverable from tracked `HEAD`; many affected files were generated or
already normalized before a comparable tracked snapshot existed. The package
therefore includes a mapping policy ledger rather than pretending the lost
per-file old values can be reconstructed.

Relevant evidence:

```text
results/source_intake_semantic_migration_summary.json
results/source_intake_semantic_migration_ledger.csv
results/source_intake_nonisomorphic_mapping_policy.csv
```

This is a limitation, not a pass condition.

## After V2 Normalization

Current-source-intake audit after v2.6 enum tightening, v2.5 warning
stratification, red-zone cleanup, placeholder split, and v2.11 source-card
authority cleanup:

```text
files scanned: 219
validated intake surfaces: 166
skipped non-target files: 53
warnings: 122
errors: 0
status: structural_pass_semantic_debt
structural_status: pass
semantic_status: debt_pending
canonical_p0_status: not_passed
```

Warning breakdown:

```text
migration_placeholder_value: 118
source_why_saved_placeholder_without_body_reason: 4
```

Semantic-class breakdown:

```text
migration_debt_defer_ok: 118
high_risk_manual_review: 4
hard_error_canonical_p0: 0 remaining in current lint
```

Legacy Project Lens files are no longer counted in canonical current lint.
Seventeen files were moved to `outputs/review/_legacy_project_lens/`, including
a later Kova overlay that appeared in the old path. They are tracked by a
separate compatibility report and tombstone, with downstream consumption
disabled by default.

The full classification rules and representative matrix are in
`WARNING_CLASSIFICATION.md`.

v2.6 also tightens enum boundaries: `retrieval_policy.pack_allowed` now uses
`none` instead of boolean/string false, persistent `project_overlay` state no
longer includes `suggested`, Source Intake core `record_kind` no longer includes
retrieval/runtime `graph_neighbor`, and `promotion_gate` no longer carries
review outcomes such as `review_passed`. This is schema-boundary cleanup, not a
claim of historical semantic equivalence.

This is important: required-field placeholders such as
`see_body_or_legacy_record`, `see_target_layers_or_body`, and
`review_if_project_scope_or_evidence_changes` are now triaged by object role.
Raw source `why_saved: see_body_or_legacy_record` is defer-ok only when the body
contains a real capture/save reason. Without that body reason, it is surfaced as
high-risk missing-reason debt. Confirmed overlay placeholders remain hard errors.
These placeholders prove that a machine field exists; they do not prove the
field has the minimum human-semantic content intended by the contract.

This should not be summarized as a single `pass_with_warnings` result. The
accurate two-layer reading is: structure-level validation is now hard enough to
pass, while semantic validation is still pending.

Likewise, source-card legacy fields are now split by risk. Top-level
`confidence` and `relations` are validator errors and have been moved out of raw
source top-level frontmatter in the current lint corpus. Softer historical
triage fields such as `freshness`, `relevance`, `source_quality`, and
`cross_source_count` have been moved to `legacy_raw_metadata` where retained.
That subtree is retained for audit only; retrieval compilers, graph compilers,
context-pack builders, and support checkers must ignore it by default.

Legacy `outputs/review/_legacy_project_lens/*.md` files are compatibility debt.
They are kept visible through a separate report, but they are excluded from
canonical current lint and must not be counted as proof that the canonical
Project Overlay P0 contract is fully satisfied.

After warning stratification, confirmed overlay placeholders, source-card
top-level `relations`, and source-card top-level `confidence` became hard
errors. The cleanup path mechanically adjusted hard red-zone fields first and
then moved soft source authority-like fields on 11 files:

```text
confidence -> source_integrity.capture_confidence
relations -> candidate_relation_suggestions
confirmed overlay sentinel placeholders -> project-local non-authority wording
freshness/relevance/source_quality/cross_source_count -> legacy_raw_metadata
```

## Remaining Boundary

This migration normalizes machine-readable boundary fields. It does not promote
any candidate note, overlay, feedback event, retrieval result, benchmark, graph
edge, or source record into reviewed knowledge or action basis.

It also remains static validation. It cannot prove real query/retrieval/answer
faithfulness, groundedness, or tool-use behavior without a separate read-only
answer/use-loop trace.

Until the semantic-compression mappings are accepted by review, the safest
reading is: v2 improves lint consistency, but does not fully preserve historical
machine semantics for every normalized file.

Until the remaining placeholder warnings are cleared or explicitly accepted, the
safest reading is: current lint has zero hard contract errors after cleanup, but
still has visible migration and save-reason debt.

The 219-file count is a collected lint corpus count, not a strict-schema object
count. The stricter reading is 166 validated intake surfaces, 53 skipped
non-target files, 122 semantic-debt warnings, and 0 hard errors after cleanup.

The package now includes a standalone current lint corpus manifest. It still
does not include a pre-normalization snapshot or 141-file patch/diff, so it
cannot prove historical semantic equivalence.
