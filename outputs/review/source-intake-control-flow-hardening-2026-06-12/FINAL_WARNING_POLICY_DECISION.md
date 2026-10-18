---
type: source_intake_final_warning_policy_decision
status: final_policy_alignment
created_at: 2026-06-13
scope: Source Intake warning classification and migration debt boundary
truth_boundary: policy alignment only; not Source Intake P0 approval
---

# Final Warning Policy Decision

## Plain Verdict

Do not treat all warnings as equal.

The final policy is:

```text
keep safe migration debt visible
upgrade true red-zone fields to hard errors
exclude legacy Project Lens from canonical P0 scope
do not aggressively clear warnings by inventing semantics
```

This supports the current package posture:

```text
structural intake contract: pass
semantic migration layer: debt_pending
canonical Source Intake P0: not passed
```

## Warnings That Can Remain Migration Debt

These can remain warnings, but only with a clear boundary:

- most raw-source `why_saved: see_body_or_legacy_record` placeholders;
- some raw-source `freshness`, `relevance`, `source_quality`, and
  `cross_source_count` legacy metadata, if retained only under
  `legacy_raw_metadata`.

Required boundary:

- retrieval, graph, pack, and support compilers must not read these fields as
  authority;
- they must not participate in action, review, or support logic;
- raw-source `why_saved` placeholders are defer-ok only when the body contains a
  real capture/save reason.

## Warnings That Must Become Hard Errors

These cannot remain warning-only in canonical P0 scope:

- canonical confirmed-overlay placeholder fields:
  - `target_ref`
  - `project_borrow_scope`
  - `project_non_borrow_scope`
  - `project_reopen_trigger`
- raw-source top-level authority-like fields:
  - `relations`
  - `confidence`

If these appear in canonical current lint, the object must fail, or the file must
be excluded from canonical scope.

## Legacy Project Lens Decision

Recommended decision:

```text
exclude first; migrate selected examples manually later
```

This means:

- do not count legacy Project Lens files as canonical overlay validated
  surfaces;
- move them to a legacy/sandbox path;
- keep a compatibility report and tombstone manifest;
- disable downstream retrieval / graph / pack / support consumption;
- manually migrate only the few files that still have clear active value.

The current package follows this policy by moving legacy Project Lens files under
`outputs/review/_legacy_project_lens/` and recording the compatibility set.

## Placeholder And Raw-Source Field Rules

`why_saved` placeholder:

- allowed as migration debt only for raw provenance/orientation records;
- not allowed to support review/action use by itself;
- must be paired with a real body reason, or remain high-risk manual-review
  debt.

canonical overlay placeholders:

- not allowed in canonical confirmed overlays;
- must be filled with real project-local semantics or excluded.

raw-source `relations`:

- do not keep top-level;
- delete, move to candidate relation suggestions, or quarantine under a legacy
  audit-only namespace.

raw-source `confidence`:

- do not keep top-level;
- if it means capture/extraction quality, rename and move under
  `adapter_ingest.capture_confidence` or
  `adapter_ingest.extraction_confidence`;
- if it means source trust, it does not belong on a raw source card.

`source_quality`, `relevance`, `freshness`, `cross_source_count`:

- do not keep as naked top-level raw-source authority fields;
- compute query-dependent values at query time where possible;
- otherwise move to `legacy_raw_metadata` and make retrieval/graph/pack/support
  ignore the subtree.

## Boundary

This policy is a static Source Intake hardening decision. It does not prove
runtime answer-loop behavior, graph compiler quarantine, feedback scope
aggregation, anchor freshness, reviewed truth, or action readiness.
