# Chinese AI/Reviewer-Operator Preflight Protocol

Status: sandbox protocol. Limited operator preflight only. No human result fabricated.

## Goal

Test whether Codex / Pro / reviewer agents can use the risk-gated `shell_core` front face to triage records consistently.

This is not an ordinary user task and not a product-grade human study. It is a small operator preflight to decide whether the renderer is clear enough for AI/reviewer maintenance work and later formal review.

The ordinary vault user should not be asked to read these cards during normal use. The user should only see short risk notices when a record affects an answer or action.

## What To Test

Use 12-24 cases from the 800 sandbox. The current packet uses 24 cases.

Cover:

- ordinary stable records
- action-basis / challenge / conflict records
- promotion candidates when available
- anchor problems
- known omission / ambiguous scope / insufficient evidence
- full-anchor click-back records
- resolved / recurrence-shaped records
- authority bait
- over-grouping near misses
- anchor jump-back failures
- serious folded / regression traps
- action outcome / decision outcome escalation examples when available
- reviewer block / high-severity wrong-answer examples when available
- source-independence-needed examples when available

Only test `shell_core` default-core rendering.

Do not mix in `shell_core_plus_recurrence` for this preflight.

## Operator Task

For each record, the AI/reviewer operator answers:

1. What is the state?
2. Why did it stay light or become thick?
3. What should happen next?
4. Can it be used as action basis now?
5. Can the reviewer jump back to source / record / evidence?
6. Is anything being misread as authority?

## Metrics

Primary metrics:

| metric | meaning |
| --- | --- |
| `time_to_triage_seconds` | how long it takes to choose the next action |
| `serious_miss_y_n` | whether a serious / blocking / review_due item was missed |
| `wrong_actionability_y_n` | whether a non-actionable record was treated as actionable |
| `clickback_source_ok_y_n` | whether source jump-back appears usable |
| `clickback_record_ok_y_n` | whether record jump-back appears usable |
| `clickback_evidence_ok_y_n` | whether evidence jump-back appears usable |
| `authority_misunderstanding_y_n` | whether count, test, dashboard, lineage, feedback, or shell output was treated as support/truth |

Secondary fields:

- `state_understood_y_n`
- `risk_reason_understood_y_n`
- `would_open_full_audit_y_n`
- `burden_1_light_5_heavy`
- `notes`

Generated Chinese operator cards must also pass:

```text
review_packet_risk_tiered_24/forbidden_wording_lint_zh.json
```

This lint uses `forbidden_wording_zh.json`. It is wording hygiene only, not
semantic safety proof.

## Pass / Concern / Fail

This preflight should not use a single score.

Use a qualitative verdict:

```text
pass:
  operator can triage and drill down without serious misses or authority confusion.

pass with concerns:
  operator mostly understands, but one or two surfaces need clearer wording or drilldown.

fail:
  operator misses serious risk, treats non-actionable items as actionable,
  cannot jump back, or treats count/test/dashboard/lineage/feedback as authority.
```

## What This Cannot Prove

The preflight cannot prove:

- independent human oracle.
- product-grade click-back.
- recurrence maturity.
- semantic firewall.
- mainline readiness.
- operation-convention readiness.

It also cannot prove that a fixed line budget is sufficient. The line budget is
only a compactness constraint; the real check is whether the operator can
triage, avoid wrong actionability, and drill down to source / record / evidence.

## Future 480 Paired Human Pilot Plan

This section is a future plan, not work already completed.

Recommended sample mix:

| pool | count | purpose | sample requirement |
| --- | ---: | --- | --- |
| SciFact | 100 | small claim + rationale span + scientific evidence | keep original claim, abstract rationale, and source anchor |
| AVeriTeC | 100 | web claim verification + multi-step evidence | include real webpage or archived snapshot for at least part of the pool |
| AmbiFC | 80 | ambiguity / conflict / scope instability | stress review_due, conflict, and over-grouping |
| FEVER | 80 | high-volume ordinary / baseline pressure | test ordinary false positives and ordinary reduction |
| Full-anchor cases | 40 | real click-back validation | cover webpage, PDF, repo file, release note, and manual span |
| Internal real rows | 80 | closest match to actual VAKS use | mix capture, query, feedback, missing anchor, challenge, and action-basis |

Total:

```text
480 cases
```

Execution:

- Each core case gets at least two variants: `baseline_full` and `shell_core`.
- Variant order is randomized for reviewers.
- Reviewers do not see gold labels or machine layers.
- Core judgments use two reviewers plus adjudication.
- Click-back success counts only against real sources or immutable snapshots.
- Fallback wrappers do not count as product-grade click-back success.

Recurrence / grouping stays out of the main packet.

Use a separate side packet:

```text
60 recurrence-heavy cases
shell_core vs shell_core_plus_recurrence
```

The side packet tests whether recurrence helps operators route repeated ordinary
items without hiding serious, conflict, challenge, anchor problem, or action-basis cases. It does not promote recurrence into default core.

## Mandatory Adversarial Add-On

Before treating the operator surface as ready for a larger human pilot, run the
12-case adversarial add-on:

