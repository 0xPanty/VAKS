# Operator renderer slot patch report

## Status

Sandbox-only renderer patch. No main-vault writeback, no `SCHEMA.md` change.

## What Changed

This patch aligns the Chinese operator renderer with
`reports/AUDIT_SHELL_V1_STATE_AND_SLOT_CONVENTION.md`.

Changes:

- Kept the required operator slots: 状态, 一句话摘要, 风险原因, 锚点状态, 处理建议, 回源入口.
- Changed per-card boundary wording from always-on `边界提醒` to targeted `定向边界提醒`.
- Removed default per-card wording like `无额外提醒；全局规则仍适用。` from ordinary stable records.
- Added explicit weak-landing reminders:
  - `claim_relevant_context_landing` is claim-related context, not evidence landing.
  - `claim_landing` is claim text, not support.
- Updated render-integrity lint so targeted boundary reminders are required only when relevant.

## Why

The operator card should not become a disclaimer-heavy artifact. Ordinary records
should stay light. Boundary reminders should appear only when the current record
has authority-bait, count/grouping, feedback/scope, anchor trouble, or weak
claim/context landing risk.

## Verification

Commands run:

```text
python -m py_compile make_risk_tiered_reviewer_preflight_24.py run_codex_local_real_operator_self_test.py
python make_risk_tiered_reviewer_preflight_24.py
python run_codex_operator_preflight_dry_run.py
python run_codex_local_real_operator_self_test.py
```

Results:

- `review_packet_risk_tiered_24/render_integrity_lint.json`: pass, 0 findings.
- `review_packet_risk_tiered_24/forbidden_wording_lint_zh.json`: pass, 0 findings.
- Codex operator dry-run:
  - risk samples: state understood 24/24, risk reason understood 24/24, wrong actionability 0, serious miss 0, authority misunderstanding 0.
  - adversarial samples: trap recognized 12/12, wrong actionability 0, authority misunderstanding 0, grouping misread 0.
- Codex local real self-test:
  - 26/26 state and action understood.
  - wrong actionability 0/26.
  - serious miss 0/26.
  - authority misunderstanding 0/26.

## Boundary

This is renderer evidence for Codex/operator use only. It is not human
adjudication, not product click-back validation, and not main-vault readiness.
The package remains `not_go_yet`.

