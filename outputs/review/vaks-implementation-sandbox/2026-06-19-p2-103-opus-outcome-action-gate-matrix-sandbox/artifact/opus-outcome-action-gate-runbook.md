# Opus Outcome Action Gate Runbook

## Purpose

Use this matrix after a real external Opus result has been retained and validated in a sandbox-only intake slice.

## Outcome Rules

- `OPUS_PASS_SANDBOX_CLOSEOUT`: retain the raw result, validate it, then prepare a user approval decision packet. It does not authorize automatic mainline merge.
- `OPUS_REVISE_SANDBOX_CLOSEOUT`: retain the raw result and create a revision slice in sandbox. Do not advance to the next program stage.
- `OPUS_BLOCKED_NEEDS_USER`: retain the raw result and stop for user input.

## Global Invariants

No Opus outcome authorizes automatic merge, promotion, reviewed knowledge writes, evidence support writes, action basis, commit, push, sync, or goal completion.