```text
review_packet_adversarial_12/
```

This packet is not broader coverage. It is a narrow anti-self-proof pressure
set focused on the failure modes most likely to make the shell look safer than
it is.

| adversarial category | typical counterexample | expected operator check |
| --- | --- | --- |
| ordinary-looking action-basis | quiet text used for recommendation, decision, or promotion | use context triggers thickening |
| explicit challenge buried in polite wording | "maybe exceptions" or "someone questioned this" phrasing | soft challenge still enters review |
| anchor pseudo-success | path exists but quote / offset / version is wrong | path existence does not count as click-back success |
| wrapper-only click-back | snapshot wrapper exists but cannot locate original text | wrapper-only is not product-grade click-back |
| review_due trap | omission, insufficient evidence, and ambiguous scope mixed together | review_due is judged by reviewer/adjudicator, not overlay replay |
| grouping near-miss | same-looking recurrence key but different action meaning | no semantic merge; no folded digest overwrite |
| serious folded trap | regression, conflict, or missing-anchor member inside a recurrence group | serious member breaks out and remains visible |
| authority paraphrase | Chinese, English, or mixed paraphrase of authority wording | lint is not enough; operator must not infer authority |
| fake numeric precision | risk 0.18, feedback +0.17, confidence 87% | numbers are diagnostics, not truth support |
| summary overwrite | member claim swallowed by exemplar summary | exemplar cannot replace member semantics |
| source-count trap | many URLs from one source chain | source count is not independence |
| lineage trap | complete lineage without independent confirmation | lineage is traceability, not truth authority |

The generated adversarial packet includes synthetic mock sources, records, and
evidence files. These are only fixtures for operator routing and boundary
recognition. They do not count toward ordinary reduction, human timing, product
click-back success, or independent truth validation.

## Required Metrics And Truth Source

For the future 480 paired human pilot, these metrics must be measured against
reviewer/adjudicator judgment, not machine overlays or renderer structure.

| metric | definition | truth source | why it is not self-proof |
| --- | --- | --- | --- |
| serious false-lite | A case that should be thick / queued / full-audit is treated as light. | Two reviewers plus adjudicator after source inspection. | Does not rely on machine overlay labels. |
| ordinary false-positive | A case that should stay ordinary is wrongly escalated. | Two reviewers plus adjudicator after source inspection. | Does not rely on renderer structure. |
| review_due precision | Among records marked review_due, the share that truly need review. | Two-reviewer adjudication. | Not replaying overlay labels. |
| review_due recall | Among records that truly need review, the share marked by shell. | Two-reviewer adjudication. | Prevents precision-only optimization. |
| source / record / evidence click-back success | Whether the reviewer can reach the source, record, and evidence. | Actual click success log; wrapper-only success does not count. | Avoids "pointer exists = click-back usable". |
| wrong actionability | Whether a reviewer treats a non-actionable record as actionable. | Reviewer decision plus adjudication. | Directly tests the VAKS action boundary. |
| authority misunderstanding | Whether a reviewer treats dashboard, test, group count, source count, lineage, or feedback as authority. | Observation prompts, notes, and adjudication. | Tests misunderstanding directly, not lint hit rate. |
| human triage time | Time from seeing the front face to choosing the next handling action. | Actual timing. | Does not use review proxy as a time substitute. |
| full-audit open rate | How often reviewers open full audit under each arm. | Actual operation record. | Measures friction directly. |
| over-grouping rate | In the side packet, share of wrongly grouped cases. | Recurrence-specific adjudication. | Directly tests grouping quality. |

Minimum warning:

```text
line reduction, front-line budget, lint hit rate, and machine overlay agreement
are diagnostics only. They cannot replace the metrics above.
```

Negative controls and the six-week validation timeline live in:

```text
reports/NEGATIVE_CONTROL_AND_VALIDATION_TIMELINE.md
```

The required controls are `leaky_or_unversioned_control`,
`authority_leaky_renderer`, and `fake_precision_feedback_renderer`. All three
must fail before the harness is considered useful.

The full go / no-go gate table is tracked in:

```text
reports/QUALITY_GATES_AND_THRESHOLDS.md
```

Current status is `not_go_yet`, because human/product hard gates are still not
measured.

## Output Location

The generated packet lives at:

```text
review_packet_risk_tiered_24/
```

Expected files:

- `README_RISK_TIERED_24.md`
- `RISK_TIERED_REVIEWER_CARDS_ZH.md`
- `RISK_TIERED_REVIEWER_SHEET_BLANK.csv`
- `hidden_gold_after_done.csv`
- `sample_coverage.json`
- `render_integrity_lint.json`

The adversarial add-on lives at:

```text
review_packet_adversarial_12/
```

Expected files:

- `README_ADVERSARIAL_12.md`
- `ADVERSARIAL_OPERATOR_CARDS_ZH.md`
- `ADVERSARIAL_REVIEW_SHEET_BLANK.csv`
- `hidden_gold_after_done.csv`
- `adversarial_coverage.json`
- `render_integrity_lint.json`
- `mock_sources/`
- `mock_records/`
- `mock_evidence/`
