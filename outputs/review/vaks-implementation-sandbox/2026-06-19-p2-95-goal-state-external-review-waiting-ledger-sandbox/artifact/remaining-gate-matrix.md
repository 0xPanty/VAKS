# Remaining Gate Matrix

| Gate | Status | Required Before | Source |
| --- | --- | --- | --- |
| `external_opus_review` | `pending_external_result` | claiming Opus approval or external sandbox acceptance | `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-review-submission-prompt.md` |
| `opus_result_intake` | `pending_external_result` | turning any Opus response into a sandbox record | `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-result-intake-gate.md` |
| `user_mainline_approval` | `not_requested_not_granted` | any main architecture merge, commit, push, sync, promotion, or truth-layer write | `future explicit user approval only` |
