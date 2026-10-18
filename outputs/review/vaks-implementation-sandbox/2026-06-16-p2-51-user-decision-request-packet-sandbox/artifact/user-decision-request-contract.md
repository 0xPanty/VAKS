---
record_kind: sandbox_contract
slice_id: 2026-06-16-p2-51-user-decision-request-packet-sandbox
status: built_pending_review
---

# User Decision Request Packet Contract

This contract allows asking the user a question. It does not collect approval, execute approval, or create action authority.

Required upstream gate:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-50-final-sandbox-closeout-readiness-dossier-sandbox\artifact\verify_closeout_readiness_dossier.py --final-gate
```

Every option must have `automatic_execution=false`. Any option that may lead toward promotion, merge, vault write, commit, push, or action-basis work must require a new scope and separate user approval.

Non-claims: not approval, not execution permission, not promotion, not mainline merge, not release, not formal vault write, not Obsidian sync, not commit, not push, not reviewed knowledge, not evidence support, not action basis, not auto advance.
