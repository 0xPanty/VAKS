---
record_kind: operator_launch_readout
slice_id: 2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox
status: built_pending_review
---

# Operator Launch Checklist

Use this as the human-facing launch surface after p2-48 passes.

## Quick Start

1. Run the p2-48 freeze final gate:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox\artifact\verify_freeze_bundle.py --final-gate
```

2. If it fails, stop. Do not use the handoff chain until the changed source slice is inspected.
3. If it passes, read p2-44 for the improvement ledger, p2-45 for handoff wording, p2-46 for status interpretation, and p2-47 for portability risk.
4. Treat p2-47 as drift-sensitive diagnostic context, not as a current launch green gate.
5. Answer plainly: sandbox product-grade chain is verified, but it is still not mainline, not formal vault, not reviewed knowledge, not evidence support, and not action basis.

## Source Chain

- `2026-06-15-p2-44-sandbox-evidence-ledger-sandbox`: evidence ledger and improvement inventory
- `2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox`: release-candidate handoff packet without release authority
- `2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox`: legacy status normalization guide
- `2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox`: static verifier portability and dependency audit
- `2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox`: checksum freeze and drift detector for p2-44 through p2-47

## Stop Immediately If

- `freeze_verifier_failed`
- `checksum_or_status_drift_detected`
- `source_product_status_not_pass_product_grade`
- `protected_path_touched_by_current_slice`
- `operator_scope_would_write_outside_current_sandbox`
- `authority_confusion_detected`
- `portability_verifier_claimed_green_despite_known_scope_drift`
- `user_approval_required_for_mainline_or_formal_vault`

## Non-Claims

- not re-acceptance
- not runtime certification
- not old verifier execution
- not release approval
- not promotion approval
- not mainline ready
- not enterprise production ready
- not formal vault approval
- not Obsidian sync
- not commit
- not push
- not reviewed knowledge
- not evidence support
- not action basis
- not auto advance
- not user approval
