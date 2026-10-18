# Narrow Operator Adjudication Packet

Status: blank human/operator adjudication packet. Sandbox only. No main-vault
writeback, no `SCHEMA.md` change, and no operation-convention promotion.

## Purpose

This is the next step recommended by Pro: a narrow but hard operator
adjudication stage. It tests whether real reviewers/operators can use the
operator surface without misreading actionability, authority, or click-back.

This is not another automatic patch and not a Codex dry-run.

## Source Materials

Reviewers should read these first:

```text
review_packet_risk_tiered_24/RISK_TIERED_REVIEWER_CARDS_ZH.md
review_packet_adversarial_12/ADVERSARIAL_OPERATOR_CARDS_ZH.md
```

Do not open hidden gold before finishing reviewer sheets.

## Sheets To Fill

```text
CORE_24_DOUBLE_REVIEW_SHEET_BLANK.csv
ADVERSARIAL_12_DOUBLE_REVIEW_SHEET_BLANK.csv
ADJUDICATION_RESOLUTION_SHEET_BLANK.csv
GATE_SUMMARY_BLANK.json
```

Use two independent reviewers/operators first. Then one adjudicator resolves
disagreements and records gate outcomes.

## What Counts

- wrong actionability
- serious miss
- authority misunderstanding
- source / record / evidence click-back success
- whether the reviewer found the correct quote/context, not merely a path
- triage time
- whether full audit was opened when needed

## What Does Not Count

- Codex dry-run
- lint pass
- test/report/dashboard pass
- source count, URL count, lineage count
- group count or recurrence count
- local wrapper-only click-back
- path existence without correct quote/context

## Current Boundary

The project remains `not_go_yet` until real reviewer/operator sheets and
adjudication are filled.
