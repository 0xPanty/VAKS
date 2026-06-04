# External Architecture Review Synthesis

Status: sandbox synthesis from user-provided Pro review. No main-vault writeback, no `SCHEMA.md` change, no operation-convention promotion.

## Plain Verdict

The external review does not reject the audit-shell direction. It reframes it.

The useful abstraction is not:

```text
better Chinese audit cards
```

The useful abstraction is:

```text
risk-gated review surface
+ evidence envelope
+ source-first drilldown
```

In plain terms:

- ordinary records should stay light.
- risky records should automatically become thicker.
- action-basis, challenge, conflict, regression, known omission, or anchor trouble should not be hidden by compression.
- every thickened record should explain why it escalated and where to jump back.
- shell, card, grouping, lint, tests, dashboard, source count, lineage, and feedback are not truth authority.

## What The Review Accepts

The current default-core direction is reasonable when it is understood as a review surface skeleton:

- hard-trigger shell
- required unresolved gate
- anchor health strip
- sparse provenance pointer with source-first jump-back
- resolved folding plus unresolved-first surface
- Chinese reviewer-facing rendering

This should be treated as a sandbox candidate core, not a main-vault rule.

## What The Review Narrows

Recurrence / grouping remains useful only as a conditional side arm:

- queue/list routing compression
- versioned fingerprint
- representative / delta digest
- breakout on serious, challenge, conflict, regression, action-basis, anchor problem, known omission, or review_due

It must not:

- change a member record's own summary.
- fold serious members.
- imply support strength.
- imply source independence.
- become part of the truth layer.

## What The Review Demotes

Authority lint, categorical feedback strip, and forbidden-wording lint are background guardrails.

They can catch crude wording leakage, but they cannot prove:

- semantic safety
- truth boundary integrity
- source independence
- evidence support
- action readiness

## What The Review Cuts

The following expressions or behaviors should be excluded:

- group count / source count / lineage count as reliability.
- dashboard green as truth.
- test pass as truth.
- LLM summary as support.
- feedback as truth confidence change.
- recurrence fold that hides serious or contested members.
- "lint passed, therefore safe".
- "click-back structure exists, therefore real click-back is validated".

## Four-Layer Mental Model

The external review suggests this four-layer model:

```text
1. truth ledger
   raw records, source anchors, evidence, lineage, and reversible traces.

2. escalation controller
   decides what must enter unresolved, full audit, or not-actionable states.

3. reviewer cockpit
   queue + risk strip + actionability + source-first drilldown.

4. reviewer-card / digest / recurrence badge
   renderer surfaces inside the cockpit, not architecture or truth.
```

The current sandbox should not jump straight to a full cockpit. The next small step is a Chinese reviewer-facing renderer for the risk-gated surface.

The later review narrows this into a product-grade shell v1 view convention:

```text
truth ledger
-> escalation controller
-> operator review surface
-> end-user answer surface
```

The ordinary user should not see audit cards by default. The operator surface is
for Codex / Pro / reviewer agents. The end-user surface should expose only short
plain-language risk notices when a risk changes an answer or action.

Front-face compactness is a budget, not a proof metric. The important invariant
is that the operator can see status, summary, risk reason, anchor state,
handling suggestion, and targeted boundary reminders, while source / record /
evidence drilldown remains available.

Sparse pointer floor:

- the front face keeps only lightweight source / record / evidence handles;
- the full audit keeps anchor / selector / quote / offset / version / hash;
- pointer presence is traceability, not evidence support;
- fragile or failed position selectors create review pressure, not action readiness.

Absorption decision:

- separate ordinary user surface and operator surface: directly absorb.
- risk-gated review surface + evidence envelope + source-first drilldown: directly absorb.
- reviewer-card as ordinary user default UI: reject.
- full reviewer cockpit: parked as a long-term direction.
- authority lint as semantic firewall: reject.
- recurrence as default core: reject for now; keep as side arm.

## What The 800 Package Proves

The 800 package gives the direction a physical shape:

- `shell_core` keeps ordinary records thinner.
- serious / review / anchor-problem records become thicker.
- unresolved-first and resolved folding exist as view policy.
- source / record / evidence pointers are retained.
- negative control fails.
- recurrence, authority, and feedback are no longer the main value story.

## What The 800 Package Does Not Prove

The package does not prove:

- natural product-log behavior.
- independent human oracle.
- product-grade click-back.
- semantic authority firewall.
- human time reduction.
- mainline readiness.
- operation-convention readiness.

The current run is still:

```text
real-row + pressure-overlay
+ frozen machine oracle
+ automated checking scaffold
+ blank human review materials
```

## Next Step

Do not expand the automatic harness.

Do not write this into the main vault.

Do not modify `SCHEMA.md`.

The next useful sandbox step is:

```text
Risk-Tiered Reviewer UX Patch
+ Chinese reviewer-facing shell renderer
+ 12-24 case usability preflight
+ small render-integrity lint
```

The preflight should test whether reviewers can:

- triage quickly.
- avoid missing serious risk.
- avoid wrong actionability.
- jump back to source / record / evidence.
- avoid treating count, test, dashboard, lineage, source count, or feedback as authority.

If the 24-case operator preflight passes, the next product-grade evidence step
still should not jump straight to broader automatic tests. Add a mandatory
12-case adversarial operator packet first:

```text
review_packet_adversarial_12/
```

This adversarial packet is not broad coverage and not a truth oracle. It is a
narrow anti-self-proof set aimed at the easiest places for the shell to look
safe while being wrong:

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

After the operator surface passes the preflight plus adversarial add-on, the
next product-grade evidence step is a 480 paired human pilot:

```text
SciFact 100
AVeriTeC 100
AmbiFC 80
FEVER 80
Full-anchor cases 40
Internal real rows 80
```

The main packet compares `baseline_full` vs `shell_core` with randomized order,
two reviewers, and adjudication. Reviewers should not see gold labels or machine
layers. Click-back success counts only on real source or immutable snapshot,
not fallback wrappers.

`shell_core_plus_recurrence` remains outside the main packet. It may be tested
only in a separate 60-case recurrence-heavy side packet.

The pilot must quantify the following metrics. Truth source must be
reviewer/adjudicator judgment and real click-back/timing logs, not overlay
replay, renderer line count, lint hit rate, or review proxy.

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

Negative-control and timeline discipline is recorded separately in:

```text
reports/NEGATIVE_CONTROL_AND_VALIDATION_TIMELINE.md
```

External primary-source priority and the final engineering judgment are
recorded separately in:

```text
reports/EXTERNAL_SOURCE_PRIORITY_AND_FINAL_JUDGMENT.md
```

At minimum, `leaky_or_unversioned_control`, `authority_leaky_renderer`, and
`fake_precision_feedback_renderer` must all fail. If any of these controls is
not caught, the automated harness is not credible enough for the next stage.

The full go / no-go gate table is tracked in:

```text
reports/QUALITY_GATES_AND_THRESHOLDS.md
```

Its current verdict is `not_go_yet`: available automated proxies pass, but
wrong actionability, authority misunderstanding, live/immutable click-back,
human timing, operation open-rate, and recurrence human-understanding gates are
not measured yet.
