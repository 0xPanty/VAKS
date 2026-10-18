---
type: source_intake_check_results
status: structural_pass_semantic_debt
created_at: 2026-06-12
scope: contract lint, current lint, failure matrix
truth_boundary: diagnostic only
---

# Check Results

## Commands

```powershell
python tools\validate_source_intake_contract.py --scope contract
python tools\validate_source_intake_contract.py --scope current
python tools\validate_source_intake_failure_matrix.py
python tools\preserve_source_intake_legacy_fields.py
python tools\clear_source_intake_red_zone.py
python tools\build_source_intake_hardening_package.py
python tools\validate_source_intake_hardening_package.py
```

## Results

| Check | Scope | Result |
|---|---:|---|
| Contract lint | 9 collected / 9 validated | PASS, 0 warnings, 0 errors |
| Current lint corpus | 219 collected / 166 validated / 53 skipped | STRUCTURAL PASS, 122 semantic-debt warnings, 0 hard errors |
| Failure matrix | 33 cases | PASS, 33 blocked |
| Source-card authority cleanup | 11 files | moved soft source authority-like fields to `legacy_raw_metadata`; hard red-zone fields absent from current lint |
| Enum registry tightening | 4 enum families | `pack_allowed: none`; no persistent `overlay_state: suggested`; no intake `graph_neighbor`; no `promotion_gate: review_passed` |
| Warning classification | 122 warnings | 118 defer-ok migration debt; 4 high-risk manual review; 0 remaining hard-error class |
| Legacy Project Lens compatibility | 17 files | moved to `_legacy_project_lens`; excluded from canonical current lint; downstream consumption disabled; tombstone emitted |
| Semantic migration recovery | 52 tracked changed Markdown files | 0 recoverable per-file rows; mapping policy emitted |
| Package check | 267 manifest files, 219 current-corpus files, 17 legacy compatibility files | PASS; PACKAGE_CHECK.json included in zip |
| SOURCE_INTAKE maturity label | frontmatter | sandbox_contract_candidate / medium confidence |

Current warning breakdown:

```text
migration_placeholder_value: 118
source_why_saved_placeholder_without_body_reason: 4
```

Current semantic-class breakdown:

```text
migration_debt_defer_ok: 118
high_risk_manual_review: 4
hard_error_canonical_p0: 0 remaining in current lint
```

These warnings are semantic/audit debt, not proof of semantic completion.
`why_saved: see_body_or_legacy_record` satisfies defer-ok migration debt only
when the body contains a real capture/save reason. Four raw source cards are
now surfaced separately as high-risk missing-reason debt. Legacy `confidence`,
top-level `relations`, and soft top-level source quality/relevance fields are no
longer left naked in current raw source frontmatter.
Legacy Project Lens files are no longer in canonical current lint. They are
moved to `outputs/review/_legacy_project_lens` and covered by a separate
compatibility report.

Softer historical source triage values (`freshness`, `relevance`,
`source_quality`, `cross_source_count`) were moved to `legacy_raw_metadata` on
11 files so they remain auditable without looking like source authority.

Do not collapse this result into a single `pass_with_warnings` verdict. The
correct reading is: structural intake contract passed, semantic migration debt
is still pending, and canonical Source Intake P0 has not passed.

The 219-file number is a collected corpus count. It is not a claim that all 219
files were strict Source Intake schema objects. The current validator reports
166 validated intake surfaces and 53 skipped non-target files.

Hard-error candidates that Pro identified have been separated from warning debt.
Confirmed overlay placeholders, raw source top-level `relations`, and raw source
top-level `confidence` are validator errors. The current cleanup report records
the latest 11-file soft source authority migration; current lint confirms the
hard red-zone source fields are absent from top-level raw source frontmatter.

## Evidence Files

```text
results/source_intake_contract_lint_summary.json
results/source_intake_contract_lint_issues.csv
results/source_intake_current_lint_summary.json
results/source_intake_current_lint_issues.csv
results/source_intake_current_lint_corpus_manifest.json
results/source_intake_current_lint_corpus_manifest.csv
WARNING_CLASSIFICATION.md
FINAL_WARNING_POLICY_DECISION.md
MINIMUM_FIX_CHECKLIST.md
MINIMUM_TEST_CASES.md
RUNTIME_RISK_MATRIX.md
results/source_intake_legacy_project_lens_compatibility.json
results/source_intake_legacy_project_lens_compatibility.csv
results/source_intake_legacy_project_lens_tombstone.md
results/source_intake_failure_matrix_summary.json
results/source_intake_failure_matrix_results.csv
results/source_intake_red_zone_cleanup_summary.json
results/source_intake_red_zone_cleanup.csv
results/source_intake_semantic_migration_summary.json
results/source_intake_semantic_migration_ledger.csv
results/source_intake_nonisomorphic_mapping_policy.csv
PACKAGE_MANIFEST.json
PACKAGE_CHECK.json
MIGRATION_STRATEGY_DECISION.md
FINAL_WARNING_POLICY_DECISION.md
```

## Failure Cases Covered

```text
FM-01 candidate becomes action basis
FM-02 suggested overlay persists
FM-03 confirmed overlay leaks outside active project
FM-04 project non-borrow becomes universal ban
FM-05 candidate summary becomes support without raw anchor
FM-06 broken anchor cited in action mode
FM-07 repeated negative feedback lacks review_due
FM-08 archived overlay remains in default retrieval
FM-09 Heavy Review Open treated as Review Passed
FM-10 enum drift bypasses filter
FM-11 feedback mutates reviewed truth
FM-12 graph/rank score becomes support
FM-13 candidate missing source/provisional/candidate points
FM-14 source card claims reviewed status
FM-15 confirmed overlay enters default retrieval
FM-16 accepted heavy review skips forbidden proxy check
FM-17 feedback lacks project/context scope
FM-18 confirmed overlay lacks project and target refs
FM-19 query-run uses invalid query_mode
FM-20 query-run candidate item is direct support
FM-21 heavy review warrant uses benchmark/proxy as support
FM-22 candidate distillation omits canonical record_kind
FM-23 legacy source_record omits canonical source_card record_kind
FM-24 query-run trace skips minimum receipt contract
FM-25 context-pack manifest skips top-level pack contract
FM-26 overlay suggestion persists as standalone record
FM-27 raw source why_saved placeholder has no body capture reason
FM-28 raw source card carries top-level relations as authority-like metadata
FM-29 duplicate YAML key hides boundary field through last-wins parsing
FM-30 legacy project_lens_overlay passes as canonical overlay without warning
FM-31 raw source card carries top-level confidence outside capture namespace
FM-32 confirmed overlay uses placeholder for semantic required field
FM-33 retrieval selects item from legacy_raw_metadata
```

Static lint and synthetic failure cases do not prove answer-loop behavior. A
separate read-only query -> retrieval -> answer/use-loop trace is still needed
before any runtime or C-lite readiness claim.
