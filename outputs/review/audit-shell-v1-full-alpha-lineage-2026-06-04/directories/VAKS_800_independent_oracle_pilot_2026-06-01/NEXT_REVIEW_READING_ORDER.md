# Next Review Reading Order

Status: reviewer reading order for the sandbox package. This file is meant to
prevent reviewers from starting with headline metrics and missing the actual
architecture boundaries.

## Highest Priority

| priority | file | why read first |
| --- | --- | --- |
| highest | `reports/AUDIT_SHELL_V1_SANDBOX_CLOSEOUT.md` | Check whether the current convergence is honest and whether claims are over-stated. |
| highest | `reports/AUDIT_SHELL_V1_REVIEWER_CARD_CANDIDATE_CONVENTION.md` | Check whether reviewer-card is correctly defined as a view-layer surface, not a truth layer. |
| highest | `reports/RISK_TIERED_REVIEWER_UX_PATCH_SPEC.md` | Check whether the design has moved from "card polish" to operator review surface. |
| highest | `reports/AUDIT_SHELL_V1_STATE_AND_SLOT_CONVENTION.md` | Check the explicit state machine and required operator front-face slots; card is only a renderer. |
| highest | `reports/OPERATOR_RENDERER_SLOT_PATCH_REPORT.md` | Check the renderer patch that made boundary reminders targeted and weak landing warnings explicit. |
| highest | `reports/CHINESE_REVIEWER_CARD_PATCH_SPEC.md` | Check whether Chinese wording avoids authority leakage. |
| highest | `reports/EXTERNAL_SOURCE_PRIORITY_AND_FINAL_JUDGMENT.md` | Check the primary external sources, immediate verification work, and final engineering judgment before treating automated metrics as proof. |
| highest | `reports/CODEX_OPERATOR_PREFLIGHT_DRY_RUN_REPORT.md` | Check what Codex could verify as operator dry-run and which human/product gates remain open. |
| highest | `reports/PRO_REVIEW_PASS_WITH_CONCERNS_AND_NEXT_ROUTE.md` | Check the latest pass-with-concerns verdict and the narrow real operator adjudication route. |
| highest | `reports/OPERATOR_ADJUDICATION_ROUND1_REVIEW_RESULT.md` | Check the imported narrow adjudication result: pass with concerns, click-back not passed, no 120-case main packet yet. |
| highest | `reports/CLICKBACK_SEMANTIC_LANDING_EVAL.md` | Check the split between transport fetch, path resolution, and claim-relevant selector landing. |
| highest | `review_packet_operator_adjudication_narrow/README_OPERATOR_ADJUDICATION_NARROW.md` | Check the blank double-review/adjudication packet that should be run next. |
| highest | `review_packet_risk_tiered_24/RISK_TIERED_REVIEWER_CARDS_ZH.md` | Inspect what the AI/reviewer operator actually sees, not only what reports claim. |

## High Priority

| priority | file | why read next |
| --- | --- | --- |
| high | `build_candidate_cases_800.py` | Check how the 800 cases were built and where profile overlays enter. |
| high | `freeze_gold_oracle_800.py` | Check the independence boundary of the frozen gold. |
| high | `renderer_800.py` | Check whether the front face is structurally self-proving and whether `group_id` is traceable. |
| high | `checker_800.py` | Check how click-back, authority leakage, grouping, and state failures are measured. |
| high | `data/clickback_snapshot_manifest.json` | Check transport fetch status: 24 live/immutable and 0 fallback wrappers. This is not semantic click-back success. |
| high | `data/clickback_semantic_landing_eval.json` | Check semantic selector status: only claim/evidence substring landing counts; `body_window` / boilerplate does not. |
| high | `review_packet/packet_summary.json` | Check whether the human packet actually covers high-risk surfaces. |

## Medium Priority

| priority | file | why read after the above |
| --- | --- | --- |
| medium | `reports/PILOT_800_REPORT.md` | Check automated results after understanding the harness boundaries. |
| medium | `reports/PATCH_800_AUTOMATED_FIX_REPORT.md` | Check what was patched and which thresholds or metrics were redefined. |

## Do Not Start Here

Do not begin with:

- `pilot_800_results.json`
- line / character reduction numbers
- threshold pass/fail summaries
- authority fuzz hit rate

Those are useful diagnostics only after reading the files above. Starting from
headline numbers makes it too easy to miss that this is still a pressure-overlay
sandbox with machine-frozen gold, not an independent human oracle.

## Review Focus

After following the reading order, judge:

- whether `shell_core` remains the only default-core candidate;
- whether Chinese operator rendering is a necessary view-layer alpha;
- whether recurrence stays a conditional side arm;
- whether authority lint / forbidden wording / feedback strip remain guardrails;
- whether repaired 24/24 live click-back snapshots are only transport success, and whether semantic selector failures block the 120-case packet;
- whether the next step stays narrow human/operator adjudication rather than another automatic patch;
- whether the current package is ready for limited operator preflight, not
  main-vault operation convention.
