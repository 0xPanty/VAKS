# External Opus Response Capture Card

Status: raw response not yet present.

When Opus responds, create a new sandbox-only intake slice and preserve the exact raw response there. Do not paste a response into this p2-107 slice.

Required capture fields:

- `raw_response_path`
- `raw_conclusion_token`
- `reviewed_evidence`
- `boundary_verdict`
- `blocking_issues`
- `recommended_next_action`

Allowed conclusion tokens:

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

Boundary: raw Opus response is external review evidence only. It is not user approval, not mainline readiness, not reviewed knowledge, not evidence support, not action basis, not commit, not push, and not sync.

