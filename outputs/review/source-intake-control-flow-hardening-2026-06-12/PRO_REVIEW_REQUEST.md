---
type: pro_review_request
status: ready_for_review_v2_12
created_at: 2026-06-12
scope: VAKS Source Intake control-flow hardening
truth_boundary: review request only
---

# Pro Review Request

Please reverse-audit this VAKS Source Intake hardening package.

Main question:

```text
Did this package correctly implement the minimum Pro recommendations for Source
Intake Control Flow, especially enum freeze + lint, receipt/pack manifest
requirements, confirmed-only overlay persistence, feedback scope limits,
forbidden proxy support checks, failure-matrix regression, and the
semantic-compression migration caveat?
```

Please check:

1. Whether `SOURCE_INTAKE.md` now states the correct control-flow contract
   without overclaiming stability or truth authority.
2. Whether `tools/source_intake_enum_registry.json` is the right minimal enum
   registry, or whether any enum should be renamed, split, or removed.
3. Whether `tools/validate_source_intake_contract.py` now catches the dangerous
   bypasses Pro identified: canonical serialization drift, missing required
   fields, overlay default retrieval, feedback without scope, query-run /
   context-pack nested support misuse, and Heavy Review proxy support.
4. Whether the current audit result is meaningful:

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
failure matrix: 33 / 33 blocked
enum registry v2.6: `pack_allowed` uses `none`, persistent `overlay_state`
excludes `suggested`, intake `record_kind` excludes `graph_neighbor`, and
`promotion_gate` excludes review results such as `review_passed`
semantic migration recovery: 0 recoverable per-file rows from tracked HEAD; non-isomorphic mapping policy emitted
package check: pass; PACKAGE_CHECK.json included in zip
package manifest: 267 files, including the 219-file current lint corpus and the 17-file legacy compatibility set
standalone current lint corpus manifest: provided as JSON and CSV
legacy project lens compatibility report: provided as JSON, CSV, and tombstone
warning classification matrix: WARNING_CLASSIFICATION.md
final warning policy decision: FINAL_WARNING_POLICY_DECISION.md
minimum fix checklist: MINIMUM_FIX_CHECKLIST.md
minimum test cases: MINIMUM_TEST_CASES.md
migration strategy decision: MIGRATION_STRATEGY_DECISION.md
runtime risk matrix: RUNTIME_RISK_MATRIX.md
SOURCE_INTAKE frontmatter maturity: sandbox_contract_candidate, confidence medium
```

Please do not treat `0 hard errors` as semantic completion. The intended
two-layer interpretation is: structural intake contract passed; semantic
migration layer still has debt; canonical Source Intake P0 is not passed unless
those debts are cleared, accepted, or promoted to hard errors where needed.

5. Whether the mechanical frontmatter normalization is safe, or
   whether any normalized value lost important semantics. In particular, future
   non-isomorphic mappings now preserve `legacy_*`, but the already-normalized
   141-file pass does not have fully recoverable per-file old enum values.
6. Whether the expanded failure matrix covers the realistic agent mistakes you
   expected, especially:

```text
candidate as action basis
suggested overlay persistence
archived overlay retrieval leak
enum drift filter bypass
broken anchor action use
feedback truth mutation
graph/rank support confusion
required field omission
query-run candidate support misuse
heavy-review proxy warrant
canonical record_kind omission
minimal query-run/context-pack shell
persisted overlay_suggestion
migration placeholder mistaken for semantic adequacy
source-card authority-like metadata mistaken for provenance-only
duplicate YAML key hidden by last-wins parsing
legacy project_lens_overlay mistaken for canonical P0 overlay
SOURCE_INTAKE status/confidence overclaims maturity
confirmed overlay placeholder treated as semantic required field
source-card top-level relations/confidence treated as warning-only debt
pack_allowed boolean/string false dual encoding
suggested overlay as persistent project_overlay state
graph_neighbor in Source Intake core record_kind
promotion_gate carrying review result such as review_passed
legacy_raw_metadata selected by retrieval/pack/support
```

7. Whether `RUNTIME_RISK_MATRIX.md` identifies the right remaining runtime
   risks that static lint cannot prove: stale index cache, answer-loop citation
   misuse, graph compiler edge promotion, confidence/reranker leakage,
   cross-project feedback suppression, stale anchors, pack-role bugs, subagent
   active-project bypass, promotion-gate write-path bypass, manual legacy lens
   copying, and `legacy_raw_metadata` runtime selection.
8. Whether `MINIMUM_FIX_CHECKLIST.md` accurately marks the Pro minimum static
   fixes as done, and whether any item should still be considered incomplete
   before P0 can pass.
9. Whether `MINIMUM_TEST_CASES.md` is the right acceptance test set, especially
   the split between static tests that are already covered and runtime tests
   that must remain not-run until a read-only answer/use-loop pilot exists.
10. Whether `MIGRATION_STRATEGY_DECISION.md` chooses the right non-aggressive
    strategy: conservative red-zone cleanup plus safe middle-mode isolation, but
    no mass invention of remaining `why_saved` semantics.
11. Whether `FINAL_WARNING_POLICY_DECISION.md` correctly captures the final
    warning policy: keep safe migration debt visible, upgrade canonical overlay
    placeholders plus raw top-level `relations` / `confidence` to hard errors,
    exclude legacy Project Lens from canonical P0 scope, and avoid aggressive
    warning clearing through invented semantics.

Please give a direct verdict:

```text
overall verdict:
can keep as sandbox evidence package:
can treat Source Intake P0 hardening as passed:
can update core docs with this contract:
if core docs can be updated, which wording is safe:
remaining blockers:
minimum next tests:
overclaims or unsafe wording:
```

Important boundary:

```text
This package does not claim runtime/C-lite readiness, automatic writeback,
reviewed truth promotion, or action-basis approval. It only claims Source Intake
contract hardening and lint/failure-matrix coverage. The validator is still a
static frontmatter plus synthetic-receipt check; it does not replace read-only
answer/use-loop traces for context relevance, groundedness, or tool behavior.
```

This v2 package should include the current lint corpus itself, not only summary
tables. Please verify whether that is sufficient for independent rerun.

v2.1 was created after the previous review found three hard validator gaps:
canonical `record_kind` drift, missing minimum receipt/pack top-level fields,
and persisted `overlay_suggestion`. Please verify whether these are now closed
or still bypassable.

Also verify the migration caveat: this package no longer claims the 141-file
mechanical normalization fully preserved old machine semantics. It provides a
mapping policy ledger and future legacy-preserving normalizer, but cannot
reconstruct per-file old enum values where no tracked pre-normalization snapshot
exists.

v2.2 was created after the latest review found two softer but important gaps:
sentinel placeholders satisfied required fields without proving semantic
adequacy, and raw source cards could still carry authority-like legacy metadata
such as `confidence`, `cross_source_count`, and `relations`. The validator now
surfaces both as warnings, not errors. Please judge whether warning-level debt is
the right treatment, or whether some of these should become hard errors before
Source Intake P0 can pass.

v2.3 was created after the latest review found three packaging/validator wording
gaps: the current lint corpus headline was too strong, duplicate YAML keys were
not detected because `yaml.safe_load()` is last-wins, and legacy sandbox
`project_lens_overlays` could be read as if they were canonical P0 overlays. The
validator now treats duplicate YAML keys as hard errors and legacy project lens
files as warning-level compatibility debt. The package validator also supports
running after extraction when the nested zip is absent, and the zip now includes
`PACKAGE_CHECK.json`.

v2.4 was created after review found the main `SOURCE_INTAKE.md` frontmatter
overstated maturity with `status: active`, `verification_status: active`, and
`confidence: high`. The document now uses `status:
sandbox_contract_candidate`, `verification_status:
local_sandbox_lint_with_warnings`, `confidence: medium`, and a confidence basis
that explicitly says this is contract lint plus synthetic failure-matrix
evidence only, not P0 passed and not answer/use-loop verified.

Core-doc adoption boundary to audit:

```text
This contract is materially harder than the previous draft and now has
rerunnable lint/failure-matrix evidence, but validator coverage is still
incomplete. Treat it as boundary hardening in progress, not as a fully passed
Source Intake governance layer.
```

Please verify whether only the boundary principles should be absorbed into core
docs for now, and whether validation conclusions such as `P0 passed`, `corpus
count 0 errors`, `package check pass`, or `validator coverage complete` must stay out
of core docs.

v2.5 was created after review requested warning stratification. The validator now
treats confirmed-overlay placeholders, source-card top-level `relations`, and
source-card top-level `confidence` as hard errors. A mechanical red-zone cleanup
then moved source `confidence` into `source_integrity.capture_confidence`, moved
source `relations` into `candidate_relation_suggestions`, and replaced confirmed
overlay sentinels with project-local non-authority wording. Please verify
whether these transformations are acceptable. Later v2.10/v2.11 passes further
reduced the current warning debt to 122 warnings.

The package also now includes standalone current lint corpus manifests:
`results/source_intake_current_lint_corpus_manifest.json` and `.csv`. It still
does not include a pre-normalization snapshot or a 141-file diff patch, so it
cannot prove historical semantic equivalence.

v2.6 was created after review flagged enum design drift. The registry now uses
a single string value `none` instead of boolean/string false for pack admission,
keeps `suggested` out of persistent `project_overlay` state, removes
`graph_neighbor` from Source Intake core record kinds, and keeps review results
out of `promotion_gate`. Please verify whether this split is the right minimal
schema boundary.

v2.7 was created after review flagged that warnings should not be flattened.
Each lint issue now carries `semantic_class` and `recommended_action`; the
current canonical warning set splits into 118 defer-ok migration-debt warnings
and 4 high-risk manual-review warnings. Please verify whether these classes and
actions match the intended semantic-risk matrix.

v2.8 was created after review recommended not batch-migrating legacy Project
Lens overlays into canonical overlays. The legacy files were moved from
`outputs/review/project_lens_overlays/` to
`outputs/review/_legacy_project_lens/`, marked with
`legacy_overlay_compatibility: true` and `canonical_p0_included: false`, removed
from canonical current lint scope, and retained in a separate compatibility
report. Please verify whether this is safer than mechanical canonical
migration, and whether 1-3 future gold examples should be migrated manually.

v2.9 extends that decision by treating the old Project Lens path as archive-only
rather than a canonical overlay migration queue. A later Kova overlay that
appeared in the old path was also archived instead of promoted, bringing the
legacy compatibility set to 17 files. The package now includes a tombstone and
marks the set with `downstream_consumption_allowed: false`. Please verify
whether direct exclusion/archive is the right P0 default, and whether any future
canonical overlay should be created only by manual gold-example migration.

v2.10 adds the final placeholder/raw-source split: raw source
`why_saved: see_body_or_legacy_record` is defer-ok only when the body contains a
real `Why Captured`, `Capture Reason`, `为什么收录`, or equivalent reason. Four
current files are now surfaced as
`source_why_saved_placeholder_without_body_reason` rather than being counted as
defer-ok migration debt. It also documents that `author` may be unknown/omitted
and that legacy `kp_ref` is a navigation pointer, not Source Intake P0 authority.
Please verify whether this treatment is strict enough without overfitting raw
source cards into heavy paperwork.

v2.11 applies the final raw-source authority-field recommendation. Top-level
raw-source `relations` are incompatible with provenance-only source cards and
must live as `candidate_relation_suggestions`, `legacy_raw_metadata`, or a
sidecar. Top-level raw-source `confidence` must be scoped as capture/extraction
confidence under `source_integrity` or `adapter_ingest`, or else move to
triage/review. Softer top-level fields (`freshness`, `relevance`,
`source_quality`, `cross_source_count`) were mechanically moved on 11 files to
`legacy_raw_metadata` instead of staying as naked source authority signals.
Please verify whether this preserves history without leaking false authority.

v2.12 adds a narrow static guard for that boundary: if a query-run or
context-pack item says it was selected from `legacy_raw_metadata`, or if a
support check tries to use `legacy_raw_metadata` as a claim/anchor, the validator
errors. This is still not runtime proof; it only prevents the mistake from being
serialized as an acceptable receipt/pack artifact.
