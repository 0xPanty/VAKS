---
record_kind: sandbox_contract
slice_id: 2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox
status: built_pending_review
---

# Operator Launch Checklist Contract

This contract turns p2-44 through p2-48 into a manual read-only operator launch sequence.

It is not re-acceptance, runtime certification, old verifier execution, release approval, promotion approval, mainline readiness, enterprise production readiness, formal vault approval, Obsidian sync, commit authorization, push authorization, reviewed knowledge, evidence support, action basis, auto advance, or user approval.

Required order:

1. Confirm p2-49 scope.
2. Run p2-48 `verify_freeze_bundle.py --final-gate`.
3. Read p2-44 evidence ledger for improvement inventory.
4. Read p2-45 handoff for user-facing wording.
5. Read p2-46 status normalization before interpreting legacy statuses.
6. Read p2-47 portability audit before manual old-verifier execution on another machine.
   Treat p2-47 as diagnostic and drift-sensitive, not as a current launch green gate.
7. Compose a plain answer with sandbox-only boundaries.
8. Stop or escalate on drift, authority confusion, protected path touch, or user-approval requirement.

Default command for this slice:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox\artifact\verify_operator_launch_checklist.py
```

Builder-only rebuild command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox\artifact\verify_operator_launch_checklist.py --rebuild
```

The checklist has 5 source slices and 8 ordered steps.
