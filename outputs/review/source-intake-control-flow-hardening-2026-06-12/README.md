---
type: source_intake_hardening_readme
status: sandbox_candidate_v2_12
created_at: 2026-06-12
scope: VAKS Source Intake control-flow hardening
truth_boundary: evidence package only; not reviewed knowledge; not action basis
---

# Source Intake Control Flow Hardening 2026-06-12

## Plain Summary

This package implements the Pro review's minimum hardening path for VAKS Source
Intake:

```text
freeze enums
lint current intake surfaces
require receipt / pack boundary metadata
keep suggested overlay trace-only
keep feedback append-only
block proxy support in Heavy Review
run failure-matrix regression
record semantic-compression migration limits
package the current lint corpus for third-party rerun
```

The goal is not to add a heavy ontology or an automatic truth system. The goal
is to make the existing VAKS boundaries mechanically checkable.

## What Changed

- `SOURCE_INTAKE.md` now documents:
  - canonical enum registry and fail-closed rule;
  - no automatic authority promotion;
  - minimal state machine;
  - object-level required fields;
  - forbidden intake fields and proxy-support rules;
  - retrieval receipt and context-pack manifest minimum fields;
  - expanded failure matrix.
- Templates now include stricter machine fields:
  - `templates/source-record.md`
  - `templates/video-source.md`
  - `templates/candidate-distillation.md`
  - `templates/project-overlay.md`
  - `templates/query-run.md`
  - `templates/feedback-event.md`
  - `templates/heavy-review-open.md`
  - `templates/context-pack-manifest.md`
- Machine checks now live in:
  - `tools/source_intake_enum_registry.json`
  - `tools/validate_source_intake_contract.py`
  - `tools/normalize_source_intake_fields.py`
  - `tools/preserve_source_intake_legacy_fields.py`
  - `tools/clear_source_intake_red_zone.py`
  - `tools/relocate_legacy_project_lens.py`
  - `tools/validate_source_intake_failure_matrix.py`
  - `tools/build_source_intake_hardening_package.py`
  - `tools/validate_source_intake_hardening_package.py`

## Verification

Latest checks:

```text
contract lint: 9 files, 0 errors
current lint corpus: 219 collected files; 166 validated intake surfaces; 53 skipped non-target files
current intake-surface lint v2.12: structural pass, semantic debt pending; 122 warnings, 0 hard errors
  - migration_placeholder_value: 118
  - source_why_saved_placeholder_without_body_reason: 4
warning classification v2.7:
  - migration_debt_defer_ok: 118
  - high_risk_manual_review: 4
  - hard_error_canonical_p0: 0 remaining in current lint
legacy project lens v2.9: 17 files moved to `outputs/review/_legacy_project_lens`,
excluded from canonical current lint, downstream consumption disabled, and recorded
in a separate compatibility report plus tombstone
source-card authority cleanup v2.11: hard top-level `confidence`/`relations`
cleared; 11 files had soft source authority-like fields moved to `legacy_raw_metadata`
failure matrix v2.12: 33 / 33 blocked
enum registry v2.6: `pack_allowed` uses `none`, persistent `overlay_state`
excludes `suggested`, intake `record_kind` excludes `graph_neighbor`, and
`promotion_gate` excludes review results such as `review_passed`
semantic migration recovery: 0 recoverable per-file rows from tracked HEAD; mapping policy emitted
package check: pass; `PACKAGE_CHECK.json` included in the zip
package manifest: 267 files, including the 219-file current lint corpus and the 17-file legacy compatibility set
current lint corpus manifest: standalone JSON and CSV included
legacy project lens compatibility report: standalone JSON, CSV, and tombstone included
SOURCE_INTAKE frontmatter maturity: sandbox_contract_candidate, confidence medium
warning classification matrix: `WARNING_CLASSIFICATION.md`
final warning policy decision: `FINAL_WARNING_POLICY_DECISION.md`
minimum fix checklist: `MINIMUM_FIX_CHECKLIST.md`
minimum test cases: `MINIMUM_TEST_CASES.md`
migration strategy decision: `MIGRATION_STRATEGY_DECISION.md`
runtime risk matrix: `RUNTIME_RISK_MATRIX.md`
raw source `why_saved` placeholder rule: defer-ok only when the body contains a real capture/save reason; 4 files are surfaced for manual review
legacy_raw_metadata rule: retained for audit only; retrieval, graph, pack, and support compilers must ignore the subtree
```

