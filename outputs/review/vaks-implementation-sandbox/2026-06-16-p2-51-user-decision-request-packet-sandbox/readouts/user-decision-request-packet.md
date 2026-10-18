---
record_kind: user_decision_request_readout
slice_id: 2026-06-16-p2-51-user-decision-request-packet-sandbox
status: built_pending_review
---

# User Decision Request Packet

This packet is ready to ask the user for the next VAKS sandbox decision. It is not approval and not execution permission.

## Prompt

sandbox 链条已经产品级通过；现在只能请你选择下一步方向，不能自动执行任何合并、发布、同步、写库或行动依据。

## Options

- `A_keep_sandbox_reference`: Keep sandbox as reference only / automatic_execution=False / requires_new_scope=False / requires_separate_user_approval=False / allowed_next_action=none
- `B_start_readonly_promotion_review_plan`: Authorize a new read-only promotion review planning slice / automatic_execution=False / requires_new_scope=True / requires_separate_user_approval=True / allowed_next_action=new_readonly_sandbox_or_plan_only
- `C_request_mainline_merge_scope`: Authorize asking for a separately scoped mainline merge review / automatic_execution=False / requires_new_scope=True / requires_separate_user_approval=True / allowed_next_action=ask_for_explicit_path_scope_only
- `D_park_or_reject_sandbox_chain`: Park or reject the sandbox chain / automatic_execution=False / requires_new_scope=False / requires_separate_user_approval=False / allowed_next_action=none

Options B and C only authorize a future scoped conversation. They do not start the future work in this slice.

## Safe Default

If the user does not reply, keep the sandbox as reference only. Do not execute anything.

## Required Upstream Gate

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-50-final-sandbox-closeout-readiness-dossier-sandbox\artifact\verify_closeout_readiness_dossier.py --final-gate
```

## Builder-Only Command

`--rebuild` rewrites generated files inside this sandbox and is for Builder repair only. Ordinary follow-up agents should use the default verifier or `--run-upstream`.