## Boundary

This package supports the narrow conclusion that the Source Intake contract is
structurally harder and more auditable after the Pro-requested hardening fixes.
It does not support the conclusion that semantic migration is complete. It also
includes the current lint corpus so a reviewer can rerun the current check after
extracting the zip. The 219-file headline is a corpus count, not a claim that all
219 files were strict schema objects; the current validator reports 166
validated intake surfaces and 53 skipped non-target files.

The safe core-doc adoption boundary is narrow:

```text
This contract is materially harder than the previous draft and now has
rerunnable lint/failure-matrix evidence, but validator coverage is still
incomplete. Treat it as boundary hardening in progress, not as a fully passed
Source Intake governance layer.
```

The preferred two-layer verdict is:

```text
structural intake contract: pass
semantic migration layer: debt_pending
canonical Source Intake P0: not passed
```

Migration strategy:

```text
conservative_plus_safe_middle
```

Final warning policy:

```text
keep safe migration debt visible
upgrade true red-zone fields to hard errors
exclude legacy Project Lens from canonical P0 scope
do not aggressively clear warnings by inventing semantics
```

This package clears true red zones and safe static isolation issues, but it does
not aggressively fill the remaining `why_saved` warnings. Visible debt is
preferred over invented semantics.

Principles that may be borrowed into core docs are limited to boundary wording:
authority/status/processing separation, no automatic authority promotion,
candidate/overlay/feedback not being action basis, independent-anchor support,
diagnostic signals not being evidence, append-only scoped feedback,
bucket-first retrieval, and forbidden-proxy checks in Heavy Review. Validation
claims, P0-pass claims, runtime readiness, and validator-completeness claims must
not be promoted into core docs from this package.

v2.1 specifically tightened canonical `record_kind` serialization, query-run /
context-pack top-level receipt requirements, and persisted overlay-suggestion
blocking. v2.2 adds warning-level surfacing for migration placeholders and
source-card authority-like legacy metadata, so those debts cannot be mistaken
for completed semantic adequacy. v2.3 adds duplicate-YAML-key detection,
warning-level surfacing for legacy `project_lens_overlays`, and a package check
that is present in the zip and can also run after extraction without requiring a
nested zip. v2.4 lowers the `SOURCE_INTAKE.md` frontmatter maturity label from
active/high to sandbox candidate/medium, because the evidence is still local
lint plus synthetic failure-matrix coverage. v2.5 classifies warning debt:
confirmed overlay placeholders, source-card top-level `relations`, and
source-card top-level `confidence` are hard errors; the current corpus cleanup
moved those out of authority-like positions. It still does not prove real
answer/use-loop behavior. v2.6 tightens enum boundaries so Source Intake core
does not keep runtime/retrieval objects in the persistent intake registry and
does not mix gate requirement with review outcome. v2.7 adds per-warning
semantic classes and recommended actions, so warning debt is no longer flattened
into a single bucket. v2.8 moves legacy Project Lens files out of canonical
current lint scope into `_legacy_project_lens`, keeps them in a separate
compatibility report, and avoids pretending they are canonical Project Overlay
P0 records. v2.12 adds a static receipt/pack guard so `legacy_raw_metadata`
cannot be serialized as a retrieval or support signal. This is still static
validation, not answer-loop validation.

It does not claim:

```text
all VAKS governance is finalized
all historical sandbox outputs are reviewed knowledge
retrieval or agent runtime is ready for writeback
feedback can mutate truth
diagnostic scores can support action
real answer-loop behavior has been proven
historical machine semantics were fully preserved for every normalized file
placeholder fields satisfy semantic adequacy
raw source-card legacy confidence / relation metadata is harmless
legacy project lens overlays are canonical P0 overlays
duplicate YAML keys are safe under last-wins parsing
SOURCE_INTAKE P0 hardening has passed
SOURCE_INTAKE is a stable active runtime module
core docs can absorb validation/P0-pass claims from this sandbox package
all remaining warnings are low risk
structural pass means semantic pass
```
